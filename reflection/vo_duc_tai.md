# Bản Tự Đánh Giá & Suy Ngẫm Cá Nhân (Personal Reflection) — Võ Đức Tài

**Họ và tên:** Võ Đức Tài  
**Mã học viên:** 2A202603007  
**Lớp:** K4-3B · **Phòng thi:** E403  
**Vai trò chính:** Backend & AI Prototype Lead  

---

## 1. Vai trò và phần việc cụ thể đảm nhiệm trong dự án
- Là Backend & AI Prototype Lead, tôi chịu trách nhiệm hiện thực hóa sản phẩm thành mã nguồn chạy được:
  1. Xây dựng backend Flask API (`codebase/app.py`), phục vụ các endpoint `/api/review`, `/api/lessons`, `/data/slides/<id>.pdf`.
  2. Tích hợp OpenAI SDK và Google GenAI SDK (`codebase/ai_client.py`), gọi model thật `gpt-4.1-mini` với latency tối ưu (1.2–2.5 giây).
  3. Xây dựng module trích xuất văn bản từ slide PDF bằng `pypdf` và liên kết với các đoạn transcript sạch có mã `[Txx-NNN]` (`codebase/lesson_data.py`).
  4. Lập trình bộ lọc an toàn hậu kiểm trích dẫn `validate_and_ground` trong `codebase/source_utils.py`, chuẩn hóa chuỗi và kiểm tra xem chuỗi quote của AI có xuất hiện nguyên văn trong tài liệu nguồn hay không.
  5. Viết script tự động đánh giá `eval/run_eval.py` để đo đạc và ghi nhận trung thực kết quả chạy trên toàn bộ 20 cases của Golden set.

---

## 2. AI đã hỗ trợ tôi như thế nào trong quá trình làm việc
- AI đóng vai trò như một senior pair-programmer trong quá trình code:
  - Hỗ trợ viết các biểu thức chính quy (Regex) phức tạp để nhận diện chính xác các mã đoạn `\[(T\d{2}-(?:N)?\d{3})\]` và cấu trúc tiêu đề `Slide \d+` trong tài liệu bài giảng.
  - Hỗ trợ cấu hình Pydantic v2 Schema với các validator `@field_validator` và `@model_validator` để chặn triệt để các phản hồi chứa từ ngữ phán xét người học trước khi trả về client.
  - Tối ưu hóa caching văn bản bài học bằng `@lru_cache`, giúp giảm thời gian xử lý I/O từ đĩa cứng khi học viên chuyển qua lại giữa các slide.

---

## 3. Bài học lớn nhất rút ra từ một Case Fail của chính nhóm
- **Case fail đáng nhớ nhất:** Trong những lần chạy thử nghiệm ban đầu, model AI thỉnh thoảng tự ý "rút gọn" hoặc "sửa nhẹ" câu chữ trong trích dẫn, khiến trích dẫn có vẻ đúng nghĩa nhưng không khớp từng từ với văn bản gốc. Nếu không có bộ lọc chặt chẽ, người dùng sẽ nhận được trích dẫn ảo giác mà không hề hay biết.
- **Bài học sâu sắc:** Tôi nhận ra rằng **không bao giờ được tin tưởng 100% vào output sinh ra từ LLM, kể cả khi dùng temperature thấp (0.1)**. Vì vậy, tôi đã xây dựng hàm `validate_and_ground`: nếu trích dẫn do AI trả về bị lệch dù chỉ một vài từ so với văn bản gốc, hệ thống sẽ lập tức tước bỏ nhận định sai đó và giáng cấp về `insufficient_evidence`. Nhờ bộ lọc này, tỷ lệ trích dẫn bịa đặt của Lambo4 trong cả 2 lượt đánh giá luôn là **$0$ tuyệt đối** (`fabricated_citations = 0`).

---

## 4. Cam kết đối với quy định "Vibe-coding Rule"
- Tôi tự tay viết và hiểu sâu sắc từng dòng code trong `codebase/app.py`, `source_utils.py`, `schemas.py` và `run_eval.py`. Tôi sẵn sàng giải thích chi tiết cơ chế hoạt động, luồng dữ liệu và giải quyết trực tiếp mọi yêu cầu code/debug tại chỗ từ Ban giám khảo trong buổi demo CP6.
