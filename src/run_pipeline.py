import os
import json
import shutil
import pandas as pd
import cv2
import requests
from ultralytics import YOLO
from datetime import datetime
import pytz
from dotenv import load_dotenv
load_dotenv()

# Constants
INPUT_FILE = "inputs/input.xlsx"
IMAGE_DIR = "data/fetched"
OVERLAY_DIR = "outputs/overlays"
MANIFEST_DIR = "outputs/manifests"
METRICS_PATH = "outputs/metrics/pipeline_metrics.csv"
CERT_DIR = "certificates"
MODEL_PATH = "models/yolo/best.pt"
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


# Clean old outputs
for folder in [IMAGE_DIR, OVERLAY_DIR, MANIFEST_DIR]:
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)

# Clean only generated certificates, not the template
if os.path.exists(CERT_DIR):
    for file in os.listdir(CERT_DIR):
        if file.endswith("_certificate.txt"):
            os.remove(os.path.join(CERT_DIR, file))
else:
    os.makedirs(CERT_DIR, exist_ok=True)

# Load YOLO model
model = YOLO(MODEL_PATH)

# Helper functions
def estimate_solar_health(panel_count, total_area):
    if panel_count == 0:
        return "N/A"
    elif total_area < 1000:
        return "Medium"
    else:
        return "High"

def is_eligible_for_certificate(qc_flag, solar_health_score):
    return qc_flag and solar_health_score in ["High", "Medium"]

def fetch_satellite_image(lat, lon, sample_id):
    url = (
        f"https://maps.googleapis.com/maps/api/staticmap"
        f"?center={lat},{lon}&zoom=20&size=640x640&maptype=satellite"
        f"&key={GOOGLE_MAPS_API_KEY}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        image_path = os.path.join(IMAGE_DIR, f"{sample_id}.jpg")
        with open(image_path, "wb") as f:
            f.write(response.content)
        return image_path
    else:
        print(f"[ERROR] Failed to fetch image for {sample_id} (lat: {lat}, lon: {lon})")
        print(f"Status code: {response.status_code}, Response: {response.text}")
        return None

# Read input Excel
try:
    input_df = pd.read_excel(INPUT_FILE)
    valid_ids = input_df["sample_id"].astype(str).str.split(".").str[0].tolist()
    with open("outputs/valid_ids.json", "w") as f:
        json.dump(valid_ids, f)
except Exception as e:
    print(f"[FATAL] Failed to read input file: {e}")
    exit(1)

# Validate required columns
required_cols = {"sample_id", "lat", "lon"}
if not required_cols.issubset(input_df.columns):
    print(f"[FATAL] Missing required columns in input file. Found: {input_df.columns.tolist()}")
    exit(1)

# Process each sample
for idx, row in input_df.iterrows():
    try:
        sample_id = str(row["sample_id"]).split(".")[0]
        lat, lon = row["lat"], row["lon"]

        # Fetch image
        image_path = fetch_satellite_image(lat, lon, sample_id)
        if not image_path or not os.path.exists(image_path):
            continue

        img = cv2.imread(image_path)
        if img is None:
            print(f"[ERROR] Image read failed: {image_path}")
            continue
        else:
            print(f"Reading: {image_path}")

        # Run YOLO inference
        results = model(img, conf=0.1)
        annotated_img = results[0].plot()

        # Count panels and calculate area
        area = 0
        panel_count = 0
        bboxes = []
        if results[0].boxes:
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                width = x2 - x1
                height = y2 - y1
                area += width * height
                bboxes.append([round(x1), round(y1), round(x2), round(y2)])
            panel_count = len(results[0].boxes)
        else:
            print(f"[INFO] No panels detected in {sample_id}.")
            panel_count = 0
            area = 0
            bboxes = []

        qc_pass = area > 1000
        solar_health_score = estimate_solar_health(panel_count, area)

        print(f"[INFO] Processed {sample_id}: {panel_count} panels, area={area:.2f}, QC={qc_pass}")

        # Save overlay image
        overlay_path = os.path.join(OVERLAY_DIR, f"{sample_id}.jpg")
        cv2.imwrite(overlay_path, annotated_img)

        # Save manifest JSON
        ist = pytz.timezone("Asia/Kolkata")
        timestamp = datetime.utcnow().isoformat() + "Z"
        manifest = {
            "sample_id": sample_id,
            "lat": lat,
            "lon": lon,
            "has_solar": panel_count > 0,
            "confidence": round(float(results[0].boxes.conf[0]), 2) if results[0].boxes else 0.0,
            "pv_area_sqm_est": round(area / 10.764, 2),
            "buffer_radius_sqft": round(area),
            "qc_status": "VERIFIABLE" if qc_pass else "NOT_VERIFIABLE",
            "bbox_or_mask": bboxes,
            "image_metadata": {
                "source": "Google Static Maps",
                "capture_date": datetime.now().strftime("%Y-%m-%d")
            },
            "timestamp": timestamp,
        }
        with open(os.path.join(MANIFEST_DIR, f"{sample_id}.json"), "w") as f:
            json.dump(manifest, f, indent=2)

        # Append to metrics CSV
        metrics_df = pd.DataFrame([{
            "sample_id": sample_id,
            "panel_count": panel_count,
            "total_area": round(area, 2),
            "qc_flag": "Pass" if qc_pass else "Fail",
            "solar_health_score": solar_health_score
        }])
        if idx == 0:
            metrics_df.to_csv(METRICS_PATH, index=False)
        else:
            metrics_df.to_csv(METRICS_PATH, mode="a", header=False, index=False)

        # Generate certificate if eligible
        if is_eligible_for_certificate(qc_pass, solar_health_score):
            template_path = "certificates/cert_temp.txt"
            if os.path.exists(template_path):
                with open(template_path, encoding="utf-8") as f:
                    template = f.read()
                certificate_text = template.format(
                    sample_id=sample_id,
                    panel_count=panel_count,
                    total_area=round(area, 2),
                    qc_flag="Pass",
                    solar_health_score=solar_health_score,
                    date=datetime.now().strftime("%Y-%m-%d")
                )
                with open(os.path.join(CERT_DIR, f"{sample_id}_certificate.txt"), "w", encoding="utf-8") as f:
                    f.write(certificate_text)
            else:
                print(f"[WARNING] Certificate template not found at {template_path}")

    except Exception as e:
        print(f"[ERROR] Failed to process {row.get('sample_id', 'UNKNOWN')}: {e}")