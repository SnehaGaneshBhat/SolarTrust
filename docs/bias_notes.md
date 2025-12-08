# Bias & Fairness Considerations

## Known Biases

- **Urban Bias**: Most training data comes from urban rooftops. Rural, sloped, or thatched roofs are underrepresented, which may reduce accuracy in those areas.
- **Visual Confounders**: Objects like blue tarps, water tanks, and skylights may resemble solar panels and lead to false positives.
- **Image Quality**: Cloudy, low-resolution, or outdated satellite images can cause the model to miss panels or misclassify rooftops.
- **Geographic Skew**: The dataset may be biased toward certain regions or countries, limiting generalizability across India.

## Potential Impact

- **False Positives**: Households without solar panels may be incorrectly marked as eligible, risking subsidy misuse.
- **False Negatives**: Genuine solar installations may be missed, denying rightful benefits to households.
- **QC Status Sensitivity**: Low-confidence predictions may be flagged as `NOT_VERIFIABLE`, requiring manual review and slowing down the process.

## Mitigation Strategies

- Expand training data to include diverse roof types, rural areas, and seasonal imagery.
- Use ensemble models or segmentation overlays to improve precision.
- Flag low-confidence or ambiguous cases for human review.
- Regularly retrain the model with new verified data from different states and roof types.

## Ethical Note

This model is intended as a **decision-support tool**, not a final authority. Final subsidy decisions should always involve human oversight, especially in edge cases or low-confidence predictions.