import os
import sys
import time
from icecream import ic

def restart():
    ic("Reiniciando bot...")
    ic(sys.executable)
    ic(['python'] + ['L1_BoT.py'])
    os.execv(sys.executable, ['python'] + ['L1_BoT.py'])

if __name__ == "__main__":
    ic()
    restart()
