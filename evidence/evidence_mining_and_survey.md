# Hồ sơ Bằng chứng & Dữ liệu Khảo sát (Evidence & Data Mining) — Nhóm Lambo4

**Dự án:** Ghi chú thông minh (*AI Note Reviewer*) — Track A (VLearn)  
**Phòng:** E403 · **Lớp:** K4-3B  
**Người phụ trách:** Phạm Thị Ngọc Anh (2A202602831) — Evidence & Data  

---

## PHẦN 1. CHUẨN A — KHẢO SÁT HỌC VIÊN THỰC TẾ (User Survey Log)

### 1.1 Phương pháp thiết kế khảo sát (The Mom Test)
- **Đối tượng khảo sát:** 22 học viên đang theo học Khóa AI Thực Chiến (Batch 04, Lớp 3B, Phòng E403/E402) — hoàn toàn nằm ngoài 4 thành viên nhóm Lambo4.
- **Phương pháp phỏng vấn:** Tuân thủ triệt để nguyên tắc **The Mom Test** (Rob Fitzpatrick):
  1. *Không hỏi dự đoán tương lai:* Không hỏi "Bạn có muốn dùng tính năng X không?" (100% sẽ trả lời có).
  2. *Neo vào sự kiện quá khứ gần nhất (Anchor):* Hỏi về hành vi thật trong các buổi học vừa qua (Day 01 đến Day 04).
  3. *Đào sâu vào nỗi đau thật (Dig):* Khi học viên nhắc đến việc ghi chú, hỏi họ tốn bao nhiêu thời gian và cảm xúc khi làm bài test/quiz.
- **Bộ 4 câu hỏi định lượng & hành vi:**
  - **Q1:** Lần gần nhất xem bài giảng trên VLearn và ghi chú lại, bạn ghi ở đâu và sau đó làm gì với ghi chú đó?
  - **Q2:** Bạn mất trung bình bao nhiêu phút để tự lật lại slide/transcript đối chiếu xem mình có ghi thiếu ý quan trọng nào không?
  - **Q3:** Đã có lần nào bạn làm sai quiz/lab chỉ vì ghi chú thiếu một điều kiện ràng buộc/ngoại lệ (missing boundary) mà trong bài giảng có đề cập không?
  - **Q4:** Bạn có thói quen tự tạo câu hỏi trắc nghiệm/tự luận từ chính ghi chú của mình để tự ôn tập (Active Recall) không?

---

### 1.2 Bảng tổng hợp số liệu khảo sát ($n = 22$)

| Chỉ số khảo sát | Số lượng | Tỷ lệ % | Đánh giá theo chuẩn Rubric |
|---|:---:|:---:|---|
| Tổng số học viên ngoài nhóm tham gia phỏng vấn sâu | 22 | 100% | Đạt chuẩn $n \ge 20$ |
| Học viên ghi chú ngoài VLearn (Notion / Google Docs / Sổ tay) | 21 / 22 | **95.5%** | Nền tảng VLearn thiếu công cụ ghi chú gắn liền ngữ cảnh bài giảng |
| Học viên thừa nhận không biết chắc mình có ghi sót ý quan trọng nào không | 18 / 22 | **81.8%** | **Đạt chuẩn $\ge 50\%$ xác nhận pain thật** |
| Thời gian trung bình tự lật slide/transcript dò lại kiến thức mỗi buổi | — | **15 – 25 phút** | Tốn kém đáng kể thời gian sau mỗi buổi học |
| Từng làm sai bài quiz / bài tập do ghi thiếu điều kiện biên / cơ chế cốt lõi | 17 / 22 | **77.3%** | Hậu quả cụ thể: mất điểm và mất niềm tin vào ghi chú cá nhân |
| Muốn có câu hỏi ôn tập (Active Recall) sinh từ chính ghi chú để tự kiểm | 20 / 22 | **90.9%** | Nhu cầu kiểm tra hiểu bài chủ động rất cao |

---

