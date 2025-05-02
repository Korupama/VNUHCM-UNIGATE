def get_report_application(application_form_dict: dict, time: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <style>
    /* Khổ giấy A4 với lề 20 mm */
    @page {{
      size: A4 portrait;
      margin: 20mm;
    }}

    body {{
      margin: 0;
      padding: 0;
      font-family: "Times New Roman", serif;
      font-size: 12pt;
      line-height: 1.4;
      box-sizing: border-box;
    }}

    /* Container căn giữa */
    .container {{
      width: 100%;
      max-width: 555px;   /* 595px - 2*20mm ≈ 555px */
      margin: 0 auto;
    }}

    /* Header */
    .header {{
      text-align: center;
      margin-bottom: 20px;
    }}
    .header h1 {{
      font-size: 24px;
      margin: 0;
    }}
    .header h2 {{
      font-size: 20px;
      margin: 4px 0 16px;
    }}

    /* Sections */
    .section {{
      margin-bottom: 16px;
    }}
    .section-title {{
      font-size: 16px;
      font-weight: bold;
      margin-bottom: 12px;
    }}
    .field {{
      margin: 2px 0;
    }}

     .header-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;  /* khoảng cách xuống tiêu đề */
    }}
    .logo {{
        width: 180px;
        height: auto;
    }}
    .ref-number{{
        font-size: 10pt;
        color: #6B7280;
    }}

    /* Số tham chiếu (Số:) */
    /* Chú ý */
    .notice-title {{
      font-size: 14px;
      font-weight: bold;
      color: #C00;
      margin-top: 24px;
      margin-bottom: 8px;
    }}
    .notice {{
      font-size: 11pt;
      color: #ad0303;
      margin: 4px 0;
    }}

    .logo-container {{
    text-align: left;      /* hoặc center nếu muốn căn giữa */
    margin-bottom: 12px;
    }}

  </style>
</head>
<body>
  <div class="container">

   <div class="header-row">
      <img class="logo" src="https://i.imgur.com/Ao2HoX9.png" alt="Logo VNUHCM"/>
      <div class="ref-number">Số: {application_form_dict['ma_ho_so_du_thi']}</div>
    </div>

    <div class="header">
      <h1>GIẤY BÁO DỰ THI</h1>
      <h2>KỲ THI ĐÁNH GIÁ NĂNG LỰC ĐHQG-HCM</h2>
    </div>

    <div class="section">
      <div class="section-title">THÔNG TIN DỰ THI</div>
      <p class="field">CCCD: {application_form_dict['cccd']}</p>
      <p class="field">Mã hồ sơ dự thi: {application_form_dict['ma_ho_so_du_thi']}</p>
      <p class="field">Địa điểm thi: {application_form_dict['dia_diem_du_thi']}</p>
      <p class="field">Thời gian gọi thi sinh: {time}</p>
    </div>

    <div class="section">
      <div class="section-title">THÔNG TIN CÁ NHÂN</div>
      <p class="field">Họ và tên: {application_form_dict['ho_ten']}</p>
      <p class="field">Ngày sinh: {application_form_dict['ngay_sinh']}</p>
      <p class="field">Giới tính: {application_form_dict['gioi_tinh']}</p>
      <p class="field">Dân tộc: {application_form_dict['dan_toc']}</p>
      <p class="field">Trường THPT: {application_form_dict['ten_truong_thpt']}, {application_form_dict['tinh']}</p>
    </div>

    <div class="section">
      <div class="section-title">THÔNG TIN LIÊN LẠC</div>
      <p class="field">Số điện thoại: {application_form_dict['so_dien_thoai']}</p>
      <p class="field">Email: {application_form_dict['email']}</p>
      <p class="field">Địa chỉ liên lạc: {application_form_dict['dia_chi_lien_lac']}</p>
    </div>

    <div>
      <div class="notice-title">THÍ SINH CẦN LƯU Ý</div>
      <p class="notice">1. Có mặt tại phòng thi đúng thời gian quy định.</p>
      <p class="notice">2. Mang theo:
        <br/>- Giấy báo dự thi (bản in)
        <br/>- CCCD bản chính
      </p>
    </div>

  </div>
</body>
</html>
"""
