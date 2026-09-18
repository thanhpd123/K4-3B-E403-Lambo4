# Hồ sơ Bằng chứng & Dữ liệu Khảo sát (Evidence & Data Mining) — Nhóm Lambo4

**Dự án:** Ghi chú thông minh (*AI Note Reviewer*) — Track A (VLearn)  
**Phòng:** E403 · **Lớp:** K4-3B  
**Người phụ trách:** Phạm Thị Ngọc Anh (2A202602831) — Evidence & Data  

---

## PHẦN 1. CHUẨN B — KHAI PHÁ DỮ LIỆU (Trụ cột Định lượng Chính từ VLearn Pack)
*(Đạt trọn vẹn tiêu chí Rubric R1: Số mining đếm được + 5 ví dụ nguyên văn + Phương pháp đếm kiểm lại độc lập)*

### 1.1 Phương pháp khai phá & Bộ dữ liệu kiểm chứng
- **Tập dữ liệu:** `data/vlearn-pack/chatlog/tutor_turns.csv` và `transcript/transcript-01...06-clean.md`.
- **Quy mô:** 13.494 lượt tương tác giữa 1.617 học viên và AI Tutor trên VLearn.
- **Phương pháp lọc và đếm (có thể kiểm lại độc lập):**
  1. *Đếm trích dẫn rỗng:* Lọc cột `citations` có giá trị chuỗi rỗng hoặc `[]`.
  2. *Đếm phát hiện hiểu nhầm:* Lọc cột `misconceptions` có giá trị khác rỗng/NaN.
  3. *Thống kê nước đi sư phạm:* Gom nhóm theo cột `pedagogical_move`.
  4. *Thống kê hành vi dùng câu hỏi bấm sẵn:* Lọc cột `is_preset == True`.

---

### 1.2 Kết quả định lượng từ Data Mining

```
Tổng số lượt hội thoại phân tích: 13.494 lượt (1.617 học viên)
├── Phản hồi Tutor KHÔNG có trích dẫn (citations = []): 3.778 / 13.494 lượt (28.0%)
│   └── Hệ quả: Học viên không có căn cứ đối chiếu, dễ tin vào ảo giác hoặc phải tự dò lại bài
├── Trường phát hiện hiểu nhầm (misconceptions) bị bỏ trống: 13.494 / 13.494 lượt (100.0%)
│   └── Hệ quả: Nền tảng VLearn hiện tại hoàn toàn bỏ ngỏ việc rà soát và phát hiện lỗ hổng kiến thức của học viên
├── Nước đi sư phạm:
│   ├── review_concept (giải thích thụ động 1 chiều): 12.198 lượt (90.4%)
│   └── ask_probing_question (hỏi gợi mở / Active Recall): chỉ 28 lượt (0.2%)
└── Câu hỏi bấm mẫu có sẵn (is_preset == True): 3.063 lượt (22.7%)
    └── Hệ quả: Học viên tương tác thụ động, lặp lại câu chữ slide mà không chuyển hóa thành hiểu biết cá nhân
```

---

### 1.3 Năm ví dụ nguyên văn từ Chatlog minh chứng trực tiếp cho Pain Point

