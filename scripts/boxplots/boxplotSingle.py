import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# === CONFIG         ===
DATASET  = "tnt"       # "tnt" (amnesic shadow) or "nas" (no amnesic shadow)
RUN_BOTH = True        # True = render both TNT and NAS
# ======================
# THIS WILL OUTPUT THE FILE TO THE MASTER FOLDER
# Given that Acc-Con and Gist-ID are pairs, and RS is separate, this script is hard-coded to plot RS only

def _base_dir():
    # scripts/boxplots -> scripts -> DATA
    return Path(__file__).resolve().parents[1] / "DATA"

def _csv_path(dataset: str, metric: str):
    prefix = "" if dataset == "tnt" else "nas "
    return _base_dir() / f"{prefix}tnt run data - {metric}.csv"

def _render(dataset: str):
    # normal set recall score (kept your original plot + labels)
    file1_path = _csv_path(dataset, "rs")
    df1 = pd.read_csv(file1_path)
    column_labels = ["Think", "No-think", "Control"]
    df1.columns = column_labels

    # melts and adds labels
    df1_melted = df1.melt(var_name="Condition", value_name="Values")
    df1_melted["Condition"] = df1_melted["Condition"] + " (Gist)"  # kept as-is

    category_order = ["Think (Gist)", "No-think (Gist)", "Control (Gist)"]
    custom_palette = ["#C4A872", "#2B736F", "#EFECDF"] # colours

    # plot
    plt.figure(figsize=(8, 8))
    ax = sns.boxplot(x="Condition", y="Values", data=df1_melted, 
                    order=category_order, showmeans=True,
                    meanprops={"marker":"x", "markerfacecolor":"#111722", "markeredgecolor":"#111722", "markersize":"4"},
                    palette=custom_palette, linewidth=0.5, width=0.5)  # Thinner boxes

    # calculate mean values for each set
    means = df1_melted.groupby("Condition")["Values"].mean()
    gist_means = means.loc[["Think (Gist)", "No-think (Gist)", "Control (Gist)"]].values

    x_positions_gist = [0, 1, 2]  
    x_positions_id = [4, 5, 6]    

    # draws dotted lines to connect the means
    plt.plot(x_positions_gist, gist_means, 'x-', linestyle="dotted", color="#111722", linewidth=1)

    plt.ylabel("Recall Score", fontsize=18)
    plt.title(f"Recall Scores — {dataset.upper()}", fontsize=16)  # add dataset to title
    plt.xlabel("") # remove x axis label
    plt.xticks(ticks=np.arange(len(category_order)), labels=["Think", "No-think", "Control"], fontsize=12)

    sns.despine() # top right and top borders
    plt.gca().patch.set_alpha(0) # transparent background

    # save (include dataset to avoid overwrite when RUN_BOTH=True)
    out_name = f"{dataset}_recall_score.png"
    plt.savefig(out_name, dpi=300, bbox_inches='tight', transparent=True)
    print(f"Saved {out_name}")
    plt.show()

if RUN_BOTH:
    for ds in ["tnt","nas"]:
        try:
            _render(ds)
        except FileNotFoundError as e:
            print(e)
else:
    _render(DATASET)