# Bản Tự Đánh Giá & Suy Ngẫm Cá Nhân (Personal Reflection) — Phạm Thị Ngọc Anh

**Họ và tên:** Phạm Thị Ngọc Anh  
**Mã học viên:** 2A202602831  
**Lớp:** K4-3B · **Phòng thi:** E403  
**Vai trò chính:** Evidence & Data Lead  

---

## 1. Vai trò và phần việc cụ thể đảm nhiệm trong dự án
- Là Evidence & Data Lead, tôi chịu trách nhiệm tạo nên nền móng sự thật vững chắc cho dự án:
  1. Thiết kế bảng hỏi và tiến hành phỏng vấn sâu học viên ngoài nhóm trong lớp K4-3B theo nguyên tắc **The Mom Test** (Rob Fitzpatrick), ghi chép đầy đủ log từng câu hỏi và từng câu trả lời nguyên văn.
  2. Khai phá bộ dữ liệu thật `data/vlearn-pack/chatlog/tutor_turns.csv` với 13.494 lượt tương tác; trích xuất các con số đắt giá: 28.0% phản hồi không có trích dẫn, 100% cột misconception bị bỏ trống, 90.4% tương tác thụ động một chiều.
  3. Lọc ra 5 ví dụ đối thoại nguyên văn có mã `turn_id` xác thực minh chứng trực tiếp cho 4 lớp chỗ khó.
  4. Cùng Đội trưởng xây dựng bộ Golden set 20 cases (`eval/golden_set.json`), trong đó có 11 cases trích xuất trực tiếp từ chatlog và transcript của khóa học.
  5. Viết tài liệu `evidence/evidence_mining_and_survey.md` đáp ứng toàn diện cả Chuẩn A và Chuẩn B.

---

## 2. AI đã hỗ trợ tôi như thế nào trong quá trình làm việc
- Tôi sử dụng các script Python hỗ trợ bởi AI để phân tích dữ liệu:
  - Viết code pandas nhanh để lọc và gom cụm các cột `citations`, `misconceptions`, `pedagogical_move` trong tập 13.494 dòng.
  - Sử dụng AI để gợi ý các biến thể paraphrase câu chữ tự nhiên cho bộ Golden set (dựa trên cách học viên hay ghi chép thực tế), giúp bộ test không bị trùng lặp ngôn từ.
  - Nhờ AI rà soát xem các câu hỏi khảo sát của tôi có vô tình mắc bẫy "hỏi ý kiến tương lai" (pitching ý tưởng) hay không, giúp bộ câu hỏi bám sát chuẩn Mom Test.

---

## 3. Bài học lớn nhất rút ra từ một Case Fail của chính nhóm
- **Case fail đáng nhớ nhất:** Trong quá trình khai phá dữ liệu ban đầu, tôi từng cố gắng tìm kiếm các bằng chứng về việc học viên chê AI Tutor trên kênh Discord để chứng minh pain. Tuy nhiên, sau khi lọc 1.092 tin nhắn Discord, tôi nhận ra phần lớn tin nhắn tuần đầu chỉ xoay quanh thủ tục hành chính và deadline (bài toán của Track B), không phản ánh đúng hành vi ghi chép trong trang học VLearn.
- **Bài học sâu sắc:** Tôi hiểu rằng **dữ liệu phải đi liền với ngữ cảnh của người dùng (contextual data)**. Thay vì lấy dữ liệu lệch kênh, tôi quay trở lại khai phá trực tiếp `tutor_turns.csv` và tiến hành phỏng vấn sâu học viên thực tế ngoài nhóm đang ngồi học trong phòng E403. Việc **100% học viên phỏng vấn sâu thừa nhận không biết mình ghi thiếu gì** và **từng mất điểm quiz** đã trở thành bằng chứng đắt giá kết hợp cùng trụ cột khai phá 13.494 lượt chatlog giúp nhóm thuyết phục được Trợ giảng và Ban giám khảo.

---

## 4. Cam kết đối với quy định "Vibe-coding Rule"
- Tôi nắm rõ từng con số trong file `evidence_mining_and_survey.md`, phương pháp đếm dữ liệu và nội dung phỏng vấn sâu học viên thực tế ngoài nhóm. Tôi tự tin bảo vệ tính trung thực và phương pháp luận của toàn bộ dữ liệu trước Ban giám khảo tại buổi thuyết trình CP6.
