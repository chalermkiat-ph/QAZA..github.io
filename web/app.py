# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, send_from_directory
import sqlite3
import os
import random  # เพิ่มการใช้งาน random สำหรับสุ่มผลลัพธ์
import requests
import base64
from werkzeug.utils import secure_filename

url = "http://127.0.0.1:8000"
url_create_personal = "/personal/createPersonal"
url_get_all_personal = "/personal/getAllPersonal"
url_get_personal_by_criteria = "/personal/getPersonalByCriteria"
url_delete_personal_by_id = "/personal/deletePersonalById"

app = Flask(__name__)

# กำหนดพาธสำหรับเก็บไฟล์ที่อัพโหลด
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# เชื่อมต่อกับฐานข้อมูล SQLite
def get_db_connection():
    conn = sqlite3.connect('databases.db')
    conn.row_factory = sqlite3.Row  # เพื่อให้สามารถเข้าถึงข้อมูลแบบ dictionary
    return conn


# ฟังก์ชันตรวจสอบว่าไฟล์ที่อัพโหลดมีนามสกุลที่อนุญาต
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # ดึงข้อมูลจากฐานข้อมูลเพื่อแสดงในหน้า admin
    items = []

    url_with_path = url + url_get_all_personal
    response = requests.get(url_with_path)

    # Checking the status code
    if response.status_code == 200:
        response_data = response.json()  # Convert JSON response to a Python dictionary
        items = response_data['data']
    else:
        print(f"Error: {response.status_code}")

    if request.method == 'POST':
        # รับข้อมูลจากฟอร์ม
        body = {}
        body['name'] = request.form['name']
        body['age'] = request.form['age']
        body['gender'] = request.form['gender']
        body['height'] = request.form['height']
        body['skin_color'] = request.form['skin_color']
        body['ethnicity'] = request.form['ethnicity']
        body['hair'] = request.form['hair']
        body['profession'] = request.form['profession']
        body['body_type'] = request.form['body_type']
        body['lifestyle'] = request.form['lifestyle']
        body['free_text'] = request.form['free_text']

        uploaded_file = request.files['profile_picture']
        if uploaded_file:
            # Read the file in binary mode and encode to Base64
            base64_bytes = base64.b64encode(uploaded_file.read())
            base64_string = base64_bytes.decode('utf-8')
            profile_picture = base64_string

            body['profile_picture'] = profile_picture

        # URL of the API
        url_with_path = url + url_create_personal
        response = requests.post(url_with_path, json=body)

        # Checking the status code
        if response.status_code == 201:
            data = response.json()  # Convert JSON response to a Python dictionary
            print(data)
        else:
            print(f"Error: {response.status_code}")

        return redirect('/admin')  # กลับไปที่หน้าแอดมิน

    return render_template('admin.html', items=items)


@app.route('/search', methods=['POST', 'GET'])
def search_get():
    criteria = {
        'name': '', 'gender': '', 'skin_color': '', 'ethnicity': '', 'hair': '', 'profession': '', 'body_type': '',
        'lifestyle': '', 'free_text': '', 'age': '', 'height': '',
    }

    if request.method == 'POST':
        for key, value in criteria.items():
            template_request_form = f"request.form.get('{key}', '').strip()"
            criteria[key] = eval(template_request_form)

        url_with_path = url + url_get_personal_by_criteria
        response = requests.post(url_with_path, json=criteria)
        response_data = response.json()  # Convert JSON response to a Python dictionary
        item = response_data['data'][0]

        return render_template('search_results_new.html', result=item)

    return render_template('search.html', **criteria)

    # return render_template('search.html',
    #                        name=criteria['name'],
    #                        gender=criteria['gender'],
    #                        skin_color=criteria['skin_color'],
    #                        ethnicity=criteria['ethnicity'],
    #                        hair=criteria['hair'],
    #                        profession=criteria['profession'],
    #                        body_type=criteria['body_type'],
    #                        lifestyle=criteria['lifestyle'],
    #                        free_text=criteria['free_text'],
    #                        age_min=criteria['age_min'],
    #                        age_max=criteria['age_max'],
    #                        height_min=criteria['height_min'],
    #                        height_max=criteria['height_max']
    # )


