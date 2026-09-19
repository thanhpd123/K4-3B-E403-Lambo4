# AI Note Reviewer — hướng dẫn prototype

AI Note Reviewer là prototype tích hợp vào giao diện học VLearn. Học viên viết ghi chú theo từng slide, chủ động yêu cầu rà soát, rồi nhận các phát hiện có trích dẫn từ đúng slide và transcript của bài học.

Hệ thống hỗ trợ học viên tự kiểm tra ghi chú. Hệ thống không chấm điểm năng lực, không tự sửa nội dung và không dùng kiến thức bên ngoài nguồn được cung cấp.

## Luồng sử dụng

1. Chọn **Day 1** hoặc **Day 2** và mở slide đang học.
2. Viết ghi chú cá nhân bằng lời của mình.
3. Bấm **Review notes**.
4. Backend lấy nội dung của slide hiện tại và tối đa 8 đoạn transcript liên quan.
5. AI phân loại từng phát hiện:
   - `correct_complete`: ghi chú đúng và đủ theo nguồn.
   - `misconception`: ghi chú mâu thuẫn rõ với nguồn.
   - `missing_boundary`: ghi chú đúng một phần nhưng thiếu điều kiện hoặc giới hạn quan trọng.
   - `insufficient_evidence`: nguồn chưa đủ để kết luận.
6. Học viên mở trích dẫn, trả lời câu hỏi tự kiểm và xem bản sửa nháp.
7. Ghi chú chỉ thay đổi sau khi học viên bấm **Xác nhận cập nhật**.

## Tính năng đã có

- Giao diện ba vùng theo phong cách VLearn: danh mục bài, slide PDF và panel ghi chú.
- Hai bài học mẫu, mỗi bài có 29 slide:
  - Day 1 — AI & LLM Foundation.
  - Day 2 — Xác định bài toán cho AI.
- Truy xuất transcript đúng bài dựa trên độ liên quan với slide và ghi chú.
- Gọi Gemini hoặc OpenAI; Gemini được ưu tiên khi cấu hình cả hai key.
- Ép output AI theo schema Pydantic.
- Kiểm tra `source_id`, loại nguồn và quote nguyên văn ở backend.
- Tự hạ kết luận xuống `insufficient_evidence` nếu citation không hợp lệ.
- Bản sửa nằm ở vùng nháp; học viên có thể giữ nguyên, bỏ qua hoặc xác nhận.
- Chế độ mock có nhãn rõ để kiểm thử giao diện khi không gọi AI thật.
- Giao diện hỗ trợ thu gọn thanh điều hướng và thay đổi độ rộng panel ghi chú.

## Yêu cầu

- Python 3.11 trở lên.
- `pip` và môi trường ảo Python.
- Một API key Gemini hoặc OpenAI để chạy AI thật.
- Data pack VLearn ở đường dẫn `data/vlearn-pack/`:
  - `slides/d1-slide-hackathon.pdf`
  - `slides/d2-slide-hackathon.pdf`
  - `transcript/transcript-01-clean.md` đến `transcript-06-clean.md`

Thư mục `data/` được ignore và không được push lên repository công khai.

## Cài đặt

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

### macOS hoặc Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

## Cấu hình

Mở `.env` và điền ít nhất một key:

```dotenv
GEMINI_API_KEY=
OPENAI_API_KEY=

GEMINI_MODEL=gemini-2.5-flash
OPENAI_MODEL=gpt-4.1-mini

NOTE_REVIEWER_MOCK=false
FLASK_DEBUG=false
```

Quy tắc chọn provider:

1. Có `GEMINI_API_KEY`: dùng Gemini.
2. Không có Gemini key nhưng có `OPENAI_API_KEY`: dùng OpenAI.
3. Không có key và mock tắt: API trả lỗi cấu hình.
4. `NOTE_REVIEWER_MOCK=true`: dùng kết quả giả lập và hiển thị cảnh báo trên giao diện.

Không commit `.env`. File này đã được khai báo trong `.gitignore`.

## Chạy ứng dụng

```bash
python run.py
```

Mở `http://127.0.0.1:5000`.

Kiểm tra backend tại `http://127.0.0.1:5000/api/health`. Ví dụ:

```json
{
  "status": "ok",
  "provider": "openai",
  "mock_mode": false
}
```

## API

### `GET /`

Trả giao diện chính.

### `GET /api/lessons`

Trả danh sách bài học, số slide, đường dẫn PDF và số transcript.

### `GET /data/slides/<lesson_id>.pdf`

Phục vụ slide PDF của bài học đã khai báo.

### `POST /api/review`

Dùng `multipart/form-data`:

| Trường | Bắt buộc | Mô tả |
|---|---:|---|
| `notes` | Có | Ghi chú của học viên, từ 3 đến 20.000 ký tự |
| `lesson_id` | Có | `day1-foundation` hoặc `day2-problem` |
| `slide_number` | Có | Số trang slide, bắt đầu từ 1 |

### `GET /api/health`

Trả provider đang được chọn và trạng thái mock.

