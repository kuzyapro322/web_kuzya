from flask import Blueprint, render_template, session, jsonify, request, current_app, redirect, url_for
import random
from os import path
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
import hashlib
import math

lab9 = Blueprint('lab9', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='knowledge_base_db',
            user='kirill_kuznetsov_knowledge_base',
            password='Kuzya_2026!'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def hash_password(password):
    """Хеширование пароля"""
    return hashlib.sha256(password.encode()).hexdigest()

#ПОЛЬЗОВАТЕЛИ

def get_user_by_login(login):
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            query = "SELECT id, login, name, password FROM users WHERE login = %s"
        else:
            query = "SELECT id, login, name, password FROM users WHERE login = ?"
        
        cur.execute(query, (login,))
        user = cur.fetchone()
        return dict(user) if user else None
    except Exception as e:
        print(f"Ошибка при получении пользователя: {e}")
        return None
    finally:
        db_close(conn, cur)

def create_user(login, password):
    conn, cur = db_connect()
    try:
        
        existing_user = get_user_by_login(login)
        if existing_user:
            return False, "Пользователь с таким логином уже существует"
        hashed_password = hash_password(password)
        
        name = login.capitalize()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            query = "INSERT INTO users (login, password, name) VALUES (%s, %s, %s)"
        else:
            query = "INSERT INTO users (login, password, name) VALUES (?, ?, ?)"
        
        cur.execute(query, (login, hashed_password, name))
        conn.commit()
        return True, "Пользователь успешно создан"
    except Exception as e:
        print(f"Ошибка при создании пользователя: {e}")
        conn.rollback()
        return False, f"Ошибка при создании пользователя: {str(e)}"
    finally:
        db_close(conn, cur)

# КОРОБКИ

def get_all_boxes():
    conn, cur = db_connect()
    try:
        cur.execute("SELECT box_id, is_opened, message, gift_image FROM boxes ORDER BY box_id")
        boxes = cur.fetchall()
        
        boxes_list = []
        for box in boxes:
            boxes_list.append({
                'box_id': box['box_id'],
                'is_opened': box['is_opened'],
                'message': box['message'],
                'gift_image': box['gift_image']
            })
        return boxes_list
    except Exception as e:
        print(f"Ошибка при получении коробок из БД: {e}")
        return []
    finally:
        db_close(conn, cur)

def get_box_by_id(box_id):
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            query = "SELECT box_id, is_opened, message, gift_image FROM boxes WHERE box_id = %s"
        else:
            query = "SELECT box_id, is_opened, message, gift_image FROM boxes WHERE box_id = ?"
        
        cur.execute(query, (box_id,))
        box = cur.fetchone()
        return dict(box) if box else None
    except Exception as e:
        print(f"Ошибка при получении коробки {box_id}: {e}")
        return None
    finally:
        db_close(conn, cur)

def update_box_state(box_id, is_opened):
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            query = "UPDATE boxes SET is_opened = %s WHERE box_id = %s"
        else:
            query = "UPDATE boxes SET is_opened = ? WHERE box_id = ?"
        
        cur.execute(query, (is_opened, box_id))
        conn.commit()
        return True
    finally:
        db_close(conn, cur)

def reset_all_boxes():
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            query = "UPDATE boxes SET is_opened = FALSE"
        else:
            query = "UPDATE boxes SET is_opened = 0"
        
        cur.execute(query)
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка при сбросе коробок: {e}")
        conn.rollback()
        return False
    finally:
        db_close(conn, cur)

def count_opened_boxes():
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            query = "SELECT COUNT(*) as count FROM boxes WHERE is_opened = TRUE"
        else:
            query = "SELECT COUNT(*) as count FROM boxes WHERE is_opened = 1"
        
        cur.execute(query)
        result = cur.fetchone()
        return result['count'] if result else 0
    except Exception as e:
        print(f"Ошибка при подсчете открытых коробок: {e}")
        return 0
    finally:
        db_close(conn, cur)


#КОРОБКИ ДЛЯ АВТОРИЗОВАННЫХ
def is_protected_box(box_id):
    protected_box_ids = [7, 8]  
    return box_id in protected_box_ids



@lab9.route('/lab9/')
def lab():
    if 'box_positions' not in session:
        # Разделяем область 80x80 на сетку
        cols = 5  # 5 колонок
        rows = 2  # 2 строки (5x2=10 ячеек)
        
        cell_width = 80 / cols  # 16% ширины
        cell_height = 80 / rows  # 40% высоты
        
        positions = []
        
        # Генерируем по порядку, но можно перемешать
        for row in range(rows):
            for col in range(cols):
                # Центр ячейки
                center_x = col * cell_width + cell_width / 2
                center_y = row * cell_height + cell_height / 2
                
                # Небольшое случайное смещение (±15% от размера ячейки)
                offset_x = random.randint(-int(cell_width * 0.3), int(cell_width * 0.3))
                offset_y = random.randint(-int(cell_height * 0.3), int(cell_height * 0.3))
                
                # Финальная позиция
                left = int(center_x + offset_x)
                top = int(center_y + offset_y)
                
                # Ограничиваем в пределах области 0-80
                left = max(0, min(80, left))
                top = max(0, min(80, top))
                
                positions.append((left, top))
        
        # Перемешиваем позиции, чтобы они не шли по порядку
        random.shuffle(positions)
        
        session['box_positions'] = positions

    # Получаем данные из БД
    boxes = get_all_boxes()
    
    # Добавляем информацию об авторизованных коробках 
    for box in boxes:
        box['requires_auth'] = is_protected_box(box['box_id'])
    
    total_opened = count_opened_boxes()
    closed_count = 10 - total_opened
    
    is_authenticated = 'user_id' in session
    user_login = session.get('user_login', None)
    name = session.get('name', None)
    
    if is_authenticated:
        if 'authenticated_opened_count' not in session:
            session['authenticated_opened_count'] = 0
        opened_count = session['authenticated_opened_count']
    else:
        if 'guest_opened_count' not in session:
            session['guest_opened_count'] = 0
        opened_count = session['guest_opened_count']
    
    return render_template('lab9/index.html', 
                         boxes=boxes,
                         positions=session['box_positions'],
                         closed_count=closed_count,
                         opened_count=opened_count,
                         is_authenticated=is_authenticated,
                         user_login=user_login,
                         name=name)


@lab9.route('/lab9/login', methods=['GET', 'POST'])
def login():
    """Страница входа"""
    error = None
    
    if request.method == 'POST':
        login_input = request.form.get('login')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me') == 'true'
        
        if not login_input or not password:
            error = "Логин и пароль обязательны для заполнения"
        else:
            user = get_user_by_login(login_input)
            
            if user:
                hashed_password = hash_password(password)
                if user['password'] == hashed_password:
                    # Сохраняем в сессии
                    session['user_id'] = user['id']
                    session['user_login'] = user['login']
                    session['name'] = user['name']
                    
                    session.pop('guest_opened_count', None)
                    session['authenticated_opened_count'] = 0
                    
                    if remember_me:
                        session.permanent = True
                    return redirect(url_for('lab9.lab'))
                else:
                    error = "Неверный пароль"
            else:
                error = "Пользователь не найден"
    
    return render_template('lab9/login.html', error=error)

@lab9.route('/lab9/register', methods=['GET', 'POST'])
def register():
    error = None
    
    if request.method == 'POST':
        login_input = request.form.get('login')
        password = request.form.get('password')
        
        if not login_input or not password:
            error = "Логин и пароль обязательны для заполнения"
        elif len(password) < 6:
            error = "Пароль должен содержать не менее 6 символов"
        else:
            success, message = create_user(login_input, password)
            
            if success:
                user = get_user_by_login(login_input)
                session['user_id'] = user['id']
                session['user_login'] = user['login']
                session['name'] = user['name']
                
                session.pop('guest_opened_count', None)
                session['authenticated_opened_count'] = 0

                return redirect(url_for('lab9.lab'))
            else:
                error = message
    
    return render_template('lab9/register.html', error=error)

@lab9.route('/lab9/logout')
def logout():
    """Выход из системы"""
    session.pop('user_id', None)
    session.pop('user_login', None)
    session.pop('name', None)
    session.pop('authenticated_opened_count', None)
    return redirect(url_for('lab9.lab'))



@lab9.route('/lab9/rest-api/boxes/', methods=['GET'])
def get_boxes_api():
    """REST API: получить все коробки"""
    boxes = get_all_boxes()
    
    for box in boxes:
        box['requires_auth'] = is_protected_box(box['box_id'])
    
    return jsonify(boxes)

@lab9.route('/lab9/rest-api/boxes/<int:box_id>', methods=['GET'])
def get_box_api(box_id):
    """REST API: получить конкретную коробку"""
    box = get_box_by_id(box_id)
    if not box:
        return jsonify({"error": "Коробка не найдена"}), 404
    
    # Проверяем, является ли коробка защищенной
    requires_auth = is_protected_box(box_id)
    box['requires_auth'] = requires_auth
    
    if requires_auth and 'user_id' not in session:
        return jsonify({
            "error": "Для открытия этой коробки необходимо авторизоваться",
            "requires_auth": True,
            "box_id": box_id
        }), 403
    
    return jsonify(box)

@lab9.route('/lab9/rest-api/boxes/<int:box_id>/open', methods=['POST'])
def open_box_api(box_id):
    """REST API: открыть коробку"""
    try:
        if box_id < 1 or box_id > 10:
            return jsonify({"error": "Некорректный ID коробки"}), 400
        
        requires_auth = is_protected_box(box_id)
        
        if requires_auth and 'user_id' not in session:
            return jsonify({
                "error": "Для открытия этой коробки необходимо авторизоваться",
                "requires_auth": True
            }), 403
        
        box = get_box_by_id(box_id)
        if not box:
            return jsonify({"error": "Коробка не найдена"}), 404
        
        if box['is_opened']:
            return jsonify({"error": "Эта коробка уже открыта!"}), 400
        
        if 'user_id' in session:
            opened_count = session.get('authenticated_opened_count', 0)
            if opened_count >= 3:
                return jsonify({"error": "Вы уже открыли 3 коробки!"}), 403
        else:
            opened_count = session.get('guest_opened_count', 0)
            if opened_count >= 3:
                return jsonify({"error": "Вы уже открыли 3 коробки!"}), 403
        
        if update_box_state(box_id, True):
            if 'user_id' in session:
                session['authenticated_opened_count'] = session.get('authenticated_opened_count', 0) + 1
                user_opened_count = session['authenticated_opened_count']
            else:
                session['guest_opened_count'] = session.get('guest_opened_count', 0) + 1
                user_opened_count = session['guest_opened_count']
            
            session.modified = True
            
            total_opened = count_opened_boxes()
            closed_count = 10 - total_opened
            
            return jsonify({
                "success": True,
                "message": box['message'],
                "gift": box['gift_image'],
                "user_opened_count": user_opened_count,
                "total_opened_count": total_opened,
                "closed_count": closed_count,
                "box_id": box_id
            })
        else:
            return jsonify({"error": "Ошибка при обновлении БД"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Ошибка: {str(e)}"}), 500

@lab9.route('/lab9/rest-api/boxes/reset', methods=['POST'])
def reset_boxes_api():
    """REST API: сбросить все коробки (Дед Мороз)"""
    # Проверяем авторизацию
    if 'user_id' not in session:
        return jsonify({"error": "Только для авторизованных пользователей"}), 401
    
    if reset_all_boxes():
        session['authenticated_opened_count'] = 0
        session.modified = True
        
        return jsonify({
            "success": True,
            "message": f"Дед Мороз {session.get('name', '')} наполнил все коробки заново! ",
            "closed_count": 10
        })
    else:
        return jsonify({"error": "Ошибка при сбросе коробок"}), 500