import requests
import random
from datetime import date
from bs4 import BeautifulSoup
from checklib import *


PORT = 9000
pirate = ['Davey','Vex','Wade','Skully','Jagger','Slyvester','Van','Chipper','Gary','Shark']


class CheckMachine:

    def __init__(self, checker):
        self.checker = checker

    def ping(self):
        r = requests.get(f'http://{self.checker.host}:{PORT}', timeout=3)
        self.checker.check_response(r, 'Check failed')

    def put_flag(self, flag, vuln):
        ipteam = self.checker.host.split(".")
        nteam = int(ipteam[2])
        if nteam > 9: nteam = 0
        n = random.randint(0, 9)
        rdata = {"name_field":pirate[n], "rank_field":"young", "login_field":pirate[n]+"-"+rnd_string(5), "password_field":rnd_string(12), "passport_field":flag, "email_field":pirate[n]+"-"+rnd_string(3)+"@corsair.team"}
        url = f'http://{self.checker.host}:{PORT}/addPirate'
        #print(url)
        r = requests.post(url, data=rdata, timeout=3)
        self.checker.check_response(r, 'Could not put flag')
        return r.text

    def get_flag(self, flag_id, vuln):
        ipteam = self.checker.host.split(".")
        nteam = int(ipteam[2])
        if nteam > 9: nteam = 0
        url = f'http://{self.checker.host}:{PORT}/getPassportFromMarque'
        rdata = {"marque_field":flag_id}
        #print(url)
        r = requests.post(url, data=rdata, timeout=3)
        #print(r.status_code)
        self.checker.check_response(r, 'Could not get flag')
        rflag = self.checker.get_text(r, 'Could not get flag /get_text/')
        return rflag
