import requests
import random
from bs4 import BeautifulSoup
from checklib import *

PORT = 5000


weapon_name = ['DIVIDED WE STAND','PROTOTYPE SHINGEN MARK V','HJKE-11 YUKIMURA','D5 SIDEWINDER','COMRADES HAMMER','NEKOMATA','KATANA', 'COCKTAIL STICK']
firmware_name = ['Big Sur', 'Monterey', 'Ventura', 'Innsbruck', 'PeaceSecYukonC','Merlot','Jazz']
device_type = ['BIODYNE BERSERK','BIONIC JOINTS','BIOCONDUCTOR','ADRENALINE BOOSTER','BLOOD PUMP','MEMORY BOOST','MECHATRONIC CORE','SELF-ICE','VISUAL CORTEX SUPPORT','METABOLIC EDITOR','PAIN EDITOR','SHOCK-N-AWE','LYNX PAWS','REINFORCED TENDONS']


class CheckMachine:

    def __init__(self, checker):
        self.checker = checker

    def ping(self):
        r = requests.get(f'http://{self.checker.host}:{PORT}/', timeout=3)
        #r1 = requests.get(f'http://{self.checker.host}:{PORT}/noopen', timeout=3)
        self.checker.check_response(r, 'Check failed')
        #self.checker.check_response(r1, 'Check failed')

    def put_flag(self, flag_id, flag, vuln):
        if int(vuln) == 1: 
            n = random.randint(0, 7)
            rdata = {"weapon_name":weapon_name[n],  
                    "serial_number":flag,
                    'button_to_update':''}
            url = f'http://{self.checker.host}:{PORT}/dblogin'
            r = requests.post(url, data=rdata, timeout=3)
            self.checker.check_response(r, 'Could not put flag')
            soup = BeautifulSoup(r.text, 'html.parser')
            new_id = soup.text[35:]
            if len(new_id) <  29:
                self.checker.cquit(Status.MUMBLE, 'Services not working correctly', 'Services not working correctly in put_flag')
            return new_id
        
        if int(vuln) == 2:
            d = random.randint(0, 13)
            ram = random.randint(0, 9999)
            f = random.randint(0, 6)
            rdata = {"firmware_name":firmware_name[f],
                     "version": flag,
                     "device":device_type[d],
                     "ram": ram,
                     "button_to_update2":''
            }
            url = f'http://{self.checker.host}:{PORT}/dblogin2'
            r = requests.post(url, data=rdata, timeout=3)
            self.checker.check_response(r, 'Could not put flag')
            soup = BeautifulSoup(r.text, 'html.parser')
            new_id = soup.text[32:]
            if len(new_id) < 30:
                self.checker.cquit(Status.MUMBLE, 'Services not working correctly', 'Services not working correctly in put_flag')
            return new_id


    def get_flag(self, flag_id, vuln):
        if int(vuln) == 1: 
            url = f'http://{self.checker.host}:{PORT}/dblogin'
            rdata = { "fn_check":flag_id,
                     'button_to_check':'' }
            try:
                r = requests.post(url, data=rdata, timeout=3)
                self.checker.check_response(r, 'Could not get flag')
                soup = BeautifulSoup(r.text, 'html.parser')    
                flag = str(soup.find(id='3'))
                return flag[60:-5]
            except IOError as e:
                self.checker.cquit(Status.MUMBLE, 'Services not working correctly', 'Services not working correctly in get_flag')
            
        
        if int(vuln) == 2: 
            url = f'http://{self.checker.host}:{PORT}/dblogin2'
            rdata = { "bios_check":f"{flag_id}",
                     'button_to_check2':'' }
            try:
                r = requests.post(url, data=rdata, timeout=3)
                self.checker.check_response(r, 'Could not get flag')
                soup = BeautifulSoup(r.text, 'html.parser')    
                flag = str(soup.find(id='2'))
                return flag[60:-5]
            except IOError as e:
                self.checker.cquit(Status.MUMBLE, 'Services not working correctly', 'Services not working correctly in get_flag')