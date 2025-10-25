from pathlib import Path
import sys

THIS_DIR   = Path(__file__).resolve().parent        
SCRIPTS_DIR= THIS_DIR.parent                        
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import settings                                  

import pandas as pd
import pingouin as pg
import statsmodels.formula.api as smf
import statsmodels.api as sm

# UTF-8 cuz windows shits itself on some characters here
def clog(*args, log=None, **kwargs):
    print(*args, **kwargs)               # console
    if log is not None:
        print(*args, **kwargs, file=log) # file

def load_metric_csv(base: Path, dataset_prefix: str, metric: str, names):
    """
    metric one of: rs, acc, con, gist, id
    dataset_prefix '' for tnt; 'nas ' for nas.
    Filenames like: 'tnt run data - rs.csv' or 'nas tnt run data - rs.csv'
    """
    fname = f"{dataset_prefix}tnt run data - {metric}.csv"
    fpath = base / fname
    if not fpath.exists():
        raise FileNotFoundError(f"Missing file: {fpath}")
    return pd.read_csv(fpath, header=None, names=names)

def melt_df(df, colname):
    df = df.copy()
    df["Subject"] = df.index + 1
    return df.melt(id_vars="Subject", var_name="Condition", value_name=colname)

def run_once(data_dir: Path, dataset: str):
    # choose prefix + log name
    if dataset == "tnt":
        prefix = ""                   
        log_name = "TNTresult.txt"
    else:
        prefix = "nas "
        log_name = "NASresult.txt"

    log_path = settings.OUTPUT_DIR / log_name
    with open(log_path, "w", encoding="UTF-8") as log:
        names = ["Think","Baseline","NoThink"]

        rs   = load_metric_csv(settings.DATA_DIR, prefix, "rs",   names)
        acc  = load_metric_csv(settings.DATA_DIR, prefix, "acc",  names)
        con  = load_metric_csv(settings.DATA_DIR, prefix, "con",  names)
        gist = load_metric_csv(settings.DATA_DIR, prefix, "gist", names)
        iden = load_metric_csv(settings.DATA_DIR, prefix, "id",   names)

        dfs = [melt_df(rs, "RecallScore"), melt_df(acc, "Accuracy"),
               melt_df(con, "Confidence"), melt_df(gist, "Gist"),
               melt_df(iden, "Identification")]

        df = dfs[0]
        for d in dfs[1:]:
            df = df.merge(d, on=["Subject","Condition"])

        measures = ["Accuracy","Confidence","RecallScore","Gist"]
        for dv in measures:
            clog(f"\n=== RM-ANOVA: {dv} ===", log=log)
            aov_acc = pg.rm_anova(dv=dv, within="Condition", subject="Subject", data=df, detailed=True)
            clog(aov_acc[["Source","F","p-unc","ng2"]], log=log)

            clog(f"\n=== Post-hoc Tests: {dv} ===", log=log)
            post = pg.pairwise_tests(dv=dv, within="Condition", subject="Subject", data=df,
                                     parametric=True, padjust="holm")

            # Bayes factors from t
            n_subj = df["Subject"].nunique()
            post["BF10"] = [pg.bayesfactor_ttest(t, n_subj, paired=True) for t in post["T"]]

            clog(post[["A","B","T","p-corr","hedges","BF10"]], log=log)

        clog("\n=== GEE: Identification ===", log=log)
        gee_id = smf.gee("Identification ~ C(Condition, Treatment('Baseline'))", "Subject",
                         family=sm.families.Binomial(), data=df).fit()
        clog(gee_id.summary().as_text(), log=log)

    print(f"Wrote {log_path}")

def main():
    if settings.RUN_BOTH:
        for ds in ["tnt","nas"]:
            try: run_once(settings.DATA_DIR, ds)
            except FileNotFoundError as e: print(e)
    else:
        run_once(settings.DATA_DIR, settings.DATASET)

if __name__ == "__main__":
    main()