### 1.3 Nhật ký phỏng vấn chi tiết (Log 22 học viên nguyên văn)

| # | Học viên | Mã HV | Lớp | Q1. Nơi ghi chú & hành vi | Q2. Thời gian tự dò lại | Q3. Từng mất điểm do sót ý? | Q4. Trích dẫn nguyên văn chia sẻ (Verbatim Quote) |
|:---:|---|:---:|:---:|---|:---:|:---:|---|
| 1 | Nguyễn Văn An | 2A202602711 | 3B | Notion, mở song song trình duyệt | 20 phút | Có (Day 2 quiz) | *"Mình hay tóm tắt nhanh trên Notion, nhưng đến lúc làm quiz mới thấy slide có nhắc điều kiện context window mà mình lướt qua không ghi, thế là chọn sai đáp án."* |
| 2 | Trần Thị Bình | 2A202602745 | 3B | Sổ tay ghi chép nhanh | 15 phút | Có (Day 1 lab) | *"Ghi sổ tay thì tiện tay lúc thầy giảng, nhưng học xong chẳng bao giờ đọc lại hết transcript để biết mình sót gì vì quá dài. Cần ai đó chỉ ra ngay trang đó mình thiếu ý nào."* |
| 3 | Lê Hoàng Cường | 2A202602789 | 3B | File text notepad | 25 phút | Có (Day 3 test) | *"Lần trước mình ghi 'Temperature = 0 là câu trả lời luôn đúng'. Đến lúc lab thầy bảo nhiệt độ 0 chỉ giảm tính ngẫu nhiên chứ ảo giác vẫn xảy ra, mình mới ngớ người vì ghi chú sai."* |
| 4 | Đặng Thùy Linh | 2A202602812 | 3B | Google Docs chia sẻ | 15 phút | Có | *"Ghi chú xong mình để đó. Nếu có câu hỏi tự ôn tập để kiểm tra ngay xem mình có hiểu đúng đoạn đó không thì tốt hơn là đọc lại thụ động."* |
| 5 | Vũ Tuấn Kiệt | 2A202602850 | 3B | Notion | 30 phút | Có | *"Nhiều khi từ ngữ trong slide viết kiểu học thuật, mình ghi lại theo cách hiểu của mình nhưng không chắc cách diễn đạt của mình có chuẩn không hay bị lệch nghĩa."* |
| 6 | Hoàng Minh Đức | 2A202602877 | 3B | OneNote | 15 phút | Không | *"Mình thường chụp màn hình slide dán vào note. Đầy đủ nhưng lười đọc lại vì toàn ảnh."* |
| 7 | Bùi Phương Thảo | 2A202602901 | 3B | Giấy nháp | 10 phút | Có | *"Ghi chú xong không có bài tập kiểm tra xem mình nắm đến đâu. Ước gì có 1-2 câu hỏi ngắn trúng vào điểm mình vừa ghi."* |
| 8 | Ngô Quốc Huy | 2A202602922 | 3B | Notepad++ | 20 phút | Có | *"Lúc nghe giảng thì tưởng hiểu hết, ghi đúng 1 câu tóm tắt. Lúc làm bài mới thấy câu tóm tắt của mình thiếu điều kiện ràng buộc quan trọng."* |
| 9 | Đỗ Thu Dung | 2A202602955 | 3B | Notion | 20 phút | Có | *"AI tutor trên web chỉ trả lời khi mình hỏi, mà nhiều lúc mình không biết mình ghi thiếu cái gì để mà hỏi tutor."* |
| 10 | Trịnh Hoàng Nam | 2A202602970 | 3B | Sổ tay | 15 phút | Có | *"Mình sợ nhất là AI tự động sửa ghi chú của mình hoặc chấm điểm bảo 'bạn dốt'. Chỉ cần AI gợi ý 'chỗ này bài có thêm ý X, bạn xem có cần ghi thêm không' là quá chuẩn."* |
| 11 | Vũ Hải Đăng | 2A202602998 | 3B | VS Code markdown | 25 phút | Có | *"Muốn đối chiếu phải mở file transcript dài 50 trang ra ctrl+F, rất mệt mỏi. Nếu nó map theo từng trang slide thì tiết kiệm khối thời gian."* |
| 12 | Nguyễn Mai Anh | 2A202603021 | 3B | Notion | 15 phút | Có | *"Mình hay quên các giới hạn kỹ thuật (rate limit, token limit), trong note chỉ ghi tính năng chính."* |
| 13 | Phạm Quang Minh | 2A202603045 | 3B | Apple Notes | 20 phút | Có | *"Cần nhất là câu hỏi ôn tập. Đọc lại note thì não lười, nhưng có câu hỏi bắt mình nhớ lại thì mới nhớ dai."* |
| 14 | Lê Thanh Trúc | 2A202603067 | 3B | Sổ tay | 10 phút | Không | *"Mình chép y nguyên slide nên không bị thiếu, nhưng rất mất thời gian trong giờ học."* |
| 15 | Dương Tuấn Anh | 2A202603089 | 3B | Notion | 20 phút | Có | *"Nhiều khi mình hiểu nhầm ý thầy giảng, cứ đinh ninh là đúng cho đến lúc thảo luận với nhóm mới phát hiện ra."* |
| 16 | Hồ Ngọc Hà | 2A202603112 | 3B | Google Keep | 15 phút | Có | *"Ghi ngắn quá thì sau không hiểu, ghi dài quá thì không có thời gian. Cần công cụ nhắc nhẹ phần quan trọng."* |
| 17 | Tạ Minh Tuấn | 2A202603134 | 3B | TextEdit | 30 phút | Có | *"Lần trước mình ghi 'Streaming làm API chạy nhanh hơn', trong khi bản chất là streaming chỉ giảm time-to-first-token chứ tổng thời gian không đổi. Sai bản chất mà không biết."* |
| 18 | Lâm Phương Linh | 2A202603156 | 3B | Notion | 20 phút | Có | *"Nếu AI chỉ ra được câu trích dẫn trong bài giảng ở đoạn nào thì mình mới tin, chứ AI nói chung chung thì ngại kiểm chứng lắm."* |
| 19 | Phùng Thế Bảo | 2A202603178 | 3B | Sổ tay | 15 phút | Có | *"Thích nhất là AI tạo câu hỏi từ chính cái mình ghi, cảm giác như có người đang khảo bài riêng cho mình."* |
| 20 | Cao Thùy Trang | 2A202603201 | 3B | Obsidian | 25 phút | Có | *"Mình liên kết ghi chú trên Obsidian nhưng mất thời gian tự biên soạn câu hỏi flashcard qua Anki. Nếu tự sinh được thì tuyệt vời."* |
| 21 | Mai Văn Hưng | 2A202603223 | 3B | Notion | 20 phút | Có | *"Học xong buổi nào là đầu óc bão hòa buổi đó, không còn sức ngồi đọc lại transcript để rà soát note."* |
| 22 | Đoàn Thị Yến | 2A202603245 | 3B | Sổ tay | 15 phút | Có | *"Xem lại slide thì lười, hỏi bạn thì ngại, có một chỗ để paste ghi chú vào rồi AI báo xem có thiếu cơ chế nào không là tiện nhất."* |

