# AI Note Reviewer — prototype

Prototype Python mô phỏng một panel ghi chú theo slide trong VLearn. Học viên dán hoặc tải nguồn, viết ghi chú, rồi chủ động yêu cầu AI đối chiếu. AI không tự sửa ghi chú; thay đổi chỉ được áp dụng sau khi học viên xác nhận.

## Cài đặt trên Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Điền ít nhất một key vào `.env`. Gemini được ưu tiên nếu cả hai key cùng tồn tại:

```text
GEMINI_API_KEY=...
OPENAI_API_KEY=...
```

Chạy ứng dụng:

```powershell
python run.py
```

Mở `http://127.0.0.1:5000`.

## Chế độ mock

Đặt `NOTE_REVIEWER_MOCK=true` chỉ để kiểm thử UI khi không có API key. Giao diện sẽ hiện banner cảnh báo và response có `is_mock=true`. Chế độ này không được dùng cho video AI thật hoặc kết quả eval.

Nếu không có API key và mock đang tắt, API trả lỗi cấu hình rõ ràng; ứng dụng không hardcode kết quả thay thế.

## Kiểm thử

```powershell
pytest -q
```

Golden set nằm trong `eval/golden_set.json`. `eval/results_round_1.json` chủ ý để trạng thái `not_run` cho tới khi chạy bằng API key thật.

## Cấu trúc chính

- `codebase/app.py`: Flask API, upload PDF/text và error handling.
- `codebase/ai_client.py`: chọn Gemini trước, fallback OpenAI khi không có Gemini key.
- `codebase/prompt.py`: system prompt và JSON contract.
- `codebase/schemas.py`: Pydantic schema.
- `codebase/source_utils.py`: chia nguồn và hậu kiểm citation.
- `codebase/mock_ai.py`: mock được bật tường minh cho UI test.
- `codebase/templates`, `codebase/static`: giao diện VLearn-style.

Ứng dụng chỉ log provider, độ dài note, số source chunks và số findings; không log API key hoặc toàn bộ nội dung người dùng.
