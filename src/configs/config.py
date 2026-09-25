show = dict(
    image="data/raw/tifs/Tv11.tif",                # path to image for overlay
    steps=None,                # list of steps to visualize
    save_dir="viz/Tv11",             # directory to save visualizations
    windows=False,              # whether to display windows
    histograms=["clahe"],            # whether to plot histograms 
)

data = dict(
    raw_dir="data/raw",       # relative to project/
    pattern="*.tif",
    out_dir="dataset",
)
 
enhance = dict(
    type="clahe",              
    clip_limit=2.0,
    tile_grid=(8, 8),
    gamma=0.5,                 # gamma for equalized image
)