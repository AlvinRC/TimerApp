#!/usr/bin/python
from time import time, localtime,asctime, sleep
import sys
import winsound
import threading

#FUNCTIONS

def alarm_sound():
    global curr_active
    while curr_active:
        winsound.PlaySound('beep_sound.wav', winsound.SND_FILENAME)        
        # winsound.Beep(freq, duration)

#this timer loop might be delayed
def input_thread():
    global finished
    global curr_result
    global curr_active
    # print(curr_active)
    while curr_active:
        curr_result = input()
        sleep(1)
    curr_active = False
    finished = True
    print("finished input thread: "+curr_result)

def input_options():
    global curr_active
    while curr_active:
        if(curr_result == "exit"):
            curr_active = False
            sys.exit()
        elif(curr_result == "stop"):
            curr_active = False
def input_waiting_options():
    global curr_active
    global alarm_time
    global finished
    global restart
    global curr_result
    while time() < alarm_time:
        if(curr_result == "exit"):
            curr_active = False
            sys.exit()
        elif(curr_result == "restart"):
            curr_active = False
            restart = True
            #wait for thread to finish
            while (not finished):
                pass
            break

#Beep Defs
duration = 1000  # milliseconds
freq = 520  # Hz
#2500 really piercing sound

#Local Time
localtimestring = asctime(localtime(time()))
curr_hr = localtime(time()).tm_hour
curr_min = localtime(time()).tm_min
curr_sec = localtime(time()).tm_sec
print("Current Time Is:")
print(localtimestring)

#Interval Loop
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

#Timer Loop
active = True
curr_active = True
while active:
    print("Timer Started, type exit or press ctrl and c at the same time to exit")
    finished = False
    restart = False
    curr_result = ""
    curr_active = True
    #input thread for exiting/stopping timer
    threading1 = threading.Thread(target=input_thread)
    threading1.daemon = True
    threading1.start()
    #Waiting Loop
    alarm_time = time() + 3600*hours + 60*mins + secs
    input_waiting_options()
    if (restart):
        continue
    print("ALARM!!! It has been "+result)
    curr_active = True
    #start timer
    threading2 = threading.Thread(target=alarm_sound)
    threading2.start()
    #if we havent restarted or exited input will still be valid here
    input_options()
    threading2.join()
    print("running again")
