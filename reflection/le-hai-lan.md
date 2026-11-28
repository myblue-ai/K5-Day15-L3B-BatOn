# Reflection — Lê Hải Lân

## 1. Vai trò và phần đóng góp

- Nối `gpt-5.6-luna` qua API tương thích OpenAI ở CP3 và hoàn thiện video gọi model thật. [Tích hợp model](../codebase/ai.py) · [Tài liệu nối model](../docs/connect-model.md) (`dbbb634`)
- Cập nhật spec §0–§7, mô tả luồng pre-class hiện tại và ghi kết quả lượt đánh giá 1. [Spec](../spec.md) (`5d7d073`)
- Chỉnh prompt để giảm báo thiếu căn cứ thừa, chạy lượt 2 và chạy mô phỏng 50 phiên dùng tỉ lệ đạt của lượt 2. [Báo cáo đánh giá](../eval/report.md) · [Kết quả mô phỏng](../cost/simulate-1-summary.md) (`93e78d8`, `7220726`)

## 2. AI hỗ trợ thế nào

Hồ sơ nhóm ghi Claude Code hỗ trợ cấu hình `OPENAI_BASE_URL`, tăng timeout và soạn một số mục spec dựa trên bằng chứng và kết quả lượt 1. [Khai báo dùng AI](../docs/ai-usage.md)

Lượt 1 xác nhận tích hợp gọi được model và ghi token sử dụng. [Kết quả lượt 1](../eval/run-1.csv)

## 3. Một câu trượt và bài học cá nhân

Ở lượt 1, A1-20 dẫn một câu trích không hỗ trợ nhận định so sánh hai model. Lượt 2 hỏi người học về tiêu chí chọn model và đạt câu này. [Phân tích cải tiến](../eval/report.md#3-một-lần-cải-tiến)

Khi người học chưa nêu tiêu chí chọn model, một câu hỏi làm rõ giúp tránh suy diễn từ đoạn chỉ nói về giá. Chạy lại cả bộ câu thử cho thấy thay đổi prompt đồng thời làm trượt A1-02 và A1-14.
