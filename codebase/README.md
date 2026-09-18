# AI Note Reviewer

Prototype Python mô phỏng tính năng ghi chú theo slide trên VLearn. Học viên viết ghi chú cá nhân, cung cấp transcript hoặc slide làm **nguồn sự thật**, sau đó chủ động yêu cầu AI đối chiếu ghi chú với nguồn.

AI chỉ đưa ra nhận xét và bản sửa nháp. Nội dung ghi chú chỉ thay đổi sau khi học viên bấm xác nhận.

## 1. Tính năng

- Nhập ghi chú cá nhân theo slide.
- Dán transcript/slide hoặc tải file `.txt`, `.md`, `.pdf`.
- Phân loại phát hiện thành:
  - `correct_complete`: đúng và đủ.
  - `misconception`: nội dung sai hoặc mâu thuẫn với nguồn.
  - `missing_boundary`: đúng một phần nhưng thiếu điều kiện, giới hạn hoặc ngoại lệ.
  - `insufficient_evidence`: nguồn chưa đủ để kết luận.
- Hiển thị citation có thể mở rộng.
- Kiểm tra citation ở backend trước khi trả kết quả cho giao diện.
- Cho phép sửa nháp, thêm vào ghi chú, giữ nguyên hoặc bỏ qua.
- Không tự động thay đổi ghi chú.
- Hỗ trợ Gemini và OpenAI; Gemini được ưu tiên.
- Có mock mode riêng để kiểm thử giao diện khi chưa có API key.

## 2. Yêu cầu hệ thống

- Python 3.11 trở lên, khuyến nghị Python 3.12.
- `pip`.
- PowerShell trên Windows hoặc terminal tương đương trên macOS/Linux.
- Một trong hai API key:
  - Gemini: `GEMINI_API_KEY`.
  - OpenAI: `OPENAI_API_KEY`.

Không ghi API key trực tiếp vào mã nguồn hoặc commit file `.env`.

## 3. Setup từ đầu trên Windows

### Bước 1 — Mở repository

```powershell
cd C:\duong-dan-den-repository\K4-3B-E403-Lambo4
```

### Bước 2 — Tạo virtual environment

```powershell
py -m venv .venv
```

Nếu máy chỉ nhận lệnh `python`:

```powershell
python -m venv .venv
```

### Bước 3 — Kích hoạt virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

Nếu PowerShell chặn script, chạy lệnh sau trong terminal hiện tại rồi kích hoạt lại:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Khi thành công, đầu dòng lệnh sẽ có `(.venv)`.

### Bước 4 — Cài dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Bước 5 — Tạo file cấu hình cục bộ

```powershell
Copy-Item .env.example .env
```

Mở `.env` và điền ít nhất một API key:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=

GEMINI_MODEL=gemini-2.5-flash
OPENAI_MODEL=gpt-4.1-mini

NOTE_REVIEWER_MOCK=false
FLASK_DEBUG=false
```

Quy tắc chọn provider:

1. Có `GEMINI_API_KEY` → dùng Gemini.
2. Không có Gemini key nhưng có `OPENAI_API_KEY` → dùng OpenAI.
3. Không có cả hai → hiển thị lỗi cấu hình, không trả kết quả hardcode.

### Bước 6 — Chạy ứng dụng

Từ thư mục gốc repository:

```powershell
python run.py
```

Mở trình duyệt tại:

```text
http://127.0.0.1:5000
```

Kiểm tra trạng thái backend:

```text
http://127.0.0.1:5000/api/health
```

Kết quả ví dụ:

```json
{
  "status": "ok",
  "provider": "gemini",
  "mock_mode": false
}
```

### Bước 7 — Dừng ứng dụng

Nhấn `Ctrl+C` trong terminal đang chạy Flask.

## 4. Setup trên macOS/Linux

```bash
cd /duong-dan-den-repository/K4-3B-E403-Lambo4
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
python run.py
```

Sau đó mở `http://127.0.0.1:5000`.

## 5. Cách sử dụng

1. Viết ghi chú vào ô **Ghi chú cá nhân**.
2. Chọn loại nguồn `Transcript` hoặc `Slide`.
3. Dán nội dung nguồn hoặc tải file `.txt`, `.md`, `.pdf`.
4. Bấm **Review notes**.
5. Đợi AI đối chiếu từng nhận định với nguồn.
6. Mở citation để kiểm tra đoạn nguồn.
7. Chọn hành động phù hợp:
   - `Xem nguồn`.
   - `Sửa nháp` hoặc `Thêm vào ghi chú`.
   - `Giữ nguyên` hoặc `Đã biết rồi`.
   - `Bỏ qua`.
8. Nếu chọn sửa, kiểm tra vùng **Bản nháp sau rà soát**.
9. Chỉ khi bấm **Xác nhận cập nhật**, nội dung mới được đưa vào ô ghi chú.

## 6. Cấu trúc dự án

