
""" Build the cilia patch dataset from raw PCD micrographs.

    Run: python -m src.pipeline.build_dataset
"""
import csv
import random
from pathlib import Path
 
import cv2
import numpy as np
 
from src.utils.utils import load_raw_gray 

def assign_splits():
    return

def extract_patches(raw, clahe, contours, pad=5):
    """Cut one patch per cilium from the raw and CLAHE image, plus a mask of that cilium."""
    H, W = raw.shape                                   # image size, to keep boxes inside the image
    patches = []
    for c in contours:
        # smallest upright rectangle around the contour: top-left (x, y), width, height
        x, y, w, h = cv2.boundingRect(c)

        # enlarge the box by `pad` on each side so the cilium doesn't touch the patch border
        # (erosion / reconstruction behave poorly at borders); clip to the image edges
        x0, y0 = max(x - pad, 0), max(y - pad, 0)
        x1, y1 = min(x + w + pad, W), min(y + h + pad, H)

        # patch-sized mask with only THIS cilium filled white (thickness=-1 = filled);
        # offset shifts the contour from full-image to patch coordinates.
        # neighbouring cilia that fall inside the box are not in this mask
        mask = np.zeros((y1 - y0, x1 - x0), np.uint8)
        cv2.drawContours(mask, [c], -1, 255, thickness=-1, offset=(-x0, -y0))

        # numpy indexes [rows, cols] = [y, x]; all crops use the same box,
        # so pixel (i, j) means the same point in each of them.
        # slices are views into the full image - use .copy() before modifying them in place
        patches.append({
            "raw":   raw[y0:y1, x0:x1],        # unaltered data, saved to the dataset
            "clahe": clahe[y0:y1, x0:x1],      # enhanced version, used for microtubule detection
            "mask":  mask,                     # cilium shape, used to drop neighbours' microtubules
            "box":   (x0, y0, x1, y1),         # position in the full image, for overlays / tracing back
        })
    return patches

def segment_cilia(img_raw, cfg):

    e = cfg.enhance
    clahe = cv2.createCLAHE(clipLimit=e["clip_limit"], tileGridSize=e["tile_grid"]).apply(img_raw)
    t, binary = cv2.threshold(clahe, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) # get the inverse binary mask of the cilia, otsu method for thresholding
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # only outermost contours, approx. shape

    return contours

def process_image(img_path: str, out_path: str, cfg: dict,  start_id: int):
    e = cfg.enhance
    
    img_raw = load_raw_gray(img_path=img_path)
    clahe = cv2.createCLAHE(clipLimit=e["clip_limit"], tileGridSize=e["tile_grid"]).apply(img_raw)
    contours = segment_cilia(img_raw, cfg)
    rows = []
    for i, p in enumerate(extract_patches(img_raw, clahe, contours)):
        # mt, n = count_microtubules(p["clahe"], p["mask"], e)

        pid = start_id + i
        name = f"{pid:05d}.png"
        cv2.imwrite(str(out_path / "images" / name), p["raw"])
        # cv2.imwrite(str(out_path / "masks" / name), mt)
        # cv2.imwrite(str(out_path / "overlays" / name), make_overlay(p["raw"], p["mask"], mt))

        x0, y0, x1, y1 = p["box"]
        rows.append(dict(id=pid, file=name, source=img_path.name,
                         x0=x0, y0=y0, x1=x1, y1=y1, mt_count=0, split=""))

    print(f"{img_path.name}: {len(rows)} cilia")
    return rows


    return

def main(cfg):
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

    print(paths)
    # process all images
    rows = []
    for p in paths:
        rows += process_image(p, out, cfg, start_id=len(rows))
    
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
 
