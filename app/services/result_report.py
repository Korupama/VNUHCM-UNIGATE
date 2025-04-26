def get_result_report(result_form_dict):
    return f"""
        <html>
        <head> 
            <style>
            body {{
                font-family: "Times New Roman", Times, serif;
            }}
            </style>
        </head>
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