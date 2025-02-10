# -*- coding: utf-8 -*-
import sqlite3

def create_database():
    try:
        # เชื่อมต่อกับฐานข้อมูล SQLite
        conn = sqlite3.connect('databases.db')
        cursor = conn.cursor()

        # สร้างตาราง items หากยังไม่มี
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age TEXT DEFAULT '',
            gender TEXT DEFAULT '',
            height TEXT DEFAULT '',
            skin_color TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            hair TEXT DEFAULT '',
            profession TEXT DEFAULT '',
            body_type TEXT DEFAULT '',
            lifestyle TEXT DEFAULT '',
            free_text TEXT DEFAULT '',
            profile_picture TEXT DEFAULT ''
        )
        ''')

        # ยืนยันการเปลี่ยนแปลง
        conn.commit()
        print("Database and table 'items' created successfully.")

    except sqlite3.Error as e:
        print("An error occurred: {}".format(e))  # ใช้ .format() แทน f-string

    finally:
        # ปิดการเชื่อมต่อฐานข้อมูล
        if conn:
            conn.close()

# เรียกฟังก์ชันสร้างฐานข้อมูล
create_database()
