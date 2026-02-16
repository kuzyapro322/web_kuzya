from flask import Blueprint, render_template, request, abort, jsonify, current_app
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

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
    """Закрытие соединения с базой данных"""
    conn.commit()
    cur.close()
    conn.close()

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')


def validate_film(film):
    errors = {}
    
    if not film.get('title_ru') or film['title_ru'].strip() == '':
        errors['title_ru'] = 'Русское название не может быть пустым'
    
    current_year = datetime.now().year
    try:
        year = int(film.get('year', 0))
        if year < 1895 or year > current_year:
            errors['year'] = f'Год должен быть в диапазоне от 1895 до {current_year}'
    except (ValueError, TypeError):
        errors['year'] = 'Год должен быть числом'
    
    description = film.get('description', '').strip()
    if not description:
        errors['description'] = 'Описание не может быть пустым'
    elif len(description) > 2000:
        errors['description'] = 'Описание не может превышать 2000 символов'
    
    return errors


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id;")
        else:
            cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id;")
        
        films_data = cur.fetchall()
        
        films_list = []
        for film in films_data:
            if current_app.config['DB_TYPE'] == 'postgres':
                films_list.append({
                    "id": film['id'],
                    "title": film['title'],
                    "title_ru": film['title_ru'],
                    "year": film['year'],
                    "description": film['description']
                })
            else:
                films_list.append({
                    "id": film[0],
                    "title": film[1],
                    "title_ru": film[2],
                    "year": film[3],
                    "description": film[4]
                })
        
        return jsonify(films_list)
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = %s;", (id,))
        else:
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = ?;", (id,))
        
        film_data = cur.fetchone()
        
        if not film_data:
            abort(404)
        
        if current_app.config['DB_TYPE'] == 'postgres':
            film = {
                "id": film_data['id'],
                "title": film_data['title'],
                "title_ru": film_data['title_ru'],
                "year": film_data['year'],
                "description": film_data['description']
            }
        else:
            film = {
                "id": film_data[0],
                "title": film_data[1],
                "title_ru": film_data[2],
                "year": film_data[3],
                "description": film_data[4]
            }
        
        return jsonify(film)
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM films WHERE id = %s;", (id,))
        else:
            cur.execute("SELECT id FROM films WHERE id = ?;", (id,))
        
        film = cur.fetchone()
        
        if not film:
            abort(404)
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM films WHERE id = %s;", (id,))
        else:
            cur.execute("DELETE FROM films WHERE id = ?;", (id,))
        
        return '', 204
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM films WHERE id = %s;", (id,))
        else:
            cur.execute("SELECT id FROM films WHERE id = ?;", (id,))
        
        film_exists = cur.fetchone()
        
        if not film_exists:
            abort(404)
        
        film = request.get_json()
        if not film:
            abort(400, description="No data provided")
        
        errors = validate_film(film)
        if errors:
            return jsonify(errors), 400
        
        title = film.get('title', '').strip()
        title_ru = film.get('title_ru', '').strip()
        if not title and title_ru:
            title = title_ru
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                UPDATE films 
                SET title = %s, title_ru = %s, year = %s, description = %s 
                WHERE id = %s
                RETURNING id, title, title_ru, year, description;
            """, (title, title_ru, film['year'], film['description'], id))
        else:
            cur.execute("""
                UPDATE films 
                SET title = ?, title_ru = ?, year = ?, description = ? 
                WHERE id = ?
            """, (title, title_ru, film['year'], film['description'], id))
        
        if current_app.config['DB_TYPE'] == 'postgres':
            updated_film = cur.fetchone()
            result = {
                "id": updated_film['id'],
                "title": updated_film['title'],
                "title_ru": updated_film['title_ru'],
                "year": updated_film['year'],
                "description": updated_film['description']
            }
        else:
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = ?;", (id,))
            film_data = cur.fetchone()
            result = {
                "id": film_data[0],
                "title": film_data[1],
                "title_ru": film_data[2],
                "year": film_data[3],
                "description": film_data[4]
            }
        
        return jsonify(result)
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    conn, cur = db_connect()
    try:
        film = request.get_json()
        if not film:
            abort(400, description="No data provided")
        
        errors = validate_film(film)
        if errors:
            return jsonify(errors), 400
        
        title = film.get('title', '').strip()
        title_ru = film.get('title_ru', '').strip()
        if not title and title_ru:
            title = title_ru
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                INSERT INTO films (title, title_ru, year, description) 
                VALUES (%s, %s, %s, %s) 
                RETURNING id;
            """, (title, title_ru, film['year'], film['description']))
        else:
            cur.execute("""
                INSERT INTO films (title, title_ru, year, description) 
                VALUES (?, ?, ?, ?);
            """, (title, title_ru, film['year'], film['description']))
        
        if current_app.config['DB_TYPE'] == 'postgres':
            new_id = cur.fetchone()['id']
        else:
            new_id = cur.lastrowid
        
        return {"id": new_id}, 201
    finally:
        db_close(conn, cur)

    