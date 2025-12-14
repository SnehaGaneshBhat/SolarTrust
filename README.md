#  EcoInnovators Ideathon 2026 – AI Powered Rooftop PV Detection
#SolarTrust

##  Overview
This project verifies rooftop solar installations using **AI and satellite imagery**.  
It supports the *PM Surya Ghar: Muft Bijli Yojana* scheme by ensuring subsidies reach genuine households.  

Instead of sending inspectors to every house, our pipeline:
- Fetches rooftop images for given coordinates.
- Detects whether solar panels are present.
- Estimates panel area (m²).
- Produces **audit‑friendly overlays** (bounding boxes/polygons).
- Outputs JSON records with confidence scores and QC status.
-Residents are also provided with a government approved certificate for presence of solar panels.

This makes subsidy distribution **faster, cheaper, and more trustworthy**.

---

##  Real‑World Example
A DISCOM officer uploads a file with 1,000 household coordinates:
- 700 houses → solar panels found.  
- 200 houses → no solar panels.  
- 100 houses → images too blurry/cloudy → NOT_VERIFIABLE.  

Officer downloads JSON + overlay images → submits as audit proof.  
Subsidies go only to verified households.

---

## Repository Structure
solar-verification-app/
├── src/
│   └── run_pipeline.py        # Main pipeline script for inference
├── app.py                     # Streamlit dashboard for DISCOM and citizen views
├── env/                       # Environment setup files
│   ├── requirements.txt
│   ├── environment.yml
│   └── python_version.txt
├── models/                    # Trained YOLOv8 model (.pt)
│   └── best.pt
├── docs/                      # Documentation
│   ├── model_card.md
│   ├── model_card.pdf
│   └── data_readme.md
├── inputs/                    # Input .xlsx files with sample_id, lat, lon
│   └── input.xlsx
├── outputs/                   # All generated outputs
│   ├── overlays/              # Audit overlay images with bounding boxes
│   ├── manifests/             # JSON prediction files
│   └── metrics/               # pipeline_metrics.csv and summary stats
├── certificates/              # Generated certificate .txt files and template
│   └── certificate_template.txt
├── training_logs/             # Training metrics (loss, F1, RMSE) across epochs
├── ui/                        # Streamlit theme and config of dashboards
│   ├── resident_dashboard
|   └── official_dashboard
├── media/
|   ├── SolarTrust.mp4         # Advertisement video for the website
|   └── figma_link             # Link to our Figma Prototype for the website
├── LICENSE                    # MIT License file
└── README.md                  # Project overview and run instructions

---

## Data
Training datasets are not included in this repository to keep it lightweight.
To run the pipeline, please provide your own data or use the API integration.

---

## Setup and Usage Instructions
### 1. Clone the repository
git clone https://github.com/roopashreejs08/-solar-verification-app---.git
cd -solar-verification-app---

### 2. Create and activate a virtual environment
python -m venv venv
**On Mac/Linux:**
source venv/bin/activate
**On Windows (PowerShell):**
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Create a .env file in the repo root
NOTE: (Judges must replace YOUR_SECRET_KEY with their own valid Google Maps API key)
echo "GOOGLE_MAPS_API_KEY=YOUR_SECRET_KEY" > .env

### 5. Run the application
streamlit run app.py\

---

## Web App Features
- Choose role: Official or Resident
- Upload Excel file with sample_id, lat, lon
- View satellite images and solar panel detection
- Download overlays, JSON manifests, and certificates

(Optional) Run the backend pipeline directly
python pipeline_code/run_pipeline.py inputs/input.xlsx

### Outputs will be saved to:
 - data/fetched/         -> Satellite images
 - outputs/overlays/     -> YOLO overlay images
 - outputs/manifests/    -> Manifest JSON files
 - outputs/metrics/      -> pipeline_metrics.csv
 - certificates/         -> Generated certificates

### Example output JSON:
 {
   "sample_id": 1234,
   "lat": 12.9716,
   "lon": 77.5946,
   "has_solar": true,
   "confidence": 0.92,
   "pv_area_sqm_est": 23.5,
   "buffer_radius_sqft": 1200,
   "qc_status": "VERIFIABLE",
   "bbox_or_mask": [[x1, y1, x2, y2], ...],
   "image_metadata": {
     "source": "Google",
     "capture_date": "2025-11-01"
   },
   "timestamp": "2025-12-08T09:52:54.484451Z"
}

---

## Evaluation Criteria
- Detection Accuracy (40%) → F1 score on solar presence.  
- Quantification Quality (20%) → RMSE for PV area estimation.  
- Generalization & Robustness (20%) → Works across diverse roof types/states.  
- Usability & Documentation (20%) → Clear repo structure, reproducibility, auditability.  

---

## Model Card (Summary)
- Data Sources: Roboflow datasets + augmentations.  
- Assumptions: Resolution thresholds, buffer zones.  
- Logic: Classification + segmentation.  
- Limitations: Shadows, occlusion, rural imagery gaps.  
- Failure Modes: Low resolution, stale imagery.  
- Retraining Guidance: Add new annotated data for diverse roof types.  

---

## Extra Features
- Solar Health Monitoring: Predicts panel efficiency using weather + visual cues.  
- Digital Certificates: Tamper‑proof verification for households.  
- Citizen Portal: Transparency for households to track subsidy status.  
- Savings Calculator on resident dashboard for residents to understand the amount of energy they're saving  per month

---

## Future Scope
- **React.js Frontend**: Replace Streamlit with a more dynamic and scalable UI.
- **Backend Integration**: Add APIs for model inference, data storage, and user management.
- **AI Chatbot**: Embed a chatbot for real-time user assistance and support.

---

##  License
This project is licensed under the **MIT License** – see the LICENSE file for details.

---

## Members
- Sneha Ganesh Bhat [https://github.com/SnehaGaneshBhat]
- Roopa Shree J S [https://github.com/roopashreejs08]

