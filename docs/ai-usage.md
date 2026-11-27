# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Codex | Viết workflow A1 đọc đoạn bài, kiểm trích dẫn và kết nối DeepInfra. | Chờ nhóm rà soát. | |
| Prompt / thiết kế lời gọi mô hình | Codex | Định dạng quyết định có căn cứ, hỏi lại, báo thiếu căn cứ và từ chối. | Chờ thử với model thật. | |
| Đào data (viết script đếm, gợi ý nhãn) | | | Kiểm tay __ dòng, khớp __ | |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | Codex | Diễn đạt lại 4 câu từ phiếu Day01 và soạn 8 câu thử theo lát cắt. | Chờ nhóm chạy tay và chấm thử. | |
| Sinh data `synthetic` (nếu có) | Codex | Biên soạn 4 đoạn video mô phỏng từ học liệu Day01. | Soạn trực tiếp, không dùng seed. Chờ nhóm kiểm tay. | |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Slide, văn bản | | | | |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