#
# @app.route('/search', methods=['POST', 'GET'])
# def search_submit():
#     criteria = {
#         'name': '',
#         'gender': '',
#         'skin_color': '',
#         'ethnicity': '',
#         'profession': '',
#         'body_type': '',
#         'lifestyle': '',
#         'free_text': '',
#         'age_min': '',
#         'age_max': '',
#         'height_min': '',
#         'height_max': '',
#     }
#     name = gender = skin_color = ethnicity = hair = profession = body_type = lifestyle = free_text = ''
#     age_min = age_max = height_min = height_max = ''
#
#     if request.method == 'POST':
#         # รับค่าจากฟอร์ม
#         criteria['name'] = request.form.get('name', '').strip()
#         criteria['gender'] = request.form.get('gender', '').strip()
#         criteria['skin_color'] = request.form.get('skin_color', '').strip()
#         criteria['ethnicity'] = request.form.get('ethnicity', '').strip()
#         criteria['hair'] = request.form.get('hair', '').strip()
#         criteria['profession'] = request.form.get('profession', '').strip()
#         criteria['body_type'] = request.form.get('body_type', '').strip()
#         criteria['lifestyle'] = request.form.get('lifestyle', '').strip()
#         criteria['free_text'] = request.form.get('free_text', '').strip()
#         criteria['age_min'] = request.form.get('age_min', '').strip()
#         criteria['age_max'] = request.form.get('age_max', '').strip()
#         criteria['height_min'] = request.form.get('height_min', '').strip()
#         criteria['height_max'] = request.form.get('height_max', '').strip()
#
#         name = request.form.get('name', '').strip()
#         gender = request.form.get('gender', '').strip()
#         skin_color = request.form.get('skin_color', '').strip()
#         ethnicity = request.form.get('ethnicity', '').strip()
#         hair = request.form.get('hair', '').strip()
#         profession = request.form.get('profession', '').strip()
#         body_type = request.form.get('body_type', '').strip()
#         lifestyle = request.form.get('lifestyle', '').strip()
#         free_text = request.form.get('free_text', '').strip()
#         age_min = request.form.get('age_min', '').strip()
#         age_max = request.form.get('age_max', '').strip()
#         height_min = request.form.get('height_min', '').strip()
#         height_max = request.form.get('height_max', '').strip()
#
#         # # ตรวจสอบว่าอย่างน้อยหนึ่งฟิลด์ต้องมีข้อมูล
#         # if not any([name, gender, skin_color, ethnicity, hair, profession, body_type, lifestyle, free_text, age_min,
#         #             age_max, height_min, height_max]):
#         #     # ถ้าไม่มีข้อมูลในฟิลด์ใดเลย
#         #     return render_template('search.html', name=name, gender=gender, skin_color=skin_color,
#         #                            ethnicity=ethnicity, hair=hair, profession=profession, body_type=body_type,
#         #                            lifestyle=lifestyle, free_text=free_text, age_min=age_min, age_max=age_max,
#         #                            height_min=height_min, height_max=height_max,
#         #                            error="กรุณาระบุข้อมูลอย่างน้อย 1 ฟิลด์")
#
#         criteria_body = {}
#         for key, value in criteria.items():
#             if value == '':
#                 continue
#             criteria_body[key] = value
#
#         url_with_path = url + url_get_personal_by_criteria
#         response = requests.post(url_with_path, json=criteria)
#         response_data = response.json()  # Convert JSON response to a Python dictionary
#         item = response_data['data']
#
#         return render_template('search_results.html', results=item)
#
#         # GET request: ส่งค่าที่กรอกกลับไปยังฟอร์ม
#     return render_template('search.html',
#                            name=criteria['name'],
#                            gender=criteria['gender'],
#                            skin_color=criteria['skin_color'],
#                            ethnicity=criteria['ethnicity'],
#                            hair=criteria['hair'],
#                            profession=criteria['profession'],
#                            body_type=criteria['body_type'],
#                            lifestyle=criteria['lifestyle'],
#                            free_text=criteria['free_text'],
#                            age_min=criteria['age_min'],
#                            age_max=criteria['age_max'],
#                            height_min=criteria['height_min'],
#                            height_max=criteria['height_max']
#     )


# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     conn = get_db_connection()
#
#     # กำหนดค่าพื้นฐานสำหรับฟอร์ม
#     name = gender = skin_color = ethnicity = hair = profession = body_type = lifestyle = free_text = ''
#     age_min = age_max = height_min = height_max = ''
#
#     if request.method == 'POST':
#         # รับค่าจากฟอร์ม
#         name = request.form.get('name', '').strip()
#         gender = request.form.get('gender', '').strip()
#         skin_color = request.form.get('skin_color', '').strip()
#         ethnicity = request.form.get('ethnicity', '').strip()
#         hair = request.form.get('hair', '').strip()
#         profession = request.form.get('profession', '').strip()
#         body_type = request.form.get('body_type', '').strip()
#         lifestyle = request.form.get('lifestyle', '').strip()
#         free_text = request.form.get('free_text', '').strip()
#         age_min = request.form.get('age_min', '').strip()
#         age_max = request.form.get('age_max', '').strip()
#         height_min = request.form.get('height_min', '').strip()
#         height_max = request.form.get('height_max', '').strip()
#
#         # ตรวจสอบว่าอย่างน้อยหนึ่งฟิลด์ต้องมีข้อมูล
#         if not any([name, gender, skin_color, ethnicity, hair, profession, body_type, lifestyle, free_text, age_min,
#                     age_max, height_min, height_max]):
#             # ถ้าไม่มีข้อมูลในฟิลด์ใดเลย
#             return render_template('search.html', name=name, gender=gender, skin_color=skin_color,
#                                    ethnicity=ethnicity, hair=hair, profession=profession, body_type=body_type,
#                                    lifestyle=lifestyle, free_text=free_text, age_min=age_min, age_max=age_max,
#                                    height_min=height_min, height_max=height_max,
#                                    error="กรุณาระบุข้อมูลอย่างน้อย 1 ฟิลด์")
#
#         # สร้างคำสั่ง SQL
#         query = "SELECT * FROM items WHERE 1=1"
#         params = []
#
#         if name:
#             query += " AND name = ?"
#             params.append(name)
#         if gender:
#             query += " AND gender = ?"
#             params.append(gender)
#         if skin_color:
#             query += " AND skin_color = ?"
#             params.append(skin_color)
#         if ethnicity:
#             query += " AND ethnicity = ?"
#             params.append(ethnicity)
#         if hair:
#             query += " AND hair = ?"
#             params.append(hair)
#         if profession:
#             query += " AND profession = ?"
#             params.append(profession)
#         if body_type:
#             query += " AND body_type = ?"
#             params.append(body_type)
#         if lifestyle:
#             query += " AND lifestyle = ?"
#             params.append(lifestyle)
#         if free_text:
#             query += " AND free_text LIKE ?"
#             params.append("%" + free_text + "%")
#
#         # เพิ่มเงื่อนไขช่วงอายุ
#         if age_min and age_max:
#             query += " AND age BETWEEN ? AND ?"
#             params.extend([age_min, age_max])
#         elif age_min:
#             query += " AND age >= ?"
#             params.append(age_min)
#         elif age_max:
#             query += " AND age <= ?"
#             params.append(age_max)
#
#         # เพิ่มเงื่อนไขช่วงส่วนสูง
#         if height_min and height_max:
#             query += " AND height BETWEEN ? AND ?"
#             params.extend([height_min, height_max])
#         elif height_min:
#             query += " AND height >= ?"
#             params.append(height_min)
#         elif height_max:
#             query += " AND height <= ?"
#             params.append(height_max)
#
#         # รันคำสั่ง SQL
#         results = conn.execute(query, params).fetchall()
#         conn.close()
#
#         # หากมีผลลัพธ์มากกว่า 1 ให้สุ่มเลือก 1 รายการ
#         if results:
#             random_result = random.choice(results)
#             return render_template('search_results.html', results=[random_result])
#
#         # ถ้าไม่มีผลลัพธ์
#         return render_template('search_results.html', results=[])
#
#     # GET request: ส่งค่าที่กรอกกลับไปยังฟอร์ม
#     return render_template('search.html', name=name, gender=gender, skin_color=skin_color,
#                            ethnicity=ethnicity, hair=hair, profession=profession, body_type=body_type,
#                            lifestyle=lifestyle, free_text=free_text, age_min=age_min, age_max=age_max,
#                            height_min=height_min, height_max=height_max)


@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    url_with_path = url + url_delete_personal_by_id
    response = requests.delete(url_with_path, params={'id': item_id})

    if response.status_code == 200:
        response_data = response.json()  # Convert JSON response to a Python dictionary
        items = response_data['data']
        print(items)
    else:
        print(f"Error: {response.status_code}")

    return redirect('/admin')  # กลับไปที่หน้าแอดมิน


# เพิ่ม route สำหรับให้บริการไฟล์จากโฟลเดอร์ uploads
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


import random

import random  # เพิ่มการใช้งาน random สำหรับสุ่มผลลัพธ์

if __name__ == '__main__':
    app.run(debug=True)  # เรียกแค่ครั้งเดียว
