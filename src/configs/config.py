show = dict(
    image="data/raw/tifs/Tv8.tif",                # path to image for overlay
    steps=None,                # list of steps to visualize
    save_dir="viz/Tv8",             # directory to save visualizations
    windows=True,              # whether to display windows
    histograms=["clahe"],            # whether to plot histograms 
    exercise1=False,
    exercise2=True,
)

data = dict(
    raw_dir="data/raw/tifs",       # relative to project/
    pattern="*.tif",
    out_dir="dataset",
)
 
enhance = dict(
    type="clahe",              
    clip_limit=2.0,
    tile_grid=(8, 8),
    gamma=0.5,                 # gamma for equalized image
    erode_size=25,              # size of the structuring element for morphological reconstruction
)