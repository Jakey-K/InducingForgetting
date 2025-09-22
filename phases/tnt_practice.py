import time, random
from psychopy import *
from bsusb import bsusb
from utils.timing import check_for_exit
from utils.config import testing

################### TNT PRACTICE PHASE #####################
def tntPracticePhase(win, wordPairs):
    # Display instructions to participant
    instructions = visual.TextStim(win, text="""
    THINK/NO-THINK PRACTICE PHASE

    For words in GREEN,
    think about the associated target image

    For words in RED,
    actively avoid thinking about the associated target image

    Press a key to begin!""", color="white")
    instructions.draw()
    win.flip()
    event.waitKeys()

    # TODO EEG Timestamp: tnt practice phase -- start
    bsusb.send("TNT_PRACTICE_START", code=bsusb.SOR)

    # Selects, at random, filler pairs to be think or no-think and assigns color accordingly
    fillerPairs = wordPairs[wordPairs["type"] == "filler"].sample(frac=1).reset_index(drop=True)
    for idx, row in fillerPairs.iterrows():
        word = row["cue"]
        random.seed(time.time())
        trial = random.choice(["think", "nothink"])
        color = "green" if trial == "think" else "red"

        # Shows the user the selected cue
        cue = visual.TextStim(win, text=word, color=color)
        cue.draw()

        # Marks EEG each trial with trial code
        label = f"Filler_{idx}"
        fillerCode = bsusb.CTL+4
        win.callOnFlip(bsusb.send, label, code=fillerCode)
        win.flip()

        #######################################################
        if testing == False:
            core.wait(4) # FOR ACTUAL EXPERIMENT
        else:
            core.wait(0.2)  # FOR TESTING
        #######################################################

        check_for_exit()
        # INSERT DIAGNOSTIC QUESTIONNAIRE
        # The diagnostic questionnaire is administered in a verbal, interactive manner

    # TODO EEG Timestamp: tnt practice phase -- end
    bsusb.send("TNT_PRACTICE_END", code=bsusb.EOR)
