from psychopy import *
from bsusb import bsusb
from utils.timing import check_for_exit
from utils.io import saveData, saveState
from utils.config import testing
import numpy as np
import random

# helpers for the mini form for the final recall phase examiner input
def render_form(win, cue, fields, active_idx):
    cueStim = visual.TextStim(win, text=f"Cue: {cue}", pos=(0, 250), color="white", height=50)
    cueStim.draw()

    y = 80
    for i, f in enumerate(fields):
        color = "yellow" if i == active_idx else "green"
        label = visual.TextStim(win, text=f["label"], pos=(-250, y), color="white", height=40, alignText="left")
        value = visual.TextStim(win, text=f["value"] or "_", pos=( 150, y), color=color,  height=40)
        label.draw(); value.draw()
        y -= 90

# for the final recall phase examiner input form
def run_form(win, cue):
    fields = [
        {"label": "Accuracy   (1-5)",             "value": ""},
        {"label": "Confidence (1-5)",             "value": ""},
        {"label": "Identification (I/N)",         "value": ""},
        {"label": "Gist elems recalled (0-5)",    "value": ""},
    ]
    converters = [
        lambda v: max(1, min(5, int(v))),
        lambda v: max(1, min(5, int(v))),
        lambda v: 1 if v.lower()=="i" else 0,
        lambda v: max(0, min(5, int(v))),
    ]
    allowed_sets = [
        list("12345"), list("12345"),
        ["i","n","I","N"], list("012345")
    ]

    idx = 0
    buffer = ""
    first_key_rt = None
    timer = core.Clock()

    while True:
        render_form(win, cue, fields, idx)
        win.flip()

        key = event.waitKeys(keyList=allowed_sets[idx] + ["backspace","tab","return","escape"])[0]

        if key == "escape":
            raise KeyboardInterrupt

        # backspace
        if key == "backspace":
            if buffer:
                buffer = buffer[:-1] 
            elif idx>0:
                # jump back, restore old value
                idx -= 1
                buffer = fields[idx]["value"]
                fields[idx]["value"] = ""
            continue

        # capture RT on first keystroke in field 0
        if idx==0 and key not in ["tab","return"]:
            if first_key_rt is None:
                first_key_rt = timer.getTime()

        # move forward
        if key in ["tab","return"]:
            if not buffer: # checks if empty
                continue
            fields[idx]["value"] = buffer 
            buffer = "" 
            if idx==3:    # last field done -- break
                break
            idx += 1
            continue # go next

        # regular character
        buffer += key

    # convert
    vals = [conv(f["value"]) for conv,f in zip(converters, fields)]
    accuracy, confidence, identification, gist_raw = vals
    rt = first_key_rt or 0.0
    return accuracy, confidence, identification, gist_raw, rt

################### FINAL RECALL PHASE #####################
def finalRecallPhase(win, wordPairs, participantInfo, participantData, control_cues, startTrial=0):
    # Set seed for consistent shuffling
    seed = int(participantInfo['ID'])
    np.random.seed(seed)
    random.seed(seed)

    instructions = visual.TextStim(win, text="""
    FINAL RECALL PHASE

    You will see cue words one at a time.

    Provide the target word associated with each cue to the examiner.

    Press any key to begin.""", color="white")
    instructions.draw()
    win.flip()
    event.waitKeys()
    check_for_exit()

    # TODO EEG Timestamp: final recall phase -- start
    bsusb.send("FINAL_RECALL_START", code=bsusb.SOR)

    # Fetch all word pairs
    testPairs = wordPairs[wordPairs["type"].isin(["think", "nothink", "baseline", "bystander"])]
    finalCues = testPairs.sample(frac=1, random_state=seed).reset_index(drop=True)

    currentTrial = startTrial  
    # look up table so it can label bystander subtype
    flash_map = (
        participantData
        .query("Phase == 'TNT' and Type == 'bystanderFlash'")
        .drop_duplicates(subset=["Cue"])         
        .set_index("Cue")["Context"]             
        .to_dict()
    )

    try:
        # Assemble list of final cues
        for idx in range(startTrial, len(finalCues)):
            row = finalCues.iloc[idx]
            word = row["cue"]
            correctTarget = row["target"]
            cueType = row["type"]

            if cueType == "bystander":
                if word in control_cues:
                    contextVal = "control"
                else:
                    contextVal = flash_map.get(word, "")   # think/nothink/baseline
            else:
                contextVal = ""

            # Sets the trial type codes for the EEG marks
            if cueType == "think":
                code  = bsusb.CTL + 1
                label = f"FINAL_RECALL_THINK_{idx}"

            elif cueType == "nothink":
                code  = bsusb.CTL + 2
                label = f"FINAL_RECALL_NOTHINK_{idx}"

            elif cueType == "baseline":
                code  = bsusb.CTL + 3
                label = f"FINAL_RECALL_BASELINE_{idx}"

            elif cueType == "bystander":       
                code  = bsusb.CTL + 4           
                label = f"FINAL_RECALL_BYSTANDER_{idx}"

            elif cueType == "filler":           
                code  = bsusb.CTL + 5
                label = f"FINAL_RECALL_FILLER_{idx}"

            else:                               
                code  = bsusb.CTL + 6
                label = f"FINAL_RECALL_FAKE_{idx}"

            accuracyRating, confidenceRating, identification, gist_raw, rt = run_form(win, word)
            gist_prop = gist_raw / 5.0 # gist 1-5 so 5 = 1.0, 4 = 0.8...

            # Record data
            trialData = {
                "Phase":        "FinalRecall",
                "Trial":        currentTrial + 1,
                "Cue":          word,
                "Target":       correctTarget,
                "Type":         cueType,
                "Context":      contextVal,

                "Accuracy":     accuracyRating,
                "Confidence":   confidenceRating,
                "RT":           rt,

                "Identification": identification,  
                "Gist":           gist_prop         
            }
                
            participantData.loc[len(participantData)] = trialData

            currentTrial += 1  

            saveData(participantData, participantInfo)
            saveState(participantInfo, {"currentPhase": "FinalRecall", "currentTrial": currentTrial})

            # ITI
            win.flip()

            #######################################################
            if testing == False:
                core.wait(0.5) # FOR ACTUAL EXPERIMENT
            else:
                core.wait(0.1)  # FOR TESTING
            #######################################################
            check_for_exit()

    except KeyboardInterrupt:
        # Save state in case of keyboard interrupt
        saveData(participantData, participantInfo)
        saveState(participantInfo, {
            "currentPhase": "FinalRecall",
            "currentTrial": currentTrial
        })
        raise 

    except Exception as e:
        # Save state in case of other exceptions
        saveData(participantData, participantInfo)
        saveState(participantInfo, {
            "currentPhase": "FinalRecall",
            "currentTrial": currentTrial
        })
        raise e

    # TODO EEG Timestamp: final recall phase -- end
    bsusb.send("FINAL_RECALL_END", code=bsusb.EOR)

    # Debrief & thank the participant
    debriefText = visual.TextStim(win, text="Thanks for participating.\n\nPress any key to exit.", color="white")
    debriefText.draw()
    win.flip()
    event.waitKeys()
    win.close()
    return participantData, currentTrial
