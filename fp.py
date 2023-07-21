from flask import request
import os
import sys
import requests

# From where the program run
# For Windows bellow:
# sys_direcrory = f'{sys.path[0]}\\app'
# noticefolder = f'{sys_direcrory}\\static\\notice\\'
#For Linux bellow also work on Windows:
sys_direcrory = f'{sys.path[0]}/app'
noticefolder = f'{sys_direcrory}/static/notice/'
def ipaddr():
    ip_addr1 = request.remote_addr
    ip_addr2 = request.environ['REMOTE_ADDR']
    ip_addr3 = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    ip_addr = [ip_addr1, ip_addr2, ip_addr3]
    return ip_addr


def noticefile():
    # Select proper path that contain file of notice
    # For Windows bellow:
    # dir = f"{sys_direcrory}\\static\\notice\\"
    # For Linux bellow:
    dir = f"{sys_direcrory}/static/notice/"
    flist = os.listdir(dir)
    # for x, file in enumerate(flist):
    #     flist[x]=flist[x].strip(".pdf")
    c = 0
    pdflist = []
    # for new list create that contain .pdf file
    for file in flist:
        if '.pdf' in file:
            pdflist.append(file)
    # For remove specific matching word(.pdf) fromm a list elements
    pdflist.sort(key=lambda x: os.path.getmtime('{}{}'.format(noticefolder,x)), reverse=True)
    for x in range(len(pdflist)):
        pdflist[x] = pdflist[x].strip(".pdf")

    return pdflist


def introduction(filename):
    # For Windows bellow:
    # f = open(f"{sys_direcrory}\\static\\images\\testfile.txt","r", encoding="utf-8")
    # For Linux bellow:
    f = open(f"{noticefolder}{filename}","r", encoding="utf-8")
    content = f.read()
    f.close()   
    return content 

def get_location(ip_addr):
    response = requests.get(f'http://ipwho.is/{ip_addr}').json()
    location_data = {
        "org": response["connection"]["org"],
        "isp": response["connection"]["isp"],
        "city": response["city"]  
    }
    return location_data
    

