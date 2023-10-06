import requests
import json
from datetime import datetime
from http import HTTPStatus
from flask import Flask, request, jsonify, render_template, render_template_string
import subprocess
import logging

app = Flask(__name__)

giga_url = "http://10.61.0.11:8989/ask"

@app.route('/', methods=['GET'])
def home():
	real_ip = None
	if "X-Real-IP" in request.headers:
		real_ip = request.headers.get("X-Real-IP")
	else:
		real_ip = request.remote_addr

	app.logger.info(f"from {real_ip} req / [Siren.py][ask][OK] {request.method} {request.headers} {request.get_data()}")

	return render_template('home.html')

@app.route('/ask', methods=['GET', 'POST'])
def ask():
	real_ip = None
	if "X-Real-IP" in request.headers:
		real_ip = request.headers.get("X-Real-IP")
	else:
		real_ip = request.remote_addr

	app.logger.info(f"from {real_ip} req /ask [Siren.py][ask][OK] {request.method} {request.headers} {request.get_data()}")

	if request.method == 'GET':
		return render_template('ask.html')
	elif request.method == 'POST':
		question = request.form.get('question')

		app.logger.info(f'User query: {question}')

		req = {"question": question}
		data = json.dumps(req, ensure_ascii=False).encode('utf-8')
		headers = {"Content-Type": "application/json"}
		res = requests.post(url=giga_url, data=data, headers=headers)
		answer = ""

		if res.status_code != HTTPStatus.OK:
			answer = "Error code: " + str(res.status_code)
		else:
			jRes = res.json()
			if not 'ans' in jRes:
				app.logger.error(f"from {real_ip} req /ask [Siren.py][ask][ERROR] Некорректный ответ от gigachat-client {res.status_code} {res.text}")
				answer = "В ответе нет поля 'ans'"
			if not 'res' in jRes:
				app.logger.error(f"from {real_ip} req /ask [Siren.py][ask][ERROR] Некорректный ответ от gigachat-client {res.status_code} {res.text}")
				answer = "В ответе нет поля 'res'"
			if 'OK' != jRes['res']:
				app.logger.error(f"from {real_ip} req /ask [Siren.py][ask][ERROR] Некорректный ответ от gigachat-client {res.status_code} {res.text}")
				answer = jRes['res']
			else:
				app.logger.info(f"from {real_ip} req /ask [Siren.py][ask][OK] {res.status_code} {res.text}")
				answer = jRes['ans']
		return render_template_string(answer)

@app.route('/do', methods=['GET', 'POST'])
def do():
	real_ip = None
	if "X-Real-IP" in request.headers:
		real_ip = request.headers.get("X-Real-IP")
	else:
		real_ip = request.remote_addr

	app.logger.info(f"from {real_ip} req /ask [Siren.py][ask][OK] {request.method} {request.headers} {request.get_data()}")

	if request.method == 'GET':
		return render_template('do.html')
	elif request.method == 'POST':
		question = request.form.get('task')

		app.logger.info(f'User query: {question}')

		req = {"question": question}
		data = json.dumps(req, ensure_ascii=False).encode('utf-8')
		headers = {"Content-Type": "application/json"}
		res = requests.post(url=giga_url, data=data, headers=headers)
		answer = ""
		code = ""
		result = ""

		if res.status_code != HTTPStatus.OK:
			app.logger.error(f"from {real_ip} req /do [Siren.py][do][ERROR] Ошибка от gigachat-client {res.status_code} {res.text}")
			answer = "Ошибка при запросе к Гигачат: " + str(res.status_code)
		else:
			jRes = res.json()
			if not 'ans' in jRes:
				answer = "В ответе нет поля 'ans'"
				app.logger.error(f"from {real_ip} req /do [Siren.py][do][ERROR] Некорректный ответ от gigachat-client {res.status_code} {res.text}")
			if not 'code' in jRes:
				answer = "В ответе нет поля 'code'"
				app.logger.error(f"from {real_ip} req /do [Siren.py][do][ERROR] Некорректный ответ от gigachat-client {res.status_code} {res.text}")
			if not 'res' in jRes:
				answer = "В ответе нет поля 'res'"
				app.logger.error(f"from {real_ip} req /do [Siren.py][do][ERROR] Некорректный ответ от gigachat-client {res.status_code} {res.text}")
			if 'OK' != jRes['res']:
				answer = jRes['res']
				app.logger.error(f"from {real_ip} req /do [Siren.py][do][ERROR] Некорректный ответ от gigachat-client {res.status_code} {res.text}")
			else:
				answer = jRes['ans']
				code = jRes['code']
				app.logger.info(f"from {real_ip} req /do [Siren.py][do][OK] {res.status_code} {res.text}")
				result = run_task(code)
				app.logger.info(f"from {real_ip} req /do [Siren.py][do][OK] Результат запуска программы: {result}")
		return render_template('do-result.html', answer=answer, code=code, result=result)

def run_task(task):
	res = None

	with open('task.py', 'w') as file:
		file.write(task)
	try:
		res = subprocess.check_output(['python', 'task.py'], stderr=subprocess.STDOUT)
		res = res.decode('utf-8')
		app.logger.info(res)
	except subprocess.CalledProcessError as e:
		app.logger.info("Мы в CalledProcessError")
		output = ""
		if not e.output is None:
			output += f"Exception output: {e.output.decode('utf-8')}\n"
		if not e.stdout is None:
			output += f"stdout: {e.stdout.decode('utf-8')}\n"
		if not e.stderr is None:
			output += f"stderr: {e.stderr.decode('utf-8')}\n"
		res = f"Выполнение задачи завершилось с ошибкой: {e.returncode}\n{output}"
	except KeyboardInterrupt:
		raise
	except Exception as e:
		res = f"Выполнение задачи завершилось с неизвестной ошибкой: {e.output}"

	return res

if __name__ == '__main__':
	logging.basicConfig(filename='./logs/siren.log',level=logging.DEBUG, format="[%(asctime)s][%(levelname)s] %(message)s")
	app.run(host='0.0.0.0', port=2345)