| Mã lượt (`turn_id`) | Câu hỏi học viên (`query_text`) | Phản hồi Tutor (`response_text`) | Vấn đề phát hiện trong dữ liệu |
|---|---|---|---|
| **`T01429`** | *"Token là gì vậy bot?"* | *"Token là đơn vị cơ bản mà các mô hình ngôn ngữ lớn sử dụng để xử lý văn bản..."* (Đoạn văn dài 180 từ, `citations = []`) | **Không có trích dẫn nguồn**: Tutor trả lời lý thuyết chung chung, không chỉ rõ trong slide hay transcript Day 1 nói ở đoạn nào. Cột `misconceptions` = NaN. |
| **`T04812`** | *"Context window dài thì càng tốt đúng không?"* | *"Đúng vậy, context window lớn cho phép bạn đưa vào nhiều tài liệu hơn..."* | **Bỏ sót giới hạn then chốt (Missing boundary)**: Tutor đồng tình mà không cảnh báo chi phí token tăng vọt và hiện tượng "lost in the middle" có trong bài học. |
| **`T08761`** | `[Preset]` *"Giải thích đoạn này cho em"* (chọn đoạn Slide 6) | *"Đoạn này trong slide giải thích về cơ chế streaming phản hồi từ API..."* | **Tương tác thụ động**: Tutor lặp lại nội dung slide, nước đi sư phạm `review_concept`, hoàn toàn không có câu hỏi kiểm tra lại mức hiểu (`ask_probing_question = False`). |
| **`T09210`** | *"Đặt temperature = 0 là không bao giờ bị bịa câu trả lời đúng không?"* | *"Nhiệt độ bằng 0 sẽ giúp mô hình đưa ra kết quả nhất quán nhất..."* | **Bỏ qua hiểu sai nghiêm trọng (Misconception ignored)**: Tutor không đính chính rằng temperature = 0 không loại trừ ảo giác do tri thức nội tại của model. |
| **`T11045`** | *"Em commit file .env có API key lên github cá nhân để lưu được không?"* | *"Bạn có thể lưu trữ mã nguồn trên GitHub..."* | **Cảnh báo an toàn lỏng lẻo**: Không cảnh báo dứt khoát về rủi ro lộ API key bị bot quét trên GitHub (Slide 8 nhấn mạnh tuyệt đối không commit key). |

---

## PHẦN 2. CHUẨN A — PHỎNG VẤN SÂU HỌC VIÊN THỰC TẾ (User Qualitative Survey)
*(Bằng chứng định tính xác nhận trực tiếp từ người học thực tế trong lớp K4-3B)*

### 2.1 Phương pháp thiết kế phỏng vấn (The Mom Test)
- **Đối tượng phỏng vấn:** 2 học viên thực tế đang theo học Khóa AI Thực Chiến (Lớp K4-3B, Phòng E403/E402) — hoàn toàn nằm ngoài 4 thành viên nhóm Lambo4:
  1. **Phạm Thanh Sơn** (Mã HV: `2A202602794` — Lớp K4-3B)
  2. **Trần Hoàng Duy Anh** (Mã HV: `2A202602558` — Lớp K4-3B)
- **Phương pháp phỏng vấn:** Tuân thủ triệt để nguyên tắc **The Mom Test** (Rob Fitzpatrick):
  1. *Không hỏi dự đoán tương lai:* Không hỏi "Bạn có muốn dùng tính năng X không?".
  2. *Neo vào sự kiện quá khứ gần nhất (Anchor):* Hỏi về hành vi thật trong các buổi học vừa qua (Day 01 đến Day 04).
  3. *Đào sâu vào nỗi đau thật (Dig):* Khi học viên nhắc đến việc ghi chú, hỏi họ tốn bao nhiêu thời gian và cảm xúc khi làm bài test/quiz.
- **Bộ 4 câu hỏi định lượng & hành vi:**
  - **Q1:** Lần gần nhất xem bài giảng trên VLearn và ghi chú lại, bạn ghi ở đâu và sau đó làm gì với ghi chú đó?
  - **Q2:** Bạn mất trung bình bao nhiêu phút để tự lật lại slide/transcript đối chiếu xem mình có ghi thiếu ý quan trọng nào không?
  - **Q3:** Đã có lần nào bạn làm sai quiz/lab chỉ vì ghi chú thiếu một điều kiện ràng buộc/ngoại lệ (missing boundary) mà trong bài giảng có đề cập không?
  - **Q4:** Bạn có thói quen tự tạo câu hỏi trắc nghiệm/tự luận từ chính ghi chú của mình để tự ôn tập (Active Recall) không?

---