## Kiểm thử

Chạy test kỹ thuật:

```bash
python -m pytest -q
```

Test kiểm tra API, tải slide, mock mode, ánh xạ dữ liệu, giữ mã transcript và loại citation không hợp lệ.

Chạy đánh giá AI thật:

```bash
python eval/run_eval.py 3
```

Lệnh tạo `eval/results_round_3.json`. Chỉ dùng kết quả từ provider thật; không dùng mock để báo cáo chất lượng AI.

### Kết quả đã ghi nhận

| Lượt | Model | Kết quả | Citation hợp lệ | Citation bịa | Đạt quality bar |
|---|---|---:|---:|---:|---:|
| Round 1 | `gpt-4.1-mini` | 15/20 — 75% | 100% | 0 | Không |
| Round 2 | `gpt-4.1-mini` | 19/20 — 95% | 100% | 0 | Có |

Quality bar đã khóa: pass rate tối thiểu 80%, citation hợp lệ 100%, không có citation bịa và không có ngôn từ phán xét người học.

`eval/golden_set.json` hiện có 32 case, trong khi Round 1 và Round 2 được ghi nhận trên phiên bản 20 case. Cần chạy một round mới để báo cáo chính xác kết quả trên toàn bộ bộ test hiện tại.

## Cấu trúc repository

```text
.
├── README.md                    # Tổng quan dự án
├── README-PROTOTYPE.md          # Hướng dẫn kỹ thuật này
├── spec.md                      # AI spec và quality bar
├── canvas-cp1.md                # Canvas bài toán
├── CP4_REPORT.md                # Báo cáo checkpoint 4
├── demo-slides.pdf              # Slide demo
├── requirements.txt
├── run.py
├── codebase/
│   ├── app.py                   # Flask routes và error handling
│   ├── ai_client.py             # Gemini/OpenAI client
│   ├── lesson_data.py           # Ánh xạ bài, đọc PDF, chọn transcript
│   ├── prompt.py                # System prompt và output contract
│   ├── schemas.py               # Pydantic schemas
│   ├── source_utils.py          # Chia nguồn và kiểm citation
│   ├── mock_ai.py               # Mock tường minh cho UI test
│   ├── templates/index.html
│   └── static/
├── eval/                        # Golden set, runner và kết quả
├── evidence/                    # Evidence mining và phỏng vấn
├── validation/                  # User validation log
├── tests/                       # Test kỹ thuật
└── data/                        # Data cục bộ, không commit
```

## Cách hệ thống bảo vệ kết quả

- Model chỉ nhận ghi chú và các source chunk được backend chọn.
- Prompt yêu cầu không dùng kiến thức ngoài nguồn.
- `misconception` và `missing_boundary` bắt buộc có citation.
- Citation chỉ được giữ khi `source_id`, `source_type` và quote đều khớp nguồn.
- Citation sai làm kết luận bị hạ xuống `insufficient_evidence` và xóa bản sửa gợi ý.
- Model output sai JSON hoặc sai schema không được render lên giao diện.
- Log chỉ ghi provider, độ dài ghi chú, số source chunk và số finding; không log API key hoặc toàn bộ ghi chú.

## Giới hạn hiện tại

- Chỉ hỗ trợ hai bài học được cấu hình sẵn.
- Truy xuất transcript dùng độ trùng từ khóa, chưa dùng embedding hoặc reranker.
- Ghi chú được giữ trong bộ nhớ của tab và mất khi tải lại trang.
- Chưa có tài khoản, database, đồng bộ nhiều thiết bị hoặc export ghi chú.
- PDF dạng ảnh scan không có text layer cần OCR trước.
- Gemini được ưu tiên theo cấu hình; ứng dụng không tự chuyển sang OpenAI nếu request Gemini thất bại.
- Kết quả AI là gợi ý học tập; học viên vẫn cần mở citation và tự quyết định cập nhật ghi chú.

## Xử lý lỗi thường gặp

### Trang báo không tìm thấy slide

Kiểm tra data pack nằm đúng `data/vlearn-pack/` và có hai file PDF trong thư mục `slides/`.

### Trang báo chưa cấu hình API key

Kiểm tra `.env` nằm cạnh `run.py`, key không để trống và khởi động lại Flask sau khi sửa.

### Citation bị đổi thành `insufficient_evidence`

Model đã trả source ID, loại nguồn hoặc quote không khớp nguyên văn. Đây là guardrail có chủ ý.

### Port 5000 đã được sử dụng

```bash
FLASK_APP=codebase.app python -m flask run --port 5001
```

Trên PowerShell:

```powershell
$env:FLASK_APP="codebase.app"
python -m flask run --port 5001
```

## Tài liệu liên quan

- [AI spec](spec.md)
- [Evidence và khảo sát](evidence/evidence_mining_and_survey.md)
- [User validation log](validation/user_feedback_log.md)
- [Kết quả eval Round 2](eval/results_round_2.json)
- [Tài liệu kỹ thuật chi tiết](codebase/README.md)
