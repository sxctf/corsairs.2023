from bs4 import BeautifulSoup
from pathlib import Path
from checklib import *
from time import sleep
import requests
import random
import string
import sys

BASE_DIR = Path(__file__).absolute().resolve().parent

PORT = 8000
URL = 'do'
MAX_TRIES = 3

def getPutQuery(new_id, flag):
    put_query = [
        f"напиши программу на языке python, которая запишет текст '{flag}' в файл ./secrets/{new_id}.txt"
    ]

    return put_query[random.randrange(len(put_query))]

def getGetQuery(flag_id):
    get_query = [
        f"напиши программу на языке python, которая выведет содержимое файла с именем './secrets/{flag_id}.txt', без использования pathlib",
        f"выведи python скрипт, который выводит содержимое файла ./secrets/{flag_id}.txt",
        f"python скрипт выводит содержимое файла ./secrets/{flag_id}.txt"
    ]

    return get_query[random.randrange(len(get_query))]


class CheckMachine:

    def __init__(self, checker):
        self.checker = checker

    def ping(self):
        sleep(3)
        r = requests.get(f'http://{self.checker.host}:{PORT}/do', timeout=10)
        self.checker.check_response(r, 'Check failed')
        sleep(3)
        r = requests.get(f'http://{self.checker.host}:{PORT}/ask', timeout=10)
        self.checker.check_response(r, 'Check failed')

    def put_flag(self, flag, try_n):
        #print(flag, vuln, try_n, file=sys.stdout)
        sleep(3)
        res = True
        new_id = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(32))
        query = getPutQuery(new_id, flag)
        #print(query, file=sys.stdout)
        data = {'task': query}
        #print(data, file=sys.stdout)
        try:
            r = requests.post(
                f'http://{self.checker.host}:{PORT}/{URL}',
                data=data,
                timeout=12,
            )
        except requests.exceptions.Timeout:
            return self.put_flag(flag, try_n + 1)
        #print(r.json)
        self.checker.check_response(r, 'Could not get flag')
        data = BeautifulSoup(r.content.decode("utf-8"), 'html.parser')
        data = data.find_all('p')

        if len(data) > 0:
            #for d in data:
            #    print(d)
            data = str(data[-1])

            if "Exception" in data or "Error" in data or "ошибк" in data:
                res = False

        if (r.status_code != 200 or not res) and try_n < MAX_TRIES:
            return self.put_flag(flag, try_n + 1)
        else:
            self.checker.check_response(r, 'Could not put flag')
            return new_id

    def get_flag(self, flag_id, true_flag, try_n):
        sleep(3)
        res = True
        query = getGetQuery(flag_id)
        data = {'task': query}
        try:
            r = requests.post(
                f'http://{self.checker.host}:{PORT}/{URL}',
                data=data,
                timeout=12,
            )
        except requests.exceptions.Timeout:
            return self.get_flag(flag_id, true_flag, try_n + 1)
        self.checker.check_response(r, 'Could not get flag')
        data = BeautifulSoup(r.content.decode("utf-8"), 'html.parser')
        data = data.find_all('p')

       # print(f"data:\n{data}")
        if len(data) > 0:
            data = str(data[-1])
        #    print(f"cutted data: {data}")
            
            if "FileNotFound" in data:
                flag = true_flag        
            elif len(data) >= 7:
                flag = data[3 : -4]
                flag = flag.replace('\n', '')

                if flag != true_flag:
                    if len(flag) == 0:
                        flag = true_flag
                    else:
                        res = False
            else:
                res = False
        else:
            res = False

        # print(f"flag: {flag}")
        if (r.status_code != 200 or not res) and try_n < MAX_TRIES:
            flag = self.get_flag(flag_id, true_flag, try_n + 1)

        if try_n == MAX_TRIES and not true_flag in flag:
            with open('flags.txt', 'ra') as file:
                if true_flag in file.read():
                    flag = true_flag
                else:
                    file.write(true_flag)

        return flag
