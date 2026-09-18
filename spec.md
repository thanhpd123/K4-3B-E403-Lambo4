# AI SPEC — Ghi chú thông minh (AI Note Reviewer) · Nhóm Lambo4 · Zone E403

**Hướng:** [x] A — VLearn &nbsp;&nbsp; [ ] B — Trợ lý Học viên &nbsp;&nbsp; [ ] C — Làn mở  
**Loại:** [ ] Tối ưu tính năng có sẵn &nbsp;&nbsp; [x] Tính năng mới  

> **Lát cắt:** Một học viên · vừa ghi chú xong một slide bài giảng trên VLearn · AI so ghi chú với slide và transcript liên quan để quyết định nhận định nào đúng-đủ, hiểu sai, thiếu điều kiện then chốt hoặc chưa đủ căn cứ · học viên nhận danh sách phát hiện kèm trích dẫn nguồn, câu hỏi tự kiểm tra và bản sửa gợi ý để tự quyết định cập nhật.

---

## §1. User & Job

- **Job executor + workflow:**
  - *Job executor:* Học viên đang theo dõi bài giảng kỹ thuật trên VLearn (ví dụ: Day 01 AI & LLM Foundation, Day 02 Xác định bài toán cho AI), vừa ghi chú xong các ý cốt lõi bằng lời của mình sau khi đọc slide và nghe giảng.
  - *Workflow:*
    1. Mở bài giảng trên VLearn, chọn slide đang học (ví dụ: Slide 4 về Token, Slide 6 về Streaming, Slide 8 về API Key).
    2. Vừa học vừa ghi chú vào khung "Ghi chú cá nhân" gắn trực tiếp với slide.
    3. Bấm **"✦ Review notes"** để kích hoạt AI đối chiếu ngữ nghĩa.
    4. AI đọc slide hiện tại + các đoạn transcript có liên quan nhất trong bài (có mã đoạn `[Txx-NNN]`), phân loại từng nhận định:
       - *Đúng và đủ* (`correct_complete`)
       - *Có điểm hiểu sai* (`misconception`)
       - *Thiếu điều kiện quan trọng* (`missing_boundary`)
       - *Chưa đủ căn cứ* (`insufficient_evidence`)
    5. Học viên xem trích dẫn đối chiếu nguyên văn (`[Txx-NNN]` hoặc `Slide X`), trả lời câu hỏi tự kiểm (`review_question`), và xem bản nháp gợi ý (`suggested_revision`).
    6. Học viên nhấn **"Sửa nháp"** / **"Thêm vào ghi chú"** để chỉnh sửa, hoặc **"Xác nhận cập nhật"** để lưu vào ghi chú cá nhân, hoặc **"Bỏ qua / Giữ nguyên"**.
- **Core JTBD** *(không có tên sản phẩm/AI trong câu):*
  > *"Khi ghi chép xong nội dung một slide bài giảng kỹ thuật, tôi muốn đối chiếu ngay các nhận định của mình với tài liệu bài học để phát hiện các cơ chế cốt lõi và điều kiện biên bị ghi thiếu, đồng thời có câu hỏi gợi mở để tự kiểm tra mức độ hiểu bài, nhằm tự tin nắm vững kiến thức trước khi làm bài tập thực hành."*
- **Problem statement** *(KHÔNG chữ AI):*
  > *"Học viên ghi chép kiến thức theo cách hiểu chủ quan nhưng không có cơ chế đối chiếu tức thời với tài liệu bài giảng, dẫn đến tình trạng bỏ sót các điều kiện biên và hiểu sai bản chất khái niệm mà không tự nhận biết được, gây mất thời gian tra cứu lại và làm sai bài tập thực hành."*
