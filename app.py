from flask import Flask, url_for, request
from datetime import datetime
import os

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7


app=Flask(__name__)

app.config['SECRET_KEY']=os.environ.get('SECRET_KEY', 'Секретно-секретный-секрет')
app.config['DB_TYPE']=os.getenv('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)


@app.route("/")
def title_page():

    lab1_url = url_for("lab1.lab")
    lab2_url = url_for("lab2.lab")
    lab3_url = url_for("lab3.lab")
    lab4_url = url_for("lab4.lab")
    lab5_url = url_for("lab5.lab")
    lab6_url = url_for("lab6.lab")
    lab7_url = url_for("lab7.lab")


    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>НГТУ, ФБ, Лабораторные работы</title>
</head>
<body>
    <header>
        НГТУ, ФБ, WEB-программирование часть 2
        <hr>
    </header>
    <main>
        <h1>Лабораторные работы по WEB-программированию</h1>

        <div class="menu"> 
            <ul>
                <li><a href="''' + lab1_url + '''">Лабораторная работа #1</a></li>
                <li><a href="''' + lab2_url + '''">Лабораторная работа #2</a></li>
                <li><a href="''' + lab3_url + '''">Лабораторная работа #3</a></li>
                <li><a href="''' + lab4_url + '''">Лабораторная работа #4</a></li>
                <li><a href="''' + lab5_url + '''">Лабораторная работа #5</a></li>
                <li><a href="''' + lab6_url + '''">Лабораторная работа #6</a></li>
                <li><a href="''' + lab7_url + '''">Лабораторная работа #7</a></li>
            </ul>
        </div>
    </main>
    <footer>
        <hr>
        &copy;Саморуков Никита, ФБИ-34, 3 курс, 2025
    </footer>
</body>
</html>
'''

logger = []

@app.errorhandler(404)
def not_found(err):
    global logger
    now = datetime.today()
    logger.append(f"[{now.strftime("%Y-%m-%d %H:%M:%S")} пользователь {request.remote_addr}] перешел по адресу: {request.url}")
    logs = ""
    for i in logger:
        log = f"<li>{i}</li> "
        logs += log
    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ошибка 404</title>
    <style>
        h1, h2 {
            font-size: 200px;
            color: violet;
            text-shadow: 5px 5px 10px purple;
            text-align: center;
            margin-bottom: 0;
            margin-top: 60px;
            animation: float 3s ease-in-out infinite;
        }

         h2 {
            font-size: 40px;
            text-shadow: none;
        }
        ul {
            list-style-type: none;
        }
        div.logger {
            position: fixed;
            bottom: 0px;
            left: 0px;
            color: green;
        }
    
        @keyframes float {
        0%   { transform: translateY(0px); }
        50%  { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
        }

    </style>
</head>
<body>
    <main>
        <h1>404</h1>
        <h2>Страница по запрашиваемому адресу не найдена</h2>
        <div class="logger">
            <ul>
                ''' + logs + '''
            </ul>
        </div>
    </main>
</body>
</html>
'''


@app.errorhandler(500)
def not_found(err):
    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ошибка 500</title>
    <style>
        h1, h2 {
            font-size: 200px;
            color: grey;
            text-shadow: 5px 5px 10px black;
            text-align: center;
            margin-bottom: 0;
            margin-top: 60px;
        }

         h2 {
            font-size: 40px;
            text-shadow: none;
        }

    </style>
</head>
<body>
    <main>
        <h1>500</h1>
        <h2>Внутренняя ошибка сервера</h2>
    </main>
</body>
</html>
'''


