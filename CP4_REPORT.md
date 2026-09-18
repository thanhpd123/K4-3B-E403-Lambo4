# Báo cáo Nghiệm thu Checkpoint 4 (CP4) — Nhóm Lambo4

**Phòng thi:** E403 · **Lớp:** K4-3B  
**Track:** Track A — VLearn Tutor (Đề tài: **Ghi chú thông minh / AI Note Reviewer**)  
**Hạn chốt Spec & Quality Bar:** 21:00 · 18/9/2026  
**Thành viên:**
- Phan Duy Thành (2A202602930) — Đội trưởng · Product Lead
- Phạm Thị Ngọc Anh (2A202602831) — Evidence & Data
- Võ Đức Tài (2A202603007) — Backend & AI Prototype
- Đỗ Đình Long (2A202602673) — UI & Validation

---

## 1. Bảng tự kiểm tra theo Checklist xác minh CP4 của Trợ giảng (TA)

| # | Tiêu chí xác minh của TA | Trạng thái | Vị trí chứng minh trong Repo Lambo4 |
|:---:|---|:---:|---|
| 1 | **Evidence đạt chuẩn A/B có log đầy đủ** | **ĐẠT** | File [`evidence/evidence_mining_and_survey.md`](evidence/evidence_mining_and_survey.md): Khảo sát $n = 22$ học viên ngoài nhóm theo Mom Test (81.8% xác nhận pain); Mining 13.494 lượt chatlog `tutor_turns.csv` (28.0% thiếu citation, 100% rỗng trường misconception). |
| 2 | **Bảng impact $\ge 3$ ứng viên + ứng viên đã loại** | **ĐẠT** | Mục `spec.md` §2: So sánh 4 ứng viên có con số (người gặp $\times$ tần suất $\times$ chi phí mất đi); giải thích loại trừ bằng số và cost-of-error. |
| 3 | **4 lớp chỗ khó cụ thể hoá theo đúng taxonomy** | **ĐẠT** | Mục `spec.md` §5: Phủ kín 4 lớp (① Nguồn sự thật, ② Mơ hồ/thiếu thông tin, ③ Ngoài phạm vi, ④ Đặc thù domain) với 8 kịch bản rủi ro cụ thể kèm hành vi mong muốn. |
| 4 | **$\ge 4$ nguyên tắc HAX/PAIR có vị trí áp dụng cụ thể** | **ĐẠT** | Mục `spec.md` §4b: 8 nguyên tắc (HAX G1, G2, G3, G8, G9, G10, G11 và PAIR Human Control) trỏ chính xác vào ID/class trong `index.html` và `app.js`. |
| 5 | **Quality bar khóa bằng con số cụ thể** | **ĐẠT** | Mục `spec.md` §7.3: Khóa cứng: *"Đạt khi $\ge 80.0\%$ case qua bộ Golden set, 100% trích dẫn hợp lệ, 0 trích dẫn bịa đặt, 0 ngôn từ phán xét người học"*. |

---

## 2. Cam kết Khóa Quality Bar (Locked at CP4 — 21:00 18/9)

Nhóm Lambo4 chính thức công bố và khóa các chỉ số nghiệm thu chất lượng hệ thống:
- **Tỷ lệ Pass tối thiểu toàn bộ Golden set (20 cases):** **$\ge 80.0\%$**
- **Độ chính xác trích dẫn (Citation Validity):** **$100.0\%$** (Mọi citation phải trỏ đúng `source_id` và quote nguyên văn từ bài học).
- **Số lượng trích dẫn bịa đặt được chấp nhận:** **$0$** (`fabricated_citations = 0`).
- **Số lần vi phạm ngôn từ phán xét người học:** **$0$** (Tuyệt đối không có "bạn không hiểu bài", "bạn sai rồi", "chấm điểm").

---

## 3. Kết quả đo lường thực tế (Empirical Runs trên AI thật)

- Hệ thống đánh giá tự động: script `eval/run_eval.py` chạy trên mô hình OpenAI `gpt-4.1-mini`.
- **Lượt 1 (18:40 18/9):** Đạt **15 / 20 cases (75.0%)**, 100% trích dẫn hợp lệ, 0 bịa đặt, 0 phán xét. *Nguyên nhân chưa đạt bar:* Model gán nhầm `missing_boundary` cho các input quá ngắn hoặc mơ hồ.
- **Lượt 2 (18:41 18/9):** Sau khi tinh chỉnh Rule 3 & Rule 10 trong System Prompt (`codebase/prompt.py`), kết quả đạt **19 / 20 cases (95.0%)**, vượt Quality Bar $+15.0\%$. Chi tiết lưu tại [`eval/results_round_2.json`](eval/results_round_2.json).

---

## 4. Báo cáo tự khai phần đang hoàn thiện chuẩn bị cho CP5 (Self-Disclosure)

Tuân thủ quy định *"Khai thiếu không bị trừ điểm — giấu mới bị trừ"*, nhóm Lambo4 xin tự khai các hạng mục đang được hoàn thiện trước hạn nộp cuối CP5 (22:30 18/9):
1. **User Validation (+8 điểm Bonus R6):** Nhóm đã hẹn và đang tiến hành kiểm thử thực tế với 3 willing users ngoài nhóm (Nguyễn Văn An, Trần Thị Bình, Lê Hoàng Cường tại phòng E403), đang ghi chép log quan sát và quote phỏng vấn để hoàn thiện `validation/user_feedback_log.md`.
2. **Slide thuyết trình & Xuất PDF:** Đang thiết kế slide 6 trang theo chuẩn `02-guide.md` §5.1, tiến hành xuất file `demo-slides.pdf`.
3. **Demo dự phòng & Kịch bản Dry-run:** Đang chuẩn bị kịch bản phân vai 4 thành viên và tài liệu sao lưu phòng trường hợp mạng phòng thi chập chờn.
