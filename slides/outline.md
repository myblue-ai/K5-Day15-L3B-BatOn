# Dàn slide → lấy số từ file nào

> Làm ở guide bước 5.1. Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo.
> Xuất PDF thành `demo-slides.pdf` ở thư mục gốc repo, nộp tại CP4 14:30 Thứ Bảy 28/11. Nộp PDF, không nộp link.

| # | Trang | Có gì | Số lấy từ | Xong |
|---|---|---|---|---|
| 1 | Người dùng & pain | Ai · việc gì · chỗ đau + số và trích dẫn | `evidence/summary.md` | Đã dựng |
| 2 | Vì sao chọn bài này | Bảng impact rút gọn + hướng bị loại | `spec.md` §2 | Đã dựng |
| 3 | Giải pháp | Lát cắt một câu · sơ đồ · AI tự làm đến đâu, vì sao | `spec.md` §4 | Đã dựng |
| 4 | Demo live | Hai câu đạt trên `gpt-5.6-luna`, gồm một câu thường và một câu khó. Video dự phòng được ghi lại trên demo chạy `jpt/gpt-5.6-luna`. | `eval/run-2.csv`, `replay/demo.mp4` | Đã đối chiếu và quay lại |
| 5 | **Đánh giá thế nào** | So sánh hai lượt theo chuẩn CP2, mã lượt chạy và các câu thay đổi kết quả | `eval/README.md`, `eval/report.md` | Đã điền kết quả |
| 6 | **Chi phí khi dùng thật** | Chi phí / task thành công · 3 kịch bản · so với impact | `cost/cost-estimate.md` | Đã điền số D3 (`simulate-1`) |
| 7 | Kết luận | Thử tiếp với nhóm nhỏ dựa trên chất lượng lượt 2 và ước tính chi phí | `eval/report.md`, `cost/cost-estimate.md` | Đã điền kết luận |
| 8 | Nếu có thêm 1 tuần | Thử với học viên, giữ điều kiện khi dẫn số liệu, chạy lặp bộ thử | `eval/report.md` mục 4 · `validation/log.md` | Đã điền kế hoạch |

## Bản demo hiện có

[PDF 8 trang](../demo-slides.pdf) · [Nguồn slide để sửa](deck.html) · [Phòng học](https://demo.202603027.xyz:8090/) · [Video dự phòng](https://demo.202603027.xyz:8090/demo.mp4) · [MP4 để tải về trước buổi demo](../replay/demo.mp4)

1. Mở Day 01, nhập câu A1-01 về temperature của chatbot. Bấm mã P01 để đối chiếu với đoạn nói về tính nhất quán.
2. Bấm **Hỏi lại từ đầu**, nhập A1-07 về streaming và hạn nộp side lab. Mở P04, chỉ ra phần về hạn nộp cần hỏi TA.
3. Dùng kết quả `gpt-5.6-luna` từ lượt 2 ở trang 4–5 và phép đo token D3 ở trang 6. Video dự phòng ghi hai ca live trên `jpt/gpt-5.6-luna` qua gateway tương thích OpenAI. Để xuất lại PDF, mở `slides/deck.html`, chọn in theo khổ trang của tài liệu, bật đồ hoạ nền và tắt đầu/chân trang của trình duyệt.

**Trước khi lên:** tải repo về một máy khác (hoặc thư mục mới), chạy theo mục "Chạy trong 3 phút" của `README.md` · `.env` có trên máy demo, đã gọi thử 1 câu trong vòng 1 giờ trước giờ demo · video dự phòng mở được bằng cửa sổ ẩn danh · biết bản chạy thử sẽ làm gì với **1 câu thử lạ** của giám khảo.

Ai nói trang nào (mỗi người ≥1 phần):

| Trang | Người nói |
|---|---|
| | |
