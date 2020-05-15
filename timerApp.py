#!/usr/bin/python
from time import time, localtime,asctime, sleep
import sys
import winsound
import threading

hours=0;mins=0;secs=0
currActive = True

# def alarmSound():
#     #Beep Defs
#     duration = 1000  # milliseconds
#     freq = 520  # Hz
#     #2500 really piercing sound
#     global currActive
#     currActive = True
#     while currActive:
#         print(currActive)

#         winsound.PlaySound('beep_sound.wav', winsound.SND_FILENAME)        
#         # winsound.Beep(freq, duration)

def setActive():
    global currActive
    currActive = False
def intervalLoop(resultObj):
    valid = False
    breakLoop = False
    global hours
    global mins
    global secs
    result = resultObj.get()
    if result == "help":
        print("Format is:1 hr 1 min 1 sec")
    elif result == "exit":
        sys.exit()
    else:
        data = result.split(' ')
        if(len(data) == 0 and len(data) > 6):
            print("Incorrect Format")
        #add more cases for 1 hr, x hr x min, x hr x min x sec, x min, x min x sec, x sec
        # elif(len(data) == 2):
        else:
            for x in range(len(data)):
                #check for hr, min, sec
                if (x > 0 and x % 2 == 1):
                    if (data[x] in ("h","hr","hrs","hour","hours")):
                        hours = float(data[x-1])
                    elif (data[x] in ("m","min","mins","minute","minutes")):
                        mins = float(data[x-1])
                    elif (data[x] in ("s","sec","secs","second","seconds")):
                        secs = float(data[x-1])
                    else:
                        print("Incorrect Format: "+''.join(data))
            if (hours or mins or secs):
                print(hours,mins,secs)
                valid = True
        print(data)
        print(hours,mins,secs)
    if(valid):
        print("valid time inputted")
    else:
        print("invalid time inputted")
    return valid

# def timerLoop():
#     active = True
#     currActive = True
#     finished = False
#     restart = False
#     currActive = True
#     #Waiting Loop
#     alarmTime = time() + 3600*hours + 60*mins + secs
#     while time() < alarmTime:
#         pass
#     print("ALARM!!! It has been %f hrs %f mins %f secs" %(hours,mins,secs))
#     currActive = True
#     #start timer
#     threading2 = threading.Thread(target=alarmSound)
#     threading2.start()
#     threading2.daemon = True

def startTimer(timerInput):
    hours = 0
    mins = 0
    secs = 0
    print("timer started")
    timerInputString = timerInput.get()
    valid = intervalLoop(timerInput)
    print(timerInput.get())
    return valid