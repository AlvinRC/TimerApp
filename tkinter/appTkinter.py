#GUI
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
#file dialog help us pick apps, text helps us display text
from tkinter import filedialog, Text
#os allows us to run applications
import os
import threading
#external file import
import timerApp
import winsound
#date time
import datetime

#---- EDIT CONFIG HERE -----
dailyTimeConfig = []
dailyTimeConfigNum = 0

#--- ROOT ---
#create root of app
root = tk.Tk()
root.title('Timer App')
#--- Default vars --- 
apps = []
checked = []
run = True; s=0; m=0; h=0
textId=-1
currActive=False; finished = False;changed = False;ended = False;paused = False;hidden = False
dh=0;dm=0;ds=0
daily = False
currActiveSep = False
defaultColour1 = '#7289da'
defaultColour2 = "#00adef"
weekday = datetime.datetime.today().weekday()

#--- Default sound file ---
soundFile = 'shortBeepSound.wav'

if not os.path.isfile('save.txt'):
    f = open("save.txt",'w+')
    f.close()

with open("save.txt",'r') as f:
    tempApps = f.read()
    tempApps = tempApps.split(',')
    #for every element in tempapps after we strip empty
    apps = [x for x in tempApps if x.strip()]



if os.path.isfile('dailyConfig.txt'):
    with open("dailyConfig.txt",'r') as f:
        tmpDaily = f.read()
        if(not tmpDaily):
            pass
        else:
            # print(tmpDaily)
            tmpDaily = tmpDaily.split('|')
            dailyTimeConfig = [x.replace('\'','').replace(',','').replace('(','').replace(')','') for x in tmpDaily if x.strip()]
            # print(dailyTimeConfig)

def populateTree(tree):
    global dailyTimeConfig
    if (not dailyTimeConfig):
        dailyTimeConfig.append(('5:0:0','5:0:0','5:0:0','5:0:0','5:0:0','4:0:0','4:0:0'))
    tree.insert('', 'end', text="Config 1", values=dailyTimeConfig[dailyTimeConfigNum])

def displayDay(tree):
    week = list(('','','','','','',''))
    week[weekday]='^'
    week = tuple(week)
    tree.config(height='2')
    tree.insert('','end',text='Current Day',values=week)
def createTree(tree):
    global weekday
    #tree view
    s = ttk.Style()
    s.configure('Treeview',rowheight=20)
    s.configure('Treeview.Cell',foreground='blue')
    # s.configure("mystyle.Treeview.column", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body

    tree['columns'] = ('mon','tue','wed','thu','fri','sat','sun')
    tree.heading("#0", text='Daily Total Timers', anchor='w')
    tree.column("#0", anchor="w")
    tree.heading('mon', text='Monday')
    tree.column('mon', anchor='center', width=80)
    tree.heading('tue', text='Tuesday')
    tree.column('tue', anchor='center', width=80)
    tree.heading('wed', text='Wednesday')
    tree.column('wed', anchor='center', width=80)
    tree.heading('thu', text='Thursday')
    tree.column('thu', anchor='center', width=80)
    tree.heading('fri', text='Friday')
    tree.column('fri', anchor='center', width=80)
    tree.heading('sat', text='Saturday')
    tree.column('sat', anchor='center', width=80)
    tree.heading('sun', text='Sunday')
    tree.column('sun', anchor='center', width=80)
    
    
        


    tree.grid()
    populateTree(tree)
    displayDay(tree)
    
    # tree.winfo_children()
    
    createDailyTimer(tree)

def createDailyTimer(tree):
    global weekday,dh,dm,ds
    configNum = 0
    currConfig = tree.item(tree.get_children()[configNum])["values"]
    currDaily = currConfig[weekday]
    print(currDaily)
    # for child in tree.get_children():
    #     print(tree.item(child)["values"])
    # pass
    
    dh = int(currDaily.split(":")[0])
    dm = int(currDaily.split(":")[1])
    ds = int(currDaily.split(":")[2])

    timerLabel = tk.Label(rightFrameDaily,text="Daily Timer: %s:%s:%s" % (dh, dm, ds), font=("Consolas", 20),bg='white')
    timerLabel.pack(anchor='w')

