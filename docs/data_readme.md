\# Rooftop solar classification — dataset overview



\## Sources used

\- Alfred Weber Institute (Roboflow export)

\- LSGI547 Project (Roboflow export)

\- Piscinas Y Tenistable (Roboflow export)



\## Folder structure

data/ raw/ alfred\_weber/ lsgi547/ piscinas\_tenistable/ processed/ alfred\_weber/ images/ labels.csv lsgi547/ images/ labels.csv piscinas\_tenistable/ images/ labels.csv train\_split.csv val\_split.csv test\_split.csv





\## Preprocessing

\- Target size: 512×512 (to be applied before training)

\- Format: JPG

\- Color: RGB

\- Filenames: Match `processed/<dataset>/images/` exactly



\## Label schema

\- Columns: `filename`, `solar\_present`

\- `solar\_present`: 1 = solar panels present, 0 = no solar panels



\## Splits

\- Ratios: Train 70%, Val 20%, Test 10%

\- Files:

&nbsp; - `data/train\_split.csv`

&nbsp; - `data/val\_split.csv`

&nbsp; - `data/test\_split.csv`



\## Counts (fill after Step 5)

\- Train: 153 images (1:127 , 0: 26)

\- Val: 33 images (1: 28, 0: 5)

\- Test: 22 images (1: 19, 0: 3)



\## Known limitations

\- Urban imagery bias; rural roofs underrepresented

\- Shadows and occlusions may hide panels

\- Resolution and date variability; stale imagery possible

\- Negative examples include pools/courts that may resemble panels



\## Attribution and licenses

\- Dataset authors: Alfred Weber, LSGI547, Piscinas Y Tenistable (respect respective licenses)

\- Use is for academic prototyping in EcoInnovators Ideathon



\## Versioning

\- Data version: v0.1 (2025‑11‑30)

\- Changes:

&nbsp; - v0.1 — Initial consolidation, labels aligned, splits created

## Baseline results (Day 3)
- **Model:** ResNet18 (transfer learning)
- **Epochs:** 10
- **Best validation F1:** 1.0000
- **Best validation accuracy:** 1.0000
- **Test accuracy:** 1.0000
- **Test F1:** 1.0000
- **Notes:** Strong baseline; verify no data leakage; proceed to Day 4 for quantification/explainability.