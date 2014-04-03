# Version: 1.0.0.0

import ftplib
import datetime
import os
from time import strftime, sleep
import Tkinter
from Tkconstants import *
import tkMessageBox

Mode = 0
"""
    Mode = 0
        Exit
    Mode = 1
        Upload Base
    Mode = 2
        Update configuration
    Mode = 3
        Update Base
"""
t1 = ('','',)

path_to_1c = ''
path_to_log = ''
path_to_cfg = ''
path_to_base = []
user = []
password = []
path_to_base_zipped = []
folders = []
directory = ''
bases = []
Tk_phrase = []
time_to_wait = []

def parse():
    """
        path_to_log
        path_to_cfg
        path_to_base[]
        user,password[]
        path_to_base_zipped[]
        directory
        path_to_1c
        secs to wait till 1c has started
        secs to wait till bases are zipped
    """
    a = []
    with open ('C:\\1c\\info.txt') as info:
        for line in info:
            a.append(line.replace('\n',''))
    global path_to_log
    path_to_log = a[0]
    global path_to_cfg
    path_to_cfg = a[1]
    start_pos = 0
    end_pos = 0
    global path_to_base
    for char in a[2]:
        if char == ' ':
            path_to_base.append(a[2][start_pos:end_pos])
            start_pos = end_pos + 1
        end_pos += 1
        if end_pos == len(a[2]):
            path_to_base.append(a[2][start_pos:end_pos])
    start_pos = 0
    end_pos = 0
    global user
    global password
    for char in a[3]:
        if char == ',':
            user.append(a[3][start_pos:end_pos])
            start_pos = end_pos + 1
        if char == ' ':
            if a[3][start_pos:end_pos]:
                password.append(a[3][start_pos:end_pos])
            else:
                password.append('')
            start_pos = end_pos + 1
        end_pos += 1
        if end_pos == len(a[3]):
            password.append(a[3][start_pos:end_pos])
    if len(user) == 1:
        i = 1
        while i<len(path_to_base):
            user.append(user[0])
            password.append(password[0])
            i+=1
    start_pos = 0
    end_pos = 0
    global path_to_base_zipped
    for char in a[4]:
        if char == ' ':
            path_to_base_zipped.append(a[4][start_pos:end_pos])
            start_pos = end_pos + 1
        end_pos += 1
        if end_pos == len(a[4]):
            path_to_base_zipped.append(a[4][start_pos:end_pos])
    global directory
    directory = a[5]
    global folders
    folders = [directory,directory+'/MSFO',directory+'/ZP',directory+'/Newbud',directory+'/Stuff']
    global path_to_1c
    path_to_1c = a[6]
    global time_to_wait
    time_to_wait.append(a[7])
    time_to_wait.append(a[8])

def parseTk():
    global Tk_phrase
    with open ('C:\\1c\\infoTk.txt') as info:
        for line in info:
            Tk_phrase.append(line.replace('\n',''))

def initMenu(tk1=''):
    global Mode
    Mode = 0
    try:
        tk1.destroy()
    except:
        Mode = 0
    tk = Tkinter.Tk()
    frame = Tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
    frame.pack(fill=BOTH,expand=1)
    label = Tkinter.Label(frame, text=Tk_phrase[0])
    label.pack(fill=X, expand=1)
    button_send = Tkinter.Button(frame,text=Tk_phrase[1],command=lambda:action_send(tk))
    button_send.pack(side=LEFT)
    button_exit = Tkinter.Button(frame,text=Tk_phrase[2],command=tk.destroy)
    button_exit.pack(side=LEFT)
    tk.mainloop()

def action_send(tk):
    global Mode
    Mode = 1
    tk.destroy()
    tk1 = Tkinter.Tk()
    frame = Tkinter.Frame(tk1, relief=RIDGE, borderwidth=2)
    frame.pack(fill=BOTH,expand=1)
    label = Tkinter.Label(frame, text=Tk_phrase[3])
    label.pack(fill=X, expand=1)
    i1 = Tkinter.IntVar()
    if Tk_phrase[4]:
        C1 = Tkinter.Checkbutton(frame, text=Tk_phrase[4],variable=i1,height=2,width = 10)
        C1.pack()
    i2 = Tkinter.IntVar()
    if Tk_phrase[5]:
        C2 = Tkinter.Checkbutton(frame,text=Tk_phrase[5],variable = i2,height=2,width=10)
        C2.pack()
    i3 = Tkinter.IntVar()
    if Tk_phrase[6]:
        C3 = Tkinter.Checkbutton(frame, text=Tk_phrase[6],variable=i3,height=2,width=10)
        C3.pack()
    button_send = Tkinter.Button(frame,text=Tk_phrase[1],command=lambda:action_send_true(tk1, i1.get(),i2.get(),i3.get()))
    button_send.pack(side=LEFT)
    button_exit = Tkinter.Button(frame,text=Tk_phrase[7],command=lambda:initMenu(tk1))
    button_exit.pack(side=LEFT)
    tk1.mainloop()

def action_send_true(tk1,i1,i2,i3):
    a = []
    a.append(i1)
    a.append(i2)
    a.append(i3)
    tk1.destroy()
    tupleList(a)

def tupleList(a):
    global bases
    for k in xrange(len(a)):
        if a[k] == 1:
            bases.append(k)