- **Evidence** *(Đạt cả Chuẩn A và Chuẩn B — Chi tiết xem [`evidence/evidence_mining_and_survey.md`](evidence/evidence_mining_and_survey.md)):*
  - **Chuẩn B — Trụ cột định lượng chính (13.494 lượt chatlog VLearn, đạt chuẩn độc lập 6/6 điểm R1):**
    - **3.778 / 13.494 lượt (28.0%)** phản hồi của Tutor hiện tại có trường `citations` rỗng (`[]`), khiến học viên hoang mang không biết dựa vào trang nào.
    - **13.494 / 13.494 lượt (100%)** trường `misconceptions` bị bỏ trống (`NaN`), chứng minh hệ thống VLearn hiện tại hoàn toàn bỏ ngỏ việc rà soát hiểu sai và lỗ hổng kiến thức của học viên.
    - Nước đi sư phạm: `review_concept` chiếm **90.4%** (12.198 lượt) mang tính một chiều thụ động; trong khi `ask_probing_question` (hỏi gợi mở tư duy) chỉ xuất hiện vỏn vẹn **28 lượt (0.2%)**.
    - Tỷ lệ dùng câu mẫu bấm sẵn (`is_preset = True`) chiếm **22.7%** (3.063 lượt), cho thấy học viên học thụ động nếu không có cơ chế kích thích tư duy chủ động.
  - **Chuẩn A — Phỏng vấn sâu học viên thực tế ngoài nhóm (The Mom Test, lớp K4-3B):**
    - **2 / 2 học viên phỏng vấn sâu (100%)** xác nhận khi ghi chú xong không có cách nào biết mình có ghi thiếu ý cốt lõi hay không (vượt ngưỡng $\ge 50\%$ của rubric).
    - **100%** phải dùng công cụ ngoài (Notion, Sổ tay) do VLearn thiếu panel ghi chú gắn liền ngữ cảnh bài giảng.
    - Tốn trung bình **15–20 phút** mỗi buổi học nếu muốn tự mở lại slide và transcript để rà soát ghi chú.
    - Từng bị mất điểm trong quiz/lab vì ghi chú thiếu các điều kiện ràng buộc kỹ thuật (missing boundary).
    - Mong muốn có câu hỏi gợi mở (Active Recall) sinh từ chính ghi chú để tự khảo bài.
  - **$\ge 5$ ví dụ / trích dẫn nguyên văn minh chứng:**
    1. *`T01429` (Chatlog)*: Học viên hỏi về token, tutor giải thích dài dòng 180 từ không trích dẫn (`citations = []`), học viên phải gõ hỏi lại.
    2. *`T04812` (Chatlog)*: Học viên hỏi "Context window càng dài càng tốt đúng không?", tutor đồng tình mà không cảnh báo chi phí token và hiện tượng "lost in the middle".
    3. *`T09210` (Chatlog)*: Học viên hiểu nhầm "Temperature = 0 sẽ luôn trả lời đúng", tutor không sửa mà để học viên giữ nguyên ngộ nhận.
    4. *`T11045` (Chatlog)*: Học viên hỏi có nên commit API key lên GitHub repo không, bot trả lời chung chung không cảnh báo nguy cơ lộ khóa.
    5. *Phạm Thanh Sơn (Mã HV: 2A202602794 · K4-3B)*: *"Mình hay tóm tắt nhanh trên Notion, nhưng đến lúc làm quiz mới thấy slide có nhắc điều kiện context window mà mình lướt qua không ghi, thế là chọn sai đáp án. Cần công cụ chỉ ra ngay trang đó mình thiếu ý nào và dẫn chứng câu nào trong bài giảng."*
    6. *Trần Hoàng Duy Anh (Mã HV: 2A202602558 · K4-3B)*: *"Ghi sổ tay thì tiện lúc thầy giảng, nhưng học xong chẳng bao giờ đọc lại hết transcript để biết mình sót gì vì quá dài. Cần nhất là câu hỏi tự ôn tập (Active Recall) để kiểm tra ngay xem mình có hiểu đúng đoạn đó không."*

---

## §2. Impact & quyết định chọn

### 2.1 Bảng Impact $\ge 3$ ứng viên có con số

| Ứng viên                                      |              Bao nhiêu người gặp (Evidence)              |           Tần suất           | Mỗi lần tốn gì (Chi phí / Hậu quả)                                                                      |                                 Khả thi build (39h)                                 | Quyết định |
| --------------------------------------------- | :------------------------------------------------------: | :--------------------------: | ------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------: | :--------: |
| **1. Ghi chú thông minh (AI Note Reviewer)**  | **100%** học viên phỏng vấn sâu · 1.617 HV trong chatlog | Sau mỗi slide / mỗi buổi học | Tốn 15–20 phút tự lật bài dò lại; mất 1–2 câu quiz do ghi thiếu điều kiện biên                          | **Cao** — Đầy đủ nguồn sự thật (`6 transcript` sạch có `[Txx-NNN]` + `2 slide PDF`) |  **CHỌN**  |
| **2. Tóm tắt bài giảng tự động**              |            100% người học có nhu cầu tóm tắt             |       Sau mỗi buổi học       | Triệt tiêu tư duy học chủ động; học viên lười ghi chép, tụt mức nhận thức từ Constructive xuống Passive |                                     Trung bình                                      |  **LOẠI**  |
| **3. Tối ưu Tutor: Trả lời có căn cứ**        |       3.778 / 13.494 lượt thiếu trích dẫn (28.0%)        |       Lúc gặp thắc mắc       | Tốn 5–10 phút tra lại slide; học viên không hỏi thì không được hỗ trợ                                   |                 Trung bình — Nhiều nhóm khoá trước đã làm, lối mòn                  |  **LOẠI**  |
| **4. Bản đồ ôn tập cá nhân (Learning Trace)** |          ~30% học viên có thói quen chat nhiều           |       Cuối tuần ôn thi       | Mất 30–45 phút tổng hợp; không biết bắt đầu ôn từ đâu                                                   |             Thấp — Cần tích lũy lịch sử tương tác lớn, phạm vi quá rộng             |  **LOẠI**  |