def setDaily(dailyTimerInput):
    global dh, dm,ds, weekday, dailyTimeConfig,dailyTimeConfigNum,tree
    #print(dailyTimerInput)
    tmpdh = int(dailyTimerInput.get().split(":")[0])
    tmpdm = int(dailyTimerInput.get().split(":")[1])
    tmpds = int(dailyTimerInput.get().split(":")[2])
    if(tmpdh not in range(0,24)):
        print("INVALID HOUR")
        return
    if(tmpdm not in range(0,59)):
        print("INVALID MINS")
        return 
    if(tmpds not in range(0,59)):
        print("INVALID SECS ")
        return
    dh = tmpdh
    dm = tmpdm
    ds = tmpds
    # print(dailyTimeConfig)
    tmpConfig = dailyTimeConfig[dailyTimeConfigNum].split(' ')
    newConfig = ''
    count = 0
    for tmp in tmpConfig:
        if(count == weekday):
            tmp = "%s:%s:%s" % (dh, dm, ds)
        # print(tmp)
        newConfig += tmp+' '
        count += 1
    print("weow")
    print(newConfig.strip().split(' '))
    dailyTimeConfig[dailyTimeConfigNum] = newConfig.strip()
    #edit tree values 
    print(tree.item(tree.get_children()[dailyTimeConfigNum])["values"])
    #tree.item(tree.get_children()[dailyTimeConfigNum])["values"]
    # print("children")
    # print(tree.get_children())
    for child in tree.get_children():
        tree.delete(child)
    # tree.delete(tree.get_children()[dailyTimeConfigNum])
    tree.insert('','end',text="Updated Config", values=newConfig.strip().split(' '))
    displayDay(tree)
    # print(newConfig.strip().split(' '))
    # print(tree.item(tree.get_children()[dailyTimeConfigNum])["values"])
    # print(tree.item(tree.get_children()[1])["values"])
    for widget in rightFrameDaily.winfo_children():
        widget.destroy()
    timerLabel = tk.Label(rightFrameDaily,text="Daily Timer: %s:%s:%s" % (dh, dm, ds), font=("Consolas", 20),bg='white')
    timerLabel.pack(anchor='w')

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

def displayApps():
    global hidden
    if (not hidden):
        print("hiding")
        leftFrame.grid_forget()
        displayAppsButton.config(text='>')
        hidden = True
    else:
        print("showing")
        leftFrame.grid(row=0,sticky='nsew')
        displayAppsButton.config(text='<')
        hidden = False
    pass


def addApp():
    global apps,checked
    checked.clear()
    count = 0
    
    filename= filedialog.askopenfilename(initialdir="/",title="Select File",
    filetypes=(("exectuables","*.exe"),("all files", "*.*")))
    if(filename):
        apps.append(filename)
    else: 
        #nothing selected
        return 
    print(filename)
    #remove dupe
    apps = list(dict.fromkeys(apps))
    #remove everything in frame first
    for widget in leftFrame1.winfo_children():
        widget.destroy()
        count = count + 1
    count = 0
    for app in apps:
        var = tk.BooleanVar()
        #create and attach label to frame
        checkButton = tk.Checkbutton(leftFrame1,text=app,bg='white',variable=var)
        checked.append(var)
        # label.pack(anchor='w')
        checkButton.grid(row=count,sticky='w')
        count = count + 1

def deleteApp():
    global apps,checked
    count = 0
    deleted = []
    for widget in leftFrame1.winfo_children():
        if(checked[count].get()):
            widget.destroy()
            deleted.append(count)
        count = count + 1
    reverseList = sorted(deleted,reverse=True)
    print(reverseList)

    for index in reverseList:
        print('deleted ',apps[index])
        del checked[index]
        del apps[index]
    # for item in checked:
    #     print(item.get())
        
    # #remove everything in frame first
    # for widget in leftFrame1.winfo_children():
    #     widget.destroy()
    #     count = count + 1
    

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
    for widget in leftFrameButtons.winfo_children():
        widget.config(background=colour)
    for widget in rightFrameButtons.winfo_children():
        widget.config(background=colour)
    for widget in separator.winfo_children():
        widget.config(background=colour)

