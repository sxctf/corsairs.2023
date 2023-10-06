import mariadb, random, string, os, subprocess, urllib.parse
from flask import Flask, render_template, has_request_context, request, redirect #url_for, flash
import logging
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
from pymongo import MongoClient
from datetime import datetime

#For logs
class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None
        return super().format(record)

formatter = RequestFormatter('[%(asctime)s] [%(levelname)s] from %(remote_addr)s req: %(url)s > %(message)s')

weapon_counter = 0
UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
connection_string = 'mongodb://ctf:try_hack_me@172.30.0.4:27017/ctf_db'
client = MongoClient(connection_string)

app = Flask(__name__)
file_log = os.path.abspath(os.getcwd()) + "/log/OKO_Events.log"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(file_log, maxBytes=1048576, backupCount=10)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def index():
    return render_template('index.html', weapon_counter=weapon_counter)


@app.route('/dblogin', methods = ['GET', 'POST'])
def interactwithdb():
    if request.method == 'GET':
        return render_template('logintodb.html')
    if request.method == 'POST':
        upd = request.form.get('button_to_update')
        auth = request.form.get('form_auth_submit')
        chk = request.form.get('button_to_check')
        

        if upd is not None:
            weapon_name = request.form['weapon_name']
            serial_number = request.form['serial_number']
            username = 'ctf'
            password = 'try_hack_me'
            factory_name = "Factory_" + generate_random_string(21)
            conn = mariadb.connect(
            user=username,
            password=password,
            host="172.30.0.3",
            port=3306,
            database='weapons'
            )
            cur = conn.cursor()
            insert_data = f'insert into ship_weapon (zavod_name, weapon_name, serial_number) values ("{factory_name}","{weapon_name}", "{serial_number}");'
            cur.execute(insert_data)
            conn.commit()
            cur.close()
            sync = os.popen('sync')
            app.logger.info('[%s] [INFO] from %s req:/dblogin [INSERT] [MARIADB] [Success] Add record: weapon name <%s> serial number <%s>', datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.remote_addr, weapon_name, serial_number)
            app.logger.error('[%s] [ERROR] from %s req:/dblogin [INSERT] [MARIADB] [Failed] Failed to add record: weapon name <%s> serial number <%s>', datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.remote_addr, weapon_name, serial_number)    
            global weapon_counter
            weapon_counter += 1
            return (f'Please check it with Factory_name: {factory_name}')
                
        
        elif auth is not None:
            login = request.form['auth_login']
            password = request.form['auth_pass']   
            conn = mariadb.connect(
                user=login,
                password=password,
                host="172.30.0.3",
                port=3306,
                database='weapons'
            )
            if conn:
                app.logger.info('[%s] [INFO] from %s [CONNECT|AUTH] [MARIADB] [Success] Authentication complete User: %s password: %s', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), request.remote_addr, login, password)
            else:
                app.logger.error('[%s] [ERROR] from %s [CONNECT|AUTH] [MARIADB] [Failed] Authentication failed User: %s password: %s', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), request.remote_addr, login, password)
            cur = conn.cursor()
            select_db = f'USE weapons;'
            cur.execute(select_db)
            show_content = f'SELECT * FROM ship_weapon;'
            cur.execute(show_content)
            elements = cur.fetchall()
            cur.close()
            return render_template ('successlogin.html', elements=elements)
            
        elif chk is not None:
            
            fn_check = request.form['fn_check']
            username = 'ctf'
            password = 'try_hack_me'
            conn = mariadb.connect(
                user=username,
                password=password,
                host="172.30.0.3",
                port=3306,
                database='weapons'
            )
            cur = conn.cursor()
            cur.execute("select * from ship_weapon where zavod_name=%(fn_check)s", {'fn_check': fn_check})
            app.logger.info('[%s] [INFO] from %s req:/dblogin [CHECK] [MARIADB] [Success] Check record: factory_name <%s> ', datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.remote_addr, fn_check)
            elements = cur.fetchall()
            cur.close()
            # app.logger.error('[%s] [ERROR] from %s req:/dblogin [CHECK] [MARIADB] [Failed] Failed to check record: factory_name <%s>', datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.remote_addr, fn_check)
            
            return render_template ('successlogin.html', elements=elements)

        