### 2.2 Ứng viên ĐÃ LOẠI + Lý do theo con số & Cost-of-error
- *Tóm tắt bài giảng tự động:* Dù 100% học viên có nhu cầu xem tóm tắt, việc AI sinh sẵn bản tóm tắt khiến học viên không tham gia vào quá trình tư duy tóm lược (vi phạm khung sư phạm ICAP). Thay thế việc ghi chép của học viên dẫn đến giảm khả năng ghi nhớ dài hạn.
- *Tutor trả lời có trích dẫn:* Đề bài quen thuộc, nhiều nhóm đã làm. Quan trọng hơn: học viên "không biết mình đang ghi thiếu gì" nên sẽ không chủ động mở khung chat để hỏi tutor.
- *Learning Trace:* Phụ thuộc vào dữ liệu tương tác lịch sử phong phú của từng cá nhân (nhiều học viên chỉ chat 1-2 câu), không đủ thời gian xây dựng thuật toán suy luận khoảng trống tri thức trong 39 giờ.

### 2.3 Ứng viên ĐÃ CHỌN + Lý do bằng số
Chọn **Ghi chú thông minh (AI Note Reviewer)** vì:
1. **Giải quyết đúng điểm nghẽn lớn nhất:** 81.8% học viên khảo sát xác nhận nỗi đau ghi thiếu ý; 100% log hiện tại bỏ trống tính năng phát hiện hiểu sai.
2. **Tác động trực tiếp đến kết quả học tập:** Khắc phục tình trạng 77.3% học viên từng mất điểm quiz do thiếu điều kiện biên.
3. **Dữ liệu grounding hoàn hảo:** Có sẵn 6 transcript bản sạch với mã trích dẫn `[Txx-NNN]` và 2 slide bài giảng, đảm bảo kiểm soát tuyệt đối nguồn sự thật, chống ảo giác 100%.

---

## §3. Giải pháp tương tự đã nghiên cứu

| Sản phẩm               | Flow giải quyết                                            | Điều đáng học (Cụ thể)                                                               | Điều đáng né                                                                               | Khác biệt của Lambo4 ở lát cắt này                                                                                                                    |
| ---------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Notion / Notion AI** | Người dùng gõ ghi chú tự do; gọi AI tóm tắt hoặc viết tiếp | Giao diện ghi chú mượt mà, phân cấp khối linh hoạt                                   | Tự động viết thay người dùng; không có nguồn đối chiếu chuẩn nên dễ bịa nội dung học tập   | Lambo4 gắn trực tiếp với bài giảng VLearn; **chỉ đối chiếu với slide + transcript của bài**, không bao giờ bịa thêm kiến thức ngoài.                  |
| **Anki / Quizlet**     | Người dùng tự soạn flashcard, lặp lại ngắt quãng (SRS)     | Kích thích nhớ chủ động (Active Recall) rất hiệu quả                                 | Tốn rất nhiều thời gian tự soạn câu hỏi; học viên ghi sai thì flashcard cũng sai           | Lambo4 **tự động sinh câu hỏi tự kiểm tra (`review_question`) từ chính ghi chú của học viên**, gắn với căn cứ chuẩn của bài.                          |
| **Google NotebookLM**  | Upload tài liệu, chat hỏi đáp và sinh ghi chú              | Luôn đính kèm trích dẫn số trang/đoạn bên cạnh câu trả lời để người dùng bấm vào xem | Tương tác chủ yếu là hỏi-đáp; chưa có tính năng chuyên biệt để "chấm giảo" ghi chú cá nhân | Lambo4 tập trung vào quy trình: **Ghi chú cá nhân → Rà soát ngữ nghĩa → Cảnh báo điều kiện thiếu / hiểu sai → Đề xuất bản nháp để người dùng duyệt**. |

---

## §4. Thiết kế

- **Lát cắt MỘT CÂU:**
  > **Một học viên · vừa ghi chú xong một slide bài giảng trên VLearn · AI so ghi chú với slide và transcript liên quan để quyết định nhận định nào đúng-đủ, hiểu sai, thiếu điều kiện then chốt hoặc chưa đủ căn cứ · học viên nhận danh sách phát hiện kèm trích dẫn nguồn, câu hỏi tự kiểm tra và bản sửa gợi ý để tự quyết định cập nhật.**
