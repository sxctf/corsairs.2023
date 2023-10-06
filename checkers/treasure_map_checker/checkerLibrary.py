import requests
from checklib import *

PORT = 4000
creds = [
    ['Trinity', 'NzIyNzQzMTIy'],
    ['Morpheus', 'NjIwZjRjZmU3'],
    ['Cyberpunk', 'ZjU0NTg2MTc1'],
    ['Shadowrun', 'NzQ1YjE0NzQz'],
    ['Technomancer', 'Yzg2ZGZkMjg0'],
    ['DeusEx', 'YjRlNjkwYjE4'],
    ['BladeRunner', 'YTQ1YmFmYTRk'],
    ['GhostInTheShell', 'MjRmNjk1ZjUw'],
    ['Akira', 'ZjA5ZjU5MzYw'],
    ['Cipher', 'Njg0ZmQyYmY0'],
    ['ZeroCool', 'ZTg3MmEyODU5'],
    ['Raven', 'YzQ3NWM4YjUx'],
    ['CyberSlicer', 'MmU5YmZlZTJm'],
    ['NeonByte', 'ZmM0ZmNkYzU1'],
    ['TechnoGeek', 'NjUwYjg4ZjQw'],
    ['Synthwave', 'YzBhZmEwYzBj'],
    ['ShadowWalker', 'NmJkZjllNGE1'],
    ['HackerElite', 'NzEwZTQxODA0'],
    ['Vaporwave', 'ODQ2YmE5YjI5'],
    ['CyborgNinja', 'MmRlNmQwZTg5'],
    ['ElectricDreams', 'Mzg5ZmEzZGMw'],
    ['FutureTech', 'MzYxZGI3NzUy']
]


class CheckerLibrary:
    def __init__(self, host):
        self.teamId = int(host.split(".")[2])
        self.username = creds[self.teamId][0]
        self.password = creds[self.teamId][1]
        self.host = "http://" + host

    def registration(self, username, password):
        url = f"{self.host}:{PORT}/user/create"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=data)
        if response.text == 'Пользователь успешно создан!' or response.status_code != 409 \
                or response.text == 'Пользователь с таким именем уже существует':
            return True
        else:
            return False

    def authentication(self, username, password):
        url = f"{self.host}:{PORT}/login"
        data = 'username=userPattern&password=pwdPattern'
        data = data.replace("userPattern", username)
        data = data.replace("pwdPattern", password)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        session = requests.Session()
        session.post(url, data=data, headers=headers)
        return session.cookies.get_dict()

    def get_cookie(self, username, pwd):
        if self.registration(username, pwd):
            response = self.authentication(username, pwd)
            return response['JSESSIONID']
        else:
            cquit(Status.MUMBLE, 'Service not working correctly',
                  'Service not working correctly in registration')

    def put_flag(self, flag):
        new_id = "Yero-" + rnd_string(10)
        url = f"{self.host}:{PORT}/container/save"
        data = {"treasure": flag,
                "locationName": "Bar Orchard Ginza"}
        headers = {"Content-Type": "application/json",
                   'Cookie': "JSESSIONID=" + self.get_cookie(self.username, self.password)}
        response = requests.post(url, headers=headers, json=data)

        if response.status_code > 400:
            cquit(Status.DOWN, 'Could not connect normally',
                  'Could not connect normally in put_flag')
        elif response.status_code != 200:
            cquit(Status.MUMBLE, 'Service not working correctly',
                  'Service not working correctly in put_flag')

        return new_id

    def get_flag(self, flag):
        url = f"{self.host}:{PORT}/location/data/Bar%20Orchard%20Ginza"
        headers = {"Content-Type": "application/json",
                   'Cookie': "JSESSIONID=" + self.get_cookie(self.username, self.password)}
        response = requests.get(url, headers=headers)

        if flag in str(response.content):
            cquit(Status.OK)
        elif response.status_code > 499:
            cquit(Status.DOWN, 'Could not connect normally',
                  'Could not connect normally in get_flag')
        else:
            cquit(Status.MUMBLE, 'Service not working correctly',
                  'Service not working correctly in get_flag')
        return flag

    def ping(self):
        if requests.get(f"{self.host}:{PORT}").status_code == 200:
            cquit(Status.OK)
        else:
            cquit(Status.DOWN, 'Could not connect normally',
                  'Could not connect normally in ping')
