from flask import Blueprint, render_template, request, redirect, session


lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error='Делить на ноль нельзя!')
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods = ['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 0
    if x2 == '':
        x2 = 0
    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/multiple-form')
def multiple_form():
    return render_template('lab4/multiple-form.html')


@lab4.route('/lab4/multiple', methods = ['POST'])
def multiple():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 1
    if x2 == '':
        x2 = 1
    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/multiple.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods = ['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/exp-form')
def exp_form():
    return render_template('lab4/exp-form.html')


@lab4.route('/lab4/exp', methods = ['POST'])
def exp():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/exp.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x1 == 0 and x2 == 0:
        return render_template('lab4/exp.html', error='Оба числа не могут быть нулями!')
    result = x1 ** x2
    return render_template('lab4/exp.html', x1=x1, x2=x2, result=result)


tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut':
        tree_count -= 1
    elif operation == 'plant':
        tree_count += 1

    return redirect('/lab4/tree')



users = [
    {'login': 'alex', 'password': '123', 'name': 'Алекса Нейстат', 'gender': 'f'},
    {'login': 'bob', 'password': '64124', 'name': 'Боб Кварк', 'gender': 'm'},
    {'login': 'max', 'password': '457', 'name': 'Максим Батурин', 'gender': 'm'},
    {'login': 'anton', 'password': 'fghfgh', 'name': 'Антон Картавин', 'gender': 'm'},
    {'login': 'egor', 'password': 'weqweq', 'name': 'Егор Манилов', 'gender': 'm'},
    {'login': 'kirill', 'password': '999', 'name': 'Кузнецов Кирилл', 'gender': 'm'},
]

@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            current_login = session['login']
            user = next((u for u in users if u['login'] == current_login), None)
            if user:
                return render_template('lab4/login.html', authorized=True, login=user['login'], name=user['name'])
        
        return render_template('lab4/login.html', authorized=False, login='')

    login_value = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()

    if not login_value:
        return render_template('lab4/login.html', authorized=False, error='Не введён логин', login=login_value)
    
    if not password:
        return render_template('lab4/login.html', authorized=False, error='Не введён пароль', login=login_value)
    for user in users:
        if login_value == user['login'] and password == user['password']:
                session['login'] = login_value
                return redirect('/lab4/users')

    return render_template('lab4/login.html', authorized=False, error='Неверные логин или пароль', login=login_value)


@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')

    login_value = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()
    confirm = request.form.get('confirm', '').strip()
    name = request.form.get('name', '').strip()
    gender = request.form.get('gender', '').strip()

    if not login_value or not password or not confirm or not name:
        return render_template('lab4/register.html', error='Не все поля заполнены')

    if password != confirm:
        return render_template('lab4/register.html', error='Пароль и подтверждение не совпадают')

    for u in users:
        if u['login'] == login_value:
            return render_template('lab4/register.html', error='Такой логин уже существует')

    users.append({'login': login_value, 'password': password, 'name': name, 'gender': gender})
    return redirect('/lab4/users')


@lab4.route('/lab4/users')
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')

    return render_template('lab4/users.html', users=users, current_login=session['login'])


@lab4.route('/lab4/delete', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    login = session['login']
    global users
    users = [u for u in users if u['login'] != login]
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/edit', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    current_login = session['login']
    user = next((u for u in users if u['login'] == current_login), None)
    if not user:
        return redirect('/lab4/login')

    if request.method == 'GET':
        return render_template('lab4/edit.html', user=user)

    new_login = request.form.get('login', '').strip()
    new_name = request.form.get('name', '').strip()
    new_password = request.form.get('password', '').strip()
    confirm = request.form.get('confirm', '').strip()

    if not new_login or not new_name:
        return render_template('lab4/edit.html', user=user, error='Логин и имя не должны быть пустыми')

    if new_password or confirm:
        if new_password != confirm:
            return render_template('lab4/edit.html', user=user, error='Пароль и подтверждение не совпадают')
        user['password'] = new_password

    user['login'] = new_login
    user['name'] = new_name
    session['login'] = new_login
    return render_template('lab4/edit.html', user=user, success='Данные успешно обновлены!')


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = None
    snowflakes = 0
    temp_value = ''

    if request.method == 'POST':
        temp = request.form.get('temperature')
        temp_value = temp

        if not temp:
            message = 'Ошибка: не задана температура'
        else:
            try:
                t = float(temp)

                if t < -12:
                    message = 'Не удалось установить температуру — слишком низкое значение'
                elif t > -1:
                    message = 'Не удалось установить температуру — слишком высокое значение'
                elif -12 <= t <= -9:
                    message = f'Установлена температура: {t}°C'
                    snowflakes = 3
                elif -9 < t <= -5:
                    message = f'Установлена температура: {t}°C'
                    snowflakes = 2
                elif -5 < t <= -1:
                    message = f'Установлена температура: {t}°C'
                    snowflakes = 1
            except ValueError:
                message = 'Ошибка: температура должна быть числом'

    return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes, temperature=temp_value)


@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    grains = {
        'barley': {'title': 'ячмень', 'price': 12000},
        'oats': {'title': 'овёс', 'price': 8500},
        'wheat': {'title': 'пшеница', 'price': 9000},
        'rye': {'title': 'рожь', 'price': 15000},
    }

    if request.method == 'GET':
        return render_template('lab4/grain.html',
                               grains=grains,
                               error=None)

    grain_code = request.form.get('grain')
    weight_str = request.form.get('weight')

    if not weight_str:
        return render_template('lab4/grain.html',
                               grains=grains,
                               error='Ошибка: не указан вес')

    try:
        weight = float(weight_str)
    except ValueError:
        return render_template('lab4/grain.html',
                               grains=grains,
                               error='Ошибка: вес должен быть числом')

    if weight <= 0:
        return render_template('lab4/grain.html',
                               grains=grains,
                               error='Ошибка: вес должен быть больше 0')

    if weight > 100:
        return render_template('lab4/grain.html',
                               grains=grains,
                               error='Такого объёма сейчас нет в наличии')

    grain_obj = grains.get(grain_code)
    if not grain_obj:
        return render_template('lab4/grain.html',
                               grains=grains,
                               error='Ошибка: не выбрано зерно')

    price_per_ton = grain_obj['price']
    base_sum = weight * price_per_ton

    discount = 0
    final_sum = base_sum

    if weight > 10:
        discount = base_sum * 0.10
        final_sum = base_sum - discount

    return render_template('lab4/grain.html',
                           grains=grains,
                           error=None,
                           success=True,
                           grain_title=grain_obj['title'],
                           weight=weight,
                           base_sum=base_sum,
                           final_sum=final_sum,
                           discount=discount)