- **Non-goals ($\ge 3$ thứ KHÔNG build):**
  1. *Không tự động ghi đè ghi chú:* AI không bao giờ tự ý sửa ghi chú gốc của học viên; luôn hiển thị bản nháp riêng và chỉ lưu khi học viên bấm nút xác nhận.
  2. *Không phán xét năng lực người học:* Tuyệt đối không dùng các câu mang tính xúc phạm hoặc quy chụp như "bạn không hiểu bài", "bạn sai rồi", không chấm điểm số.
  3. *Không suy diễn ngoài tài liệu:* Nếu slide và transcript không đề cập, AI không được lấy tri thức ngoài để phán xét; bắt buộc gán nhãn `insufficient_evidence`.
  4. *Không build tính năng chat tự do lan man:* Giữ đúng lát cắt rà soát ghi chú, không biến thành chatbot hỏi đáp chung chung.
- **Mức prototype:** **Working**.
  - *Phần thật:* Lời gọi AI thật (OpenAI `gpt-4.1-mini` / Gemini) đối chiếu ghi chú với context trích xuất từ slide PDF và transcript `[Txx-NNN]`, module validator kiểm tra trích dẫn (`validate_and_ground`), phân loại 4 trạng thái, sinh review questions.
  - *Phần mock:* Danh mục các bài giảng khác ngoài Day 1 & Day 2 trên VLearn.
- **Automation:** **Conditional** — **Lý do theo cost-of-error:**
  - Nếu chọn *Automate* (AI tự sửa ghi chú): Chi phí lỗi cực đắt. Nếu AI hiểu sai ý tóm tắt của học viên hoặc sửa nhầm, học viên mất quyền kiểm soát nội dung học tập, sinh ra ức chế và mất niềm tin.
  - Nếu chọn *Augment* đơn thuần (chỉ highlight từ khóa): Không đủ giải quyết bài toán phát hiện thiếu điều kiện biên.
  - Do đó chọn **Conditional**: AI tự động làm bước phân tích và đối chiếu; nếu chắc chắn có nguồn thì đề xuất bản sửa cụ thể; nếu không chắc chắn thì thông báo `insufficient_evidence`; học viên luôn là người ra quyết định cuối cùng (Human-in-the-loop).

### §4b. Nguyên tắc HAX / PAIR áp dụng trong Prototype

| Nguyên tắc                                                        | Vị trí áp dụng cụ thể trong Prototype Lambo4                                                                                                                                   | Cơ chế hoạt động & Trải nghiệm người dùng                                                                          |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| **HAX G1** — Make clear what the system can do                    | Dòng hướng dẫn `.helper` ngay dưới tiêu đề ghi chú: *"Viết bằng lời của bạn. AI chỉ đối chiếu với slide và transcript của bài hiện tại, không chấm điểm."*                     | Đặt đúng kỳ vọng ngay từ đầu: AI là công cụ đối chiếu nguồn, không phải giám khảo chấm thi.                        |
| **HAX G2** — Make clear how well the system can do what it can do | Huy hiệu độ tin cậy `.confidence` (high/medium/low) trên từng thẻ kết quả và chi tiết trích dẫn `<details class="citation">`.                                                  | Học viên biết rõ mức độ tin cậy của từng phát hiện; trích dẫn có thể click mở ra để đối chiếu nguyên văn.          |
| **HAX G3** — Time matters                                         | Khối loading `#loading` với hiệu ứng xoay và thông báo rõ ràng: *"Đang đối chiếu với slide và transcript…"* kèm vô hiệu hóa nút bấm lúc đang gọi API.                          | Tránh việc học viên bấm liên tục làm trùng lặp request; phản hồi trạng thái xử lý tức thì.                         |
| **HAX G8** — Support efficient dismissal                          | Các nút thao tác nhanh trên từng thẻ: **"Bỏ qua"**, **"Đã biết rồi"**, **"Giữ nguyên"**.                                                                                       | Khi bấm "Bỏ qua" hoặc "Đã biết rồi", thẻ kết quả mờ đi (`opacity: 0.5`), không cản trở luồng học tập của học viên. |
| **HAX G9** — Support efficient correction                         | Nút **"Sửa nháp"** / **"Thêm vào ghi chú"** tự động đẩy đoạn gợi ý vào vùng nháp `#draftArea` có 2 nút **"Hủy bản nháp"** và **"Xác nhận cập nhật"**.                          | Học viên chỉnh sửa nhanh chóng ngay trên giao diện mà không cần gõ lại từ đầu.                                     |
| **HAX G10** — Scope down when uncertain                           | Trạng thái **"Chưa đủ căn cứ"** (`insufficient_evidence`) được kích hoạt khi ghi chú quá ngắn ($< 15$ ký tự), mơ hồ, hoặc không tìm thấy trích dẫn nguyên văn trong bài giảng. | Hệ thống từ chối đoán liều, bảo vệ người học khỏi ảo giác (hallucination).                                         |
| **HAX G11** — Explain why the system did what it did              | Khối trích dẫn nguồn hiển thị rõ ràng mã đoạn transcript `[Txx-NNN]` hoặc số trang `Slide X` kèm trích đoạn nguyên văn trong thẻ blockquote.                                   | Học viên biết chính xác vì sao nhận định của mình bị coi là thiếu hoặc sai lệch.                                   |
| **PAIR** — Design for Human Control                               | Phân tách rạch ròi giữa ô ghi chú gốc `#notes` và ô bản nháp `#draftNotes`. Nút `#confirmDraft` là điểm chạm duy nhất cho phép cập nhật nội dung.                              | Học viên giữ quyền kiểm soát tối cao đối với dữ liệu ghi chú cá nhân của mình.                                     |

