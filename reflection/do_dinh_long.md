# Bản Tự Đánh Giá & Suy Ngẫm Cá Nhân (Personal Reflection) — Đỗ Đình Long

**Họ và tên:** Đỗ Đình Long  
**Mã học viên:** 2A202602673  
**Lớp:** K4-3B · **Phòng thi:** E403  
**Vai trò chính:** UI & User Validation Lead  

---

## 1. Vai trò và phần việc cụ thể đảm nhiệm trong dự án
- Là UI & User Validation Lead, tôi chịu trách nhiệm về cảm nhận và trải nghiệm tương tác của người học:
  1. Xây dựng giao diện web mô phỏng không gian học tập VLearn (`codebase/templates/index.html` và `static/style.css`), bao gồm thanh điều hướng slide, iframe viewer và panel ghi chú bên phải.
  2. Lập trình luồng JavaScript tương tác (`codebase/static/app.js`) hiện thực hóa đầy đủ 4 đường trải nghiệm (Happy path, Low confidence, Failure/Không căn cứ, Correction path).
  3. Hiện thực hóa các nguyên tắc HAX Toolkit của Microsoft:
     - HAX G1: Dòng thông báo helper làm rõ phạm vi hệ thống.
     - HAX G2/G11: Hiển thị độ tin cậy và chi tiết thẻ trích dẫn `<details class="citation">`.
     - HAX G3: Trạng thái xoay loading `#loading` ngăn bấm trùng request.
     - HAX G8/G9: Nút bấm thao tác nhanh và vùng bản nháp `#draftArea`.
   4. Trực tiếp tổ chức các phiên User Testing với 2 học viên ngoài nhóm (Phạm Thanh Sơn, Trần Hoàng Duy Anh), ghi chép nhật ký kiểm thử và đo lường chỉ số Sean Ellis PMF tại `validation/user_feedback_log.md`.
   5. Chuyển hóa các phản hồi người dùng thành 2 cải tiến tính năng cụ thể trên giao diện trước giờ nộp CP5.

---

## 2. AI đã hỗ trợ tôi như thế nào trong quá trình làm việc
- AI giúp tôi đẩy nhanh tốc độ xây dựng giao diện và tối ưu UX:
  - Hỗ trợ viết CSS Flexbox/Grid hiện đại, tối ưu responsive và tạo các hiệu ứng micro-animations tinh tế cho các nút bấm và trạng thái loading.
  - Hỗ trợ xây dựng kịch bản phỏng vấn think-aloud trung tính theo chuẩn Stanford CS177, giúp tôi giữ được sự im lặng và khách quan khi quan sát người dùng thật thao tác.
  - Gợi ý cách thiết kế bảng bản nháp sau rà soát (`#draftArea`) sao cho việc so sánh giữa câu ghi chú cũ và câu sửa mới trực quan nhất.

---

## 3. Bài học lớn nhất rút ra từ một Case Fail của chính nhóm
- **Case fail đáng nhớ nhất:** Trong phiên test với bạn Trần Hoàng Duy Anh, khi AI phát hiện ra một điều kiện bị ghi thiếu (`missing_boundary`), bạn Duy Anh bảo rằng: *"Ý này mình đã biết rồi, nhưng lười ghi vào note thôi. Giao diện cứ hiện đỏ/vàng bắt mình phải sửa nháp làm mình thấy bị ép buộc."* Lúc đó tôi mới nhận ra giao diện của mình đang thiếu cơ chế **Gạt bỏ dễ dàng (HAX G8)**.
- **Bài học sâu sắc:** Tôi hiểu rằng **không phải mọi gợi ý của AI người dùng đều muốn đưa vào ghi chú**. Một thiết kế tôn trọng người dùng phải cho phép họ từ chối hoặc bỏ qua một cách nhẹ nhàng. Ngay sau buổi test, tôi đã thêm nút **"Đã biết rồi"** và hiệu ứng làm mờ thẻ (`opacity: 0.5`). Thay đổi nhỏ này đã khiến bạn Duy Anh mỉm cười hài lòng và chấm điểm trải nghiệm tăng vọt.

---

## 4. Cam kết đối với quy định "Vibe-coding Rule"
- Tôi làm chủ toàn bộ mã nguồn giao diện HTML, CSS, JavaScript và phương pháp luận của vòng User Validation. Tôi sẵn sàng thao tác trực tiếp trên màn hình, giải thích từng quyết định UI/UX và trả lời mọi câu hỏi của Ban giám khảo tại buổi thuyết trình CP6.
