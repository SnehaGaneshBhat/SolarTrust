import cv2, os, json

PRED_JSON = "outputs/predictions/predictions.json"
IMG_DIR = "data/test"
OUT_DIR = "outputs/overlays"
os.makedirs(OUT_DIR, exist_ok=True)

with open(PRED_JSON) as f:
    preds = json.load(f)

for p in preds:
    img = cv2.imread(os.path.join(IMG_DIR, p["image"]))
    for b in p["boxes"]:
        x1,y1,x2,y2 = map(int, b["xyxy"])
        cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
        cv2.putText(img, f"conf={b['conf']:.2f}", (x1,y1-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    cv2.imwrite(os.path.join(OUT_DIR, p["image"]), img)