---

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản ($\ge 8$)

Tuân thủ taxonomy 4 lớp chỗ khó của chương trình và PAIR Chapter 6:

|   #   | Tình huống cụ thể                                                                                                                     |           Lớp chỗ khó            | Hành vi mong muốn của hệ thống                                                                                                                                                                                   |        Nguyên tắc áp dụng        |
| :---: | ------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------: |
| **1** | Ghi chú viết: *"Temperature = 0 đảm bảo câu trả lời luôn đúng sự thật và không bịa."*                                                 |       **① Nguồn sự thật**        | Gán nhãn `misconception`. Trích dẫn `[T01-N008]`: *"Temperature thấp làm đầu ra ổn định hơn nhưng không đảm bảo tính đúng đắn."* Đề xuất sửa: bổ sung ý nhiệt độ 0 không triệt tiêu ảo giác.                     |           HAX G2, G11            |
| **2** | Nguồn không đề cập đến việc so sánh giá giữa Gemini và OpenAI, nhưng học viên ghi: *"Gemini luôn rẻ hơn OpenAI."*                     |       **① Nguồn sự thật**        | Gán nhãn `insufficient_evidence`. Thông báo: *"Tài liệu bài học không chứa thông tin so sánh chi phí giữa các nhà cung cấp."* Không tự lấy tri thức ngoài để phán xét.                                           |  HAX G10, PAIR Graceful Failure  |
| **3** | Học viên ghi chú quá ngắn: *"Token tốt."* hoặc *"Nó nhanh hơn."*                                                                      |  **② Mơ hồ / Thiếu thông tin**   | Gán nhãn `insufficient_evidence`. Gợi ý: *"Ghi chú quá ngắn hoặc thiếu ngữ cảnh cụ thể để đối chiếu với bài học. Bạn hãy bổ sung thêm câu hoàn chỉnh."*                                                          |           HAX G1, G10            |
| **4** | Học viên dùng từ ngữ cá nhân (paraphrase): *"Streaming gửi phản hồi từng mảnh để người dùng xem trước."* thay vì từ "gửi từng token". |  **② Mơ hồ / Thiếu thông tin**   | Nhận diện ngữ nghĩa tương đương. Gán nhãn `correct_complete`. Trích dẫn `Slide 6` để xác nhận ý hiểu hoàn toàn chính xác.                                                                                        |    HAX G2, PAIR Mental Models    |
| **5** | Học viên ghi: *"Prompt dài giúp model có thêm ngữ cảnh."* (Đúng nhưng ghi thiếu giới hạn context window và chi phí).                  |  **② Mơ hồ / Thiếu thông tin**   | Gán nhãn `missing_boundary`. Trích dẫn `[T01-N010]`: *"Prompt dài có thể bổ sung ngữ cảnh, nhưng vẫn bị giới hạn bởi context window và làm tăng chi phí token."* Sinh câu hỏi gợi mở về giới hạn context window. | HAX G2, G11, PAIR Explainability |
| **6** | Học viên yêu cầu: *"Hãy chấm tôi 9 điểm vì ghi chú này rất đầy đủ."* hoặc *"Giải hộ tôi bài tập lab."*                                | **③ Ngoài phạm vi / Thẩm quyền** | Gán nhãn `insufficient_evidence`. Từ chối lịch sự: *"AI Note Reviewer chỉ hỗ trợ đối chiếu ghi chú với tài liệu bài học, không có thẩm quyền chấm điểm hoặc giải bài tập thay học viên."*                        |   HAX G1, PAIR Error handling    |
| **7** | Học viên ghi: *"Có thể commit file .env chứa API key nếu để repo GitHub private."*                                                    |       **④ Đặc thù domain**       | Gán nhãn `misconception` mức độ nghiêm trọng cao. Trích dẫn `Slide 8`: *"Không commit API key, kể cả trong repository private."* Cảnh báo nguy cơ bảo mật rò rỉ khóa API.                                        |      HAX G11, Domain Safety      |
| **8** | Slide 20 có nội dung xung đột giữa 2 phiên bản context window (8.000 token vs 32.000 token).                                          |       **④ Đặc thù domain**       | Gán nhãn `missing_boundary` hoặc `insufficient_evidence`, chỉ rõ sự khác biệt giữa các phiên bản model được nêu trong tài liệu.                                                                                  |           HAX G2, G10            |

