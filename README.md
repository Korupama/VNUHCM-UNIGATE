(English below)
# VNUHCM-UNIGATE: Cổng thông tin tuyển sinh thông minh cho Kỳ thi Đánh giá năng lực ĐHQG TP.HCM

## Giới thiệu dự án

VNUHCM-UNIGATE là cổng thông tin tuyển sinh thông minh được phát triển để tối ưu hóa quy trình thi và xét tuyển bằng kết quả kỳ thi Đánh giá năng lực (ĐGNL) của Đại học Quốc gia Thành phố Hồ Chí Minh (ĐHQG TP.HCM). Dự án không chỉ là một giải pháp quản lý tuyển sinh mà còn là một ứng dụng hỗ trợ học tập, giúp thí sinh chuẩn bị tốt nhất cho kỳ thi và định hướng ngành học phù hợp.

## Các tính năng chính

* **Quản lý thi ĐGNL và xét tuyển:**
    * Cho phép thí sinh đăng ký dự thi, đăng ký xét tuyển, tra cứu kết quả thi và kết quả xét tuyển.
    * Cung cấp giao diện cho trường thành viên và ĐHQG quản lý và công bố kết quả xét tuyển.
    * Áp dụng phương pháp "lọc ảo" để đảm bảo thí sinh chỉ trúng tuyển vào một nguyện vọng duy nhất (nguyện vọng cao nhất đủ điều kiện).
* **Hỗ trợ thí sinh chuẩn bị cho kỳ thi:**
    * Phát triển bài thi thử trực tuyến dựa trên cấu trúc đề thi mẫu kỳ thi ĐGNL năm 2025.
    * Tích hợp cơ sở dữ liệu tài liệu số (ebooks) từ Thư viện ĐHQG để cung cấp nguồn tài liệu ôn tập phong phú.
* **Phân tích kết quả thi và khuyến nghị ngành học:**
    * Phân tích chi tiết kết quả thi (đặc biệt là kết quả thi cao nhất trong 2 đợt) để chỉ ra điểm mạnh, điểm yếu và đưa ra lời khuyên cải thiện.
    * Xây dựng hệ thống khuyến nghị ngành học phù hợp với năng lực và điểm số của thí sinh dựa trên kết quả thi.
* **Cộng đồng học tập:**
    * Diễn đàn để thí sinh, cựu sinh viên và những người quan tâm trao đổi, chia sẻ kinh nghiệm, phương pháp học tập và thông tin chính thức từ các trường.
* **Tích hợp Trí tuệ nhân tạo:**
    * Chatbot hỗ trợ giải đáp các thắc mắc đơn giản về quy trình tuyển sinh, hồ sơ, ngành học... một cách nhanh chóng và chính xác.
    * Hệ thống tư vấn học thuật và nghề nghiệp dựa trên AI.

## Công nghệ sử dụng

* **Frontend:** ReactJS + REST API + Axios
* **Backend:** Django + FastAPI
* **Hệ thống quản lý phiên bản:** Github
* **Cơ sở dữ liệu:** PostgreSQL (dữ liệu quan hệ), NoSQL (bài đăng, ebook)
* **Trí tuệ nhân tạo:** Chatbots, Hệ thống khuyến nghị ngành học.
* **Xử lý dữ liệu lớn:** Thuật toán "lọc ảo", Hệ thống khuyến nghị ngành học.
* **Công nghệ khác:** Azure Database for PostgreSQL flexible server, Adobe Photoshop.

## Tính khả thi

Thực tế cho thấy, cơ sở hạ tầng công nghệ thông tin của ĐHQG TPHCM hiện nay đã được đầu tư, đổi mới nhằm phục vụ chuyển đổi số, nên chúng tôi tin rằng việc triển khai dự án vào thực tế có tính khả thi cao. Dự án sử dụng các công nghệ hiện đại, phổ biến và có cộng đồng hỗ trợ mạnh mẽ. Việc tích hợp AI (chatbot, khuyến nghị ngành học) cũng đã được chứng minh tính khả thi trong nhiều dự án. Chi phí phát triển và duy trì được đánh giá nằm trong tầm kiểm soát với việc sử dụng mã nguồn mở và dịch vụ điện toán đám mây. Hệ thống được thiết kế để có khả năng mở rộng theo chiều ngang, đáp ứng lượng truy cập lớn trong mùa cao điểm tuyển sinh, đồng thời chú trọng đến bảo mật và dự phòng dữ liệu. Kiến trúc phân tầng cho phép dễ dàng mở rộng và tích hợp tính năng mới trong tương lai.


## Hướng phát triển tương lai

