
# Inducing Forgetting of Unwanted Memories Through Subliminal Reactivation

Jaikaran Kelley
2207367

If you've been handed this project and need help with anything, feel free to reach out: <jakeykelley@gmail.com>.

This was built for my Capstone research project. I was not able to fully conduct a laboratory EEG & GSR experiment with a significant sample size due to the ethics timeline taking over 3 months (too close to the Capstone deadline). If someone inherits this, I would love to help and see the study flourish. The full EEG & GSR acquisition modules are already nearly done, albeit they are commented out/missing in this repo. I have the code saved separately -- reach out and I'd be happy to share it.

Also, all the stimuli images are from OASIS and IAPS. For that reason, they are not included in this repo. If institutionally permitted, I would be happy to share the exact set I curated (I spent a long time considering emotional aversiveness (in an attempt to balance participant comfort with potential GSR impact)).

## README Chapters

- Project Structure
- Tutorial
- Analysis and Plots
- Info
- Tested Systems/Versions
- Original Experiment

## Project Structure

├── README.md
├── requirements.txt              # pip install -r requirements.txt
├── data/                         # participant CSV + state files
├── images/                       # stimuli images (user-supplied; not in repo)
├── masks/                        # mask images (run mask.py to generate masks from /images/)
├── bsusb/                        # BioSemi trigger helper
├── main.py                       # run this to launch experiment
├── phases/
    ├── learning.py               # learning phase logic
    ├── tnt_practice.py           # tnt practice phase logic
    ├── tnt.py                    # tnt phase logic
    ├── pair_refresher.py         # optional pair refresher phase logic
    └── final_recall.py           # final recall phase logic
├── utils/
    ├── config.py                 # testing flag (set testing=True to speed up program for debugging)
    ├── io.py                     # per-participant state JSONs, per-participant data CSVs
    ├── stimuli.py                # word-image table assembly (left descriptions of my experiment's images in the case of future project inheritance)
    └── timing.py                 # press Escape during pauses in the experiment to safely close the experiment (closing PsychoPy windows can be a pain)
└── scripts/
    ├── mask.py                   # generates masks from /images/
    ├── resize.py                 # resizes each image to 400px height while keeping aspect ratio
    ├── analysis/
        └── analysis.py           # analysis (GEE, ANOVA/RM-ANOVA, post-hoc (Holm), Bayes factors)
    ├── boxplots/
        ├── boxplotSingle.py      # plots a single boxplot
        └── boxplotDouble.py      # two metrics, side-by-side
    └── DATA/                     # means of different conditions from each experiment (data supplied from my own experiment)

## Tutorial

Step 1:

```bash
python -m venv .venv
.venv\Scripts\activate # on windows
pip install --upgrade pip
pip install -r requirements.txt
```

Step 2:
(1) Add your stimuli. This repo does NOT include my images due to OASIS/IAPS licensing concerns. Place 110 images, named 1.jpg, 2.jpg, ... 110.jpg in /images.
(2) Then resize your images to a consistent height. This is optional, but I would personally recommend it. Running resize.py will resize all images in /images, default height 400px and keeps aspect ratio.
(3) Then generate your masks. By running mask.py, all images in /images will generate equivalent mask images in /masks.

Step 3:

```bash
python main.py
```

When you run main.py, the program will ask you to input your participant ID. In the case of the program crashing, you can use this to restore progress.
The program follows a modified Think/No-Think paradigm. During the Think/No-Think phase, sandwich-masked bystander targets will be subliminally presented throughout each trial.

## Analysis and Plots

To run the analysis and plot scripts;

Step 1:
Find /scripts/DATA/ and input the following CSVs (inspect my data for the format):

- nas tnt run data - acc.csv
- nas tnt run data - con.csv
- nas tnt run data - gist.csv
- nas tnt run data - id.csv
- nas tnt run data - rs.csv
- tnt run data - acc.csv
- tnt run data - con.csv
- tnt run data - gist.csv
- tnt run data - id.csv
- tnt run data - rs.csv

Step 2:
Find each script (boxplotSingle.py, boxplotDouble.py, analysis.py), and edit the configs in each script. For example:

```py
# === CONFIG         ===
DATASET  = "tnt"       # "tnt" (amnesic shadow) or "nas" (no amnesic shadow)
RUN_BOTH = True        # True = render both TNT and NAS
COMPARE  = "acc-con"   # "acc-con" or "gist-id"
# ======================
```

Step 3:

```bash
python scripts\analysis\analysis.py
python scripts\boxplots\boxplotSingle.py
python scripts\boxplots\boxplotDouble.py
```

## Info

PsychoPy is frame-locked, but this repo did not include photodiode verification; expect small timing noise outside a lab. This is particularly relevant for this experiment, as keeping  bystander cues appearing subliminally, so as close to 15ms as possible, is imperative.
Run this experiment on 60hz refresh rate, even if the monitor can handle 144hz, 240hz, 360hz, 500hz, etc. 1 frame is ~16ms.
Disable Game Mode and Freesync/G-Sync/whatever variable refresh rates. Keep monitor plugged into GPU if possible. Enable high performance power plans, especially if on a laptop. Optionally, you can also try and maximise the bystander cue presentation consistency by using a program like Process Lasso to keep PsychoPy bound to CPU core #0 on high priority.
Especially if the monitor is not OLED, attempt to keep the participant looking straight at the monitor, with a consistent viewing angle for all participants.

For optimal results, try to minimise delays between phases (while balancing the participant's focus) and seriously hammer in that they should not be substituting thoughts during No-Think trials.

To skip to a phase for testing purposes, you can change the participant's state file to a certain stage.
e.g. if the file reads something like: {"currentPhase": "FinalRecall", "currentTrial": 14}, change it to any of these stages to start from there:
    - "Learning"
    - "TNTPractice"
    - "TNT"
    - "PairRefresher"
    - "FinalRecall"
    - "Completed"

What is NAS? NAS = “No Amnesic Shadow” — i.e., the standard TNT items without bystander flashes. In the scripts you’ll see both TNT and NAS datasets.

## Tested Systems/Versions

Tested on:

- Desktop, Windows 11 LTSC,             Python 3.10, 1080p 24" 360hz monitor limited to 60hz (ASUS PG259QN), Ryzen 7800x3D, GTX 4070
- Laptop,  Fedora 40 (AwesomeWM, SDDM), Python 3.10, 1080p 15.6" 240hz monitor limited to 60hz (AORUS 15P),  i7-11800H,     GTX 3070 Mobile

Has worked fine with minimal issues -- timing checks via screen recordings and high FPS (within reason -- I'm sure particularly high FPS cameras would prove to be accurate for this) camera are indicative only; a photodiode is recommended for true verification.

## Original Experiment

Z. Zhu, M. C. Anderson, and Y. Wang, “Inducing forgetting of unwanted memories through subliminal reactivation,” Nature Communications, vol. 13, no. 1, Oct. 2022, doi: <https://doi.org/10.1038/s41467-022-34091-1>.
