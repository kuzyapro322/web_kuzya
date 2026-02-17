from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3 
from os import path


lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login = session.get('login'),
                           name=session.get('name'))


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


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method =='GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    name = request.form.get('name')

    if not login or not password or not name:
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"SELECT login FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute(f"SELECT login FROM users WHERE login=?;", (login, ))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html',
                               error='Такой пользователь уже существует')
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"INSERT INTO users (login, password, name) VALUES (%s, %s, %s);", (login, password_hash, name))
    else:
        cur.execute(f"INSERT INTO users (login, password, name) VALUES (?, ?, ?);", (login, password_hash, name))

    db_close(conn, cur)
    return render_template('lab5/success.html',
                            name=name)


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method =='GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute(f"SELECT * FROM users WHERE login=?;", (login, ))

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')
    name = user['name']

    session['login'] = login
    session['name'] = name
    db_close(conn, cur)
    return render_template('lab5/success_login.html',
                            name=name)


@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab5/create_article.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute(f"SELECT * FROM users WHERE login=?;", (login, ))

    user_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"INSERT INTO articles(user_id, title, article_text)\
                      VALUES (%s, %s, %s);", (user_id, title, article_text))
    else:
        cur.execute(f"INSERT INTO articles(login_id, title, article_text)\
                      VALUES (?, ?, ?);", (user_id, title, article_text))
    
    db_close(conn, cur)
    return redirect('/lab5')


@lab5.route('/lab5/list', methods=['GET'])
def list():
    login = session.get('login')
    
    conn, cur = db_connect()
    
    if login:
        # Для авторизованных пользователей - их статьи + публичные чужие
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(f"SELECT id FROM users WHERE login = %s;", (login, ))
        else:
            cur.execute(f"SELECT id FROM users WHERE login = ?;", (login, ))

        user_id = cur.fetchone()['id']

        if current_app.config['DB_TYPE'] == 'postgres':
            # Сначала свои статьи, потом публичные чужие
            cur.execute("""
                (SELECT *, true as is_own FROM articles WHERE user_id = %s)
                UNION ALL
                (SELECT *, false as is_own FROM articles WHERE user_id != %s AND is_public = True)
                ORDER BY is_own DESC, is_favorite DESC, id DESC;
            """, (user_id, user_id))
        else:
            cur.execute("""
                SELECT *, 
                    (login_id = ?) as is_own 
                FROM articles 
                WHERE login_id = ? OR is_public = 1
                ORDER BY is_own DESC, is_favorite DESC, id DESC;
            """, (user_id, user_id))
    else:
        # Для неавторизованных - только публичные статьи
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(f"SELECT * FROM articles WHERE is_public = True ORDER BY id DESC;")
        else:
            cur.execute(f"SELECT * FROM articles WHERE is_public = 1 ORDER BY id DESC;")

    articles = cur.fetchall()
    db_close(conn, cur)

    if not articles:
        return render_template('lab5/articles.html', error='Статьи отсутствуют')
    else:
        return render_template('lab5/articles.html', articles=articles, login=login)


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    session.pop('name', None)
    return render_template('lab5/lab5.html')


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    
    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id = %s;", (article_id,))
        else:
            cur.execute("SELECT * FROM articles WHERE id = ?;", (article_id,))
        
        article = cur.fetchone()
        db_close(conn, cur)
        
        if not article:
            return "Статья не найдена", 404
            
        return render_template('lab5/edit.html', article=article)

    new_title = request.form.get('new_title')
    new_article_text = request.form.get('new_article_text')

    if not new_title or not new_article_text:
        return render_template('lab5/edit.html', error='Поля не могут быть пустыми', article=article)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login = ?;", (login,))

    user_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title = %s, article_text = %s WHERE id = %s AND user_id = %s;", 
                   (new_title, new_article_text, article_id, user_id))
    else:
        cur.execute("UPDATE articles SET title = ?, article_text = ? WHERE id = ? AND login_id = ?;", 
                   (new_title, new_article_text, article_id, user_id))
    
    db_close(conn, cur)

    return redirect('/lab5/list')


