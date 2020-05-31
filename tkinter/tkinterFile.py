
import os
#os allows us to run applications

def readApps():
    if not os.path.isfile('save.txt'):
        f = open("save.txt",'w+')
        f.close()
    apps = []
    with open("save.txt",'r') as f:
        tempApps = f.read()
        tempApps = tempApps.split(',')
        #for every element in tempapps after we strip empty
        apps = [x for x in tempApps if x.strip()]
    return apps

def readDaily():
    if not os.path.isfile('dailyConfig.txt'):
        f = open("dailyConfig.txt",'w+')
        f.close()
    dailyTimeConfig = []
    with open("dailyConfig.txt",'r') as f:
        tmpDaily = f.read()
        if(not tmpDaily):
            pass
        else:
            # print(tmpDaily)
            tmpDaily = tmpDaily.split('|')
            dailyTimeConfig = [x.replace('\'','').replace(',','').replace('(','').replace(')','') for x in tmpDaily if x.strip()]
    return dailyTimeConfig

def runApps(apps):
    for app in apps:
        os.startfile(app)

def saveApps(apps):
    with open('save.txt','w') as f:
        #remove dupes
        apps = list(dict.fromkeys(apps))

        #save our preferences comma separated
        for app in apps:
            f.write(app + ',')
def saveDaily(dailyTimeConfig):
    with open('dailyConfig.txt','w') as f:
        #save our preferences comma separated
        for dailyConfig in dailyTimeConfig:
            print(dailyConfig)
            f.write(str(dailyConfig) + '|')