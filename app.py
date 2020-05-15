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
changed = False
defaultColour1 = '#7289da'
defaultColour2 = "#00adef"

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
    for widget in leftFrame1.winfo_children():
        widget.destroy()

    filename= filedialog.askopenfilename(initialdir="/",title="Select File",
    filetypes=(("exectuables","*.exe"),("all files", "*.*")))
    apps.append(filename)
    print(filename)
    #remove dupe
    apps = list(dict.fromkeys(apps))

    count = 0
    for app in apps:
        #create and attach label to frame
        label = tk.Label(leftFrame1,text=app,bg='white')
        # label.pack(anchor='w')
        label.grid(row=count,sticky='w')
        count = count + 1

def runApps():
    for app in apps:
        os.startfile(app)

def changeColours():
    global changed,defaultColour1,defaultColour2
    colour = defaultColour1
    if(not changed):
        colour = defaultColour2
        changed = True
    else:
        changed = False
    # print(colour,changed)
    canvas.config(background=colour)
    footerFrame.config(background=colour)
    for widget in footerFrame.winfo_children():
        widget.config(background=colour)
def runTimer(timerInput):
    global textId,currActive

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
        for widget in rightFrameTimer.winfo_children():
            widget.destroy()
        #add new text
        timerLabel = tk.Label(rightFrameTimer,text="Timer: Invalid Format", font=("Consolas", 20),bg='white')
        timerLabel.pack(anchor='w')
def displayTimer(timerInputList):
    global run, s, m, h,textId,currActive,finished
    
    for widget in rightFrameTimer.winfo_children():
        widget.destroy()
    #add new text
    timerLabel = tk.Label(rightFrameTimer,text="Timer: %s:%s:%s" % (h, m, s), font=("Consolas", 20),bg='white')
    timerLabel.pack(anchor='w')
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
canvas.pack(expand='true',fill='x') 

#--- FRAMES ---
#base frames
# headerFrame = tk.Frame(canvas)
# headerFrame.place(relwidth=1,relheight=0.1)
mainFrame = tk.Frame(canvas,bg="#99aab5")
mainFrame.place(relwidth=1,relheight=0.85,rely=0.1)
#stretch x
mainFrame.grid_columnconfigure(0,weight=1,uniform='groupname')
mainFrame.grid_columnconfigure(1,weight=0)
mainFrame.grid_columnconfigure(2,weight=2,uniform='groupname')
#stretch y
mainFrame.grid_rowconfigure(0,weight=1)

# mainFrame.place(relwidth=0.994,relheight=0.85,rely=0.1,relx=0.003)
footerFrame = tk.Frame(canvas,bg="#7289da")
footerFrame.place(relwidth=1,relheight=0.05,rely=0.95)

#left
#create and attach frame to root, set bg to white
#make frame take up 0.8 of roots heigh and width and be centered with a 10% border
leftFrame = tk.Frame(mainFrame,bg="white")
leftFrame.grid(row=0,column=0,sticky='nsew')
leftFrame.grid_columnconfigure(0,weight=1)

#left frames
leftFrame1 = tk.Frame(leftFrame,bg="white")
leftFrame1.grid(row=0,column=0,sticky='nsew')
leftFrame2 = tk.Frame(leftFrame,bg="black")
leftFrame2.grid(row=1,column=0,sticky='nsew')
# #separator
separator = tk.Frame(mainFrame,bg="black")
separator.grid(row=0,column=1,sticky='ns',ipadx=1)

#right
rightFrame = tk.Frame(mainFrame,bg="white")
rightFrame.grid(row=0,column=2,sticky='nsew')
#scale based of text size
rightFrame.grid_columnconfigure(0,weight=2,uniform='group2')
rightFrame.grid_columnconfigure(1,weight=1,uniform='group2')

# rightFrame.place(relwidth=0.49,relheight=0.8, relx=0.51, rely=0.05)

#right frames
rightFrame1 = tk.Frame(rightFrame,bg="#99aab5")
rightFrame1.grid(row=0,sticky='w')
rightFrame1right = tk.Frame(rightFrame,bg="#99aab5")
rightFrame1right.grid(row=0,column=1,sticky='e')
rightFrame2 = tk.Frame(rightFrame,bg="#99aab5")
rightFrame2.grid(row=1,sticky='w')
rightFrame2right = tk.Frame(rightFrame,bg="#99aab5")
rightFrame2right.grid(row=1,column=1,sticky='e')

rightFrameTimer = tk.Frame(rightFrame,bg="#99aab5")
rightFrameTimer.grid(row=2,columnspan=2,stick='w')

rightFrame
#--- INPUT GRID
label1 = tk.Label(rightFrame1,text="Enter Timer Interval",bg='white')
timerInput = tk.Entry(rightFrame1right,bg="lightgray")
label2 = tk.Label(rightFrame2,text="Enter Sound File Name: e.g beep.wav",bg='white')
soundInput = tk.Entry(rightFrame2right,bg="lightgray")

label1.pack(anchor='w')
timerInput.pack(anchor='e')
label2.pack(anchor='w')
soundInput.pack(anchor='e')

# soundInput.place( relx=0.51, rely=0.10)
print(timerInput.get())






#--- BUTTONS ---
stopTimer = tk.Button(footerFrame, text="Stop Timer", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=setActive)
stopTimer.pack(side='right',anchor='s')
startTimer = tk.Button(footerFrame, text="Start Timer", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=lambda: runTimer(timerInput))
startTimer.pack(side='right',anchor='s')
setSoundButton = tk.Button(footerFrame, text="Set Alarm Sound", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=lambda: setSoundFile(soundInput))
setSoundButton.pack(side='right',anchor='s')

changeColour = tk.Button(footerFrame, text="Change Colours", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=changeColours)
changeColour.pack(side='left',anchor='s')

openFile = tk.Button(footerFrame, text="Open File", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=addApp)
openFile.pack(side='left',anchor='s')
runApps = tk.Button(footerFrame, text="Run Apps", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=runApps)
runApps.pack(side='left',anchor='s')

#when app starts up for first time
count = 0
for app in apps:
    label = tk.Label(leftFrame1,text=app,bg='white')
    # label.pack(anchor='w')
    label.grid(row=count,sticky='w')
    count = count + 1
    
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