@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"SELECT id FROM users WHERE login = %s;", (login, ))
    else:
        cur.execute(f"SELECT id FROM users WHERE login = ?;", (login, ))

    user_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"DELETE FROM articles WHERE user_id = %s AND id = %s;", (user_id, article_id))
    else:
        cur.execute(f"DELETE FROM articles WHERE login_id = ? AND id = ?;", (user_id, article_id))

    db_close(conn, cur)

    return redirect('/lab5/list')


@lab5.route('/lab5/users', methods=['GET'])
def user_list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    cur.execute(f"SELECT login, name FROM users")

    users = cur.fetchall()

    db_close(conn, cur)

    return render_template('lab5/users.html', users=users)


@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    if request.method =='GET':

        login = session.get('login')
        if not login:
            return redirect('/lab5/login')
        
        name = session.get('name')

        return render_template('lab5/profile.html', name=name)
    
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    name = request.form.get('name')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    if not name or not old_password or not new_password:
        return render_template('lab5/login.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"SELECT password FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute(f"SELECT password FROM users WHERE login=?;", (login, ))

    password = cur.fetchone()['password']

    if not check_password_hash(password, old_password):
        db_close(conn, cur)
        return render_template('lab5/profile.html',
                               error='Неверный пароль')
    
    hashed_new_password = generate_password_hash(new_password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"UPDATE users SET name = %s, password = %s WHERE login=%s;", (name, hashed_new_password, login, ))
    else:
        cur.execute(f"UPDATE users SET name = ?, password = ? WHERE login=?;", (name, hashed_new_password, login, ))

    db_close(conn, cur)

    session['name'] = name

    return render_template('lab5/success_profile.html',
                            name=name)


@lab5.route('/lab5/favorite/<int:article_id>', methods=['POST'])
def favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"SELECT id FROM users WHERE login = %s;", (login, ))
    else:
        cur.execute(f"SELECT id FROM users WHERE login = ?;", (login, ))

    user_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"UPDATE articles SET is_favorite = True WHERE id = %s AND user_id = %s;", (article_id, user_id))
    else:
        cur.execute(f"UPDATE articles SET is_favorite = 1 WHERE id = ? AND login_id = ?;", (article_id, user_id))

    db_close(conn, cur)

    return redirect('/lab5/list')


@lab5.route('/lab5/unfavorite/<int:article_id>', methods=['POST'])
def unfavorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"SELECT id FROM users WHERE login = %s;", (login, ))
    else:
        cur.execute(f"SELECT id FROM users WHERE login = ?;", (login, ))

    user_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"UPDATE articles SET is_favorite = False WHERE id = %s AND user_id = %s;", (article_id, user_id))
    else:
        cur.execute(f"UPDATE articles SET is_favorite = 0 WHERE id = ? AND login_id = ?;", (article_id, user_id))

    db_close(conn, cur)

    return redirect('/lab5/list')


@lab5.route('/lab5/public/<int:article_id>', methods=['POST'])
def make_public(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"SELECT id FROM users WHERE login = %s;", (login, ))
    else:
        cur.execute(f"SELECT id FROM users WHERE login = ?;", (login, ))

    user_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"UPDATE articles SET is_public = True WHERE id = %s AND user_id = %s;", (article_id, user_id))
    else:
        cur.execute(f"UPDATE articles SET is_public = 1 WHERE id = ? AND login_id = ?;", (article_id, user_id))

    conn.commit()
    db_close(conn, cur)

    return redirect('/lab5/list')


@lab5.route('/lab5/private/<int:article_id>', methods=['POST'])
def make_private(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"SELECT id FROM users WHERE login = %s;", (login, ))
    else:
        cur.execute(f"SELECT id FROM users WHERE login = ?;", (login, ))

    user_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"UPDATE articles SET is_public = False WHERE id = %s AND user_id = %s;", (article_id, user_id))
    else:
        cur.execute(f"UPDATE articles SET is_public = 0 WHERE id = ? AND login_id = ?;", (article_id, user_id))

    conn.commit()
    db_close(conn, cur)

    return redirect('/lab5/list')
