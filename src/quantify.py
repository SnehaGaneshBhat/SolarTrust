import json, os, pandas as pd

PRED_JSON = "outputs/predictions/predictions.json"
OUT_CSV = "outputs/metrics/area_summary.csv"
os.makedirs("outputs/metrics", exist_ok=True)

def box_area(xyxy):
    x1,y1,x2,y2 = xyxy
    return (x2-x1) * (y2-y1)

with open(PRED_JSON) as f:
    preds = json.load(f)

rows = []
for p in preds:
    total_area = sum(box_area(b["xyxy"]) for b in p["boxes"])
    max_conf = max((b["conf"] for b in p["boxes"]), default=0)
    rows.append({"image": p["image"], "num_boxes": len(p["boxes"]),
                 "total_area_pixels": total_area, "max_conf": max_conf})

pd.DataFrame(rows).to_csv(OUT_CSV, index=False)
print(f"Saved {OUT_CSV}")