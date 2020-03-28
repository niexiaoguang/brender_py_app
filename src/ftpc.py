import os
import ftplib
from ftplib import FTP


def ftp_connect(host, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp

def download_file(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)
    fp.close()


def upload_file(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')

    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()

def conn():
    print('start connecting')
    ftp = FTP()

    ftp.connect('ftp.brender.cn',22121)
    ftp.login('user','12345')
    print(ftp.getwelcome())

    # files = []
    # ftp.dir(files.append)
    # print(files)
    # with ftplib.FTP('182.92.200.86',22121) as ftp:
    #     print('connecting')
    #     try:
    #         ftp.login('user','12345')  

    #         files = []

    #         ftp.dir(files.append)

    #         print(files)
                
    #     except ftplib.all_errors as e:
    #         print('FTP error:', e)

conn()