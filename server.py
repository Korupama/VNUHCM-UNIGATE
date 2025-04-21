from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import psycopg2
from dotenv import load_dotenv
import json
from datetime import datetime
from fastapi.responses import FileResponse
from pydantic import BaseModel
import re
import unicodedata
from psycopg2.extras import RealDictCursor

class Post(BaseModel):
    id: int
    username: str
    question: str
    answer: list
    topic: str
    date: str


# Import the exam registration router
from app.routers import exam_registration
from app.routers import exam_results

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

app = FastAPI(
    title="VNUHCM-UNIGATE API",
    description="API for the VNUHCM-UNIGATE Admission Portal",
    version="1.0.0",
) 
app.mount("/static", StaticFiles(directory="assets"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Make DB connection available to routers
exam_registration.router.db_connection = conn

# Include the exam registration router
app.include_router(exam_registration.router)

# Include the exam results router
app.include_router(exam_results.router)

# Existing API routes
@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI"}

@app.get("/api/get-posts")
def get_posts():
    with open('./nosqlDB/forum.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

@app.get("/api/get-post-topics")
def get_post_topics():
    with open('./nosqlDB/forum.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    topics = set()
    for post in data:
        topics.add(post['topic'])
    return {
        "topics": list(topics),
        "number_of_topics": len(data)
    }


@app.post('/api/create-post')
def create_post(post: Post):
    with open('./nosqlDB/forum.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    post_dict = post.dict()
    post_dict['id'] = len(data) + 1
    post_dict['date'] = datetime.now().strftime("%Y-%m-%d")
    data.append(post_dict)

    with open('./nosqlDB/forum.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return {"message": "Post created successfully"}

@app.post('/api/delete-post')
def delete_post(post_id: int):
    with open('./nosqlDB/forum.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data = [post for post in data if post['id'] != post_id]
    with open('./nosqlDB/forum.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    return {"message": "Post deleted successfully"}

@app.post('/api/update-post')
def update_post(post_id: int, updated_post: dict):
    with open('./nosqlDB/forum.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for post in data:
        if post['id'] == post_id:
            post.update(updated_post)
            break
    with open('./nosqlDB/forum.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    return {"message": "Post updated successfully"}
























@app.get("/api/get-topic-posts")
def get_topic_posts(topic: str):
    with open('./nosqlDB/forum.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    def slugify(text):
        text = unicodedata.normalize('NFD', str(text).lower())
        text = text.encode('ascii', 'ignore').decode('ascii')
        text = re.sub(r'[^a-z0-9\s-]', '', text)
        text = re.sub(r'\s+', '-', text)
        text = re.sub(r'-+', '-', text)
        return text.strip()
        
    slug_topic = slugify(topic)
    topic_posts = list(filter(lambda post: slugify(post['topic']) == slug_topic, data))
    return {
        "posts": topic_posts,
        "number_of_posts": len(topic_posts)
    }


@app.get("/api/authenticate-user")
def authenticate_user(cccd: str, password: str):
    with conn.cursor() as cur:
        cur.execute("select check_password(%s,%s)", (cccd, password))
        user = cur.fetchone()
    if user:
        return {"message": "User authenticated successfully", "user": cccd, "token": cccd}
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


@app.get("/api/get-documents-list")
def get_documents_list():
    with open('./nosqlDB/documents.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

@app.get("/api/get-document")
def get_document(id: int):
    # Check if document exists and return it as PDF
    with open('./nosqlDB/documents.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    document = next((doc for doc in data if doc['id'] == id), None)
    if not document:
        return {"error": "Document not found"}
    name = document['filename']
    filepath = f"./documents/{name}"
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type="application/pdf", filename=f"{name}")
    else:
        return {"error": "Document not found"}


@app.get("/api/get-result-form", response_class=HTMLResponse)
def get_result_form(cccd: str, dot_thi: int):
    ma_ho_so = ''
    if dot_thi == 1:
        ma_ho_so = 'HS' + cccd
    elif dot_thi == 2:
        ma_ho_so = 'H2' + cccd
    with conn.cursor() as cur:
        cur.execute("select * from report_application where ma_ho_so_du_thi = %s", (ma_ho_so,))
        result_form = cur.fetchall() 
    if result_form:
        result_form = result_form[0]
        result_form_dict = {
            "cccd": result_form[0],
            "ma_ho_so_du_thi": result_form[1],
            "dia_diem_du_thi": result_form[2],
            "dot_thi": result_form[3], 
            "ho_ten": result_form[4],
            "ngay_sinh": result_form[5],
            "ten_truong_thpt": result_form[6],
            "tinh": result_form[7],
            "diem_thanh_phan_tieng_viet": result_form[8], 
            "diem_thanh_phan_tieng_anh": result_form[9], 
            "diem_thanh_phan_toan_hoc": result_form[10],
            "diem_thanh_phan_logic_phan_tich_so_lieu": result_form[11],
            "diem_thanh_phan_suy_luan_khoa_hoc": result_form[12], 
            "ket_qua_thi": result_form[13]
        }
  
        
        html = f"""
        <html>
        <body>
        
        </body>
        </html>

        """
        return HTMLResponse(content=html)
    else:
        return {"message": "No result form found for this user"}
