import sqlite3


# 创建一个新的数据库文件
def create_database():
    conn = sqlite3.connect('database/bilibili.db')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        mid INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        latest_time INTEGER NOT NULL
    )
    ''')

    conn.commit()
    conn.close()
