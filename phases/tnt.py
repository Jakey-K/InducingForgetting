import os, time, random
import numpy as np
from psychopy import *
from bsusb import bsusb
from utils.timing import check_for_exit
from utils.config import testing
from utils.io import saveData, saveState

# function to output the subliminal flashes of the bystander cues
def flash_bystander(win, imageFile, maskDuration=0.5, imgDuration=0.016):
    maskPath = os.path.join("masks", f"mask_{os.path.basename(imageFile)}")
    if not os.path.exists(maskPath):
        raise FileNotFoundError(f"Missing mask file: {maskPath}")

    mask_stim  = visual.ImageStim(win, image=maskPath, pos=(0, 0))
    image_stim = visual.ImageStim(win, image=imageFile, pos=(0, 0))

    ######################################################
    if testing == False:
        mDur = maskDuration # FOR ACTUAL EXPERIMENT
    else:
        mDur = 0.01         # FOR TESTING
    #######################################################
    # Choose durations based on testing mode
    mDur = 0.01 if testing else maskDuration

    # forward maskd
    mask_stim.draw()
    win.flip()
    core.wait(mDur)

    # brief image flash (keep @ 16 ms even in testing so timing matches)
    image_stim.draw()
    win.flip()
    core.wait(imgDuration)

    # backward mask
    mask_stim.draw()
    win.flip()
    core.wait(mDur)

################### TNT PHASE ##############################
def tntPhase(win, wordPairs, participantData, participantInfo, bystanderPoolMaster, control_cues, tntBlockIndex=0):
    # set seed for consistent shuffling
    seed = int(participantInfo['ID'])
    np.random.seed(seed)
    random.seed(seed)

    # display instructions to participant
    instructions = visual.TextStim(win, text="""
    THINK/NO-THINK PHASE

    For words in GREEN,
    think about the associated target image

    For words in RED,
    actively avoid thinking about the associated target image

    Press a key to begin!""", color="white")
    instructions.draw()
    win.flip()
    event.waitKeys()

    # TODO EEG Timestamp: tnt phase -- start
    bsusb.send("TNT_START", code=bsusb.SOR)  # EEG marker

    # fetch all think and nothink apirs
    tntPairs = wordPairs[wordPairs["type"].isin([   "think", "nothink"])].copy()
    tntPairs = tntPairs.loc[tntPairs.index.repeat(3)].reset_index(drop=True)
    tntPairs = tntPairs.sample(frac=1, random_state=seed).reset_index(drop=True)

    # bystander pool & iterator
    bystander_iter = iter(
        bystanderPoolMaster.sample(frac=1, random_state=seed).itertuples()
    )

    totalTrials    = len(tntPairs)
    trialsPerBlock = totalTrials // 4 # this changes amount of blocks for participant to rest
    c=0

    # TNT trials
    try:
        for idx in range(tntBlockIndex * trialsPerBlock, totalTrials):
            row        = tntPairs.iloc[idx]
            word       = row.cue
            imageFile  = row.target
            trialType  = row.type
            colour     = "green" if trialType == "think" else "red"

            try:
                b_row = next(bystander_iter)
            except StopIteration:
                bystanderPool  = bystanderPoolMaster.sample(frac=1, random_state=int(time.time()))
                bystander_iter = iter(bystanderPool.itertuples())
                b_row          = next(bystander_iter)

            # log the flash
            participantData.loc[len(participantData)] = {
                "Phase":   "TNT", 
                "Trial":   idx + 1, 
                "Cue":     b_row.cue,
                "Target":  b_row.target, 
                "Type":    "bystanderFlash",
                "Context": b_row.context
            }

            # TODO EEG Timestamp -- TNT Trial
            ttl_label = f"TNT_{trialType.upper()}_{idx}"
            code = bsusb.CTL + (1 if trialType == "think" else 2)

            # fixation cross to help participant focus
            fixation = visual.TextStim(win, text="+", color="white")
            fixation.draw()
            win.flip()

            #######################################################
            if testing == False:
                core.wait(0.6)     # FOR ACTUAL EXPERIMENT
            else:
                core.wait(0.01)  # FOR TESTING
            #######################################################
            check_for_exit()

            # shows "Think" or "No-think"
            cueStim = visual.TextStim(win, text=word, color=colour)
            cueStim.draw()
            win.callOnFlip(bsusb.send, ttl_label, code=code)
            win.flip()  

            gap = random.randint(1,3)
            #######################################################
            if testing == False:
                core.wait(gap)     # FOR ACTUAL EXPERIMENT
            else:
                core.wait(0.01)  # FOR TESTING
            #######################################################
            check_for_exit()

            # shows subliminal bystander cue 
            flash_bystander(win, os.path.join("images", b_row.target))
            win.flip()

            cueStim.draw()
            win.flip()

            #######################################################
            if testing == False:
                core.wait(4-gap)     # FOR ACTUAL EXPERIMENT
            else:
                core.wait(0.01)  # FOR TESTING
            #######################################################
            check_for_exit()

            # log cue trial
            participantData.loc[len(participantData)] = {
                "Phase": "TNT", 
                "Trial": idx + 1, 
                "Cue": word,
                "Target": imageFile, 
                "Type": trialType
            }

            # separates tnt phase into blocks to help participant focus
            if (idx + 1) % trialsPerBlock == 0 and (idx + 1) < totalTrials:
                
                restMsg = visual.TextStim(win, text="Rest 30 s – press key to continue.", color="white")
                restMsg.draw() 
                win.flip() 
                
                #######################################################
                if testing == False:
                    core.wait(30)     # FOR ACTUAL EXPERIMENT
                else:
                    core.wait(0.5)  # FOR TESTING
                #######################################################
                event.waitKeys()

        bsusb.send("TNT_END", code=bsusb.EOR) 

    except Exception as e:
        # save state in case of crash
        saveData(participantData, participantInfo)
        saveState(participantInfo, {
            "currentPhase": "TNT",
            "currentTrial": idx + 1,
            "tntBlockIndex": tntBlockIndex})
        raise e

    return participantData, tntBlockIndex
