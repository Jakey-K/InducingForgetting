import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# === CONFIG         ===
DATASET  = "tnt"       # "tnt" (amnesic shadow) or "nas" (no amnesic shadow)
RUN_BOTH = True        # True = render both TNT and NAS
COMPARE  = "acc-con"   # "acc-con" or "gist-id"
# ======================
# THIS WILL OUTPUT THE FILE TO THE MASTER FOLDER

def _base_dir():
    # /scripts/DATA
    return Path(__file__).resolve().parents[1] / "DATA"

def _csv_path(dataset: str, metric: str):
    prefix = "" if dataset == "tnt" else "nas "
    return _base_dir() / f"{prefix}tnt run data - {metric}.csv"

def _render(dataset: str):
    # default here uses acc vs con (kept your code)\
    if COMPARE == "acc-con":
        file1_path = _csv_path(dataset, "acc")
        file2_path = _csv_path(dataset, "con")
    else: # gist vs id
        file1_path = _csv_path(dataset, "gist")
        file2_path = _csv_path(dataset, "id")
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)

    column_labels = ["Think", "No-think", "Control"]
    df1.columns = column_labels
    df2 = df2.iloc[:, :3]  
    df2.columns = column_labels

    # melts and adds labels
    if COMPARE == "acc-con":
        value1 = "Accuracy"
        value2 = "Confidence"
    else:
        value1 = "Gist"
        value2 = "ID"
    df1_melted = df1.melt(var_name="Condition", value_name="Values")
    df1_melted["Condition"] = df1_melted["Condition"] + " (" + value1 + ")"
    df2_melted = df2.melt(var_name="Condition", value_name="Values")
    df2_melted["Condition"] = df2_melted["Condition"] + " (" + value2 + ")"

    # fake category for spacing
    gap_df = pd.DataFrame({"Condition": [" "], "Values": [None]}) 

    # combines the datasets
    df_combined = pd.concat([df1_melted, gap_df, df2_melted], ignore_index=True)

    category_order = ["Think (" + value1 + ")", "No-think (" + value1 + ")", "Control (" + value1 + ")",  
                    " ",  # this is the gap in the middle (aesthetic)
                    "Think (" + value2 + ")", "No-think (" + value2 + ")", "Control (" + value2 + ")"]

    custom_palette = ["#C4A872", "#2B736F", "#EFECDF", "white", "#C4A872", "#2B736F", "#EFECDF"]

    # plot
    plt.figure(figsize=(10, 6))
    ax = sns.boxplot(x="Condition", y="Values", data=df_combined, 
                    order=category_order, showmeans=True,
                    meanprops={"marker":"x", "markerfacecolor":"#111722", "markeredgecolor":"#111722", "markersize":"4"},
                    palette=custom_palette, linewidth=0.5, width=0.5)  

    # calculate mean values for each set
    means = df_combined.groupby("Condition")["Values"].mean()
    gist_means = means.loc[["Think (" + value1 + ")", "No-think (" + value1 + ")", "Control (" + value1 + ")"]].values
    id_means = means.loc[["Think (" + value2 + ")", "No-think (" + value2 + ")", "Control (" + value2 + ")"]].values

    x_positions_gist = [0, 1, 2]  
    x_positions_id = [4, 5, 6]    

    # draws dotted lines to connect the means
    plt.plot(x_positions_gist, gist_means, 'x-', linestyle="dotted", color="#111722", linewidth=1)
    plt.plot(x_positions_id, id_means, 'x-', linestyle="dotted", color="#111722", linewidth=1)

    #### LABELS
    plt.ylabel("% Correctly Recalled", fontsize=18)
    plt.title(value1 + " Recall Scores                     " + value2 + " Recall Scores", fontsize=16)

    #### LABELS
    plt.xlabel("") # remove x axis label
    plt.xticks(ticks=np.arange(len(category_order)), labels=["Think", "No-think", "Control", "", "Think", "No-think", "Control"], fontsize=12)

    sns.despine() # top right and top borders
    plt.gca().patch.set_alpha(0) # transparent background

    # save (include dataset to avoid overwrite when RUN_BOTH=True)
    out_name = f"{dataset}_NameMe.png"
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
