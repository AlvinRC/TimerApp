#!/usr/bin/python
from time import time, localtime,asctime, sleep
import sys
import winsound
import threading

hours=0;mins=0;secs=0
currActive = True


def validateTimer(resultObj):
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

def startTimer(timerInput):
    hours = 0
    mins = 0
    secs = 0
    print("timer started")
    timerInputString = timerInput.get()
    valid = validateTimer(timerInput)
    print(timerInput.get())
    return valid

def validateDaily(dailyTimerInput):
    tmpdh = int(dailyTimerInput.get().split(":")[0])
    tmpdm = int(dailyTimerInput.get().split(":")[1])
    tmpds = int(dailyTimerInput.get().split(":")[2])
    if(tmpdh not in range(0,24)):
        print("INVALID HOUR")
        return False
    if(tmpdm not in range(0,59)):
        print("INVALID MINS")
        return False
    if(tmpds not in range(0,59)):
        print("INVALID SECS ")
        return False
    return True