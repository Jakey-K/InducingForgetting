import os, random
import numpy as np
from psychopy import *

from utils.config import testing
from utils.stimuli import loadWordPairs
from utils.io import getParticipantInfo, initializeDataStorage, saveData, saveState, loadState

from phases.learning import learningPhase
from phases.tnt_practice import tntPracticePhase
from phases.tnt import tntPhase
from phases.pair_refresher import pairRefresherPhase
from phases.final_recall import finalRecallPhase

################### MAIN FUNCTION ##########################
def runExperiment():
    ### bsusb.init() 
    wordPairs = loadWordPairs()
    participantInfo = getParticipantInfo()

    # Set random seed using participant ID
    seed = int(participantInfo['ID'])
    random.seed(seed)
    np.random.seed(seed)

    all_bs = wordPairs[wordPairs["type"] == "bystander"]

    control_set = (
        all_bs.sample(n=10, random_state=seed).assign(context="control")
    )

    leftover    = all_bs[~all_bs.index.isin(control_set.index)].sample(frac=1, random_state=seed) # shuffle

    think_set   = leftover.iloc[:10].assign(context="think")
    nothink_set = leftover.iloc[10:20].assign(context="nothink")

    bystanderPoolMaster = pd.concat([think_set, nothink_set]).reset_index(drop=True)
    control_cues = control_set.cue.tolist()

    participantData = initializeDataStorage()
    currentPhase = None
    currentTrial = 0
    tntBlockIndex = 0

    # Check for existing data and state in case participant crashed and is restarting the program
    dataFilename = f"data/participant_{participantInfo['ID']}_data.csv"
    stateFilename = f"data/participant_{participantInfo['ID']}_state.json"

    if os.path.exists(dataFilename) and os.path.exists(stateFilename):
        # Ask whether to resume 
        dlg = gui.Dlg(title="Resume Experiment")
        dlg.addText("An existing session was found for this participant.")
        dlg.addText("Do you want to resume from where you left off?")
        dlg.addField("Resume?", choices=["Yes", "No"])
        ok_data = dlg.show()

        # Check if the dialog was cancelled or closed
        if not dlg.OK or ok_data is None:
            core.quit()

        # Load previous data if resuming
        resume = ok_data.get('Resume?') == "Yes"
        if resume:
            participantData = pd.read_csv(dataFilename)
            state = loadState(participantInfo)
            currentPhase = state.get("currentPhase")
            currentTrial = state.get("currentTrial", 0)
            tntBlockIndex = state.get("tntBlockIndex", 0)

        else:
            participantData = initializeDataStorage()
            currentPhase = None
            currentTrial = 0
            tntBlockIndex = 0

    else:
        participantData = initializeDataStorage()
        currentPhase = None
        currentTrial = 0
        tntBlockIndex = 0

    win = visual.Window(size=(1920, 1080), fullscr=True, color="black", units="pix")

    try:
        if currentPhase in [None, "Learning"]:
            participantData = learningPhase(win, wordPairs, participantData, participantInfo)
            saveData(participantData, participantInfo)
            saveState(participantInfo, {"currentPhase": "TNTPractice", "currentTrial": 0})
            currentPhase = "TNTPractice"

        if currentPhase == "TNTPractice":
            tntPracticePhase(win, wordPairs)
            saveState(participantInfo, {"currentPhase": "TNT", "currentTrial": 0, "tntBlockIndex": tntBlockIndex})
            currentPhase = "TNT"

        if currentPhase == "TNT":
            participantData, tntBlockIndex = tntPhase(win, wordPairs, participantData, participantInfo, bystanderPoolMaster, control_cues, tntBlockIndex)
            saveData(participantData, participantInfo)
            saveState(participantInfo, {"currentPhase": "PairRefresher", "currentTrial": 0})
            currentPhase = "PairRefresher"

        if currentPhase == "PairRefresher":
            pairRefresherPhase(win, wordPairs)
            currentTrial = 0  # Reset currentTrial for Final Recall Phase
            saveState(participantInfo, {"currentPhase": "FinalRecall", "currentTrial": currentTrial})
            currentPhase = "FinalRecall"

        # Independent probe testing fake cues (word stems)
        ## REDUNDANT -- NOT USING FAKE CUES ANYMORE ##
        # replacements = { ... }
        # wordPairs = fakeCueSetup(wordPairs, replacements)

        if currentPhase == "FinalRecall":
            participantData, currentTrial = finalRecallPhase(win, wordPairs, participantInfo, participantData, control_cues, startTrial=currentTrial)
            saveData(participantData, participantInfo)
            saveState(participantInfo, {"currentPhase": "Completed", "currentTrial": 0})
            currentPhase = "Completed"

    except KeyboardInterrupt:
        print("Experiment aborted by user.")
        saveData(participantData, participantInfo)
        ### bsusb.close()
        win.close()

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        saveData(participantData, participantInfo)
        ### bsusb.close()
        win.close()
        raise

    finally:
        ### bsusb.close()
        core.quit()

if __name__ == '__main__':  
    import pandas as pd
    runExperiment()
