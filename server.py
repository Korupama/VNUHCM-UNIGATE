from fastapi import FastAPI, Response, Form, Depends, HTTPException, Request
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
from app.services.auth_utils import verify_user, create_access_token, get_current_user

class Post(BaseModel):
    id: int
    username: str
    question: str
    answer: list
    topic: str
    date: str
    content: str

class AnswerInput(BaseModel):
    answer: str
    username: str
class LoginForm(BaseModel):
    username: str
    password: str

# Import the exam registration router
from app.routers import exam_registration
from app.routers import exam_results
from app.routers import admission_info
from app.routers import admission_preferences
from app.routers import admission_results

# ...existing code...
from app.routers import admission_preferences
from app.routers import admission_results

# ...existing code...

# Include the admission preferences router
#app.include_router(admission_preferences.router)

# Include the admission results router
#app.include_router(admission_results.router)

# ...existing code...
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

# Include the admission information router
app.include_router(admission_info.router)

# Include the admission preferences router
app.include_router(admission_preferences.router)

# Include the admission results router
app.include_router(admission_results.router)

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
    topic_len = {}
    for topic in topics:
        topic_len[topic] = len(list(filter(lambda post: post['topic'] == topic, data)))
    last_post_title_dict = {}
    for topic in topics:
        last_post = max(filter(lambda post: post['topic'] == topic, data), key=lambda x: x['date'])
        last_post_title_dict[topic] = last_post['question']
    last_post_time_dict = {}
    for topic in topics:
        last_post = max(filter(lambda post: post['topic'] == topic, data), key=lambda x: x['date'])
        last_post_time_dict[topic] = last_post['date']
    last_post_time_dict = dict(sorted(last_post_time_dict.items(), key=lambda item: item[1]))
    return {
        "topics": list(topics),
        "number_of_topics": topic_len,
        "last_post_title": last_post_title_dict,
        "last_post_time": last_post_time_dict
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


@app.get("/api/get-post/{post_id}")
def get_post(post_id: int):
    try:
        with open('./nosqlDB/forum.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except FileNotFoundError:
        return {"error": "Không tìm thấy file dữ liệu."}
    except json.JSONDecodeError:
        return {"error": "Lỗi đọc file JSON."}

    # Tìm bài viết theo ID
    for post in posts:
        if post.get("id") == post_id:
            return post

    return {"error": "Không tìm thấy bài viết."}

@app.get("/api/latest-posts")
def get_latest_posts():
    try:
        with open('./nosqlDB/forum.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Bỏ qua bài viết không có trường "date"
        posts = [post for post in data if "date" in post]

        # Chuyển date thành kiểu datetime để so sánh
        for post in posts:
            try:
                post["parsed_date"] = datetime.strptime(post["date"], "%Y-%m-%d")
            except ValueError:
                post["parsed_date"] = datetime.min  # Nếu lỗi định dạng thì đẩy về rất xa

        # Sắp xếp theo ngày giảm dần
        sorted_posts = sorted(posts, key=lambda x: x["parsed_date"], reverse=True)

        # Chọn 5 bài viết mới nhất
        latest_posts = sorted_posts[:5]

        # Xoá trường phụ trước khi trả về
        for post in latest_posts:
            del post["parsed_date"]

        return latest_posts

    except Exception as e:
        return {"error": str(e)}
    
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

@app.post("/api/submit-answer/{id}")
def submit_answer(id: int, data: AnswerInput):
    try:
        # Đọc dữ liệu từ JSON file
        with open('./nosqlDB/forum.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
# Tìm bài viết theo id
        for post in posts:
            if post["id"] == id:
                # Tạo comment mới
                username = data.username.strip() or "Ẩn danh"
                new_answer = {
                    "answer": data.answer,
                    "username": username,
                    "date": datetime.now().strftime("%Y-%m-%d")
                }

                # Đảm bảo post có trường answer là list
                if "answer" not in post or not isinstance(post["answer"], list):
                    post["answer"] = []

                # Thêm comment vào danh sách
                post["answer"].append(new_answer)

                # Ghi lại vào file JSON
                with open('./nosqlDB/forum.json', 'w', encoding='utf-8') as f:
                    json.dump(posts, f, indent=4, ensure_ascii=False)

                return {"message": "Trả lời đã được thêm", "new_answer": new_answer}

        return {"error": "Không tìm thấy bài viết có id =", "id": id}

    except Exception as e:
        return {"error": "Lỗi server", "detail": str(e)}



@app.post("/api/login")
def login(data: LoginForm, response: Response):
    user = verify_user(conn, data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Sai tài khoản hoặc mật khẩu")

    token = create_access_token({"sub": user["username"]})
    return {"access_token": token}  # Gửi về body để FE decode

        
@app.get("/api/me")
def read_me(request: Request, current_user: dict = Depends(get_current_user)):
    print(request.headers, flush=True)
    return current_user


@app.post("/api/logout")
def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    return {"message": "Đăng xuất thành công"}


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
    <div style="width: 100%; height: 100%; position: relative">
	<div style="width: 595px; height: 842px; left: 0px; top: 0px; position: absolute; background: white; box-shadow: 0px 0px 0px rgba(0, 0, 0, 0)"></div>
	<div style="width: 595px; height: 100px; left: 0px; top: 0px; position: absolute; background: #F8F9FA; border-bottom: 0.80px #E9ECEF solid"></div>
	<div style="left: 423px; top: 40px; position: absolute; text-align: right; color: #6B7280; font-size: 13px; font-family: Times New Roman; font-weight: 400; line-height: 19.50px; word-wrap: break-word">Số:</div>
	<div style="left: 444px; top: 40px; position: absolute; text-align: right; color: #6B7280; font-size: 13px; font-family: Times New Roman; font-weight: 400; line-height: 19.50px; word-wrap: break-word">{result_form_dict['ma_ho_so_du_thi']}</div>
	<div style="left: 451px; top: 59px; position: absolute; text-align: right; color: #6B7280; font-size: 13px; font-family: Times New Roman; font-weight: 400; line-height: 19.50px; word-wrap: break-word">Ngày: 15/06/2025</div>
	<div style="left: 188px; top: 119px; position: absolute; text-align: center; color: black; font-size: 24px; font-family: Telex; font-weight: 400; line-height: 32px; word-wrap: break-word">GIẤY BÁO ĐIỂM THI</div>
	<div style="left: 67px; top: 151px; position: absolute; text-align: center; color: black; font-size: 24px; font-family: Telex; font-weight: 400; line-height: 32px; word-wrap: break-word">KỲ THI ĐÁNH GIÁ NĂNG LỰC ĐHQG-HCM</div>
	<div style="width: 238px; height: 134px; left: 48px; top: 215px; position: absolute; border-left: 4px #4B5563 solid"></div>
	<div style="left: 64px; top: 215px; position: absolute; color: black; font-size: 16px; font-family: Times New Roman; font-weight: 700; line-height: 24px; word-wrap: break-word">THÔNG TIN DỰ THI</div>
	<div style="left: 64px; top: 255px; position: absolute; color: black; font-size: 13px; font-family: Times New Roman; font-weight: 400; line-height: 19.50px; word-wrap: break-word">CCCD:</div>
	<div style="left: 110px; top: 255px; position: absolute; color: black; font-size: 13px; font-family: Times New Roman; font-weight: 700; line-height: 19.50px; word-wrap: break-word">{result_form_dict['cccd']}</div>
	<div style="left: 64px; top: 282px; position: absolute; color: black; font-size: 13px; font-family: Times New Roman; font-weight: 400; line-height: 19.50px; word-wrap: break-word">Mã hồ sơ:</div>
	<div style="left: 124px; top: 282px; position: absolute; color: black; font-size: 13px; font-family: Times New Roman; font-weight: 700; line-height: 19.50px; word-wrap: break-word">{result_form_dict['ma_ho_so_du_thi']}</div>
	<div style="left: 64px; top: 310px; position: absolute; color: black; font-size: 13px; font-family: Times New Roman; font-weight: 400; line-height: 19.50px; word-wrap: break-word">Đợt thi:</div>
	<div style="left: 108px; top: 310px; position: absolute; color: black; font-size: 13px; font-family: Times New Roman; font-weight: 400; line-height: 19.50px; word-wrap: break-word">1</div>
	<div style="width: 238px; height: 134px; left: 309px; top: 215px; position: absolute; border-left: 4px #4B5563 solid"></div>
	<div style="left: 325px; top: 215px; position: absolute; color: black; font-size: 16px; font-family: Times New Roman; font-weight: 700; line-height: 24px; word-wrap: break-word">THÔNG TIN CÁ NHÂN</div>
	<div style="left: 325px; top: 255px; position: absolute; color: black; font-size: 13px; font-family: Times New Roman; font-weight: 400; line-height: 19.50px; word-wrap: break-word">Họ và tên:</div>
	<div style="left: 387px; top: 255px; position: absolute; color: black; font-size: 13px; font-family: Times New Roman; font-weight: 700; line-height: 19.50px; word-wrap: break-word">{result_form_dict['ho_ten']}</div>
	<div style="left: 325px; top: 282px; position: absolute; color: black; font-size: 13px; font-family: Times New Roman; font-weight: 400; line-height: 19.50px; word-wrap: break-word">Ngày sinh:</div>

	<div style="left: 389px; top: 282px; position: absolute; color: black; font-size: 13px; font-family: Times New Roman; font-weight: 700; line-height: 19.50px; word-wrap: break-word">{result_form_dict['ngay_sinh']}</div>
	<div style="left: 325px; top: 310px; position: absolute; color: black; font-size: 13px; font-family: Times New Roman; font-weight: 400; line-height: 19.50px; word-wrap: break-word">Trường: {result_form_dict['ten_truong_thpt']},<br/> tỉnh {result_form_dict['tinh']}</div>
	<div style="width: 499px; height: 366px; left: 48px; top: 351px; position: absolute; border-top: 0.80px #E9ECEF solid"></div>
	<div style="left: 248px; top: 355px; position: absolute; text-align: center; color: black; font-size: 16px; font-family: Times New Roman; font-weight: 700; line-height: 24px; word-wrap: break-word">KẾT QUẢ THI</div>
	<div style="width: 113px; height: 90px; left: 119px; top: 387px; position: absolute; background: #F8F9FA; border-radius: 4px"></div>
	<div style="left: 147px; top: 403px; position: absolute; text-align: center; color: #6B7280; font-size: 13px; font-family: Times New Roman; font-weight: 400; line-height: 19.50px; word-wrap: break-word">Tiếng Việt</div>
	<div style="left: 140px; top: 430px; position: absolute; text-align: center; color: black; font-size: 20px; font-family: Times New Roman; font-weight: 700; line-height: 30px; word-wrap: break-word">{result_form_dict['diem_thanh_phan_tieng_viet']}/300</div>
	<div style="width: 113px; height: 90px; left: 361px; top: 387px; position: absolute; background: #F8F9FA; border-radius: 4px"></div>
	<div style="left: 391px; top: 403px; position: absolute; text-align: center; color: #6B7280; font-size: 13px; font-family: Times New Roman; font-weight: 400; line-height: 19.50px; word-wrap: break-word">Toán học</div>
	<div style="left: 382px; top: 430px; position: absolute; text-align: center; color: black; font-size: 20px; font-family: Times New Roman; font-weight: 700; line-height: 30px; word-wrap: break-word">{result_form_dict['diem_thanh_phan_toan_hoc']}/300</div>
	<div style="width: 113px; height: 90px; left: 175px; top: 484px; position: absolute; background: #F8F9FA; border-radius: 4px"></div>
	<div style="left: 218px; top: 500px; position: absolute; text-align: center; color: #6B7280; font-size: 13px; font-family: Times New Roman; font-weight: 400; line-height: 19.50px; word-wrap: break-word">Logic</div>
	<div style="left: 200px; top: 527px; position: absolute; text-align: center; color: black; font-size: 20px; font-family: Times New Roman; font-weight: 700; line-height: 30px; word-wrap: break-word">{result_form_dict['diem_thanh_phan_logic_phan_tich_so_lieu']}/120</div>
	<div style="width: 113px; height: 90px; left: 304px; top: 484px; position: absolute; background: #F8F9FA; border-radius: 4px"></div>
	<div style="left: 313px; top: 500px; position: absolute; text-align: center; color: #6B7280; font-size: 13px; font-family: Times New Roman; font-weight: 400; line-height: 19.50px; word-wrap: break-word">Suy luận khoa học</div>
	<div style="left: 328px; top: 527px; position: absolute; text-align: center; color: black; font-size: 20px; font-family: Times New Roman; font-weight: 700; line-height: 30px; word-wrap: break-word">{result_form_dict['diem_thanh_phan_suy_luan_khoa_hoc']}/180</div>
	<div style="width: 113px; height: 90px; left: 241px; top: 387px; position: absolute; background: #F8F9FA; border-radius: 4px"></div>
	<div style="left: 269px; top: 403px; position: absolute; text-align: center; color: #6B7280; font-size: 13px; font-family: Times New Roman; font-weight: 400; line-height: 19.50px; word-wrap: break-word">Tiếng Anh</div>
	<div style="left: 264px; top: 430px; position: absolute; text-align: center; color: black; font-size: 20px; font-family: Times New Roman; font-weight: 700; line-height: 30px; word-wrap: break-word">{result_form_dict['diem_thanh_phan_tieng_anh']}/300</div>
	<div style="width: 499px; height: 131px; left: 48px; top: 583px; position: absolute; border-radius: 4px; border: 2px black solid"></div>
	<div style="left: 254px; top: 609px; position: absolute; text-align: center; color: #6B7280; font-size: 16px; font-family: Times New Roman; font-weight: 400; line-height: 24px; word-wrap: break-word">TỔNG ĐIỂM</div>

	<div style="left: 267px; top: 641px; position: absolute; text-align: center; color: black; font-size: 32px; font-family: Times New Roman; font-weight: 700; line-height: 48px; word-wrap: break-word">{result_form_dict['ket_qua_thi']}</div>
	<div style="left: 337px; top: 717px; position: absolute; text-align: right; color: black; font-size: 13px; font-family: Times New Roman; font-weight: 700; line-height: 19.50px; word-wrap: break-word">TP.HCM, ngày 15 tháng 06 năm 2025</div>
	<div style="left: 366px; top: 746px; position: absolute; text-align: center; color: black; font-size: 16px; font-family: Times New Roman; font-weight: 700; line-height: 24px; word-wrap: break-word">HỘI ĐỒNG <br />KỲ THI ĐÁNH GIÁ<br />NĂNG LỰC NĂM 2025 </div>
	<img style="width: 180px; height: 55px; left: 48px; top: 32px; position: absolute" src="https://placehold.co/180x55" />
    </div>
     </body>
     </html>

        """
        return HTMLResponse(content=html)
    else:
        return {"message": "No result form found for this user"}




