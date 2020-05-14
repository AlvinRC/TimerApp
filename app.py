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
finished = False

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
        print(currActive,soundFile)
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
    for widget in leftFrame.winfo_children():
        widget.destroy()

    filename= filedialog.askopenfilename(initialdir="/",title="Select File",
    filetypes=(("exectuables","*.exe"),("all files", "*.*")))
    apps.append(filename)
    print(filename)
    #remove dupe
    apps = list(dict.fromkeys(apps))

    for app in apps:
        #create and attach label to frame
        label = tk.Label(leftFrame,text=app, bg="gray")
        label.pack()

def runApps():
    for app in apps:
        os.startfile(app)

def runTimer(timerInput):
    global textId,currActive
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
        currActive = True
        finished = False
        displayTimer(timerInputList)
    else:
        if (textId != -1):
            canvas.delete(textId)
        # Add new text
        textId = canvas.create_text(
            [10, 20], anchor='w', text="Timer: Invalid Format", font=("Consolas", 20), fill="#99aab5"
            )
    #doesnt reach this (TODO)
    # threading2.join()
def displayTimer(timerInputList):
    global run, s, m, h,textId,currActive,finished
    
    if (textId != -1):
        canvas.delete(textId)
    
    # Add new text
    textId = canvas.create_text(
        [10, 20], anchor='w', text="Timer: %s:%s:%s" % (h, m, s), font=("Consolas", 20), fill="#99aab5"
        )

    s+=1
    if s == 59:
        m+=1; s=0
    elif m == 59:
        h+=1; m=0
    
    #check that new time isnt > time limit
    
    if (not currActive):
        #reset timer vars now
        h = 0
        m = 0
        s = 0
        finished = False
        return
    if (not (h == timerInputList[0] and m == timerInputList[1] and s == timerInputList[2]) and not finished):
        # After 1 second, call Run again (start an infinite recursive loop)
        root.after(1000, displayTimer, timerInputList)
    else:
        if(h == timerInputList[0] and m == timerInputList[1] and s == timerInputList[2]):
            finished = True
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
            finished = False
            # alarmThread.join()

#--- CANVAS ---
#create and attach canvas to root, set height,width and background colour
canvas = tk.Canvas(root,height=700,width=700,bg="#7289da")
#Load canvas
canvas.pack()

#--- FRAMES ---
#base frames
# headerFrame = tk.Frame(canvas)
# headerFrame.place(relwidth=1,relheight=0.1)
mainFrame = tk.Frame(canvas,bg="#99aab5")
mainFrame.place(relwidth=1,relheight=0.85,rely=0.1)
footerFrame = tk.Frame(canvas,bg="#7289da")
footerFrame.place(relwidth=1,relheight=0.05,rely=0.95)

#left
#create and attach frame to root, set bg to white
#make frame take up 0.8 of roots heigh and width and be centered with a 10% border
leftFrame = tk.Frame(mainFrame,bg="white")
leftFrame.grid(row=0,sticky='nsew')
# leftFrame.place(relwidth=0.49,relheight=0.8, relx=0.0, rely=0.05)
#separator
separator = tk.Frame(mainFrame,bg="black")
separator.grid(row=0,column=1,sticky='ns')

#right
rightFrame = tk.Frame(mainFrame,bg="white")
rightFrame.grid(row=0,column=2,sticky='nsew')
# rightFrame.place(relwidth=0.49,relheight=0.8, relx=0.51, rely=0.05)

#right frames
rightFrame1 = tk.Frame(rightFrame,bg="#99aab5")
rightFrame1.pack()
rightFrame2 = tk.Frame(rightFrame,bg="#99aab5")
rightFrame2.pack()

#--- INPUT GRID
label1 = tk.Label(rightFrame1,text="Enter Timer Interval")
timerInput = tk.Entry(rightFrame1,bg="grey")
label2 = tk.Label(rightFrame2,text="Enter Sound File Name: e.g beep.wav")
soundInput = tk.Entry(rightFrame2,bg="grey")

label1.grid(row=0)
label2.grid(row=1)
timerInput.grid(row=0,column=1)
soundInput.grid(row=1,column=1)
# label1.pack(side='left')
# timerInput.pack(side='left')
# label2.pack(side='left')
# soundInput.pack(side='left')

# soundInput.place( relx=0.51, rely=0.10)
print(timerInput.get())






#--- BUTTONS ---
stopTimer = tk.Button(footerFrame, text="Stop Timer", padx=10,
                    pady=5,fg="white",bg="#7289da", command=setActive)
stopTimer.pack(side='right',anchor='s')
startTimer = tk.Button(footerFrame, text="Start Timer", padx=10,
                    pady=5,fg="white",bg="#7289da", command=lambda: runTimer(timerInput))
startTimer.pack(side='right',anchor='s')
setSoundButton = tk.Button(footerFrame, text="Set Alarm Sound", padx=10,
                    pady=5,fg="white",bg="#7289da", command=lambda: setSoundFile(soundInput))
setSoundButton.pack(side='right',anchor='s')
openFile = tk.Button(footerFrame, text="Open File", padx=10,
                    pady=5,fg="white",bg="#7289da", command=addApp)
openFile.pack(side='left',anchor='s')
runApps = tk.Button(footerFrame, text="Run Apps", padx=10,
                    pady=5,fg="white",bg="#7289da", command=runApps)
runApps.pack(side='left',anchor='s')

#when app starts up for first time
for app in apps:
    label = tk.Label(leftFrame,text=app)
    label.pack()


#run root
root.mainloop()
currActive = False
#save and write to txt file
with open('save.txt','w') as f:
    #remove dupes
    apps = list(dict.fromkeys(apps))

    #save our preferences comma separated
    for app in apps:
        f.write(app + ',')