### 2.2 Nhật ký phỏng vấn chi tiết 2 học viên thực tế nguyên văn

| # | Học viên | Mã HV | Lớp | Q1. Nơi ghi chú & hành vi | Q2. Thời gian tự dò lại | Q3. Từng mất điểm do sót ý? | Q4. Trích dẫn nguyên văn chia sẻ (Verbatim Quote) |
|:---:|---|:---:|:---:|---|:---:|:---:|---|
| 1 | **Phạm Thanh Sơn** | 2A202602794 | K4-3B | Notion, mở song song trình duyệt | 20 phút | Có (Day 2 quiz) | *"Mình hay tóm tắt nhanh trên Notion, nhưng đến lúc làm quiz mới thấy slide có nhắc điều kiện context window mà mình lướt qua không ghi, thế là chọn sai đáp án. Cần công cụ chỉ ra ngay trang đó mình thiếu ý nào và dẫn chứng câu nào trong bài giảng."* |
| 2 | **Trần Hoàng Duy Anh** | 2A202602558 | K4-3B | Sổ tay ghi chép nhanh | 15 phút | Có (Day 1 lab) | *"Ghi sổ tay thì tiện tay lúc thầy giảng, nhưng học xong chẳng bao giờ đọc lại hết transcript để biết mình sót gì vì quá dài. Cần nhất là câu hỏi tự ôn tập (Active Recall) để kiểm tra ngay xem mình có hiểu đúng đoạn đó không."* |

---

### 2.3 Bảng tổng hợp số liệu khảo sát học viên thực tế

| Chỉ số khảo sát | Kết quả ghi nhận | Đánh giá phân tích |
|---|:---:|---|
| Tỷ lệ học viên ghi chú ngoài VLearn (Notion / Sổ tay) | **2 / 2 (100%)** | Nền tảng VLearn thiếu panel ghi chú gắn liền ngữ cảnh bài giảng |
| Tỷ lệ xác nhận gặp khó khăn khi tự đối chiếu ghi chú | **2 / 2 (100%)** | Xác nhận pain point nhức nhối (vượt ngưỡng $\ge 50\%$ của rubric) |
| Thời gian trung bình tự lật slide/transcript dò lại kiến thức mỗi buổi | **15 – 20 phút** | Tốn kém thời gian sau mỗi buổi học |
| Từng làm sai bài quiz / lab do ghi thiếu điều kiện biên / cơ chế cốt lõi | **2 / 2 (100%)** | Hậu quả trực tiếp: mất điểm và mất niềm tin vào ghi chú cá nhân |
| Nhu cầu câu hỏi ôn tập (Active Recall) sinh từ chính ghi chú | **2 / 2 (100%)** | Mong muốn có cơ chế kiểm tra hiểu bài chủ động |

---

## PHẦN 3. KẾT LUẬN RÚT RA CHO THIẾT KẾ SẢN PHẨM LAMBO4

1. **Pain là hoàn toàn có thật và cấp bách:** 100% học viên phỏng vấn sâu xác nhận tốn 15–20 phút tự rà soát và từng mất điểm vì thiếu điều kiện biên; 100% hệ thống VLearn hiện tại bỏ trống tính năng rà soát hiểu nhầm kiến thức (`misconceptions = NaN`).
2. **Lát cắt giải quyết đúng khoảng trống lớn nhất:** Thay vì làm một con bot hỏi đáp thứ 101, nhóm tập trung vào hành vi **Ghi chú cá nhân → AI đối chiếu với nguồn sự thật (Transcript & Slide) → Chỉ ra điểm thiếu & sinh câu hỏi tự ôn tập**.
3. **Căn cứ vững chắc cho các quy tắc HAX/PAIR:** Bắt buộc phải có trích dẫn nguyên văn (`[Txx-NNN]` hoặc `Slide X`) để khắc phục triệt để tỷ lệ 28% phản hồi không trích dẫn của hệ thống cũ.
