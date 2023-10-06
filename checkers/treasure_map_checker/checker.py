#!/usr/bin/env python3

import sys

import requests
from checklib import *

from checkerLibrary import CheckerLibrary

PORT = 4000
class Checker(BaseChecker):
    def __init__(self, host: str):
        super().__init__(host)
        self.host = host
        self.CheckerLibrary = CheckerLibrary(host)

    def action(self, action, *args, **kwargs):
        try:
            super().action(action, *args, **kwargs)
        except requests.exceptions.ConnectionError:
            self.cquit(Status.DOWN, 'Connection error', 'Got requests connection error')

    def check(self):
        self.CheckerLibrary.ping()
        self.cquit(Status.OK)

    def put(self, flag_id, flag, vuln):
        new_id = self.CheckerLibrary.put_flag(flag)
        self.cquit(Status.OK, new_id)

    def get(self, flag_id, flag, vuln):
        self.CheckerLibrary.get_flag(flag)
        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])
    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
