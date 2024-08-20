import sqlite3
import json

def get_db_connection():
    conn = sqlite3.connect('message.db')
    return conn


def save_bot_type(user_id, bot_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bot_types (user_id, bot_type)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET bot_type=excluded.bot_type
    ''', (user_id, bot_type))
    conn.commit()
    conn.close()


def get_bot_type(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT bot_type FROM bot_types WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def save_history(user_id, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    message_json = json.dumps(message)
    cursor.execute('''
        INSERT INTO user_histories (user_id, message)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET message=excluded.message
    ''', (user_id, message_json))
    conn.commit()
    conn.close()


def get_history(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT message FROM user_histories WHERE user_id = ?', (user_id,))
    messages = cursor.fetchone()
    conn.close()

    if messages:
        return json.loads(messages[0])
    else:
        return []