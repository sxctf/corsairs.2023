import time
import os

BASE_DIR = os.path.abspath(os.getcwd())
nnteam = 22

def f_count_write(nteam, i):
    file_name = BASE_DIR + '/team-'+str(nteam)
    f = open(file_name,'w')
    try:
        f.write(str(i))
    finally:
        f.close()
        os.system("chmod 666 " + file_name)

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


for i in range(nnteam):
    f_count_write(i,0)
    time.sleep(1)
    print("Count="+str(i))