def openLog(path_to_log):
    if os.path.isfile(path_to_log):
        log = open(path_to_log,'a+b')
        log.write('Log opened on ' + strftime("%Y-%m-%d %H:%M:%S")+"\n"+"Mode = "+str(Mode)+"\n")
    else:
        log = open(path_to_log,'a+b')
        log.write('Log created on ' + strftime("%Y-%m-%d %H:%M:%S")+"\n"+"Mode = "+ str(Mode)+"\n")
    return log

def zippedBaseTime(path_to_zipped,log):
    if os.path.isfile(path_to_zipped):
        modification_time = os.path.getmtime(path_to_zipped)
        log.write ('Previous base was zipped on '+ str(datetime.datetime.fromtimestamp(modification_time))+'\n')
        return modification_time#datetime.datetime.fromtimestamp(modification_time)
    else:
        log.write('There are no zipped bases\n')
        return 0


def closeLog(log):
    log.write('End of session\n')
    log.close()

def createCFG(path_to_cfg, log, i,Mode=1):
    try:
        cfg = open(path_to_cfg,'w')
        log.write('Successfully created cfg file\n')
    except:
        log.write('Couldn\'t create cfg file\n')
    try:
        cfg.write('[General]\nQuit='+str(Mode)+'\nSaveData=1\n[SaveData]\nSaveToFile = "'+path_to_base_zipped[i]+'"')
        log.write('Info was written to cfg file. Base Number '+str(i+1)+' of '+str(len(path_to_base_zipped))+'\n')
    except:
        log.write('Info wasn\'t written to cfg file. Base Number '+str(i+1)+'\n')

def Open1c(i,log):
    path = path_to_1c+' config /d'+path_to_base[i]+' /n'+user[i]
    if password[i]:
        path += ' /p'+password[i]
    path += ' /@'+path_to_cfg
    os.system(path)

    log.write('1c is Opened\n')

def updatedFile(path,time0,log):
    i = 0
    log.write ("Checking for update\n")
    while i<int(time_to_wait[0]): #30 seconds
        if zippedBaseTime(path,log)>time0:
            return True
        i+=1
        sleep(1)
    return False

def checkForZip(path,log):
    import zipfile
    time_to_wait = []
    time_to_wait.append(30)
    for k in range(time_to_wait[0]):
        try:
            zfile = zipfile.ZipFile(path)
            zfile.close()
            log.write('Base is zipped. Second: %d Its size: %d ' %(k,os.path.getsize(path)))
            break
        except:
            sleep(1)
    if k<(time_to_wait[0]-1):
        return True
    return False

def createFolder(ftp,path,log):
    try:
        ftp.cwd(path)
        log.write('Directory '+path+' has already been created\n')
    except:
        print(path)
        ftp.mkd(path)
        log.write('Directory '+path+' has just been created\n')

def logIn(log):
    """
        logs in to FTP server
        creates a directory, if not created
        goes to this directory
        returns ftp
    """
    ftp = ftplib.FTP()
    ftp.connect('yunima1c.ucoz.com', 21)
    log.write (ftp.getwelcome()+'\n')
    try:
        log.write ('Logging in...\n')
        ftp.login('dyunima1c', 'a02121987')
    except:
        log.write ('failed to login\n')
    try:
        ftp.set_pasv(True)
        log.write ('success set pasv\n')
    except:
        log.write ('failed set pasv\n')
    i=0
    while (i<len(folders)):
        createFolder(ftp,folders[i],log)
        i+=1
    return ftp

def uploadFile(ftp,path0,path1,log):
    if (len(ftp.nlst(path1))<3):
        path1 += '/1cv7_'+str(len(ftp.nlst(path1)))+'.zip'
    else:
        ftp.delete(path1+'/1cv7_0.zip')
        ftp.rename(path1+'/1cv7_1.zip',path1+'/1cv7_0.zip')
        ftp.rename(path1+'/1cv7_2.zip',path1+'/1cv7_1.zip')
        path1 += '/1cv7_'+str(len(ftp.nlst(path1)))+'.zip'
    #+'/1cv7.zip'
    try:
        file = open(path0,'rb')
        log.write('Starting uploading file\n')
    except:
        log.write('Can\'t open file '+path0+'\n')
    try:
        log.write(ftp.storbinary('STOR '+path1,file))
        log.write('File has been successfully uploaded\n\n\n')
    except:
        log.write('File hasn\'t been uploaded\n')
    file.close()

def logOff(ftp):
    log = open(path_to_log,'rb')
    ftp.storlines('STOR '+folders[4]+'/log.txt',log)
    log.close()
    ftp.quit()

parse()
parseTk()

initMenu()
log = openLog(path_to_log)
ftp = logIn(log)
for i in bases:
    createCFG(path_to_cfg, log, i)
    time0 = zippedBaseTime(path_to_base_zipped[i],log)
    Open1c(i,log)
    if updatedFile(path_to_base_zipped[i],time0,log) and checkForZip(path_to_base_zipped[i],log):
        uploadFile(ftp,path_to_base_zipped[i],folders[i+1],log)


tk2 = Tkinter.Tk()
frame = Tkinter.Frame(tk2, relief=RIDGE)
frame.pack(fill=BOTH,expand=1)
label = Tkinter.Label(frame, text=Tk_phrase[9])
label.pack(fill=X, expand=1)
button_OK = Tkinter.Button(frame,text='OK',command=tk2.destroy)
button_OK.pack(side=BOTTOM)
tk2.mainloop()

closeLog(log)
logOff(ftp)