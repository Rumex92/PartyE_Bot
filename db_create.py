import sqlite3

def create_tables():
    conn = sqlite3.connect('message.db')
    cursor = conn.cursor()

    # for bot types
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bot_types (
            user_id INTEGER PRIMARY KEY,
            bot_type INTEGER
        )
    ''')

    # for user message histories
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_histories (
            user_id INTEGER PRIMARY KEY,
            message TEXT
        )
    ''')

    conn.commit()
    conn.close()

create_tables()