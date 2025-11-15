# Backend cho [VNUHCM-UNIGATE](https://github.com/KhanhVy-r2/VNUHCM-UNIGATE)

Đây là backend API phục vụ Cổng Tuyển sinh Đại học Quốc gia TP.HCM - UNIGATE.
Xây dựng bằng FastAPI + PostgreSQL + JSON-based NoSQL.

## Chức năng chính

- **Xác thực người dùng**: Đăng ký, đăng nhập, đăng xuất, kiểm tra thông tin người dùng (`/api/register`, `/api/login`, `/api/logout`, `/api/me`).
- **Quản lý bài viết diễn đàn**:
  - Lấy danh sách bài viết (`/api/get-posts`, `/api/get-topic-posts`)
  - Tạo bài viết (`/api/create-post`), chỉnh sửa, xoá (`/api/update-post`, `/api/delete-post`)
  - Gửi câu trả lời (bình luận) (`/api/submit-answer/{id}`)
  - Thống kê chủ đề, bài mới nhất (`/api/get-post-topics`, `/api/latest-posts`)
- **Quản lý tài liệu ôn tập**:
  - Lấy danh sách tài liệu (`/api/get-documents-list`)
  - Tải tài liệu PDF (`/api/get-document`)
- **Quản lý hồ sơ dự thi**:
  - Tạo báo cáo hồ sơ thi (`/api/get-application-report`)
  - Tạo báo cáo kết quả thi (`/api/get-result-report`)
- **Tư vấn ngành học**:
  - Gợi ý ngành học dựa trên kết quả thi (`/api/recommend-field-of-study`)
- **Chatbot hỗ trợ tuyển sinh**:
  - Hỏi đáp tự động (`/api/get-bot-answer`)

## Công nghệ sử dụng

- **FastAPI**: Xây dựng API nhanh gọn, hiệu suất cao.
- **PostgreSQL**: Lưu trữ thông tin tài khoản, hồ sơ dự thi.
- **JSON file**: Quản lý bài viết diễn đàn và tài liệu ôn tập.
- **OAuth2 (JWT)**: Quản lý phiên đăng nhập.
- **CORS Middleware**: Cho phép giao tiếp frontend (`localhost:5173`) và backend.

## Cài đặt

### Cài đặt môi trường
Cài đặt các biến môi trường trong file `.env` với mẫu trong file `example.env`.

### Cài đặt thư viện và chạy server
1. Sử dụng [uv](https://github.com/astral-sh/uv)

- Cài đặt các thư viện cần thiết với lệnh `uv sync`
- Chạy server với lệnh `uv run uvicorn main:app` hoặc `uv run uvicorn main:app --reload` (để tự động tải lại khi có thay đổi trong mã nguồn).

2. Sử dụng [pipenv](https://pipenv.pypa.io/en/latest/)

- Cài đặt các thư viện cần thiết với lệnh `pip install -r requirements.txt --require-hashes` 
- Chạy server với lệnh `uvicorn main:app` hoặc `uvicorn main:app --reload` (để tự động tải lại khi có thay đổi trong mã nguồn).

![chatbot(1)](https://github.com/user-attachments/assets/49bb3e8c-14a0-4e24-b24e-b1500b174c56)