* Tối ưu hiệu suất xử lý dữ liệu và đảm bảo ổn định, đặc biệt vào mùa cao điểm.
* Cải thiện giao diện và trải nghiệm người dùng (UI/UX).
* Phát triển ứng dụng hỗ trợ xét tuyển các trường ngoài ĐHQG TP.HCM sử dụng kết quả ĐGNL.
* Tích hợp các phương thức xét tuyển khác (tuyển thẳng, ưu tiên...).
* Tăng cường bảo mật hệ thống (mã hóa dữ liệu, 2FA...).
* Phát triển phiên bản ứng dụng dành cho thiết bị di động.
* Xây dựng mô hình AI riêng nhằm tối đa cá nhân hóa trong việc tư vấn tuyển sinh.
* Tích hợp Machine Learning để dự đoán xu hướng tuyển sinh.

## Đội ngũ phát triển (Đội: JAPANESE GOBLIN)

* **Huỳnh Hoàng Hưng:** Nhóm trưởng, Fullstack, Viết báo cáo.
* **Nguyễn Hữu Lam Giang:** Database Administrator, Backend Lead, Fullstack.
* **Nguyễn Khánh Vy:** Frontend, Thiết kế poster.
* **Trần Hải Đông:** Fullstack.
* **Nguyễn Xuân Thanh:** Frontend, Thiết kế poster.

## Tài liệu tham khảo

* Trung tâm Khảo thí và Đánh giá Chất lượng đào tạo - Đại học Quốc gia TP.HCM, Đề án tổ chức Kỳ thi Đánh giá năng lực ĐHQG-HCM năm 2025, 2025

---

# VNUHCM-UNIGATE: Smart Admission Portal for VNU-HCM Competency Assessment Exam

## Project Introduction

VNUHCM-UNIGATE is a smart admission portal developed to optimize the process of taking and applying with the results of the Competency Assessment Exam (CAE) of Vietnam National University, Ho Chi Minh City (VNU-HCM). The project is not only an admission management solution but also a learning support application, helping candidates prepare for the exam and orientate towards suitable majors.

## Key Features

* **CAE Exam and Admission Management:**
    * Allows candidates to register for the exam, register for admission, look up exam results and admission results.
    * Provides an interface for member universities and VNU-HCM to manage and announce admission results.
    * Applies a "virtual filtering" method to ensure candidates are admitted to only one nguyện vọng (their highest priority eligible nguyện vọng).
* **Support for Candidates Preparing for the Exam:**
    * Develop online mock tests based on the structure of the 2025 CAE sample test.
    * Integrates a digital document database (ebooks) from the VNU Library to provide a rich source of study materials.
* **Exam Result Analysis and Major Recommendation:**
    * Provides detailed analysis of exam results (especially the highest score from 2 attempts) to identify strengths and weaknesses and offer advice for improvement.
    * Builds a system to recommend suitable majors based on candidates' abilities and scores from the exam results.
* **Learning Community:**
    * A forum for candidates, alumni, and interested individuals to exchange and share experiences, study methods, and official information from universities.
* **Artificial Intelligence Integration:**
    * Chatbot supports answering simple questions about the admission process, hồ sơ, majors, etc., quickly and accurately.
    * AI-based academic and career counseling system.

## Technologies Used

* **Frontend:** ReactJS + REST API + Axios
* **Backend:** Django + FastAPI
* **Version Control System:** Github
* **Database:** PostgreSQL (relational data), NoSQL (posts, ebooks)
* **Artificial Intelligence:** Chatbots, Major Recommendation System.
* **Big Data Processing:** "Virtual filtering" algorithm, Major Recommendation System.
* **Other Technologies:** Azure Database for PostgreSQL flexible server, Adobe Photoshop.

## Feasibility

The project utilizes modern, popular technologies with strong community support. The integration of AI (chatbot, major recommendation) has also proven feasible in many projects. Development and maintenance costs are assessed to be manageable with the use of open-source software and cloud computing services. The system is designed for horizontal scaling to handle high traffic during peak admission season, while also focusing on data security and backup. The layered architecture allows for easy expansion and integration of new features in the future.

## Future Development Directions

* Optimize data processing performance and ensure stability, especially during peak season.
* Improve user interface and user experience (UI/UX).
* Develop an application to support admission applications to universities outside VNU-HCM that also use CAE results.
* Integrate other admission methods (direct admission, priority admission...).
* Enhance system security (data encryption, 2FA...).
* Develop a mobile application version.
* Integrate Machine Learning to predict admission trends.

## Development Team (Team: JAPANESE GOBLIN)

* **Huỳnh Hoàng Hưng:** Team Leader, Fullstack, Report Writing.
* **Nguyễn Hữu Lam Giang:** Database Administrator, Backend Lead, Fullstack.
* **Nguyễn Khánh Vy:** Frontend, Poster Design.
* **Trần Hải Đông:** Fullstack.
* **Nguyễn Xuân Thanh:** Frontend, Poster Design.

## References

* Center for Testing and Quality Assessment of Training - Vietnam National University, Ho Chi Minh City, Project Proposal for the 2025 VNU-HCM Competency Assessment Exam, 2025
