
""" Build the cilia patch dataset from raw PCD micrographs.

    Run: python -m src.pipeline.build_dataset
"""
import csv
import random
from pathlib import Path
 
import cv2
import numpy as np
 
from src.configs import config as cfg
from src.utils.utils import load_raw_gray 

def assign_splits():
    return


def process_image(img_path: str, out_path: str, start_id: int):
    img_raw = load_raw_gray(img_path=img_path)


    return

def main():
    # input paths
    raw = Path(cfg.data["raw_dir"])
    out = Path(cfg.data["out_dir"])

    # clearing before producing
    for sub in ("images", "masks", "overlays"):
        (out / sub).mkdir(parents=True, exist_ok=True)
        for f in (out / sub).glob("*.png"):  # clear stale results
            f.unlink()

    # all image paths
    paths = sorted(raw.glob(cfg.data["pattern"]))
    if not paths:
        raise FileNotFoundError(f"no {cfg.data['pattern']} in {raw.resolve()}")

    # process all images
    rows = []
    for p in paths:
        rows += process_image(p, out, start_id=len(rows))
    
    if not rows:
        print("No cilia kept - check the area / shape limits in config.py")
        return
 
    assign_splits(rows)
    with open(out / "meta.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
 
    counts = [r["mt_count"] for r in rows]
    print(f"\n{len(rows)} patches -> {out}/")
    print(f"microtubule count: median={np.median(counts):.0f}  "
          f"==11: {sum(c == 11 for c in counts)}/{len(counts)}")
 
 
if __name__ == "__main__":
    main()