from pathlib import Path

# auto-detect repo root 
REPO_ROOT = Path(__file__).resolve().parents[1]

# data + images
DATA_DIR   = REPO_ROOT / "scripts" / "DATA"   # csvs folder
IMAGES_DIR = REPO_ROOT / "images"             # images folder

# analysis toggles
RUN_BOTH = True       # True = run TNT and NAS in one go
DATASET  = "nas"       # "tnt" or "nas" when RUN_BOTH is False

# boxplotSingle options
SINGLE_METRIC = "rs"             # one of: "rs","acc","con","gist","id"
SINGLE_LABEL  = "Recall Score"   # or None to auto-label

# boxplotDouble options
DOUBLE_PAIR = "acc-con"    # "gist-id" or "acc-con"

# outputs
OUTPUT_DIR = REPO_ROOT     # where PNGs and result logs are written

# resize tool
START_INDEX   = 1
END_INDEX     = 110        # set to however many images you have
RESIZE_HEIGHT = 300        
