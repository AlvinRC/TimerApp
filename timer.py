#!/usr/bin/python
from time import time, localtime,asctime
localtimestring = asctime(localtime(time()))
curr_hr = localtime(time()).tm_hour
curr_min = localtime(time()).tm_min
curr_sec = localtime(time()).tm_sec
print("Current Time Is:")
print(localtimestring)
valid = False
hours = 0
mins = 0
secs = 0
while not valid:
    try:
        result = input("What Interval Do You Want To Use?")
        print(result)
    except:
        print("Sorry I Didn't Understand Your Input")

    if result == "help":
        print("Format is: 1 hr 1 min 1 sec")
    else:
        data = result.split(' ')
        if(len(data) != 6):
            print("Incorrect Format")
        else:
            hours = float(data[0])
            mins = float(data[2])
            secs = float(data[4])
            valid = True

active = True
while active:
    alarm_time = time() + 3600*hours + 60*mins + secs
    while time() < alarm_time:
        pass
    print("ALARM!!! It has been "+result)
    print("running again")

#implement an exit from active
        
# curr_time = time()
# curr_localtime = time.localtime(curr_time)
# print(curr_localtime)