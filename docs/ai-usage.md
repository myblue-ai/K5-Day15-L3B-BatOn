# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Codex | Viết workflow A1 đọc đoạn bài, kiểm trích dẫn và kết nối DeepInfra. | Workflow được dùng trong các lượt đánh giá và bản demo. | |
| Nối model thật | Claude Code | Thêm `OPENAI_BASE_URL` vào `ai.py` để gọi `gpt-5.6-luna` qua nhà cung cấp trung gian chuẩn OpenAI, tăng timeout. |  chạy `run.py`, `eval --try`, `eval` với key thật. |  |
| Chấm cột `pass` lượt 1 | Claude Code | Hỗ trợ chấm 22 câu của `run-1.csv` theo `pass_criterion`, gom nhóm lỗi và điền `pass`, `ghi_chu`. | Nhóm duyệt 4 câu ranh giới (A1-02, A1-05, A1-14, A1-20). |  |
| Spec §0, §1, §5–§7 | Claude Code | Soạn từ số trong `evidence/` và `eval/run-1.csv`. | Nhóm xác nhận nội dung và cung cấp ảnh §0. |  |
| Prompt / thiết kế lời gọi mô hình | Codex | Định dạng quyết định có căn cứ, hỏi lại, báo thiếu căn cứ và từ chối. | Nhóm chạy đánh giá với model thật và ghi thay đổi prompt giữa hai lượt. | |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | Codex | Diễn đạt lại 4 câu từ phiếu Day01 và soạn 8 câu thử theo lát cắt. | Nhóm ghi kết quả chấm thử và hai lượt đánh giá trong `eval/README.md`. | |
| Học liệu mô phỏng | Codex | Biên soạn 4 đoạn bài từ học liệu Day01. | Các đoạn được dùng làm căn cứ trong `data/a1_demo_lesson.json`. | |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