def pauseTimer():
    global paused
    setActive()
    paused = True

def resumeTimer():
    global paused,currActive
    currActive = True
    paused = False

def endTimer():
    global ended,paused,daily
    setActive()
    daily = False
    ended = True
    paused = False

def setActive():
    global currActive
    currActive = False

def setSoundFile(soundInput):
    global soundFile
    soundFile = soundInput.get()

def runTimer(timerInput):
    global textId,currActive
    global h,m,s,finished
    if (currActive):
        #already running
        return
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
    global run, s, m, h,textId,currActive,finished,dh,dm,ds,daily
    global paused,ended
    #check that new time isnt > time limit
    #stop early
    if (not currActive):
        # print(paused,ended)

        if(paused):
            #TODO:do something to wait here until resume or stop
            root.after(1000, displayTimer, timerInputList)
            # pass
        elif(ended):
            #reset timer vars now
            h = 0
            m = 0
            s = 0
            paused = False
            finished = False
            daily = False
        return 
    
    for widget in rightFrameTimer.winfo_children():
        widget.destroy()
    #add new text
    timerLabel = tk.Label(rightFrameTimer,text="Timer: %s:%s:%s" % (h, m, s), font=("Consolas", 20),bg='white')
    timerLabel.pack(anchor='w')
    if (daily):
        for widget in rightFrameDaily.winfo_children():
            widget.destroy()
        dailyLabel = tk.Label(rightFrameDaily,text="Daily Timer: %s:%s:%s" % (dh, dm, ds), font=("Consolas", 20),bg='white')
        dailyLabel.pack(anchor='w')
        
        
        ds-=1
        if(ds == -1):
            dm-=1; ds = 59
            if dm == -1:
                dh-=1; dm = 59
                if dh == -1:
                    #finished
                    dh = 0
                    dm = 0
                    ds = 0
                    print("Daily Finished")
                    currActive = True
                    #play sound
                    alarmThread = threading.Thread(target=alarmSound)
                    alarmThread.start()
                    daily = False
                    return

    # if dh == 0 and dm == 0 and ds == 0:
    #     return     
    # rightFrameDaily
    s+=1
    if s == 59:
        m+=1; s=0
    if m == 60:
        h+=1; m=0; s=0
    
    
    if (not (h == timerInputList[0] and m == timerInputList[1] and s == timerInputList[2]) and not finished):
        # After 1 second, call Run again (start an infinite recursive loop)
        root.after(1000, displayTimer, timerInputList)
    else:
        if(h == timerInputList[0] and m == timerInputList[1] and s == timerInputList[2]):
            finished = True
            root.after(1000, displayTimer, timerInputList)
        else:
            print(h,m,s,timerInputList)
            #display timer finishedz
            currActive = True
            #play sound
            alarmThread = threading.Thread(target=alarmSound)
            alarmThread.start()
            #exit timer
            #reset timer vars now
            h = 0
            m = 0
            s = 0
            finished = False
            daily = False
            # alarmThread.join()

def runDaily(timerInput):
    global daily
    daily = True
    runTimer(timerInput)

#--- CANVAS ---
#create and attach canvas to root, set height,width and background colour
canvas = tk.Canvas(root,height=700,width=700,bg="#7289da")
#Load canvas
canvas.pack(expand='true',fill='x') 

#--- FRAMES ---
#base frames
headerFrame = tk.Frame(canvas)
headerFrame.grid(row=0,sticky='ew')

