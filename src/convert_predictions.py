import os
import json

# Load raw predictions
with open("outputs/predictions/predictions.json") as f:
    raw_data = json.load(f)

# Create output folder
output_dir = "outputs/train_predictions"
os.makedirs(output_dir, exist_ok=True)

# Process each image's predictions
for item in raw_data:
    image_name = item["image"]
    sample_id = os.path.splitext(image_name)[0]
    boxes = item["boxes"]

    panel_count = len(boxes)
    total_area = 0.0

    for box in boxes:
        x1, y1, x2, y2 = box["xyxy"]
        area = (x2 - x1) * (y2 - y1)
        total_area += area

    # Apply QC logic
    if panel_count == 0:
        qc_flag = "No panels"
    elif total_area < 1000:
        qc_flag = "Too small"
    else:
        qc_flag = "Pass"

    # Create summary dictionary
    summary = {
        "sample_id": sample_id,
        "panel_count": panel_count,
        "total_area": round(total_area, 2),
        "qc_flag": qc_flag
    }

    # Save as individual JSON
    output_path = os.path.join(output_dir, f"{sample_id}.json")
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Saved {sample_id}.json → {panel_count} panels, area={total_area:.1f}, QC={qc_flag}")