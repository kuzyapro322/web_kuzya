from flask import Blueprint, render_template, request, make_response, redirect, url_for


lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name') or 'Аноним'
    age = request.cookies.get('age') or 'Неизвестный'
    name_color = request.cookies.get('name_color') or 'black'
    return render_template('lab3/lab3.html', name=name,
                                             age=age,
                                             name_color=name_color)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'cornflowerblue')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user,
                                              age=age,
                                              sex=sex,
                                              errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    elif drink == 'green-tea':
        price = 70
    else:
        price = 0

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    size = request.args.get('size')
    background_color = request.args.get('background_color')
    font_style = request.args.get('font_style')
    if color or size:
        resp = make_response(redirect('/lab3/settings'))
        resp.set_cookie('color', color)
        resp.set_cookie('size', size)
        resp.set_cookie('background_color', background_color)
        resp.set_cookie('font_style', font_style)
        return resp

    color = request.cookies.get('color')
    size = request.cookies.get('size')
    background_color = request.cookies.get('background_color')
    font_style = request.cookies.get('font_style')
    resp = make_response(render_template('lab3/settings.html', color=color,
                                         size=size,
                                         background_color=background_color,
                                         font_style=font_style))
    return resp


@lab3.route('/lab3/ticket')
def ticket():
    # Если форма не отправлена - показываем пустую форму
    if not request.args:
        return render_template('lab3/ticket_buy.html')

    # Берем данные из формы
    fio = request.args.get('fio')
    berth = request.args.get('berth')
    age = request.args.get('age')
    from_city = request.args.get('from_city')
    to_city = request.args.get('to_city')
    date = request.args.get('date')
    
    # Проверяем чекбоксы
    linen = request.args.get('linen') == 'on'
    baggage = request.args.get('baggage') == 'on'
    insurance = request.args.get('insurance') == 'on'

    # Проверяем что все поля заполнены
    if not all([fio, berth, age, from_city, to_city, date]):
        return "Все поля должны быть заполнены!", 400

    # Проверяем возраст
    try:
        age_int = int(age)
        if not (1 <= age_int <= 120):
            return "Возраст должен быть от 1 до 120 лет!", 400
    except ValueError:
        return "Возраст должен быть числом!", 400

    # Расчет цены
    is_child = age_int < 18
    price = 700 if is_child else 1000
    
    if berth in ['нижняя', 'нижняя боковая']:
        price += 100
    
    if linen:
        price += 75
    if baggage:
        price += 250
    if insurance:
        price += 150

    return render_template(
        'lab3/ticket_result.html',
        fio=fio,
        berth=berth,
        linen=linen,
        baggage=baggage,
        age=age_int,
        from_city=from_city,
        to_city=to_city,
        date=date,
        insurance=insurance,
        is_child=is_child,
        price=price
    )


@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('background_color')
    resp.delete_cookie('font_style')
    resp.delete_cookie('size')
    return resp


products = [
    {"name": "iPhone 15 Pro", "price": 119000, "brand": "Apple", "color": "Титановый"},
    {"name": "Samsung Galaxy S24", "price": 89900, "brand": "Samsung", "color": "Черный"},
    {"name": "Xiaomi 14", "price": 64900, "brand": "Xiaomi", "color": "Зеленый"},
    {"name": "Google Pixel 8", "price": 75900, "brand": "Google", "color": "Белый"},
    {"name": "OnePlus 12", "price": 69900, "brand": "OnePlus", "color": "Синий"},
    {"name": "iPhone 14", "price": 78900, "brand": "Apple", "color": "Фиолетовый"},
    {"name": "Samsung Galaxy A54", "price": 34900, "brand": "Samsung", "color": "Серебристый"},
    {"name": "Xiaomi Redmi Note 13", "price": 25900, "brand": "Xiaomi", "color": "Черный"},
    {"name": "Realme 11 Pro", "price": 28900, "brand": "Realme", "color": "Золотой"},
    {"name": "iPhone SE", "price": 45900, "brand": "Apple", "color": "Красный"},
    {"name": "Samsung Galaxy Z Flip5", "price": 99900, "brand": "Samsung", "color": "Фиолетовый"},
    {"name": "Google Pixel 7a", "price": 44900, "brand": "Google", "color": "Синий"},
    {"name": "Xiaomi Poco X6", "price": 29900, "brand": "Xiaomi", "color": "Желтый"},
    {"name": "Nothing Phone 2", "price": 54900, "brand": "Nothing", "color": "Белый"},
    {"name": "iPhone 13", "price": 59900, "brand": "Apple", "color": "Розовый"},
    {"name": "Samsung Galaxy S23 FE", "price": 49900, "brand": "Samsung", "color": "Зеленый"},
    {"name": "Xiaomi 13T", "price": 47900, "brand": "Xiaomi", "color": "Черный"},
    {"name": "Motorola Edge 40", "price": 42900, "brand": "Motorola", "color": "Синий"},
    {"name": "Honor 90", "price": 37900, "brand": "Honor", "color": "Серебристый"},
    {"name": "Vivo V29", "price": 41900, "brand": "Vivo", "color": "Красный"},
]


@lab3.route('/lab3/products')
def products_view():
    # Получаем мин и макс цены из всех товаров
    min_all = min(p['price'] for p in products)
    max_all = max(p['price'] for p in products)
    
    # Обработка сброса
    if request.args.get('action') == 'reset':
        resp = make_response(redirect(url_for('lab3.products_view')))
        resp.delete_cookie('price_min')
        resp.delete_cookie('price_max')
        return resp
    
    # Получаем значения из формы или куки
    min_raw = request.args.get('min', '')
    max_raw = request.args.get('max', '')
    
    if not min_raw and not max_raw:
        min_raw = request.cookies.get('price_min', '')
        max_raw = request.cookies.get('price_max', '')
    
    # Обрабатываем цены
    price_min = None
    price_max = None
    
    if min_raw.strip():
        try:
            price_min = int(min_raw)
        except ValueError:
            price_min = None
            
    if max_raw.strip():
        try:
            price_max = int(max_raw)
        except ValueError:
            price_max = None
    
    # Исправляем если min > max
    if price_min and price_max and price_min > price_max:
        price_min, price_max = price_max, price_min
    
    # Фильтруем товары
    filtered = []
    for p in products:
        if price_min and p['price'] < price_min:
            continue
        if price_max and p['price'] > price_max:
            continue
        filtered.append(p)
    
    # Сохраняем в куки если был поиск
    if request.args.get('min') is not None or request.args.get('max') is not None:
        resp = make_response(render_template(
            'lab3/products.html',
            items=filtered,
            count=len(filtered),
            min_all=min_all,
            max_all=max_all,
            value_min='' if price_min is None else price_min,
            value_max='' if price_max is None else price_max
        ))
        if price_min is None:
            resp.delete_cookie('price_min')
        else:
            resp.set_cookie('price_min', str(price_min))
        if price_max is None:
            resp.delete_cookie('price_max')
        else:
            resp.set_cookie('price_max', str(price_max))
        return resp
    
    return render_template(
        'lab3/products.html',
        items=filtered if (price_min or price_max) else products,
        count=len(filtered) if (price_min or price_max) else len(products),
        min_all=min_all,
        max_all=max_all,
        value_min='' if price_min is None else price_min,
        value_max='' if price_max is None else price_max
    )