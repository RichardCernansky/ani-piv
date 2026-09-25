import cv2, numpy as np, matplotlib.pyplot as plt

def to_256(img):
    """Convert any image to uint8 0–255"""
    if img.dtype == np.uint8:
        return img
    if img.dtype == bool:
        return img.astype(np.uint8) * 255
    if np.issubdtype(img.dtype, np.floating):
        if img.min() >= 0 and img.max() <= 1:            # float in [0, 1]
            return (img * 255).round().astype(np.uint8)
    # anything else stretch min–max to 0–255 (uint16, float outside [0, 1])
    return cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

def gamma(img, g):
    return cv2.pow(img.astype(np.float32), g)       # already float in [0, 1]

# show image
def imshow(name, img):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, img)

# plot historgram
def plot_hist(img, title, ax=None):
    """Plot the 256-bin histogram of a uint8 grayscale image. Returns the figure."""
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    if ax is None:
        _, ax = plt.subplots() # only single plot, creates a new figure
    ax.plot(hist)
    ax.set_xlim(0, 255)
    ax.set_xlabel("intensity")
    ax.set_ylabel("pixel count")
    ax.set_title(title)
    return ax.figure
 
 
def load_raw_gray(img_path: str):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    return img

def print_img_stats(img):
    print(img.dtype, img.shape, img.min(), img.max())

def normalize_img(img_256):
    img_f = cv2.normalize(img_256, None, 0, 1, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    return img_f

