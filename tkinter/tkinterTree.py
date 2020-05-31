import tkinter.ttk as ttk
def initTree(treeFrame):
    tree = ttk.Treeview(treeFrame,style="Treeview",height='1')
    return tree
def populateTree(tree,dailyTimeConfig,dailyTimeConfigNum):
    if (not dailyTimeConfig):
        dailyTimeConfig.append(('5:0:0','5:0:0','5:0:0','5:0:0','5:0:0','4:0:0','4:0:0'))
    tree.insert('', 'end', text="Config 1", values=dailyTimeConfig[dailyTimeConfigNum])

def displayDay(tree,weekday):
    week = list(('','','','','','',''))
    week[weekday]='^'
    week = tuple(week)
    tree.config(height='2')
    tree.insert('','end',text='Current Day',values=week)

def createTree(tree):
    #tree view
    s = ttk.Style()
    s.configure('Treeview',rowheight=20)
    s.configure('Treeview.Cell',foreground='blue')
    # s.configure("mystyle.Treeview.column", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
    tree['columns'] = ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
    tree.heading("#0", text='Daily Total Timers', anchor='w')
    tree.column("#0", anchor="w")
    for col in tree['columns']:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=80)
    tree.grid()