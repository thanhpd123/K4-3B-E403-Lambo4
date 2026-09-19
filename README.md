# Lambo4 — AI Note Reviewer cho VLearn

Prototype Track A của mini hackathon AI20k. Sản phẩm giúp học viên đối chiếu ghi chú theo từng slide với transcript và slide chính thức, phát hiện điểm hiểu sai hoặc thiếu điều kiện quan trọng, xem nguồn và tự quyết định có cập nhật ghi chú hay không.

## Điểm chính

- Rà ghi chú theo đúng bài và slide đang học.
- Bốn trạng thái: đúng và đủ, hiểu sai, thiếu điều kiện, chưa đủ căn cứ.
- Mỗi kết luận quan trọng phải có citation khớp nguyên văn với nguồn.
- Sinh câu hỏi tự kiểm và bản sửa nháp.
- Không tự ghi đè ghi chú, không chấm điểm hoặc phán xét học viên.
- Hỗ trợ Gemini, OpenAI và mock mode có nhãn rõ.

## Kết quả hiện tại

- Eval Round 2 bằng `gpt-4.1-mini`: **19/20 case đạt — 95%**.
- Citation hợp lệ: **100%**.
- Citation bịa lọt qua validator: **0**.
- Test kỹ thuật cần data pack cục bộ tại `data/vlearn-pack/`.

Kết quả Round 2 dùng bộ 20 case. Golden set hiện tại đã mở rộng lên 32 case nên cần chạy round mới trước khi dùng con số trên để mô tả bản model/prompt hiện tại.

## Chạy nhanh

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python run.py
```

Điền `GEMINI_API_KEY` hoặc `OPENAI_API_KEY` trong `.env`, rồi mở `http://127.0.0.1:5000`.

Trên Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python run.py
```

## Kiểm thử

```bash
python -m pytest -q
python eval/run_eval.py 3
```

Không commit `.env` hoặc thư mục `data/`. Data pack thuộc phạm vi hackathon và được giữ cục bộ.

## Thành viên

| Thành viên | Vai trò |
|---|---|
| Phan Duy Thành | Product lead, spec, prompt và output contract |
| Phạm Thị Ngọc Anh | Evidence, data mining và golden set |
| Võ Đức Tài | Flask backend, AI integration và citation validator |
| Đỗ Đình Long | Giao diện và user validation |

## Tài liệu

- [Hướng dẫn prototype đầy đủ](README-PROTOTYPE.md)
- [AI spec](spec.md)
- [Evidence và khảo sát](evidence/evidence_mining_and_survey.md)
- [User validation](validation/user_feedback_log.md)
- [Báo cáo CP4](CP4_REPORT.md)
- [Slide demo](demo-slides.pdf)
