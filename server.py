from fastapi import FastAPI, Response, Form, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
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
from app.services.application_report import get_report_application 
from app.services.result_report import get_result_report

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
from app.routers import user_registration
from app.routers import user_update

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

# Make DB connection available to routers
user_registration.router.db_connection = conn

# Include the user registration router
app.include_router(user_registration.router)

# Make DB connection available to routers
user_update.router.db_connection = conn

# Include the user update router
app.include_router(user_update.router)

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
    admin_usernames = os.getenv('ADMIN_USERS', '')
    admin_passwords = os.getenv('ADMIN_PASSWORDS', '')

    admin_users = dict(zip(admin_usernames.split(','), admin_passwords.split(',')))

    username = data.username.strip()
    password = data.password.strip()

    if username in admin_users and admin_users[username] == password:
        token = create_access_token({"sub": username, "role": "admin"})
        return {"access_token": token}
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
    response = JSONResponse(content={"message": "Đăng xuất thành công"})
    response.delete_cookie("access_token", path="/")
    return response

@app.get("/api/get-documents-list")
def get_documents_list():
    with open('./nosqlDB/documents.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

@app.post("/api/get-document")
async def get_document(request: Request):
    body = await request.json()
    id = body.get("id")
    json_path = './nosqlDB/documents.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    document = next((doc for doc in data if doc['id'] == id), None)
    if not document:
        return {"error": "Document not found"}

    document['downloads'] += 1

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    filepath = f"./documents/{document['filename']}"
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type="application/pdf", filename=document['filename'])
    else:
        return {"error": "File not found"}


@app.get("/api/get-application-report", response_class=HTMLResponse)
def get_application_report(cccd: str, dot_thi: int):
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
        
        html = get_report_application(application_form_dict, time)
        return HTMLResponse(content=html)
    else:
        return {"message": "No application form found for this user"}

@app.get("/api/get-result-report", response_class=HTMLResponse)
def get_result_report(cccd: str, dot_thi: int):
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
  
        html = get_result_report(result_form_dict)
        return HTMLResponse(content=html)
    else:
        return {"message": "No result form found for this user"}


@app.get("/api/recommend-field-of-study")
def recommend_field_of_study(cccd: str):
    """
    API endpoint to recommend a field of study based on the provided CCCD.
    """
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Execute the query with the provided CCCD
            cur.execute("SELECT * FROM fn_khuyen_nghi_nganh_hoc(%s);", (cccd,))
            results = cur.fetchall()
        
        # Return the results as a JSON response
        return {"recommendations": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




