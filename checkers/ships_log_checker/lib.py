import requests
import random
from datetime import date
from bs4 import BeautifulSoup
from checklib import *


PORT = 8080
location = ['Night_City','Watson','Westbrook','Outskirts','Heywood','Pacifica','Santo_Domingo']


class CheckMachine:

    def __init__(self, checker):
        self.checker = checker

    def ping(self):
        r = requests.get(f'http://{self.checker.host}:{PORT}', timeout=3)
        self.checker.check_response(r, 'Check failed')

    def put_flag(self, flag, vuln):
        new_id = "flag_id"
        ipteam = self.checker.host.split(".")
        nteam = int(ipteam[2])
        if nteam > 9: nteam = 0
        n = random.randint(0, len(location)-1)
        ddate = date.fromisoformat("2077-09-19")
        rdata = {"name":rnd_string(12), "destination":location[n], "description":flag, "date":ddate, "status":"Planned"}
        url = f'http://{self.checker.host}:{PORT}/add'
        #print(url)
        r = requests.post(url, data=rdata, timeout=3)
        self.checker.check_response(r, 'Could not put flag')
        data = self.checker.get_text(r, 'Invalid response from /put/')
        sp = BeautifulSoup(data, features="html.parser")
        th3 = sp.find_all('h3')
        #print(len(th3))
        for row in th3:
            if len(row) > 0:
                str0 = row.text.strip()
                if str0.find("Your access code is") != -1:
                    #print(str0)
                    str1 = str0.split(" ")
                    new_id = str1[4]
        return new_id

    def get_flag(self, flag_id, vuln):
        rflag = "NotFlag"
        ipteam = self.checker.host.split(".")
        nteam = int(ipteam[2])
        if nteam > 9: nteam = 0
        url = f'http://{self.checker.host}:{PORT}/checkCode'
        rdata = {"verificationCode":flag_id}
        #print(url)
        r = requests.post(url, data=rdata, timeout=3)
        #print(r.status_code)
        if r.status_code != 200:
            self.checker.cquit(Status.MUMBLE, 'Services not working correctly', 'Services not working correctly in get_flag')
        data = self.checker.get_text(r, 'Invalid response from /get/')
        sp = BeautifulSoup(data, features="html.parser")
        #tables = sp.find_all('table')
        table = sp.find('table', border="1px")
        if table:
            for row in table.find_all('tr'):
                columns = row.find_all('td')
                if(columns != []):
                    #print("TD=" + columns[2].text.strip())
                    if columns[6].text.strip() == flag_id:
                        rflag = columns[3].text.strip()
        return rflag
