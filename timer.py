#!/usr/bin/python
from time import time, localtime,asctime, sleep
import sys
import winsound
import threading

#FUNCTIONS

def alarmSound():
    #Beep Defs
    duration = 1000  # milliseconds
    freq = 520  # Hz
    #2500 really piercing sound
    global currActive
    while currActive:
        winsound.PlaySound('beepSound.wav', winsound.SND_FILENAME)        
        # winsound.Beep(freq, duration)

#this timer loop might be delayed
def inputThread():
    global finished
    global currResult
    global currActive
    # print(currActive)
    while currActive:
        currResult = input()
        sleep(1)
    currActive = False
    finished = True
    print("finished input thread: "+currResult)

def inputOptions():
    global currActive
    while currActive:
        if(currResult == "exit"):
            currActive = False
            sys.exit()
        elif(currResult == "stop"):
            currActive = False
def inputWaitingOptions():
    global currActive
    global alarmTime
    global finished
    global restart
    global currResult
    while time() < alarmTime:
        if(currResult == "exit"):
            currActive = False
            sys.exit()
        elif(currResult == "restart"):
            currActive = False
            restart = True
            #wait for thread to finish
            while (not finished):
                pass
            break

def intervalLoop():
    valid = False
    hours = 0
    mins = 0
    secs = 0
    while not valid:
        try:
            result = input("What Interval Do You Want To Use? ")
            #print(result)
        except:
            print("Sorry I Didn't Understand Your Input")

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

def timerLoop():
    active = True
    currActive = True
    while active:
        print("Timer Started, type exit or press ctrl and c at the same time to exit")
        finished = False
        restart = False
        currResult = ""
        currActive = True
        #input thread for exiting/stopping timer
        threading1 = threading.Thread(target=inputThread)
        threading1.daemon = True
        threading1.start()
        #Waiting Loop
        alarmTime = time() + 3600*hours + 60*mins + secs
        inputWaitingOptions()
        if (restart):
            continue
        print("ALARM!!! It has been "+result)
        currActive = True
        #start timer
        threading2 = threading.Thread(target=alarmSound)
        threading2.start()
        #if we havent restarted or exited input will still be valid here
        inputOptions()
        threading2.join()
        print("running again")



def timerApp():
    #Local Time
    localtimestring = asctime(localtime(time()))
    currHr = localtime(time()).tm_hour
    currMin = localtime(time()).tm_min
    currSec = localtime(time()).tm_sec
    print("Current Time Is:")
    print(localtimestring)
    #GET INTERVAL FROM USER
    intervalLoop()
    #Timer Loop
    timerLoop()

timerApp()