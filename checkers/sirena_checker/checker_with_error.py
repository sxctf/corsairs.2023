from bs4 import BeautifulSoup
from time import sleep
import requests
import random
import string

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
        f"напиши программу на языке python, которая выведет содержимое файла с именем './secrets/{flag_id}.txt', без использования pathlib"
    ]

    return get_query[random.randrange(len(get_query))]


class CheckMachine:

    def __init__(self, checker):
        self.checker = checker

    def ping(self):
        r = requests.get(f'http://{self.checker.host}:{PORT}/do', timeout=2)
        self.checker.check_response(r, 'Check failed')
        r = requests.get(f'http://{self.checker.host}:{PORT}/ask', timeout=2)
        self.checker.check_response(r, 'Check failed')

    def put_flag(self, flag, vuln, try_n):
        new_id = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(32))
        query = getPutQuery(new_id, flag)
        data = {'task': query}
        print(data)
        sleep(1)
        r = requests.post(
            f'http://{self.checker.host}:{PORT}/{URL}',
            data=data,
            timeout=10,
        )
        if r.status_code != 200 and try_n < MAX_TRIES:
            return self.put_flag(flag, vuln, try_n + 1)
        else:
            self.checker.check_response(r, 'Could not put flag')
            return new_id

    def get_flag(self, flag_id, true_flag, try_n):
        query = getGetQuery(flag_id)
        data = {'task': query}
        sleep(1)
        r = requests.post(
            f'http://{self.checker.host}:{PORT}/{URL}',
            data=data,
            timeout=10,
        )
        self.checker.check_response(r, 'Could not get flag')
        data = BeautifulSoup(r.content.decode("utf-8"), 'html.parser')
        data = data.find_all('p')

        if len(data) > 0:
            data = str(data[-1])

            if len(data) > 7:
                flag = data[3 : -4]
                flag = flag.replace('\n', '')

                if flag != true_flag:
                    flag = "False"
            else:
                flag = "False"
        else:
            flag = "False"

        if flag == "False" and try_n < MAX_TRIES:
            flag = self.get_flag(flag_id, true_flag, try_n + 1)
        
        return flag
