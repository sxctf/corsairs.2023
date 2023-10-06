import requests
import random
from datetime import date
from bs4 import BeautifulSoup
from checklib import *
import base64
from pathlib import Path
import os


PORT = 7000
nnteam = 21
npoint = ['', '/myprofile', '/mytask', '/tasklist', '/kanban', '/userstatus']
corsair = [['Santa','uRcwJC3gvVKP'],['Dreadful','aCRLCmUJ9R39'],['Seadog','U3jqKetrstFv'],['Blackbeard','p4x4poYfWidX'],['Davey','KyjcxvVRe3ik'],['Jolly','jjFjg4UeczNX'],['Storm','7KvcqsqWYJaU'],['Booty','NkesgFq3Ujzq'],['Crabby','WdatEF7yPKEv'],['Dubloon','aVCLCf4uEuAL'],['Spike','YkwpLpH3Epyu'],['Wade','mdxrNoFUsTH9'],['Lazyjacks','Jd7FtAiTeKb7'],['Mullins','C3jU9ddbgvzC'],['Crawford','nef99ioRbPuW'],['Winters','p7MrmyHuaMTK'],['Hawk','LqNdsqzkb3Ty'],['Drake','g7Aod7HdJhwt'],['Simpson','NeaKfcXw4K9b'],['Sandy','7jJy7LJaWWqU'],['Chipper','kWgmpL4unKWo'],['Heart','XqREteNEF77K'],['Sander','4vXnUbtRtYnN']]
taskname = [['Find_treasure','Vessel_hijacking','Explore_location','Cargo_delivery'],['Vessel_repair','Deck_cleaning','Inventory','Education'],['Load_weapon','Reboot_system','Update_Firmware','Update_maps']]
BASE_DIR = Path(__file__).absolute().resolve().parent

def f_user_reg(host, i, ulogin):
    rdata = {"login":ulogin, "password":corsair[i][1], "email":""}
    url = f'http://{host}:{PORT}/reg'
    r = requests.post(url, data=rdata, timeout=2)
    #print(url)
    #print(rdata)
    #print("User_Reg %s", r.text)
    if r.status_code != 200: return False
    return True

def f_user_login(host, i, ulogin):
    s = requests.Session()
    rdata = {"login":ulogin, "password":corsair[i][1]}
    url = f'http://{host}:{PORT}/login'
    #print(url)
    r = s.post(url, data=rdata, timeout=2)
    if r.status_code != 200:
        s = False
    ustatus = r.text.find('Login or password incorrect')
    if ustatus > 0:
        s = False
    return s

def f_user_logout(host, s):
    url = f'http://{host}:{PORT}/logout'
    #print(url)
    r = s.get(url, timeout=2)
    if r.status_code != 200: return False
    return True

def f_count_write(nteam, i):
    f = open(BASE_DIR / ('team-'+str(nteam)),'w')
    try:
        f.write(str(i))
    finally:
        f.close()

def f_count_read(nteam):
    st = '0'
    fname = BASE_DIR / ('team-'+str(nteam))
    if not os.path.exists(fname):
        f_count_write(nteam, st)
    f = open(fname,'r')
    try:
        st = f.readline()
    finally:
        f.close()
    return int(st)

def f_find_il(ulogin):
    lname = ulogin.split("-")
    i = 0
    for el in corsair:
        if el[0] == lname[0]:
            return i
        i += 1
    return -1


class CheckMachine:

    def __init__(self, checker):
        self.checker = checker

    def ping(self):
        num = random.randint(0, len(npoint)-1)
        url = f'http://{self.checker.host}:{PORT}'+npoint[num]
        r = requests.get(url, timeout=5)
        #print(url)
        #print("Ping %s", r)
        self.checker.check_response(r, 'Check failed')

    def put_flag(self, flag, vuln):
        new_id = ""
        ipteam = self.checker.host.split(".")
        nteam = int(ipteam[2])
        if nteam > nnteam: nteam = 0
        count = f_count_read(nteam)
        il = random.randint(1, nnteam)
        ulogin = corsair[il][0]+"-"+str(count)
        f_count_write(nteam,count+1)
        strb1 = ulogin.encode()
        new_id = base64.b64encode(strb1).decode()
        fres = f_user_reg(self.checker.host, il, ulogin)
        if not fres:
            self.checker.cquit(Status.MUMBLE, 'Services not working correctly', 'Services not working correctly in put_flag - f_user_reg')
        s = f_user_login(self.checker.host, il, ulogin)
        if not s:
            self.checker.cquit(Status.MUMBLE, 'Services not working correctly', 'Services not working correctly in put_flag - f_user_login')
        n1 = random.randint(0, 2)
        n2 = random.randint(0, 3)
        rdata = {"title":taskname[n1][n2], "description":flag, "did":str(n1), "private":"True"}
        url = f'http://{self.checker.host}:{PORT}/taskcreate'
        #print(url)
        r = s.post(url, data=rdata, timeout=3)
        self.checker.check_response(r, 'Could not put flag')
        fres = f_user_logout(self.checker.host, s)
        if not fres:
                self.checker.cquit(Status.MUMBLE, 'Services not working correctly', 'Services not working correctly in put_flag')
        return new_id

    def get_flag(self, flag_id, flag, vuln):
        rflag = "NotFlag"
        ipteam = self.checker.host.split(".")
        nteam = int(ipteam[2])
        if nteam > nnteam: nteam = 0
        strb1 = flag_id.encode()
        ulogin = base64.b64decode(strb1).decode()
        il = f_find_il(ulogin)
        if il == -1:
            self.checker.cquit(Status.MUMBLE, 'Services not working correctly', 'Services not working correctly in get_flag - f_find_il')
        s = f_user_login(self.checker.host, il, ulogin)
        if not s:
            self.checker.cquit(Status.MUMBLE, 'Services not working correctly', 'Services not working correctly in get_flag - f_user_login')
        url = f'http://{self.checker.host}:{PORT}/mytask'
        #print(url)
        r = s.get(url, timeout=2)
        #print(r.status_code)
        if r.status_code != 200:
            self.checker.cquit(Status.MUMBLE, 'Services not working correctly', 'Services not working correctly in get_flag')
        #self.checker.check_response(r, 'Could not get flag')
        data = self.checker.get_text(r, 'Invalid response from /get/')
        sp = BeautifulSoup(data, features="html.parser")
        #tables = sp.find_all('table')
        table = sp.find('table', class_='table-dark')
        for row in table.tbody.find_all('tr'):
            columns = row.find_all('td')
            if(columns != []):
                #print("TD=" + columns[3].text.strip())
                if columns[3].text.strip() == flag:
                    rflag = columns[3].text.strip()
        fres = f_user_logout(self.checker.host, s)
        return rflag