```text
K4-3B-E403-Lambo4/
├── .env.example                 # Mẫu biến môi trường, không chứa key thật
├── .gitignore                   # Loại .env, .venv, cache Python khỏi Git
├── requirements.txt             # Dependencies được khóa phiên bản
├── run.py                       # Entry point chạy Flask
├── codebase/
│   ├── __init__.py
│   ├── README.md                # Tài liệu này
│   ├── app.py                   # Flask app, route, upload và error handling
│   ├── ai_client.py             # Gemini/OpenAI client và chọn provider
│   ├── mock_ai.py               # Mock tường minh chỉ dùng test UI
│   ├── prompt.py                # System prompt và user prompt
│   ├── schemas.py               # Pydantic models và business validation
│   ├── source_utils.py          # Chia nguồn, chuẩn hóa và kiểm citation
│   ├── static/
│   │   ├── app.js               # Tương tác UI và quản lý bản nháp
│   │   └── style.css            # Giao diện mô phỏng VLearn
│   └── templates/
│       └── index.html           # Trang chính
├── eval/
│   ├── golden_set.json          # 20 test case đánh giá AI
│   └── results_round_1.json      # Kết quả lượt chạy thật
├── tests/
│   ├── test_app.py              # Test route, cấu hình và mock mode
│   └── test_source_utils.py     # Test tách nguồn và citation validator
└── build/data/vlearn-pack/      # Dữ liệu transcript/slide của challenge
```

## 7. Luồng hoạt động tổng thể

```text
Học viên nhập ghi chú
        │
        ├── Dán nguồn hoặc tải TXT/MD/PDF
        │
        ▼
Flask nhận POST /api/review
        │
        ├── Pydantic kiểm tra độ dài và source_type
        ├── PDF được trích xuất thành text theo từng trang
        └── Transcript/slide được chia thành SourceChunk có source_id
        │
        ▼
Chọn AI provider
        │
        ├── Có Gemini key ───────► Gemini
        ├── Chỉ có OpenAI key ───► OpenAI
        ├── Bật mock mode ───────► Mock có cảnh báo
        └── Không có cấu hình ───► Lỗi rõ ràng cho UI
        │
        ▼
AI trả JSON theo schema
        │
        ├── Pydantic validate cấu trúc
        ├── Kiểm status và confidence
        └── misconception/missing_boundary phải có citation
        │
        ▼
Citation grounding validator
        │
        ├── source_id phải tồn tại
        ├── source_type phải khớp
        └── quote phải nằm nguyên văn trong source chunk
        │
        ├── Hợp lệ ──────────────► Giữ kết luận
        └── Không hợp lệ ────────► Hạ xuống insufficient_evidence
                                      và xóa suggested_revision
        │
        ▼
UI hiển thị findings và citation
        │
        ├── Giữ nguyên / bỏ qua
        ├── Xem nguồn
        └── Tạo bản sửa nháp
                │
                ▼
      Học viên xác nhận cập nhật
```

## 8. JSON contract

Mỗi finding có cấu trúc:

```json
{
  "status": "correct_complete",
  "note_excerpt": "Token là đơn vị văn bản mà mô hình xử lý.",
  "finding": "Nhận định phù hợp với nguồn.",
  "explanation": "Nguồn định nghĩa token theo cùng ý.",
  "citations": [
    {
      "source_type": "transcript",
      "source_id": "T03-N001",
      "quote": "Token là đơn vị văn bản mà mô hình xử lý."
    }
  ],
  "suggested_revision": "",
  "review_question": "Token được dùng ở bước nào khi gọi model?",
  "confidence": "high"
}
```

Response của API:

```json
{
  "findings": [],
  "provider": "gemini",
  "is_mock": false
}
```

## 9. Quy tắc an toàn

- AI chỉ được dùng nội dung trong nguồn người dùng cung cấp.
- Không kết luận học viên “không hiểu bài”.
- Không chấm điểm học viên.
- Không tự cập nhật ghi chú.
- Không được bịa citation.
- Không có citation hợp lệ thì không được kết luận `misconception` hoặc `missing_boundary`.
- `suggested_revision` luôn là bản nháp.
- Model output lỗi JSON sẽ trả thông báo an toàn thay vì render dữ liệu chưa kiểm tra.
- API key không xuất hiện trong log.
- Log chỉ ghi provider, độ dài ghi chú, số source chunks và số findings.

## 10. Cách nguồn được xử lý

### Transcript

Nếu transcript có mã như:

```text
[T03-N001] Nội dung đoạn thứ nhất.
[T03-N002] Nội dung đoạn thứ hai.
```

Hệ thống giữ nguyên `T03-N001`, `T03-N002` làm citation ID.

Nếu không có mã, hệ thống sinh ID `SRC-N001`, `SRC-N002` theo từng đoạn văn.

### Slide dạng text

Nên dùng định dạng:

```text
Slide 1
Nội dung slide thứ nhất.

Slide 2
Nội dung slide thứ hai.
```

### PDF

Mỗi trang PDF được trích xuất và gắn ID `Slide 1`, `Slide 2`, ... bằng `pypdf`.

PDF dạng ảnh scan không có text layer sẽ không trích xuất tốt. Với loại PDF này, cần OCR trước hoặc dán transcript dạng text.

## 11. Mock mode

Mock chỉ dùng để kiểm thử giao diện:

```dotenv
NOTE_REVIEWER_MOCK=true
```

Khi bật:

- Không gọi Gemini/OpenAI.
- Trang hiển thị banner `MOCK UI TEST`.
- API trả `provider: "mock"` và `is_mock: true`.
- Kết quả không được sử dụng cho demo AI thật hoặc `eval/results_round_1.json`.

Để quay demo AI thật:

```dotenv
NOTE_REVIEWER_MOCK=false
```

## 12. Chạy test

Kích hoạt `.venv`, sau đó:

```powershell
python -m pytest -q
```

Test hiện kiểm tra:

- Health endpoint.
- Lỗi rõ ràng khi thiếu API key.
- Mock phải được bật tường minh và response phải có nhãn mock.
- Giữ đúng transcript ID.
- Citation giả bị loại và kết luận bị hạ xuống `insufficient_evidence`.

Kiểm tra cú pháp toàn bộ code:

```powershell
python -m compileall -q codebase run.py tests
```

## 13. Golden set và đánh giá AI thật

`eval/golden_set.json` có 20 case, bao gồm:

- Ghi chú đúng và đủ.
- Paraphrase khác từ nhưng đúng ý.
- Misconception.
- Thiếu điều kiện/ranh giới.
- Không đủ bằng chứng.
- Input ngắn hoặc mơ hồ.
- Yêu cầu ngoài phạm vi.
- Nguồn mâu thuẫn.

Quality bar hiện tại:

- Ít nhất 80% case đạt.
- 100% citation hợp lệ.
- 0 citation bịa.

Chỉ cập nhật `eval/results_round_1.json` sau khi chạy bằng API key thật. Không điền kết quả mock hoặc kết quả tự ước lượng.

## 14. API reference

### `GET /`

Trả giao diện chính.

### `GET /api/health`

Trả trạng thái app, provider được chọn và mock mode.

### `POST /api/review`

Request dùng `multipart/form-data`:

| Trường | Bắt buộc | Nội dung |
|---|---:|---|
| `notes` | Có | Ghi chú cá nhân |
| `source_text` | Có nếu không tải file | Transcript hoặc slide dạng text |
| `source_type` | Có | `transcript` hoặc `slide` |
| `source_file` | Không | File `.txt`, `.md` hoặc `.pdf` |

Nếu vừa có `source_text` vừa có `source_file`, file upload được ưu tiên.

## 15. Xử lý lỗi thường gặp

### `python` hoặc `py` không được nhận diện

Cài Python 3.11+ và chọn tùy chọn **Add Python to PATH**, sau đó mở terminal mới.

### PowerShell không cho kích hoạt `.venv`

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Trang báo chưa cấu hình API key

- Kiểm tra file phải có tên chính xác `.env`, không phải `.env.txt`.
- Đặt `.env` tại thư mục gốc, cạnh `run.py`.
- Khởi động lại Flask sau khi sửa `.env`.

### Gemini lỗi nhưng OpenAI key cũng đã cấu hình

Fallback OpenAI chỉ xảy ra khi **không có** Gemini key. Nếu Gemini key tồn tại nhưng request Gemini thất bại, ứng dụng trả lỗi thay vì âm thầm đổi provider. Cách này tránh việc chạy nhầm model trong quá trình đánh giá. Muốn dùng OpenAI, để trống `GEMINI_API_KEY` rồi khởi động lại app.

### Citation bị chuyển thành `insufficient_evidence`

Model đã trả source ID hoặc quote không khớp nguyên văn với nguồn. Đây là hành vi bảo vệ có chủ ý, không phải lỗi giao diện.

### PDF không có nội dung

PDF có thể là ảnh scan. Hãy OCR file hoặc dùng transcript dạng `.txt`/`.md`.

### Port 5000 đang được sử dụng

Chạy bằng Flask CLI với port khác:

```powershell
$env:FLASK_APP="codebase.app"
python -m flask run --port 5001
```

## 16. Nguyên tắc phát triển tiếp

- Không bỏ citation validator để cải thiện tỷ lệ pass giả tạo.
- Không dùng mock trong luồng AI thật.
- Thêm field mới phải cập nhật đồng thời schema, prompt, UI và golden set.
- Mọi thay đổi prompt cần chạy lại đủ 20 case.
- Không sửa quality bar sau khi đã xem kết quả eval.
- Không commit `.env`, `.venv`, cache hoặc dữ liệu chứa thông tin cá nhân.
