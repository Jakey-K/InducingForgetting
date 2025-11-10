from psychopy import event

# HELPER DECLARATIONS 
# Failsafe so don't have to wait 10 yrs if something isn't working
def check_for_exit():
    if event.getKeys(keyList=["escape"]):
        raise KeyboardInterrupt