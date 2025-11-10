import os
from psychopy import *
from bsusb import bsusb
from utils.timing import check_for_exit
from utils.config import testing
import random

################### LEARNING PHASE #########################
def learningPhase(win, wordPairs, participantData, participantInfo):
    # Instructions!
    instructions = visual.TextStim(win, text="Learning Phase:\nMemorize the pairs of words and images.\n\nPress any key to begin.", color="white")
    instructions.draw()
    win.flip()
    event.waitKeys()

    # TODO EEG Timestamp: learning phase pair presentation -- start
    bsusb.send("LEARNING_START", code=bsusb.SOR)

    # Present pairs to participant, 4-second delay between each
    for idx, row in wordPairs.iterrows():
        word = row["cue"]
        imageFile = row["target"]
        trialType = row["type"]

        image = visual.ImageStim(win, image=os.path.join("images", imageFile), pos=(0, -100))
        text = visual.TextStim(win, text=word, pos=(0, 200), color="white")

        text.draw()
        image.draw()
        win.flip()
        #######################################################
        if testing == False:
            core.wait(3) # FOR ACTUAL EXPERIMENT
        else:
            core.wait(0.01) # FOR TESTING
        #######################################################
        check_for_exit()

    ################### TEST FEEDBACK LOOP ################### 
    attempts = 0
    while attempts < 5:
        success = 0
        attempts += 1
        # Shuffle pairs
        quizPairs = wordPairs.sample(frac=1).reset_index(drop=True)

        # Start the actual quiz
        for idx, row in quizPairs.iterrows():
            word = row["cue"]
            correctImage = row["target"]
            trialType = row["type"]

            # Summon 3 random targets in random order that are not the actual target we're looking for
            # So we can display a cue and 4 targets then ask the participant to identify the correct target
            incorrectImages = wordPairs[wordPairs["target"] != correctImage].sample(3)["target"].tolist()
            options = incorrectImages + [correctImage]
            random.seed(idx)
            random.shuffle(options)

            # Display the cue & options
            cueText = visual.TextStim(win, text=f"Select the image associated with '{word}':", pos=(0, 450), color="white", wrapWidth=800)
            images = [visual.ImageStim(win, image=os.path.join("images", img), pos=pos) for img, pos in zip(options, [(-400, 200), (400, 200), (-400, -200), (400, -200)])]
            optionKeys = ["1", "2", "3", "4"]
            optionTexts = [visual.TextStim(win, text=f"{key}", pos=(pos[0], pos[1]-100), color="white") for key, pos in zip(optionKeys, [(-400, 200), (400, 200), (-400, -200), (400, -200)])]

            cueText.draw()
            for img, txt in zip(images, optionTexts):
                img.draw()
                txt.draw()
            win.flip()

            # Collect response and reaction time of user response (1,2,3,4)
            timer = core.Clock()
            response = event.waitKeys(keyList=optionKeys)
            rt = timer.getTime()
            if response:
                chosen_idx = optionKeys.index(response[0])
                chosenImage = options[chosen_idx]

                # Provides feedback to the user regarding the accuracy of their selected choice
                if chosenImage == correctImage:
                    feedback = visual.TextStim(win, text="Correct", color="green")
                    success += 1
                    accuracy = 1
                else:
                    feedback = visual.TextStim(win, text="Wrong", color="red")
                    accuracy = 0
                feedback.draw()
                win.flip()
                #######################################################
                if testing == False:
                    core.wait(0.5)  # FOR ACTUAL EXPERIMENT
                else:
                    core.wait(0.01) # FOR TESTING
                #######################################################
                check_for_exit()

                # Record data
                trialData = {"Phase": "Learning", "Trial": idx + 1, "Cue": word, "Target": correctImage, "Type": trialType, "Response": chosenImage, "Accuracy": accuracy, "RT": rt}
                participantData.loc[len(participantData)] = trialData

        # Check if accuracy > criterion
        accuracyRate = (success / len(quizPairs))
        #######################################################
        if testing == False:
            criterion = 0.65
        else:
            criterion = 0.01
        #######################################################
        # If accuracy is above the criterion (0.65), they move on to the next phase
        if accuracyRate >= criterion:
            completionText = visual.TextStim(win, text="You have successfully completed the learning phase.", color="green")
            completionText.draw()
            # TODO EEG Timestamp: learning phase pair presentation -- end
            bsusb.send("LEARNING_END", code=bsusb.EOR)
            win.flip()
            core.wait(2)
            break
        else:
            retryText = visual.TextStim(win, text="Didn't meet accuracy criterion. Try again.", color="red")
            retryText.draw()
            win.flip()
            core.wait(2)

    return participantData
