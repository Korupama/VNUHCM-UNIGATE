from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import psycopg2
from dotenv import load_dotenv
import json
from datetime import datetime

def connect_db():
    load_dotenv()
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRESQL_DB'),
        user=os.getenv('POSTGRESQL_USER'),
        password=os.getenv('POSTGRESQL_PASSWORD'),
        host=os.getenv('POSTGRESQL_HOST'),
        port=os.getenv('POSTGRESQL_PORT'),
        sslmode='require'
    )
    return conn

conn = connect_db()

app = FastAPI() 
app.mount("/static", StaticFiles(directory="assets"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Định nghĩa API route
@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI"}

@app.get("/api/get-posts")
def get_posts():
    with open('./nosqlDB/forum.json', 'r') as f:
        data = json.load(f)
    return data

@app.get("/api/get-post-topics")
def get_post_topics():
    with open('./nosqlDB/forum.json', 'r') as f:
        data = json.load(f)
    topics = set()
    for post in data:
        topics.add(post['topic'])
    return {
        "topics": list(topics),
        "number_of_topics": len(data)
    }


@app.post('/api/create-post')
def create_post(post: dict):
    with open('./nosqlDB/forum.json', 'r') as f:
        data = json.load(f)
    post['id'] = len(data) + 1
    post['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data.append(post)
    with open('./nosqlDB/forum.json', 'w') as f:
        json.dump(data, f, indent=4)
    return {"message": "Post created successfully"}

@app.post('/api/delete-post')
def delete_post(post_id: int):
    with open('./nosqlDB/forum.json', 'r') as f:
        data = json.load(f)
    data = [post for post in data if post['id'] != post_id]
    with open('./nosqlDB/forum.json', 'w') as f:
        json.dump(data, f, indent=4)
    return {"message": "Post deleted successfully"}

@app.post('/api/update-post')
def update_post(post_id: int, updated_post: dict):
    with open('./nosqlDB/forum.json', 'r') as f:
        data = json.load(f)
    for post in data:
        if post['id'] == post_id:
            post.update(updated_post)
            break
    with open('./nosqlDB/forum.json', 'w') as f:
        json.dump(data, f, indent=4)
    return {"message": "Post updated successfully"}

# @app.post('/api/update-post')

@app.get("/api/authenticate-user")
def authenticate_user(cccd: str, password: str):
    # print("Username:", cccd)
    # print("Password:", password)
    with conn.cursor() as cur:
        cur.execute("select check_password(%s,%s)", (cccd, password))
        user = cur.fetchone()
    if user:
        return {"message": "User authenticated successfully", "user": cccd}
    else:
        return {"message": "Invalid username or password"}

@app.get("/api/get-application-form", response_class=HTMLResponse)
def get_application_form(cccd: str, dot_thi: int):
    ma_ho_so = ''
    if dot_thi == 1:
        ma_ho_so = 'HS' + cccd
    elif dot_thi == 2:
        ma_ho_so = 'H2' + cccd
    with conn.cursor() as cur:
        cur.execute("select * from report_application where ma_ho_so_du_thi = %s", (ma_ho_so,))
        application_form = cur.fetchall() 
    # print("Application Form:", application_form)
    if application_form:
        application_form = application_form[0]
        application_form_dict = {
            "cccd": application_form[0],
            "ma_ho_so_du_thi": application_form[1],
            "dia_diem_du_thi": application_form[2],
            "ho_ten": application_form[3],
            "ngay_sinh": application_form[4],
            "gioi_tinh": application_form[5],
            "dan_toc": application_form[6],
            "ten_truong_thpt": application_form[7],
            "so_dien_thoai": application_form[8],
            "email": application_form[9],
            "dia_chi_lien_lac": application_form[10],
            "tinh": application_form[11],
        }
        time = ''
        if dot_thi == 1:
            time = '07h30 ngày 30/3/2025'
        elif dot_thi == 2:
            time = '07h30 ngày 30/6/2025'
        
        html = f"""
        <html>
        <body>
        <div style="width: 100%; height: 100%; position: relative; background: white; overflow: hidden">
            <img style="width: 180px; height: 55px; left: 42px; top: 39px; position: absolute" src="/static/logovnuhcm.png" />
            <div
                style="left: 70px; top: 102px; position: absolute; text-align: center; color: black; font-size: 24px; font-family: Telex; font-weight: 400; word-wrap: break-word">
                GIẤY BÁO DỰ THI<br />KỲ THI ĐÁNH GIÁ NĂNG LỰC ĐHQG-HCM</div>
            <div style="width: 456px; left: 70px; top: 179px; position: absolute"><span
                    style="color: black; font-size: 16px; font-family: Roboto; font-weight: 700; word-wrap: break-word">THÔNG
                    TIN DỰ THI<br /></span><span
                    style="color: black; font-size: 13px; font-family: Roboto; font-weight: 400; word-wrap: break-word"><br />CCCD:
                    {application_form_dict['cccd']}<br /><br />Mã hồ sơ dự thi: {application_form_dict['ma_ho_so_du_thi']}<br /><br />Địa điểm thi: {application_form_dict['dia_diem_du_thi']}<br /><br />Thời
                                gian gọi thí sinh vào phòng thi: {time}<br /><br /></span><span
                    style="color: black; font-size: 16px; font-family: Roboto; font-weight: 700; word-wrap: break-word">THÔNG
                    TIN CÁ NHÂN<br /></span><span
                    style="color: black; font-size: 16px; font-family: Roboto; font-weight: 400; word-wrap: break-word"><br /></span><span
                    style="color: black; font-size: 13px; font-family: Roboto; font-weight: 400; word-wrap: break-word">Họ và
                    tên: {application_form_dict['ho_ten']}<br /><br />Ngày tháng năm sinh: {application_form_dict['ngay_sinh']}<br /><br />Giới tính: {application_form_dict['gioi_tinh']}<br /><br />Dân
                                tộc: {application_form_dict['dan_toc']}<br /><br />Trường THPT: {application_form_dict['ten_truong_thpt']}, {application_form_dict['tinh']}<br /><br /></span><span
                    style="color: black; font-size: 16px; font-family: Roboto; font-weight: 700; word-wrap: break-word">THÔNG
                    TIN LIÊN LẠC<br /></span><span
                    style="color: black; font-size: 16px; font-family: Roboto; font-weight: 400; word-wrap: break-word"><br /></span><span
                    style="color: black; font-size: 13px; font-family: Roboto; font-weight: 400; word-wrap: break-word">Số điện
                    thoại: {application_form_dict['so_dien_thoai']}<br /><br />Email: {application_form_dict['email']}<br /><br />Địa chỉ liên lạc: {application_form_dict['dia_chi_lien_lac']}
                                <br /></span><span
                    style="color: black; font-size: 16px; font-family: Roboto; font-weight: 400; word-wrap: break-word"><br /><br /><br /></span>
            </div>
            <div style="width: 456px; left: 70px; top: 634px; position: absolute"><span
                    style="color: #FF0000; font-size: 16px; font-family: Roboto; font-weight: 700; word-wrap: break-word"><br /><br />THÍ
                    SINH CẦN LƯU Ý:<br /></span><span
                    style="color: #FF0000; font-size: 13px; font-family: Roboto; font-weight: 400; word-wrap: break-word"><br />1.Thí
                    sinh phải có mặt tại phòng thi đúng thời gian quy định ghi trong giấy báo dự thi.<br /><br />2.Khi đi thi,
                    thí sinh cần mang theo các giấy tờ sau, nếu không sẽ không được vào phòng thi:<br />
                    - Giấy báo dự thi (bản in từ website kỳ thi)<br />- Giấy tờ tùy thân mà thí sinh đã sử dụng để đăng ký thi:
                    CCCD bản chính<br /></span></div>
            <div
                style="left: 438px; top: 39px; position: absolute; text-align: right; color: #6B7280; font-size: 13px; font-family: Roboto; font-weight: 400; line-height: 19.50px; word-wrap: break-word">
                Số:</div>
            <div
                style="left: 459px; top: 39px; position: absolute; text-align: right; color: #6B7280; font-size: 13px; font-family: Roboto; font-weight: 400; line-height: 19.50px; word-wrap: break-word">
                EX2025001</div>
        </div>
        </body>
        </html>

        """
        return HTMLResponse(content=html)
    else:
        return {"message": "No application form found for this user"}