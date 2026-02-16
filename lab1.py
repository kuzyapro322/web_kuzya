from flask import Blueprint, url_for, request, redirect
from datetime import datetime

lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1/")
def lab():
    title_page = url_for('title_page')
    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Лабораторная 1</title>
</head>
<body>
    <main>
        <p>Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов
        веб-приложений, сознательно предоставляющих лишь самые ба-
        зовые возможности.</p>

        <br><a href="''' + title_page + '''">Назад в главное меню</a>

        <h2>Список роутов</h2>

        <ul>
            <li><a href="/lab1/web">/lab1/web</a></li>
            <li><a href="/lab1/author">/lab1/author</a></li>
            <li><a href="/lab1/image">/lab1/image</a></li>
            <li><a href="/lab1/counter">/lab1/counter</a></li>
            <li><a href="/lab1/counter/clear">/lab1/counter/clear</a></li>
            <li><a href="/lab1/info">/lab1/info</a></li>
            <li><a href="/lab1/create">/lab1/create</a></li>
            <li><a href="/lab1/400">/lab1/400</a></li>
            <li><a href="/lab1/401">/lab1/401</a></li>
            <li><a href="/lab1/402">/lab1/402</a></li>
            <li><a href="/lab1/403">/lab1/403</a></li>
            <li><a href="/lab1/405">/lab1/405</a></li>
            <li><a href="/lab1/418">/lab1/418</a></li>
            <li><a href="/lab1/500">/lab1/500</a></li>
            <li><a href="/lab1/aboba">Несуществующая страница</a></li>
        </ul>

    </main>
</body>
</html>
'''


@lab1.route("/lab1/web")
def start():
    return"""<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
           </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }


@lab1.route("/lab1/author")
def author():

    name = "Кузнецов Кирилл Сергеевич"
    group = "ФБИ-34"
    faculty = "ФБ"

    return"""<!doctype html>
        <html>
           <body>
               <p>Студент: """ + name + """</p>
               <p>Группа: """ + group + """</p>
               <p>Факультет: """ + faculty + """</p>
           </body>
        </html>"""


@lab1.route("/lab1/image")
def image():

    path = url_for("static", filename = "lab1/oak.jpg")
    style = url_for("static", filename = "lab1/lab1.css")

    return'''<!doctype html>
        <html>
           <head>
               <link rel="stylesheet" href="''' + style + '''">
           </head>
           <body>
               <h1>Дуб</h1>
                <img src="''' + path + '''">
           </body>
        </html>''', 200, {
            'Content-Language': 'ru',
            'X-Img-Name': 'oak',
            'X-Hotel': 'Trivago'
        }

count = 0

@lab1.route("/lab1/counter")
def counter():
    global count
    time = datetime.today()
    url = request.url
    client_ip = request.remote_addr
    counter_clear_route = url_for('lab1.clear_counter')

    count += 1

    return'''
<!doctype html>
    <html>
        <body>
            Сколько раз вы сюда заходили: ''' + str(count) + '''
            <hr>
            Дата и время: ''' + str(time) + '''
            <br> Запрошенный адрес: ''' + url + '''
            <br> Ваш IP адрес: ''' + client_ip + '''
            <br><a href="''' +  counter_clear_route + '''">Обнулить счетчик</a>
        </body>
    </html>
'''


@lab1.route("/lab1/counter/clear")
def clear_counter():
    global count
    count = 0

    return redirect("/lab1/counter")


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/create")
def created():
    return'''
<!doctype html>
    <html>
        <body>
            <h1>Создано успешно!</h1>
            <div><i>Что-то создано...</i></div>
        </body>
    </html>
''', 201


@lab1.route("/lab1/400")
def error_400():
    return "Некорректный запрос", 400


@lab1.route("/lab1/401")
def error_401():
    return "Пользователь не авторизован", 401


@lab1.route("/lab1/402")
def error_402():
    return "Необходима оплата", 402


@lab1.route("/lab1/403")
def error_403():
    return "Доступ закрыт", 403


@lab1.route("/lab1/405")
def error_405():
    return "Метод не поддерживается", 405


@lab1.route("/lab1/418")
def error_418():
    return "Я чайник :D", 418


@lab1.route("/lab1/500")
def error_500():

    a = 0
    b = 100

    return b/a
