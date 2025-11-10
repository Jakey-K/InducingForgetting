import os
import json
import pandas as pd
from psychopy import gui, core

# preps participant data
def getParticipantInfo():
    participantInfo = {
        "ID": "",
    }
    dlg = gui.DlgFromDict(participantInfo, title="Welcome")
    if not dlg.OK:
        core.quit()
    return participantInfo

# Initializes the spreadsheet columns
def initializeDataStorage():
    dataColumns = ["Phase", "Trial", "Cue", "Target", "Type", "Response", "Accuracy", "Confidence", "RT", "Context", "Identification", "Gist"]
    participantData = pd.DataFrame(columns=dataColumns)
    return participantData

# Saves the state that the participant is in 
def saveState(participantInfo, state):
    if not os.path.exists("data"):
        os.makedirs("data")
    stateFilename = f"data/participant_{participantInfo['ID']}_state.json"
    with open(stateFilename, 'w') as f:
        json.dump(state, f)

# Opens & reads the participants' data and returns the phase they were in
def loadState(participantInfo):
    stateFilename = f"data/participant_{participantInfo['ID']}_state.json"
    if os.path.exists(stateFilename):
        with open(stateFilename, 'r') as f:
            state = json.load(f)
        return state
    else:
        return None

# Saves participant data to file
def saveData(participantData, participantInfo):
    if not os.path.exists("data"):
        os.makedirs("data")
    filename = f"data/participant_{participantInfo['ID']}_data.csv"
    participantData.to_csv(filename, index=False)
    print("Data saved to", filename)