# Mongodb
@app.route('/dblogin2', methods = ['GET', 'POST'])
def interactwithdb2():

    if request.method == 'GET':
        return render_template('mongo.html')

    if request.method == 'POST':
        upd_2 = request.form.get('button_to_update2')
        chk_2 = request.form.get('button_to_check2')

    if upd_2 is not None:
        firmware_name = request.form['firmware_name']
        version = request.form['version']
        bios_name = "BIOS_name" + generate_random_string(21)
        device = request.form['device']
        ram = request.form['ram']
        record = { 
            "Firmware_name": f"{firmware_name}", 
            "Version": f"{version}",
            "Device_type" : f"{device}",
            "RAM size" : f"{ram}",
            "bios" : f"{bios_name}",
            "enabled" : f"{bool(random.getrandbits(1))}"
        }
        try:
            query = client.ctf_db.firmware.insert_one(record) 
            app.logger.info('[%s] [INFO] from %s req:/dblogin2 [INSERT] [MONGODB] [Success] Insert data to mongodb: Firmware_name <%s> Version <%s> Device_type <%s> RAM_size <%s>', datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.remote_addr, firmware_name, version, device, ram)
        except:
            app.logger.error('[%s] [ERROR] from %s req:/dblogin2 [INSERT] [MONGODB] [Failed] Failed to insert data to mongodb: Firmware_name <%s> Version <%s> Device_type <%s> RAM_size <%s>', datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.remote_addr, firmware_name, version, device, ram)
            
        return (f'Please check it with BIOS_name: {bios_name}')
        
    elif chk_2 is not None:
        bios_name = request.form['bios_check']
        query = "function () { return this.bios == '%s';}" %bios_name
        try:
            elements = client.ctf_db.firmware.find({'$where': f"{query}"})
            app.logger.info('[%s] [INFO] from %s req:/dblogin2 [CHECK] [MONGODB] [Success] Check data from mongodb: BIOS_name <%s>', datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.remote_addr, bios_name)
            elements = list(elements) 
            return render_template('successmongo.html',elements=elements, query=query)

        except IOError:
            app.logger.error('[%s] [ERROR] from %s req:/dblogin2 [CHECK] [MONGODB] [Failed] Check data from mongodb: BIOS_name <%s>', datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.remote_addr, bios_name)
            print('Uppppppps')


@app.route('/noopen', methods=['GET','POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('noopen.html')
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return redirect(request.url)
            file = request.files['file']
            
            if file.filename == '':
                return redirect(request.url)
            
            if file.filename.split('.')[1]  == 'txt':
                try:
                    content_of_file = []
                    ids = []
                    app.logger.info('[%s] [INFO] from %s req:/noopen [FILE] [UPLOAD] [Success] File: <%s>', datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.remote_addr, file)
                    with open(f'./{file.filename}', encoding='utf-8', mode='r') as f:
                        for line in f:
                            for raw in line.splitlines():
                                word = raw.split(';')
                                content_of_file.append(word)

                    for element in content_of_file:
                        bios_name = "BIOS_" + generate_random_string(21)
                        record = { 
                            "Firmware_name": f"{element[0]}", 
                            "Version": f"{element[1]}",
                            "Device_type" : f"{element[2]}",
                            "RAM size" : f"{int(element[3])}",
                            "bios" : f"{bios_name}",
                            "enabled" : f"{bool(random.getrandbits(1))}"
                            }
                    
                        query = client.ctf_db.firmware.insert_one(record)
                        ids.append(bios_name)
                    return (f'Please check it with BIOS_name: {ids}')

                except IOError as e:
                    app.logger.error('[%s] [ERROR] from %s req:/noopen [FILE] [UPLOAD] [Failed] File: <%s>', datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.remote_addr, file)

            if file is not None:
                file_b = True
                if allowed_file(file.filename) <= file_b:
                    filename = file.filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    app.logger.info('[%s] [INFO] from %s req:/noopen [FILE] [UPLOAD] [Success] File: <%s>', datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.remote_addr, file)
                    return "File Uploaded"
        except IOError as e:
            print('Oooops')
            app.logger.error('[%s] [ERROR] from %s req:/noopen [FILE] [UPLOAD] [Failed] File: <%s>', datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.remote_addr, file)


@app.route('/besteverapi', methods = ['GET'])
def start():
    try:
        query = request.args.get('query')
        if query and query != '':
            query = urllib.parse.unquote(query)
            app.logger.info('[%s] [INFO] from %s req:/besteverapi [GET] [QUERY] [Success] Payload query: <%s>', datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.remote_addr, query)
            result = subprocess.run(query.split(), stdout=subprocess.PIPE).stdout.decode('utf-8')

        return render_template('result.html',result = result)
    except:
        app.logger.error('[%s] [ERROR] from %s req:/besteverapi [GET] [QUERY] [Failed] Payload query: <%s>', datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.remote_addr, query)

if __name__ == '__main__':
    app.run(debug = False, host='0.0.0.0')
    
