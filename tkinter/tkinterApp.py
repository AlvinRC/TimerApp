

def displayApps(hidden,frame,button):
    if (not hidden):
        print("hiding")
        frame.grid_forget()
        button.config(text='>')
        hidden = True
    else:
        print("showing")
        frame.grid(row=0,sticky='nsew')
        button.config(text='<')
        hidden = False
    print(hidden)
    return hidden