# Reflection — Khương Hoàng Nguyên

## 1. Vai trò và phần đóng góp

- Thiết kế workflow đọc đoạn bài, gọi model và kiểm mã đoạn cùng câu trích. Chuẩn bị 12 câu thử đầu, bốn đoạn Day01 và data card. [Agent](../codebase/agent.py) · [Data card](../data/DATA_CARD.md) (`2b58489`)
- Rà nguồn và tình huống của benchmark CP3. Hoàn thiện cách trình bày chi phí theo hai mức giá model và ba quy mô sử dụng. [Benchmark](../eval/benchmark.csv) · [Ước tính chi phí](../cost/cost-estimate.md) (`bf0278e`, `e6aac32`)
- Dựng demo web, slide, video dự phòng và cấu hình triển khai. [Demo web](../codebase/web.py) · [Dàn slide](../slides/outline.md) · [Hướng dẫn triển khai](../deploy/README.md) (`e6aac32`, `ab0aa66`, `990dcfe`)

## 2. AI hỗ trợ thế nào

Hồ sơ nhóm ghi Codex hỗ trợ soạn workflow, câu thử ban đầu và bốn đoạn học liệu mô phỏng. [Khai báo dùng AI](../docs/ai-usage.md)

*Nguyên bổ sung một đoạn code, câu thử hoặc đoạn học liệu mình đã đối chiếu với yêu cầu và sửa sau khi nhận gợi ý từ AI.*

## 3. Một câu trượt và bài học cá nhân

A1-20 cho thấy bộ kiểm có thể xác nhận câu trích nằm trong tài liệu, trong khi câu trích vẫn thiếu căn cứ cho nhận định mà tutor đưa ra. [Lỗi trích dẫn lượt 1](../eval/report.md#2-lỗi-lượt-1--gom-thành-nhóm-có-tên)

*Nguyên bổ sung bài học về cách mình sẽ kiểm mối liên hệ giữa câu trả lời và câu trích trước khi hiển thị.*
