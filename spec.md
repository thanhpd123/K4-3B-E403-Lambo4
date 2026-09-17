# AI SPEC — Ghi chú thông minh · Nhóm Lambo4 · Zone E403

Hướng: [x] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới

> Lát cắt: **Ghi chú thông minh** — AI so ghi chú của học viên với transcript + slide để sinh câu hỏi ôn tập và chỉ ra kiến thức bị ghi sót.

## §1. User & Job

- **Job executor + workflow:** Học viên đang xem bài giảng trên VLearn, vừa ghi chú xong những ý mình cho là quan trọng (hiện tại ghi ngoài: giấy / Notion / tự nhớ). Sau buổi học muốn kiểm tra lại xem mình có ghi sót ý nào không.
  Workflow: mở bài giảng → học (xem slide, đọc transcript) → ghi chú → dán ghi chú vào công cụ → nhận danh sách "ý có trong bài nhưng chưa thấy trong ghi chú" kèm nguồn + câu hỏi ôn tập từ chính ghi chú.
- **Core JTBD** (không tên sản phẩm/AI): Khi tôi ghi chú xong một buổi học, tôi muốn biết mình đã ghi đủ các ý quan trọng chưa và có câu hỏi để tự ôn, để đến lúc ôn không bỏ sót phần nào.
- **Problem statement** (KHÔNG chữ AI): Học viên ghi chú xong không biết mình có ghi sót ý quan trọng nào không, và không có câu hỏi ôn tập từ chính ghi chú → đến lúc ôn không biết mình thiếu phần nào.
- **Evidence:**
  - Số liệu mining: VLearn hiện **không có tính năng ghi chú cá nhân** trong trang học. Data có sẵn "nguồn sự thật" để so: `6 transcript` có mã đoạn `[Txx-NNN]` + `2 bộ slide` (d1, d2).
  - Khảo sát nhanh `XX` học viên: `XX/XX` ghi chú nhưng không biết mình ghi sót ý nào; `XX/XX` muốn có câu hỏi ôn tập từ chính ghi chú. *(điền số thật sau khi chạy khảo sát)*
  - ≥5 quote/ví dụ nguyên văn + nguồn: *(bổ sung sau khảo sát — lưu log trong repo)*

## §2. Impact & quyết định chọn

| Ứng viên                                                                | Bao nhiêu người             | Tần suất         | Tốn gì mỗi lần                   | Khả thi                        |
| ----------------------------------------------------------------------- | --------------------------- | ---------------- | -------------------------------- | ------------------------------ |
| **Ghi chú thông minh** (so ghi chú ↔ transcript/slide + câu hỏi ôn tập) | Mọi học viên có ghi chú     | Sau mỗi buổi học | 10–15 phút tự dò lại             | Cao — data đủ nguồn sự thật    |
| Tóm tắt bài giảng tự động                                               | Mọi học viên                | Mỗi buổi         | Sinh sẵn làm học viên bỏ ghi chú | Trung bình                     |
| Tutor trả lời có trích dẫn                                              | Học viên có câu hỏi         | Lúc hỏi          | Dò lại slide                     | Trung bình — nhiều nhóm đã làm |
| Learning Trace (bản đồ ôn tập cá nhân)                                  | Học viên có lịch sử hỏi–đáp | Sau buổi học     | Không biết bắt đầu từ đâu        | Thấp — cần nhiều log hơn       |

- **Ứng viên ĐÃ LOẠI + vì sao:**
  - *Tóm tắt bài giảng tự động:* thay học viên làm việc ghi chú → làm lười việc học chủ động, lệch mục tiêu "hỗ trợ ôn tập".
  - *Tutor trả lời có trích dẫn:* không mới, đã có nhiều nhóm khoá trước làm.
  - *Learning Trace:* phạm vi rộng hơn, phụ thuộc lịch sử hỏi–đáp — lát cắt đầu cần nhỏ hơn.
- **Ứng viên CHỌN + vì sao:** *Ghi chú thông minh* — tác động trực tiếp lên hành vi ghi chú của mọi học viên (tần suất cao: mỗi buổi học), và data đã có sẵn "nguồn sự thật" (transcript có mã đoạn + slide) để so được, không cần thu thập thêm.

## §3. Giải pháp tương tự đã nghiên cứu