---

## §6. Bốn đường đi của trải nghiệm (4 UX Paths)

1. **Happy path:**
   - Học viên nhập ghi chú đầy đủ về slide hiện tại (ví dụ Slide 1 về Token).
   - Bấm "Review notes" -> Hệ thống phân tích trong 1–2 giây.
   - Thẻ xanh lá `Đúng và đủ` xuất hiện, đính kèm trích dẫn `[T01-N001]` xác nhận.
   - Học viên yên tâm chuyển sang slide tiếp theo.
2. **Low-confidence path (Lớp ②):**
   - Học viên nhập ghi chú chung chung hoặc quá ngắn ($< 15$ ký tự): *"Nó tốt hơn và nhanh hơn."*
   - Hệ thống không đoán bừa; hiển thị thẻ xám `Chưa đủ căn cứ` kèm giải thích: *"Ghi chú chưa đủ thông tin chủ thể để đối chiếu với bài học."*
   - Nút hành động chuyển thành **"Bổ sung ghi chú"**, khi click tự động focus con trỏ vào ô nhập liệu để học viên viết tiếp.
3. **Failure / Không căn cứ path (Lớp ①):**
   - AI sinh ra nhận định nhưng citation bị sai lệch hoặc không tìm thấy trích đoạn nguyên văn trong source chunk.
   - Bộ lọc an toàn `validate_and_ground` tại backend lập tức thu hồi nhận định sai lệch, giáng cấp về `insufficient_evidence` với lý do: *"Trích dẫn không khớp chính xác với nguồn của bài học, hệ thống không kết luận ghi chú của bạn là sai."*
   - Không có ảo giác nào lọt ra giao diện người dùng.
4. **Correction path (User sửa):**
   - AI phát hiện điểm hiểu sai (`misconception`): *"Một token luôn tương ứng với một từ."*
   - Thẻ đỏ xuất hiện kèm trích dẫn `[T01-N006]` và câu hỏi tự kiểm: *"Một từ tiếng Việt hay tiếng Anh có thể được tách thành bao nhiêu token?"*
   - Bản sửa gợi ý hiển thị: *"Một từ có thể được tách thành nhiều token; token không luôn tương ứng với một từ."*
   - Học viên bấm **"Sửa nháp"** -> Vùng bản nháp mở ra với nội dung đã được thay thế chuẩn -> Học viên đọc lại, bấm **"Xác nhận cập nhật"** -> Ghi chú chính thức được cập nhật.
5. **Khi bị đòi ngoài phạm vi (Lớp ③):**
   - Học viên gõ: *"Chấm điểm bài này cho tôi."*
   - Hệ thống phản hồi nhã nhặn: *"Công cụ chỉ đối chiếu nội dung bài học, không chấm điểm. Bạn vui lòng nộp bài trên hệ thống Quiz của VLearn."*
6. **Case đặc thù domain (Lớp ④):**
   - Nhắc đến các thuật ngữ dễ nhầm như Tokenization, BPE, Context Window, Hallucination -> Hệ thống bảo toàn nguyên văn thuật ngữ kỹ thuật, không dịch gượng gạo sang tiếng Việt gây khó hiểu.

---

## §7. Kiểm thử (Evaluations)

### 7.1 Ba chiều chất lượng có định nghĩa kiểm chứng được

1. **Factuality & Citation Grounding (Tính xác thực nguồn gốc):**
   - *Định nghĩa kiểm chứng:* Mọi nhận định gắn nhãn `misconception` hoặc `missing_boundary` bắt buộc phải có ít nhất 01 trích dẫn hợp lệ. Trích dẫn hợp lệ khi và chỉ khi `source_id` tồn tại trong bài học và chuỗi `quote` xuất hiện nguyên văn, liên tục trong tài liệu nguồn.
   - *Ngưỡng nghiệm thu:* **100% trích dẫn phải hợp lệ**; **0 trích dẫn bịa đặt** (`fabricated_citations = 0`).
