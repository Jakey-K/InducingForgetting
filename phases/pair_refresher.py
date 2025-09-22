import os
from psychopy import *
from bsusb import bsusb
from utils.timing import check_for_exit
from utils.config import testing

################### PAIR REFRESHER PHASE ################### 
def pairRefresherPhase(win, wordPairs):
    # Ask participant if pair refresher phase is needed
    instructions = visual.TextStim(win, text="""
Examiner Instructions:

Do you want to proceed with the Pair Refresher Phase?

Press Y for Yes or N for No.""", color="white")
    instructions.draw()
    win.flip()
    keys = event.waitKeys(keyList=["y", "n"])

    if "n" in keys:
        return
    elif "y" in keys:
        # Commence pair refresher phase
        participantInstructions = visual.TextStim(win, text="""
PAIR REFRESHER PHASE

We will now refresh your memory of some word-image pairs.

Press any key to begin.""", color="white")
        participantInstructions.draw()
        win.flip()
        event.waitKeys()

        # TODO EEG Timestamp: pair refresher phase -- start
        bsusb.send("PAIR_REFRESHER_START", code=bsusb.SOR)

        # Present the filler word pairs
        baselinePairs = wordPairs[wordPairs["type"] == "filler"]
        for idx, row in baselinePairs.iterrows():
            word = row["cue"]
            imageFile = row["target"]
            text = visual.TextStim(win, text=word, pos=(0, 250), color="white")
            image = visual.ImageStim(win, image=os.path.join("images", imageFile), pos=(0, -100))
            text.draw()
            image.draw()
            win.flip()

            #######################################################
            if testing == False:
                core.wait(2) # FOR ACTUAL EXPERIMENT
            else:
                core.wait(0.1)  # FOR TESTING
            #######################################################
            check_for_exit()

        # TODO EEG Timestamp: pair refresher phase -- end
        bsusb.send("PAIR_REFRESHER_END", code=bsusb.EOR)