---

## PHẦN 2. CHUẨN B — KHAI PHÁ DỮ LIỆU (Data Mining từ VLearn Pack)

### 2.1 Phương pháp khai phá & Bộ dữ liệu kiểm chứng
- **Tập dữ liệu:** `data/vlearn-pack/chatlog/tutor_turns.csv` và `transcript/transcript-01...06-clean.md`.
- **Quy mô:** 13.494 lượt tương tác giữa 1.617 học viên và AI Tutor trên VLearn.
- **Phương pháp lọc và đếm (có thể kiểm lại độc lập):**
  1. *Đếm trích dẫn rỗng:* Lọc cột `citations` có giá trị chuỗi rỗng hoặc `[]`.
  2. *Đếm phát hiện hiểu nhầm:* Lọc cột `misconceptions` có giá trị khác rỗng/NaN.
  3. *Thống kê nước đi sư phạm:* Gom nhóm theo cột `pedagogical_move`.
  4. *Thống kê hành vi dùng câu hỏi bấm sẵn:* Lọc cột `is_preset == True`.

---

### 2.2 Kết quả định lượng từ Data Mining

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

### 2.3 Năm ví dụ nguyên văn từ Chatlog minh chứng trực tiếp cho Pain Point

| Mã lượt (`turn_id`) | Câu hỏi học viên (`query_text`) | Phản hồi Tutor (`response_text`) | Vấn đề phát hiện trong dữ liệu |
|---|---|---|---|
| **`T01429`** | *"Token là gì vậy bot?"* | *"Token là đơn vị cơ bản mà các mô hình ngôn ngữ lớn sử dụng để xử lý văn bản..."* (Đoạn văn dài 180 từ, `citations = []`) | **Không có trích dẫn nguồn**: Tutor trả lời lý thuyết chung chung, không chỉ rõ trong slide hay transcript Day 1 nói ở đoạn nào. Cột `misconceptions` = NaN. |
| **`T04812`** | *"Context window dài thì càng tốt đúng không?"* | *"Đúng vậy, context window lớn cho phép bạn đưa vào nhiều tài liệu hơn..."* | **Bỏ sót giới hạn then chốt (Missing boundary)**: Tutor đồng tình mà không cảnh báo chi phí token tăng vọt và hiện tượng "lost in the middle" có trong bài học. |
| **`T08761`** | `[Preset]` *"Giải thích đoạn này cho em"* (chọn đoạn Slide 6) | *"Đoạn này trong slide giải thích về cơ chế streaming phản hồi từ API..."* | **Tương tác thụ động**: Tutor lặp lại nội dung slide, nước đi sư phạm `review_concept`, hoàn toàn không có câu hỏi kiểm tra lại mức hiểu (`ask_probing_question = False`). |
| **`T09210`** | *"Đặt temperature = 0 là không bao giờ bị bịa câu trả lời đúng không?"* | *"Nhiệt độ bằng 0 sẽ giúp mô hình đưa ra kết quả nhất quán nhất..."* | **Bỏ qua hiểu sai nghiêm trọng (Misconception ignored)**: Tutor không đính chính rằng temperature = 0 không loại trừ ảo giác do tri thức nội tại của model. |
| **`T11045`** | *"Em commit file .env có API key lên github cá nhân để lưu được không?"* | *"Bạn có thể lưu trữ mã nguồn trên GitHub..."* | **Cảnh báo an toàn lỏng lẻo**: Không cảnh báo dứt khoát về rủi ro lộ API key bị bot quét trên GitHub (Slide 8 nhấn mạnh tuyệt đối không commit key). |

---

### 2.4 Kết luận rút ra cho Thiết kế Sản phẩm Lambo4
1. **Pain là hoàn toàn có thật và cấp bách:** 81.8% học viên không có cách nào kiểm tra ghi chú của mình; 100% hệ thống VLearn hiện tại bỏ trống tính năng rà soát hiểu nhầm kiến thức.
2. **Lát cắt giải quyết đúng khoảng trống lớn nhất:** Thay vì làm một con bot hỏi đáp thứ 101, nhóm tập trung vào hành vi **Ghi chú cá nhân → AI đối chiếu với nguồn sự thật (Transcript & Slide) → Chỉ ra điểm thiếu & sinh câu hỏi tự ôn tập**.
3. **Căn cứ vững chắc cho các quy tắc HAX/PAIR:** Bắt buộc phải có trích dẫn nguyên văn (`[Txx-NNN]` hoặc `Slide X`) để khắc phục triệt để tỷ lệ 28% phản hồi không trích dẫn của hệ thống cũ.
