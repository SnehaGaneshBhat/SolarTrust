# Model Card – solar-panel-detector-v1

## Overview
- **Purpose:** Detect rooftop solar panels from satellite imagery.
- **Model:** YOLOv8, trained for 10 epochs.
- **Version:** v1.0

## Intended Use
- For verifying presence and area of solar panels on rooftops.
- Not for legal enforcement or real-time control.

## Data Sources
- Training images from Roboflow datasets and/or Google/ESRI imagery.
- Labels created manually using Roboflow annotation tool.

## Assumptions
- Panels are visible from top-down view.
- Images are 512x512 resolution.
- Panels have rectangular, dark-colored appearance.

## Limitations
- May miss small or shaded panels.
- Trained on limited roof types and geographies.
- May confuse skylights or dark roof tiles.

## Training Summary
- **Epochs:** 10
- **Model:** YOLOv8
- **Input size:** 512x512
- **Augmentations:** (list any you used, like flipping, rotation)

## Performance
- First image detected correctly.
- Second image missed a panel (needs more training).
- Confidence threshold: 0.25

## Inference & Outputs
- Input: `.xlsx` with sample_id, lat, lon
- Output:
  - JSON: `outputs/manifests/{sample_id}.json`
  - Overlay: `outputs/overlays/{sample_id}.jpg`
  - Metrics: `outputs/metrics/pipeline_metrics.csv`
  - Training predictions are summarized in `outputs/train_predictions/` for auditability.

## Retraining Guidance
- Resume training: `yolo detect train resume=True epochs=20`
- Add more diverse training data.
- Adjust confidence threshold if needed.

## Maintenance
- Monitor false positives/negatives.
- Retrain when adding new data or if performance drops.