- **Notion (ghi chú):** flow — ghi tự do, tổ chức theo trang. Đáng học: ghi nhanh, linh hoạt. Đáng né: không đối chiếu nội dung với bài học. Mình khác: chủ động so ghi chú với nguồn sự thật của bài.
- **Anki / Quizlet (flashcard):** flow — người dùng tự tạo câu hỏi rồi ôn lặp. Đáng học: ôn tập chủ động. Đáng né: mất thời gian tự tạo câu hỏi. Mình khác: câu hỏi sinh tự động từ chính ghi chú + bài học.
- **Notion AI / công cụ tóm tắt:** flow — tóm tắt, sinh câu hỏi từ văn bản. Đáng học: sinh câu hỏi nhanh. Đáng né: kết luận mức độ hiểu, thiếu nguồn trích dẫn. Mình khác: chỉ ra "ý thiếu" kèm nguồn `[Txx-NNN]`, không kết luận hiểu sai.

## §4. Thiết kế

- **Lát cắt MỘT CÂU:** Một học viên · vừa ghi chú xong một buổi học trên VLearn · AI so ghi chú với transcript + slide để quyết định ý quan trọng nào chưa được ghi và sinh câu hỏi ôn tập từ chính ghi chú · học viên biết mình thiếu kiến thức gì và có câu hỏi để tự kiểm.
- **Non-goals (KHÔNG build):**
  1. Không kết luận "bạn hiểu sai / không hiểu" — ghi chú là tóm tắt chủ quan.
  2. Không tự sửa ghi chú của học viên.
  3. Không sinh nội dung bài giảng mới / tài liệu thay thế bài giảng.
  4. Không chấm điểm bài kiểm tra.
- **Mức prototype nhắm tới:** [x] Mock → Working. **Phần thật:** lời gọi AI đối chiếu ghi chú ↔ transcript/slide + sinh câu hỏi ôn tập. **Phần mock:** giao diện ghi chú còn lại trên VLearn.
- **Automation:** [ ] augment  [x] conditional  [ ] automate — **lý do theo cost-of-error:** kết luận sai về mức hiểu làm học viên ôn lệch trọng tâm, mất niềm tin → AI chỉ gợi ý "ý chưa thấy trong ghi chú" kèm nguồn, học viên tự quyết định bổ sung hay không.
- **§4b. Nguyên tắc đã áp dụng (HAX/PAIR):**

| Nguyên tắc                                 | Áp cụ thể vào đâu trong prototype                                            |
| ------------------------------------------ | ---------------------------------------------------------------------------- |
| HAX G1 — Make clear what the system can do | Đầu luồng nêu rõ: AI chỉ "so sánh & gợi ý", không chấm đúng/sai              |
| HAX G2 — Show contextually relevant info   | Mỗi ý thiếu đều kèm nguồn `[Txx-NNN]` / slide tương ứng                      |
| HAX G3 — Time matters                      | Trả kết quả ngay sau khi học viên dán ghi chú, có loading state              |
| HAX — Support efficient correction         | Học viên đánh dấu "ý này tôi đã ghi rồi" để hệ thống cập nhật, không lặp lại |
| PAIR — Design for human control            | Học viên là người quyết định bổ sung / giữ nguyên ghi chú                    |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8)

| #   | Lớp               | Kịch bản                                           | Cách xử lý                                            |
| --- | ----------------- | -------------------------------------------------- | ----------------------------------------------------- |
| 1   | Đầu vào thiếu     | Ghi chú quá ngắn, không đủ ngữ cảnh để đối chiếu   | Yêu cầu học viên bổ sung ghi chú, không đoán          |
| 2   | Đầu vào thiếu     | Ghi chú diễn đạt khác từ nhưng đúng ý (paraphrase) | Đối chiếu theo ý (semantic), không so khớp từ         |
| 3   | Nguồn sự thật     | Transcript/slide không khớp mã đoạn `[Txx-NNN]`    | Nếu không truy xuất được nguồn → nói "chưa đủ căn cứ" |
| 4   | Nguồn sự thật     | AI bịa mã nguồn không tồn tại                      | Validator kiểm tra mã nguồn trước khi trả về          |
| 5   | Đầu ra lệch       | Câu hỏi ôn tập lạc đề so với bài                   | Chỉ sinh câu hỏi từ ý đã xác định được nguồn          |
| 6   | Đầu ra lệch       | AI kết luận "bạn không hiểu ý X"                   | Cấm mẫu câu kết luận mức hiểu trong system prompt     |
| 7   | Giới hạn hệ thống | Ghi chú quá dài vượt giới hạn token                | Chia đoạn, đối chiếu từng phần rồi gộp kết quả        |
| 8   | Ngoài phạm vi     | Học viên yêu cầu chấm điểm / chữa bài              | Từ chối rõ và giải thích phạm vi của công cụ          |

