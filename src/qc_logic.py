import pandas as pd

df = pd.read_csv("outputs/metrics/area_summary.csv")

def qc(row):
    if row["num_boxes"] == 0: return "NOT_VERIFIABLE"
    if row["max_conf"] < 0.5: return "NOT_VERIFIABLE"
    if row["total_area_pixels"] < 1000: return "NOT_VERIFIABLE"
    return "VERIFIABLE"

df["qc_status"] = df.apply(qc, axis=1)
df.to_csv("outputs/metrics/area_qc.csv", index=False)
print("QC results saved")