#!/usr/bin/python
from time import time, localtime,asctime
import sys
import winsound
import threading

#FUNCTIONS

def alarm_sound():
    global curr_active
    while curr_active:
        winsound.Beep(freq, duration)

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
        result = input("What Interval Do You Want To Use?")
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
                        print("Incorrect Format: "+data)
            if (hours or data or secs):
                valid = True
            
        # else:
        #     hours = float(data[0])
        #     mins = float(data[2])
        #     secs = float(data[4])
        #     valid = True
        print(data)
        print(hours,mins,secs)

#Timer Loop
active = True
while active:
    print("Timer Started, press ctrl and c at the same time to exit")
    alarm_time = time() + 3600*hours + 60*mins + secs
    while time() < alarm_time:
        #IMPLEMENT A STOP TIMER HERE
        pass
    print("ALARM!!! It has been "+result)
    
    curr_active = True
    # now threading1 runs regardless of user input
    threading1 = threading.Thread(target=alarm_sound)
    threading1.start()
    while curr_active:
        curr_result = input()
        if(curr_result == "exit"):
            curr_active = False
            sys.exit()
        elif(curr_result == "stop"):
            curr_active = False
    threading1.join()
    print("running again")

#implement an exit from active
        
# curr_time = time()
# curr_localtime = time.localtime(curr_time)
# print(curr_localtime)