# headerFrame.place(relwidth=1,relheight=0.1)
mainFrame = tk.Frame(canvas,bg="#99aab5")
mainFrame.grid(row=1,sticky='nsew')
# mainFrame.place(relwidth=1,relheight=0.85,rely=0.1)
#stretch x
# mainFrame.grid_columnconfigure(0,weight=0,uniform='groupname')
# mainFrame.grid_columnconfigure(1,weight=0)
# mainFrame.grid_columnconfigure(2,weight=1,uniform='groupname')
#stretch y
mainFrame.grid_rowconfigure(0,weight=1)

# mainFrame.place(relwidth=0.994,relheight=0.85,rely=0.1,relx=0.003)
footerFrame = tk.Frame(canvas,bg="#7289da")
footerFrame.grid(row=2,sticky='ew')
# footerFrame.place(relwidth=1,relheight=0.05,rely=0.95)

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
leftFrameButtons = tk.Frame(leftFrame,bg="white")
leftFrameButtons.grid(row=2,column=0,sticky='nsew')
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
rightFrameTree = tk.Frame(rightFrame,bg="#99aab5")
rightFrameTree.grid(row=0,columnspan=2,stick='w')
rightFrameDaily = tk.Frame(rightFrame,bg="#99aab5")
rightFrameDaily.grid(row=1,sticky='w')

rightFrame1 = tk.Frame(rightFrame,bg="#99aab5")
rightFrame1.grid(row=2,sticky='w')
rightFrame1right = tk.Frame(rightFrame,bg="#99aab5")
rightFrame1right.grid(row=2,column=1,sticky='e')
rightFrame2 = tk.Frame(rightFrame,bg="#99aab5")
rightFrame2.grid(row=3,sticky='w')
rightFrame2right = tk.Frame(rightFrame,bg="#99aab5")
rightFrame2right.grid(row=3,column=1,sticky='e')
rightFrame3 = tk.Frame(rightFrame,bg="#99aab5")
rightFrame3.grid(row=4,sticky='w')
rightFrame3right = tk.Frame(rightFrame,bg="#99aab5")
rightFrame3right.grid(row=4,column=1,sticky='e')
# rightFrame4 = tk.Frame(rightFrame,bg="#99aab5")
# rightFrame4.grid(row=5,sticky='w')
# rightFrame4right = tk.Frame(rightFrame,bg="#99aab5")
# rightFrame4right.grid(row=5,column=1,sticky='e')

rightFrameTimer = tk.Frame(rightFrame,bg="#99aab5")
rightFrameTimer.grid(row=5,columnspan=2,stick='w')

rightFrameButtons = tk.Frame(rightFrame,bg="#99aab5")
rightFrameButtons.grid(row=6,columnspan=2,stick='w')



tree = ttk.Treeview(rightFrameTree,style="Treeview",height='1')
createTree(tree)
# self.grid_rowconfigure(0, weight = 1)
# self.grid_columnconfigure(0, weight = 1)


# label = tk.Label(rightFrame1,text="Daily Timers",bg='white')
# labelMonday = tk.Label(rightFrame1,text="Monday",bg='white')
# labelTuesday = tk.Label(rightFrame1,text="Tuesday",bg='white')
# labelWednesday = tk.Label(rightFrame1,text="Wednesday",bg='white')
# labelThursday = tk.Label(rightFrame1,text="Thursday",bg='white')
# labelFriday = tk.Label(rightFrame1,text="Friday",bg='white')
# labelSaturday = tk.Label(rightFrame1,text="Saturday",bg='white')
# labelMonday = tk.Label(rightFrame1,text="Sunday",bg='white')




#--- INPUT GRID

label1 = tk.Label(rightFrame1,text="Enter Timer Interval",bg='white')
timerInput = tk.Entry(rightFrame1right,bg="lightgray")
label2 = tk.Label(rightFrame2,text="Enter Custom Daily Timer",bg='white')
dailyTimerInput = tk.Entry(rightFrame2right,bg="lightgray")
label3 = tk.Label(rightFrame3,text="Enter Sound File Name: e.g beep.wav",bg='white')
soundInput = tk.Entry(rightFrame3right,bg="lightgray")
# label4 = tk.Label(rightFrame4,text="Enter Separate Timer Interval",bg='white')
# timerInputSeparate = tk.Entry(rightFrame4right,bg="lightgray")