## §6. Bốn đường đi của trải nghiệm

- **Happy path:** Học viên dán ghi chú → AI trả danh sách "ý có trong bài nhưng chưa thấy trong ghi chú" kèm nguồn `[Txx-NNN]` + câu hỏi ôn tập từ chính ghi chú.
- **Low-confidence (②):** Signal yếu (ghi chú quá ngắn / nguồn mơ hồ) → AI nói "chưa đủ căn cứ", gợi ý bổ sung ghi chú, chỉ đưa những ý chắc chắn.
- **Failure / không căn cứ (①):** Không truy xuất được nguồn phù hợp → nói rõ "chưa đủ căn cứ", không bịa nguồn, không sinh câu hỏi.
- **Correction (user sửa):** Học viên đánh dấu "ý này tôi đã ghi rồi" → hệ thống ghi nhận, loại khỏi danh sách thiếu và không lặp lại ở lần sau.
- **Khi bị đòi ngoài phạm vi (③):** Yêu cầu chấm điểm/chữa bài → từ chối kèm giải thích phạm vi.
- **Case đặc thù domain (④):** Thuật ngữ chuyên môn trong transcript → giữ nguyên thuật ngữ gốc, giải thích ngắn nếu có trong slide.

## §7. Kiểm thử

- **Chiều chất lượng + định nghĩa kiểm chứng được:**
  1. *Đối chiếu không sót ý quan trọng* — danh sách "ý thiếu" phủ đúng các ý chính trong bài (so với đáp án golden set).
  2. *Câu hỏi ôn tập có căn cứ* — mỗi câu hỏi phải trỏ được về một nguồn `[Txx-NNN]`/slide đúng.
  3. *Không kết luận mức hiểu* — không xuất hiện mẫu câu "bạn hiểu sai/không hiểu".
- **Golden set (≥20 case):** 20 case gồm: ghi chú đầy đủ (5) · thiếu 1–2 ý (5) · paraphrase khác từ (3) · ghi chú quá ngắn (2) · ghi chú lạc đề (2) · ghi chú dài nhiều đoạn (2) · yêu cầu ngoài phạm vi (1). File trong `eval/`.
- **Quality bar** (chốt từ hạn chốt spec, giữ nguyên sau đó): "Đạt khi ≥ 80% case qua bộ, và 0 case bịa nguồn / kết luận mức hiểu."
- **Kết quả các lượt chạy** (bảng % — cập nhật đến trước CP6):

| Lượt chạy | Thời điểm | Đạt/tổng | %   | Ghi chú          |
| --------- | --------- | -------- | --- | ---------------- |
| Lần 1     | —         | —        | —   | *(cập nhật sau)* |

## §8. Phân công & kế hoạch

- **Phân công có tên:**
  - **Phan Duy Thành (2A202602930)** — Đội trưởng · product lead: canvas/spec, system prompt, output contract.
  - **Phạm Thị Ngọc Anh (2A202602831)** — evidence & data: khảo sát học viên, mining transcript/slide, golden set.
  - **Võ Đức Tài (2A202603007)** — prototype: build luồng ghi chú + lời gọi AI thật (đối chiếu ghi chú ↔ transcript/slide).
  - **Đỗ Đình Long (2A202602673)** — UI & validate: giao diện, 4 đường trải nghiệm, user test + changelog.
- **Willing users (≥2 tên) + kế hoạch validation:** `[Tên 1]`, `[Tên 2]` *(điền tên thật đã khai từ CP1)* — kế hoạch: giao task "dán ghi chú của buổi học gần nhất" rồi ngồi quan sát, ghi quote nguyên văn, làm ở CP5 trong `validation/`.
- **Multi-prototype (nếu làm):** *(chưa làm — bổ sung nếu có ≥2 phương án)*

## §9. Changelog

| Thời điểm  | Đổi gì                          | Vì sao (trỏ về feedback/case nào) |
| ---------- | ------------------------------- | --------------------------------- |
| 17/9 (CP1) | Chốt canvas 7 dòng + khung spec | Khởi tạo từ canvas-cp1            |
