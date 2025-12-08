import os

def use_local_placeholder(sample_id, src_image_path):
    out_path = f"data/fetched/{sample_id}.jpg"
    with open(src_image_path, "rb") as src, open(out_path, "wb") as dst:
        dst.write(src.read())
    return out_path, None