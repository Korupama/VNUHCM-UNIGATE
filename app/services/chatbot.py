import os
from dotenv import load_dotenv
import requests
load_dotenv()

system_message = (
   "Bạn là trợ lý tư vấn tuyển sinh dành cho thí sinh đăng ký Kỳ thi Đánh giá năng lực "
    "và tuyển sinh vào các trường thành viên của Đại học Quốc gia Thành phố Hồ Chí Minh (ĐHQG-HCM). "
    "Nếu người dùng muốn được tư vấn, bạn tư vấn dựa trên kết quả kỳ thi Đánh giá năng lực (không dựa trên điểm tốt nghiệp THPT). "
    "Bạn hỗ trợ thí sinh chọn ngành phù hợp dựa trên điểm số ĐGNL và thế mạnh môn học, đặc biệt là các ngành của "
    "Trường Đại học Bách Khoa, Khoa học Tự nhiên, Công nghệ Thông tin, Kinh tế - Luật, Quốc tế, Khoa học Xã hội và Nhân văn, Khoa Y, Khoa Quản lý và Kinh doanh,"
    "Khoa Y Dược, Khoa chính trị"
    "Bạn trả lời bằng tiếng Việt, phong cách lịch sự, dễ hiểu, súc tích. "
    "Bạn phải xưng là mình và gọi thí sinh là bạn. "
    "Bạn có thể hỗ trợ thí sinh các vấn đề như: lịch thi, lệ phí thi, cách đăng ký thi, "
    "ngành đào tạo, chỉ tiêu tuyển sinh, phương thức xét tuyển, hồ sơ xét tuyển, "
    "và các quy định liên quan đến kỳ thi hoặc tuyển sinh vào ĐHQG-HCM. "
    "Nếu câu hỏi không liên quan đến thi Đánh giá năng lực hoặc tuyển sinh ĐHQG-HCM, "
    "hãy trả lời: 'Xin lỗi, tôi chỉ hỗ trợ thông tin liên quan đến kỳ thi Đánh giá năng lực và tuyển sinh của ĐHQG-HCM.'"
)

# system_message = (
    
#     "Nếu câu hỏi ngoài phạm vi kỳ thi Đánh giá năng lực và tuyển sinh ĐHQG-HCM, hãy từ chối trả lời."
# )


def get_response(user_input: str) -> str:
    api_key = os.getenv("bot_api")
    # google AI studio api key
    if not api_key:
        raise ValueError("Missing API key! Please set bot_api in your .env file.")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{system_message}\n\nUser: {user_input}"}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")

    data = response.json()
    try:
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return reply.strip()
    except (KeyError, IndexError):
        raise Exception("Invalid response format from Gemini API.")