label1.grid(row=2,sticky='w')
timerInput.grid(row=2,column=1,sticky='w')
label2.grid(row=3,column=1,sticky='w')
dailyTimerInput.grid(row=3,sticky='w')
label3.grid(row=4,column=1,sticky='w')
soundInput.grid(row=4,sticky='w')
# label4.grid(row=5,column=1,sticky='w')
# timerInputSeparate.grid(row=5,sticky='w')

# label1.pack(anchor='w')
# timerInput.pack(anchor='e')
# label2.pack(anchor='w')
# soundInput.pack(anchor='e')

# soundInput.place( relx=0.51, rely=0.10)
print(timerInput.get())


#TITLE:
label1 = tk.Label(headerFrame,text="App Runner",bg='white')
label2 = tk.Label(headerFrame,text="Timer",bg='white')
label1.grid(row=0,sticky='w')
label2.grid(row=0,column=2,sticky='w')
# headerFrame.grid_columnconfigure(0,weight=1,uniform='title')
# headerFrame.grid_columnconfigure(1,weight=0)
# headerFrame.grid_columnconfigure(2,weight=1,uniform='title')

#--- BUTTONS ---
setSoundButton = tk.Button(rightFrameButtons, text="Set Alarm Sound", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=lambda: setSoundFile(soundInput))
setSoundButton.pack(side='right',anchor='s')
setNewDaily = tk.Button(rightFrameButtons, text="Set Custom Daily", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=lambda: setDaily(dailyTimerInput))
setNewDaily.pack(side='right',anchor='s')
stopTimer = tk.Button(rightFrameButtons, text="Stop Timer", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=endTimer)
stopTimer.pack(side='right',anchor='s')
pauseTimerButton = tk.Button(rightFrameButtons, text="Pause Timer", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=pauseTimer)
pauseTimerButton.pack(side='right',anchor='s')
resumeTimerButton = tk.Button(rightFrameButtons, text="Resume Timer", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=resumeTimer)
resumeTimerButton.pack(side='right',anchor='s')
startTimer = tk.Button(rightFrameButtons, text="Start Timer", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=lambda: runTimer(timerInput))
startTimer.pack(side='right',anchor='s')
startDailyTimer = tk.Button(rightFrameButtons, text="Start Daily Timer", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=lambda: runDaily(timerInput))
startDailyTimer.pack(side='right',anchor='s')


changeColour = tk.Button(footerFrame, text="Change Colours", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=changeColours)
changeColour.pack(side='left',anchor='s')

openFile = tk.Button(leftFrameButtons, text="Add App", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=addApp)
openFile.pack(side='left',anchor='s')
deleteFile = tk.Button(leftFrameButtons, text="Delete App", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=deleteApp)
deleteFile.pack(side='left',anchor='s')
runApps = tk.Button(leftFrameButtons, text="Run Apps", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=runApps)
runApps.pack(side='left',anchor='s')


#arrow button <> goes here probably in middle frame?
displayAppsButton = tk.Button(separator, text="<", padx=10,
                    pady=5,fg="white",bg=defaultColour1, command=displayApps)
displayAppsButton.pack(side='left',expand=True,fill='both', anchor='s')
# hideAppsButton = tk.Button(separator, text="Hide Apps", padx=10,
#                     pady=5,fg="white",bg=defaultColour1, command=hideApps)
# hideAppsButton.pack(side='left',expand=True,fill='both',anchor='s')


#when app starts up for first time
count = 0
for app in apps:
    var = tk.BooleanVar()
    #create and attach label to frame
    checkButton = tk.Checkbutton(leftFrame1,text=app,bg='white',variable=var)
    checked.append(var)
    checkButton.grid(row=count,sticky='w')
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
with open('dailyConfig.txt','w') as f:
    #save our preferences comma separated
    for dailyConfig in dailyTimeConfig:
        print(dailyConfig)
        f.write(str(dailyConfig) + '|')