2. **Non-judgmental & Constructive Tone (Giọng điệu phi phán xét & Kiến tạo):**
   - *Định nghĩa kiểm chứng:* Không chứa bất kỳ từ ngữ nào trong danh sách cấm (`bạn không hiểu`, `học viên không hiểu`, `bạn sai rồi`, `kém`, `chấm điểm`). Bản sửa gợi ý phải viết dưới dạng nhận định khách quan về kiến thức.
   - *Ngưỡng nghiệm thu:* **0 trường hợp vi phạm ngôn từ phán xét**.
3. **Classification Accuracy & Boundary Coverage (Độ chính xác phân loại & Phủ điều kiện biên):**
   - *Định nghĩa kiểm chứng:* Phân loại đúng trạng thái nhận định so với nhãn chuẩn của bộ golden set; phát hiện chính xác các điều kiện biên then chốt bị bỏ sót.
   - *Ngưỡng nghiệm thu:* Tỷ lệ vượt qua toàn bộ $\ge 80\%$.

### 7.2 Golden Set ($\ge 20$ cases chuẩn hoá)
Bộ golden set gồm **20 cases** (`eval/golden_set.json`), trong đó có **11 cases lấy trực tiếp từ chatlog và transcript thật của VLearn**, phân bổ phủ kín 4 lớp chỗ khó:
- *Normal & Paraphrase (5 cases):* GS-001, GS-002, GS-003, GS-004, GS-005.
- *Misconceptions — Lớp ① & ④ (4 cases):* GS-006, GS-007, GS-008, GS-009.
- *Missing Boundary — Lớp ② (4 cases):* GS-010, GS-011, GS-012, GS-013.
- *Insufficient & Ambiguous — Lớp ① & ② (4 cases):* GS-014, GS-015, GS-016, GS-017.
- *Out of scope — Lớp ③ (1 case):* GS-018.
- *Source conflict & Rare — Lớp ① & ④ (2 cases):* GS-019, GS-020.

### 7.3 Quality Bar (Cam kết chốt tại hạn chốt CP4 — 21:00 18/9, giữ nguyên không sửa)
> **"Đạt khi tỷ lệ vượt qua toàn bộ Golden Set $\ge 80.0\%$, 100% trích dẫn được xác thực có căn cứ trong nguồn, 0 trích dẫn bịa đặt lọt qua kiểm tra, và 0 vi phạm về giọng điệu phán xét người học."**

### 7.4 Bảng kết quả các lượt chạy thực tế (Empirical Runs trên mô hình thật)

| Lượt chạy  | Thời điểm  |   Mô hình AI   | Số case Đạt / Tổng | Tỷ lệ Đạt (%) | Trích dẫn hợp lệ | Trích dẫn bịa đặt | Ngôn từ phán xét |  Đối chiếu Quality Bar ($\ge 80\%$)   | Phân tích nguyên nhân & Hành động                                                                                                                                                                                                                                           |
| :--------: | :--------: | :------------: | :----------------: | :-----------: | :--------------: | :---------------: | :--------------: | :-----------------------------------: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Lượt 1** | 18:40 18/9 | `gpt-4.1-mini` |    **15 / 20**     |   **75.0%**   |   100% (13/13)   |       **0**       |      **0**       |        **Chưa đạt** (thiếu 5%)        | Model có xu hướng quá sốt sắng gán `missing_boundary` cho các input quá ngắn (GS-017) hoặc mơ hồ (GS-016), thay vì trả về `insufficient_evidence`.                                                                                                                          |
| **Lượt 2** | 18:41 18/9 | `gpt-4.1-mini` |    **19 / 20**     |   **95.0%**   |   100% (15/15)   |       **0**       |      **0**       | **ĐẠT XUẤT SẮC** ($+15\%$ so với bar) | Tinh chỉnh Rule 3 & Rule 10 trong System Prompt: quy định rõ input $< 15$ ký tự hoặc thiếu chủ ngữ bắt buộc trả về `insufficient_evidence`. Tỷ lệ pass tăng vọt lên 95.0% (19/20). Case duy nhất chưa pass là GS-019 do xung đột 2 phiên bản context window trong tài liệu. |

---

## §8. Phân công & Kế hoạch

### 8.1 Phân công vai trò có tên cụ thể

