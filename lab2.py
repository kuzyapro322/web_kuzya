from flask import Blueprint, url_for, redirect, abort, render_template

from static.lab2.book_list import books
from static.lab2.flowers_list import flowers


lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a/')
def a_slash():
    return 'ok'


@lab2.route('/lab2/a')
def a():
    return 'ok'

flower_list = [{'name': 'роза', 'price': 400},
               {'name': 'тюльпан', 'price': 350},
               {'name': 'незабудка', 'price': 250},
               {'name': 'ромашка', 'price': 100}]

@lab2.route('/lab2/flowers/<int:flower_id>')
def flower_details(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    else:
        return render_template('lab2/flower_info.html',
                                flower=flower_list[flower_id])


@lab2.route('/lab2/add_flower/')
@lab2.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name=None, price=0):
    if name:
        flower_list.append({'name': name, 'price': price})
        return render_template('lab2/flower_result.html', name=name, price=price, flower_list=flower_list, error=False)
    else:
        return render_template('lab2/flower_result.html', message="Вы не задали имя цветка", error=True), 400


@lab2.route('/lab2/flowers')
def list_flowers():
    return render_template('lab2/flower_all.html', flower_list=flower_list)


@lab2.route('/lab2/flowers/clear')
def clear_flowers():
    flower_list.clear()
    return render_template('lab2/flower_clear.html')


@lab2.route('/lab2/flowers/delete/<int:flower_id>')
def del_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    del flower_list[flower_id]
    return redirect(url_for('lab2.list_flowers'))


@lab2.route('/lab2/example')
def example():
    name = 'Кузнецов Кирилл'
    group = 'ФБИ-34'
    lab = 2
    course = 3
    fruits = [{'name': 'яблоки', 'price': 150},
              {'name': 'персики', 'price': 250},
              {'name': 'бананы', 'price': 200}, 
              {'name': 'абрикосы', 'price': 200},
              {'name': 'манго', 'price': 300}]
    return render_template('lab2/example.html', name=name,
                                           group=group,
                                           lab=lab,
                                           course=course,
                                           fruits=fruits
                            )


@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('lab2/filter.html',
                           phrase=phrase)


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return f'''
<!doctype html>
<html>
  <body>
    <h1>Выражения</h1>
    <br> Суммирование: {a} + {b} = {a + b}
    <br> Вычитание: {a} - {b} = {a - b}
    <br> Умножение: {a} × {b} = {a * b}
    <br> Деление: {a} / {b} = {'Делить на 0 нельзя!' if b == 0 else a / b}
    <br> Возведение в с тепень: {a}<sup>{b}</sup> = {a ** b}
  </body>
</html>
'''


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
def calc_missing(a):
    return redirect(f'/lab2/calc/{a}/1')



@lab2.route('/lab2/books')
def book_list():
    return render_template('lab2/books.html',
                           books=books)


@lab2.route('/lab2/tsvetochki')
def show_berries():
    return render_template('lab2/tsvetochki.html', items=flowers)
