#GUI
import tkinter as tk
#file dialog help us pick apps, text helps us display text
from tkinter import filedialog, Text
#os allows us to run applications
import os
import threading
#external file import
import timerApp
import winsound

#--- ROOT ---
#create root of app
root = tk.Tk()

#--- Default vars --- 
apps = []
run = True; s=0; m=0; h=0
textId=-1
currActive = True

#--- Default sound file ---
soundFile = 'shortBeepSound.wav'

if os.path.isfile('save.txt'):
    with open("save.txt",'r') as f:
        tempApps = f.read()
        tempApps = tempApps.split(',')
        #for every element in tempapps after we strip empty
        apps = [x for x in tempApps if x.strip()]


def alarmSound():
    #Beep Defs
    duration = 1000  # milliseconds
    freq = 520  # Hz
    #2500 really piercing sound
    global currActive
    global soundFile
    currActive = True
    while currActive:
        print(currActive)
        winsound.PlaySound(soundFile, winsound.SND_FILENAME)        
        # winsound.Beep(freq, duration)
    currActive = False

def setActive():
    global currActive
    currActive = False

def setSoundFile(soundInput):
    global soundFile
    soundFile = soundInput.get()

def addApp():
    global apps
    #remove everything in frame first
    for widget in frame1.winfo_children():
        widget.destroy()

    filename= filedialog.askopenfilename(initialdir="/",title="Select File",
    filetypes=(("exectuables","*.exe"),("all files", "*.*")))
    apps.append(filename)
    print(filename)
    #remove dupe
    apps = list(dict.fromkeys(apps))

    for app in apps:
        #create and attach label to frame
        label = tk.Label(frame1,text=app, bg="gray")
        label.pack()

def runApps():
    for app in apps:
        os.startfile(app)

def runTimer(timerInput):
    global textId
    #maybe store time from here and pass in?
    #need to run threads for this (THEY DONT WORK?)
    # threading2 = threading.Thread(target=timerApp.startTimer(timerInput))
    # threading2.start()

    valid = timerApp.startTimer(timerInput)
    print(valid)
    if(valid):
        hours = 0
        mins = 0
        secs = 0
        data = timerInput.get().split(' ')
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
        timerInputList = [hours,mins,secs]
        #runs indefinitely
        displayTimer(timerInputList)
    else:
        if (textId != -1):
            canvas.delete(textId)
        # Add new text
        textId = canvas.create_text(
            [10, 20], anchor='w', text="Timer: Invalid Format", font=("Consolas", 20), fill="white"
            )
    #doesnt reach this (TODO)
    # threading2.join()
def displayTimer(timerInputList):
    global run, s, m, h,textId
    
    if (textId != -1):
        canvas.delete(textId)

    
    # Add new text
    textId = canvas.create_text(
        [10, 20], anchor='w', text="Timer: %s:%s:%s" % (h, m, s), font=("Consolas", 20), fill="white"
        )

    s+=1
    if s == 59:
        m+=1; s=-1
    elif m == 59:
        h+=1; m=-1
    
    #check that new time isnt > time limit
    
    if (h <= timerInputList[0] and m <= timerInputList[1] and s <= timerInputList[2]):
        # After 1 second, call Run again (start an infinite recursive loop)
        root.after(1000, displayTimer, timerInputList)
    else:
        print(h,m,s,timerInputList)
        #display timer finished
        currActive = True
        #play sound
        alarmThread = threading.Thread(target=alarmSound)
        alarmThread.start()
        #reset timer vars now
        h = 0
        m = 0
        s = 0
        # alarmThread.join()

#--- CANVAS ---
#create and attach canvas to root, set height,width and background colour
canvas = tk.Canvas(root,height=700,width=700,bg="#263D42")
#Load canvas
canvas.pack()

#--- FRAME ---
#left
#create and attach frame to root, set bg to white
frame1 = tk.Frame(root,bg="white")
#make frame take up 0.8 of roots heigh and width and be centered with a 10% border
frame1.place(relwidth=0.49,relheight=0.8, relx=0.0, rely=0.05)
#right
frame2 = tk.Frame(root,bg="white")
frame2.place(relwidth=0.49,relheight=0.8, relx=0.51, rely=0.05)
frame2frame1 = tk.Frame(frame2,bg="white")
frame2frame1.pack()
frame2frame2 = tk.Frame(frame2,bg="white")
frame2frame2.pack()

#--- RIGHT FRAME TIMER INPUT ---
label = tk.Label(frame2frame1,text="Enter Timer Interval")
label.pack(side='left')
timerInput = tk.Entry(frame2frame1,bg="grey")
timerInput.pack(side='left')
# timerInput.place( relx=0.51, rely=0.05)
# canvas.create_window(200,140,window=w)
label = tk.Label(frame2frame2,text="Enter Sound File Name: e.g beep.wav")
label.pack(side='left')
soundInput = tk.Entry(frame2frame2,bg="grey")
timerInput.pack(side='left')
# soundInput.place( relx=0.51, rely=0.10)
print(timerInput.get())

#--- BUTTONS ---
stopTimer = tk.Button(root, text="Stop Timer", padx=10,
                    pady=5,fg="white",bg="#263D42", command=setActive)
stopTimer.pack(side='right')
startTimer = tk.Button(root, text="Start Timer", padx=10,
                    pady=5,fg="white",bg="#263D42", command=lambda: runTimer(timerInput))
startTimer.pack(side='right')
setSoundButton = tk.Button(root, text="Set Alarm Sound", padx=10,
                    pady=5,fg="white",bg="#263D42", command=lambda: setSoundFile(soundInput))
setSoundButton.pack(side='right')
openFile = tk.Button(root, text="Open File", padx=10,
                    pady=5,fg="white",bg="#263D42", command=addApp)
openFile.pack(side='left')
runApps = tk.Button(root, text="Run Apps", padx=10,
                    pady=5,fg="white",bg="#263D42", command=runApps)
runApps.pack(side='left')

#when app starts up for first time
for app in apps:
    label = tk.Label(frame1,text=app)
    label.pack()


#run root
root.mainloop()

#save and write to txt file
with open('save.txt','w') as f:
    #remove dupes
    apps = list(dict.fromkeys(apps))

    #save our preferences comma separated
    for app in apps:
        f.write(app + ',')