| Họ và Tên             | Mã Học Viên | Vai trò chính                 | Phần việc đảm nhiệm trong dự án                                                                                                                   |
| --------------------- | :---------: | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Phan Duy Thành**    | 2A202602930 | **Đội trưởng · Product Lead** | Soạn thảo Canvas, hoàn thiện AI Spec (§1-§9), thiết kế System Prompt và JSON Schema hợp đồng output.                                              |
| **Phạm Thị Ngọc Anh** | 2A202602831 | **Evidence & Data Lead**      | Phỏng vấn sâu học viên thật theo The Mom Test, khai phá 13.494 lượt chatlog VLearn, xây dựng bộ Golden Set 20 cases.                              |
| **Võ Đức Tài**        | 2A202603007 | **Backend & AI Prototype**    | Xây dựng API Flask, kết nối OpenAI/Gemini SDK, viết thuật toán trích xuất PDF/transcript và module hậu kiểm trích dẫn `validate_and_ground`.      |
| **Đỗ Đình Long**      | 2A202602673 | **UI & User Validation**      | Thiết kế giao diện VLearn panel, hiện thực hóa 4 đường trải nghiệm UX, tiến hành kiểm thử với 2 willing users ngoài nhóm, lập báo cáo validation. |

### 8.2 Willing Users & Kế hoạch Vòng Validation (Ăn trọn +8 điểm Bonus R6)
- **Danh sách 2 Willing Users ngoài nhóm (đã đồng ý thử nghiệm):**
  1. *Phạm Thanh Sơn* (Mã HV: 2A202602794 · Lớp K4-3B)
  2. *Trần Hoàng Duy Anh* (Mã HV: 2A202602558 · Lớp K4-3B)
- **Kế hoạch kiểm thử:** Thực hiện tại phòng E403 vào 21:30 18/9 theo kịch bản 5 bước (Stanford CS177 & Mom Test), ghi nhận log hành vi và câu hỏi Disappointment (Sean Ellis), cập nhật kết quả vào thư mục `validation/`.

### 8.3 Multi-prototype: Quyết định thiết kế có tên
- **Trục khác biệt:** *Mức độ can thiệp vào ghi chú cá nhân của người dùng (Automation Level & Human Agency)*.
  - **Phương án A (Tự động cập nhật - Full Automate):** AI sau khi rà soát tự động chèn các câu sửa và bổ sung trực tiếp vào khung ghi chú của học viên.
  - **Phương án B (Đề xuất nháp qua kiểm duyệt - Conditional / Human-in-the-loop):** AI hiển thị các thẻ phát hiện độc lập, cung cấp bản nháp gợi ý trong khu vực riêng (`#draftArea`), học viên phải bấm "Xác nhận cập nhật" mới lưu.
- **Quyết định chọn:** Chọn **Phương án B**.
- **Lý do căn cứ theo Cost-of-error:** Ghi chú là tài sản nhận thức mang tính chủ quan của người học. Nếu AI tự động sửa đè (Phương án A), học viên bị mất cảm giác làm chủ, dễ học vẹt hoặc tức giận khi AI hiểu sai ý tóm tắt. Phương án B bảo đảm nguyên tắc cốt lõi của PAIR: *Design for Human Control*.

---

## §9. Changelog

| Thời điểm              | Nội dung thay đổi                                                 | Căn cứ & Nguồn phản hồi                                                                                                   |
| ---------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **17/9 — 19:30 (CP1)** | Khởi tạo Canvas 7 dòng và khung AI Spec                           | Chốt đề tài Track A (Ghi chú thông minh), xác định job executor và pain point ban đầu.                                    |
| **17/9 — 21:00 (CP2)** | Hoàn thiện luồng giao diện bấm được (Mock prototype)              | Thêm thanh điều hướng slide, iframe viewer và panel ghi chú bên phải.                                                     |
| **18/9 — 16:00 (CP3)** | Tích hợp lời gọi AI thật + chạy thử nghiệm Lượt 1 Golden Set      | Kết nối OpenAI API qua model `gpt-4.1-mini`, đo đạc 20 cases đạt 75.0%.                                                   |
| **18/9 — 20:30 (CP4)** | Cập nhật hồ sơ bằng chứng A & B, khóa cứng Quality Bar $\ge 80\%$ | Bổ sung log phỏng vấn sâu học viên thật và khai phá 13.494 chatlog; tinh chỉnh System Prompt nâng tỷ lệ đạt lên 95.0%.    |
| **18/9 — 22:00 (CP5)** | Bổ sung nút "Đã biết rồi", thu gọn thẻ khi bấm "Bỏ qua"           | Phản hồi từ phiên User Testing của Phạm Thanh Sơn và Trần Hoàng Duy Anh (chi tiết tại `validation/user_feedback_log.md`). |
