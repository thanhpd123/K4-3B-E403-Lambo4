# Bản Tự Đánh Giá & Suy Ngẫm Cá Nhân (Personal Reflection) — Phan Duy Thành

**Họ và tên:** Phan Duy Thành  
**Mã học viên:** 2A202602930  
**Lớp:** K4-3B · **Phòng thi:** E403  
**Vai trò chính:** Đội trưởng · Product Lead  

---

## 1. Vai trò và phần việc cụ thể đảm nhiệm trong dự án
- Là Product Lead và Đội trưởng nhóm Lambo4, tôi trực tiếp chịu trách nhiệm định hướng bài toán từ mốc CP1 đến CP5:
  1. Soạn thảo Canvas 7 dòng, viết trọn vẹn tài liệu AI Spec 9 phần (`spec.md`) chuẩn hóa theo template của chương trình.
  2. Xác định lát cắt sản phẩm: chọn bài toán **Ghi chú thông minh** giải quyết đúng khoảng trống 81.8% học viên ghi chép thiếu ý cốt lõi.
  3. Thiết kế System Prompt và JSON contract cho AI model; trực tiếp xây dựng bộ quy tắc phân loại 4 trạng thái (`correct_complete`, `misconception`, `missing_boundary`, `insufficient_evidence`).
  4. Đề xuất và kiên quyết bảo vệ quyết định kiến trúc: **Conditional Automation / Human-in-the-loop** (không để AI tự ghi đè ghi chú).
  5. Thiết kế slide thuyết trình 6 trang và tổng hợp báo cáo nghiệm thu CP4, CP5.

---

## 2. AI đã hỗ trợ tôi như thế nào trong quá trình làm việc
- Tôi sử dụng Claude và ChatGPT như một người phản biện thiết kế (Design sparring partner):
  - Hỗ trợ rà soát các trường hợp biên của prompt: khi tôi đưa ra các trường hợp ghi chú ngắn hoặc câu hỏi ngoài phạm vi, AI giúp tôi nhận diện những kẽ hở khiến model có thể bịa đặt trích dẫn.
  - Hỗ trợ xây dựng kịch bản 8 lỗi rủi ro theo taxonomy HAX Playbook của Microsoft, giúp nhóm không bỏ sót các trường hợp hiểm hóc.
  - AI giúp tôi tổng hợp và định dạng dữ liệu thô thành các bảng biểu trực quan, tiết kiệm 40% thời gian viết tài liệu.

---

## 3. Bài học lớn nhất rút ra từ một Case Fail của chính nhóm
- **Case fail đáng nhớ nhất:** Tại Lượt chạy 1 của Golden set, tỷ lệ đạt của nhóm chỉ là **75.0% (15/20 cases)**, dưới mức cam kết Quality Bar (80%). Nguyên nhân chính nằm ở việc tôi viết System Prompt quá khắt khe: Rule 10 thúc ép model *"ưu tiên tìm điểm thiếu (missing_boundary)"*, khiến model quá sốt sắng bắt bẻ cả những câu ngắn cộc lốc như *"Token tốt"* hay câu mơ hồ *"Nó nhanh hơn"*.
- **Bài học sâu sắc:** Tôi nhận ra rằng **một prompt quá sốt sắng tìm lỗi cũng độc hại không kém một prompt dễ dãi bỏ qua lỗi**. Trong thiết kế sản phẩm AI, việc biết khi nào nên **"thừa nhận chưa đủ căn cứ" (Graceful Failure - HAX G10)** quan trọng hơn nhiều so với việc cố gắng đưa ra câu trả lời trong mọi hoàn cảnh. Sau khi tôi bổ sung quy tắc dứt khoát đưa các câu dưới 15 ký tự về `insufficient_evidence`, tỷ lệ đạt nhảy vọt lên **95.0%**.

---

## 4. Cam kết đối với quy định "Vibe-coding Rule"
- Tôi nắm vững 100% cấu trúc file `spec.md`, logic phân luồng trong System Prompt và cam kết Quality Bar. Tôi sẵn sàng trả lời độc lập và tự tin mọi câu hỏi phản biện từ Ban giám khảo về lý do thiết kế, quyết định đánh đổi (trade-offs) và nguyên lý kiểm soát chất lượng của sản phẩm.
