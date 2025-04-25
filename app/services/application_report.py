

def get_report_application( application_form_dict: dict, time: str):
    return f"""
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
                {application_form_dict['ma_ho_so_du_thi']}</div>
        </div>
        </body>
        </html>

        """