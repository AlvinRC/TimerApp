#!/usr/bin/python
from time import time, localtime,asctime, sleep
import sys
import winsound
import threading

def alarmSound():
    #Beep Defs
    duration = 1000  # milliseconds
    freq = 520  # Hz
    #2500 really piercing sound
    global currActive
    while currActive:
        winsound.PlaySound('beep_sound.wav', winsound.SND_FILENAME)        
        # winsound.Beep(freq, duration)
def startTimer():
    pass