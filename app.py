#GUI
import tkinter as tk
#file dialog help us pick apps, text helps us display text
from tkinter import filedialog, Text
#os allows us to run applications
import os

#external file import
import timerApp

#--- ROOT ---
#create root of app
root = tk.Tk()
apps = []

if os.path.isfile('save.txt'):
    with open("save.txt",'r') as f:
        tempApps = f.read()
        tempApps = tempApps.split(',')
        #for every element in tempapps after we strip empty
        apps = [x for x in tempApps if x.strip()]

def addApp():
    #remove everything in frame first
    for widget in frame.winfo_children():
        widget.destroy()

    filename= filedialog.askopenfilename(initialdir="/",title="Select File",
    filetypes=(("exectuables","*.exe"),("all files", "*.*")))
    apps.append(filename)
    print(filename)
    for app in apps:
        #create and attach label to frame
        label = tk.Label(frame,text=app, bg="gray")
        label.pack()

def runApps():
    for app in apps:
        os.startfile(app)

#--- CANVAS ---
#create and attach canvas to root, set height,width and background colour
canvas = tk.Canvas(root,height=700,width=700,bg="#263D42")
#Load canvas
canvas.pack()

#--- FRAME ---
#left
#create and attach frame to root, set bg to white
frame2 = tk.Frame(root,bg="white")
#make frame take up 0.8 of roots heigh and width and be centered with a 10% border
frame2.place(relwidth=0.49,relheight=0.8, relx=0.51, rely=0.05)
#right
frame = tk.Frame(root,bg="white")
frame.place(relwidth=0.49,relheight=0.8, relx=0.0, rely=0.05)

#--- RIGHT FRAME TIMER ---
w = tk.Entry(root,bg="grey")
w.place(relwidth=0.49,relheight=0.1, relx=0.51, rely=0.05)
# canvas.create_window(200,140,window=w)
print(w.get())

#--- BUTTONS ---
startTimer = tk.Button(root, text="Start Timer", padx=10,
                    pady=5,fg="white",bg="#263D42", command=timerApp.startTimer)
startTimer.pack()
openFile = tk.Button(root, text="Open File", padx=10,
                    pady=5,fg="white",bg="#263D42", command=addApp)
openFile.pack(side='right',expand=True)
runApps = tk.Button(root, text="Run Apps", padx=10,
                    pady=5,fg="white",bg="#263D42", command=runApps)
runApps.pack(side='left',expand=True)

#when app starts up for first time
for app in apps:
    label = tk.Label(frame,text=app)
    label.pack()

#run root
root.mainloop()

#save and write to txt file
with open('save.txt','w') as f:
    #save our preferences comma separated
    for app in apps:
        f.write(app + ',')