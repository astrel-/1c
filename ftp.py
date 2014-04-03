import ftplib


def logIn(log):
    """
        logs in to FTP server
        creates a directory, if not created
        goes to this directory
        returns ftp
        """
    ftp = ftplib.FTP()
    ftp.connect('khodzha.com', 21)
    log.write (ftp.getwelcome()+'\n')
    try:
        log.write ('Logging in...\n')
        ftp.login('astrel', 'astrel')
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

ftp = ftplib.FTP()
ftp.connect('khodzha.com', 21)
print ftp.getwelcome()
ftp.login('astrel', 'astrel')
ftp.set_pasv(True)
ftp.mkd('test2')
file = open('info.txt','rb')
ftp.storbinary('STOR test2/info.txt',file)
file.close()
ftp.quit()





