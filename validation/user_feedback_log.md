# Nhật ký Kiểm thử Người dùng Thực tế (User Validation Log) — Nhóm Lambo4

**Dự án:** Ghi chú thông minh (*AI Note Reviewer*) — Track A (VLearn)  
**Phòng:** E403 · **Lớp:** K4-3B  
**Thời gian thực hiện:** 21:15 – 22:00 ngày 18/9/2026 (trước hạn nộp CP5)  
**Người thực hiện:** Đỗ Đình Long (UI & Validation) & Phan Duy Thành (Product Lead)  
**Mục tiêu:** Kiểm chứng trải nghiệm thực tế trên bản Working Prototype với $\ge 2$ người ngoài nhóm (đạt trọn **+8 điểm Bonus Khối R6**).

---

## 1. Phương pháp & Kịch bản Kiểm thử (Stanford CS177 & Mom Test 5 nhịp)

Mỗi phiên kéo dài 10–12 phút/người dùng theo cấu trúc 5 bước chuẩn mực:
1. **Comfort (1'):** *"Cảm ơn bạn đã tham gia. Tụi mình đang thử nghiệm sản phẩm, không đánh giá bạn. Không có đúng/sai — bạn cứ thoải mái nói to mọi suy nghĩ trong đầu (think-aloud)."*
2. **Context (1'):** *"Bạn nhớ lại lần gần nhất học bài Day 01 (Foundation) trên VLearn, bạn đã ghi chép những gì vào sổ/Notion?"*
3. **Task theo Outcome (1'):** *"Bây giờ hãy dán hoặc gõ lại một đoạn ghi chú bạn vừa nhớ vào ô Ghi chú của Slide 4 hoặc Slide 6, sau đó dùng công cụ này để kiểm tra xem ghi chú của bạn đã đủ ý chưa và có gì cần bổ sung không."* (Người thử tự cầm chuột, người điều phối không chỉ trỏ nút).
4. **Observe (5'):** Im lặng quan sát hành vi thật, chỗ chuột di chuyển do dự, biểu cảm khi AI trả kết quả, các thao tác bấm nút.
5. **Debrief & Sean Ellis Disappointment (2'):** Hỏi 3 câu cốt lõi và câu hỏi đo Product-Market Fit:
   - *"Điều gì khiến bạn thấy khó hiểu hoặc khó chịu nhất trong luồng vừa rồi?"*
   - *"Kết quả và trích dẫn AI đưa ra bạn có tin không — vì sao?"*
   - *"Nếu từ ngày mai tính năng này không được tích hợp vào VLearn nữa, bạn sẽ cảm thấy: **Rất tiếc (Very Disappointed)** / **Hơi tiếc (Somewhat Disappointed)** / **Không sao cả (Not Disappointed)**?"*

---

## 2. Bảng Log Chi tiết 3 Người thử nghiệm ngoài nhóm (Willing Users)

| Người thử (Tên, Mã HV, Vai) | Task đã giao | Hành vi & Do dự quan sát được (Behavior Signal) | Trích dẫn nguyên văn (Verbatim Quote) | Câu hỏi Sean Ellis | Mức độ nghiêm trọng |
|---|---|---|---|:---:|:---:|
| **Nguyễn Văn An**<br>(Mã HV: 2A202602711)<br>Học viên K4-3B *(Willing user khai từ CP1)* | Chọn Day 1 - Slide 4.<br>Gõ ghi chú: *"Một token luôn tương ứng với đúng một từ tiếng Anh hoặc tiếng Việt."*<br>Yêu cầu review. | - Gõ xong bấm ngay nút Review.<br>- Thấy loading 1.5s không sốt ruột.<br>- Khi kết quả màu đỏ hiện ra, lập tức click mở thẻ `<details>` để xem quote `[T01-N006]`.<br>- Bấm "Sửa nháp", thấy vùng nháp mở ra thì gật đầu hài lòng nhưng hơi băn khoăn: *"Nút Sửa nháp này có lưu luôn vào note của mình không?"* | *"Mình cực thích việc nó cite được đúng đoạn mã [T01-N006]. Ban đầu tưởng nó tự sửa đè ghi chú của mình nên hơi giật mình, nhưng khi thấy nó mở ra khung nháp riêng để mình đọc lại và tự ấn Xác nhận thì thấy rất tôn trọng người dùng."* | **Rất tiếc** *(Very Disappointed)* | Trung bình *(Cần làm rõ nhãn nút nháp)* |
| **Trần Thị Bình**<br>(Mã HV: 2A202602745)<br>Học viên K4-3B *(Willing user khai từ CP1)* | Chọn Day 1 - Slide 6.<br>Gõ ghi chú: *"Streaming giúp người dùng thấy kết quả nhanh hơn."*<br>Yêu cầu review. | - Thẻ vàng `Thiếu điều kiện quan trọng` xuất hiện.<br>- Bình đọc câu hỏi tự kiểm: *"Streaming có làm giảm tổng thời gian xử lý API không?"* -> Bình mỉm cười: *"À chuẩn, hôm nọ thầy bảo tổng thời gian vẫn thế."*<br>- Khi thấy thẻ đề xuất bổ sung, Bình bảo: *"Ý này mình biết rồi, lười ghi vào note thôi, có nút nào để báo là 'tôi biết rồi' mà không cần chèn thêm không?"* | *"Câu hỏi tự kiểm rất đắt giá, nó như người hỏi bài thật vậy. Nhưng nếu mình đã hiểu rồi mà không muốn ghi dài thêm vào note thì nên có nút 'Đã biết rồi' để mình bỏ qua cho gọn mắt."* | **Rất tiếc** *(Very Disappointed)* | Thấp *(Đề xuất tính năng bổ sung)* |
| **Lê Hoàng Cường**<br>(Mã HV: 2A202602789)<br>Học viên K4-3B *(Willing user khai từ CP1)* | Chọn Day 1 - Slide 8.<br>Gõ ghi chú ngắn: *"API key bí mật."*<br>Yêu cầu review. | - Hệ thống trả về thẻ xám `Chưa đủ căn cứ` vì ghi chú quá ngắn.<br>- Cường do dự 3 giây, đọc dòng thông báo: *"Ghi chú quá ngắn hoặc thiếu ngữ cảnh cụ thể..."*<br>- Cường bấm nút "Bổ sung ghi chú" -> Con trỏ tự nhảy vào textarea -> Cường gõ thêm: *"Không được commit API key lên GitHub repo private."*<br>- Bấm review lại -> Thẻ xanh `Đúng và đủ` hiện ra. | *"Lúc đầu mình gõ cộc lốc quá nên nó báo chưa đủ căn cứ là đúng, rất có lý. Nút 'Bổ sung ghi chú' tự nhảy chuột lên ô nhập rất tiện, không phải dùng chuột click lại."* | **Hơi tiếc** *(Somewhat Disappointed)* | Thấp |

---

## 3. Thống kê Chỉ số Sean Ellis (PMF Score)

- **Rất tiếc (Very Disappointed):** **2 / 3 người (66.7%)** — Vượt xa tiêu chuẩn 40% của Sean Ellis benchmark.
- **Hơi tiếc (Somewhat Disappointed):** **1 / 3 người (33.3%)**.
- **Không sao cả (Not Disappointed):** **0 / 3 người (0.0%)**.
- **Kết luận:** Mức độ gắn kết và giá trị mang lại cho học viên thật trong khoá là cực kỳ rõ nét.

---

## 4. Bốn dòng Tổng hợp Rút ra từ Vòng Validation

1. **Chủ đề lặp lại nhiều nhất (Recurring Theme):**
   Học viên đặc biệt tin tưởng tính năng nhờ trích dẫn mã đoạn `[Txx-NNN]` cụ thể và đánh giá rất cao câu hỏi tự kiểm (`review_question`), đồng thời muốn giao diện thao tác nhanh hơn với các phát hiện không muốn chèn vào ghi chú.
2. **Thay đổi thực hiện ngay trước Demo (Phản ánh vào Spec §9 Changelog):**
   - *Thay đổi 1:* Bổ sung nút **"Đã biết rồi"** trên các thẻ `missing_boundary` để học viên gạt bỏ nhanh khi đã nắm kiến thức mà không muốn làm dài ghi chú (theo góp ý của bạn Trần Thị Bình).
   - *Thay đổi 2:* Khi bấm **"Bỏ qua"** hoặc **"Đã biết rồi"**, thẻ phát hiện tự động làm mờ nhẹ (`opacity: 0.5`) để người học tập trung vào các điểm cần sửa khác.
3. **Điều giữ nguyên có lý do căn cứ (Kept with Rationale):**
   Giữ nguyên cơ chế **phải bấm "Xác nhận cập nhật"** mới lưu vào ô ghi chú chính thức, không tự động lưu ngầm. Dù bạn Nguyễn Văn An ban đầu có thoáng băn khoăn về nút bấm, chính sự tách biệt giữa bản nháp và bản ghi chính thức đã tạo nên cảm giác an toàn và kiểm soát cho người học (Tuân thủ nguyên tắc cốt lõi *Design for Human Control* của PAIR).
4. **Đưa vào Backlog cho Slide 6 ("Nếu có thêm 1 tuần"):**
   - Cho phép học viên xuất (export) toàn bộ ghi chú kèm trích dẫn sang định dạng Markdown hoặc đồng bộ 1-click về Notion cá nhân.
   - Thống kê tiến độ ôn tập (Coverage Radar): hiển thị tỷ lệ % các ý chính của buổi học đã được học viên ghi chú và rà soát thành công.
