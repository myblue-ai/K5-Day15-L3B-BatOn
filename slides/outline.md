# Dàn slide → lấy số từ file nào

> Làm ở guide bước 5.1. Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo.
> Xuất PDF thành `demo-slides.pdf` ở thư mục gốc repo, nộp tại CP4 14:30 Thứ Bảy 28/11. Nộp PDF, không nộp link.

| # | Trang | Có gì | Số lấy từ | Xong |
|---|---|---|---|---|
| 1 | Người dùng & pain | Ai · việc gì · chỗ đau + số và trích dẫn | `evidence/summary.md` | Đã dựng |
| 2 | Vì sao chọn bài này | Bảng impact rút gọn + hướng bị loại | `spec.md` §2 | Đã dựng |
| 3 | Giải pháp | Lát cắt một câu · sơ đồ · AI tự làm đến đâu, vì sao | `spec.md` §4 | Đã dựng |
| 4 | Demo live | 1 trường hợp thường + 1 trường hợp khó (lấy từ bộ câu thử); mạng hỏng → video dự phòng | `eval/benchmark.csv` | Đã dựng |
| 5 | **Đánh giá thế nào** | Dataset · bộ câu thử · metric · lượt 1 → lượt 2 so với chuẩn "đạt" (kèm run ID) · lỗi chính | `eval/README.md`, `eval/report.md` | Bản nháp |
| 6 | **Chi phí khi dùng thật** | Chi phí / task thành công · 3 kịch bản · so với impact | `cost/cost-estimate.md` | Đã điền số D3 (`simulate-1`) |
| 7 | Kết luận | Go / iterate / stop — dẫn số ở trang 1, 5, 6 | — | Bản nháp |
| 8 | Nếu có thêm 1 tuần | 2–3 việc, trỏ về lỗi còn lại / phản hồi người dùng | `eval/report.md` mục 4 · `validation/log.md` | Bản nháp |

## Bản demo hiện có

[PDF 8 trang](../demo-slides.pdf) · [Nguồn slide để sửa](deck.html) · [Phòng học](https://demo.202603027.xyz:8090/) · [Video dự phòng](https://demo.202603027.xyz:8090/demo.mp4) · [MP4 để tải về trước buổi demo](../replay/demo.mp4)

1. Mở Day 01, nhập câu A1-01 về temperature của chatbot. Bấm mã P01 để đối chiếu với đoạn nói về tính nhất quán.
2. Bấm **Hỏi lại từ đầu**, nhập A1-07 về streaming và hạn nộp side lab. Mở P04, chỉ ra phần về hạn nộp cần hỏi TA.
3. Khi có D1/D2, thử lại hai câu trên bản mới và cập nhật video nếu luồng thay đổi. Điền so sánh hai lượt ở trang 5, bảng D3 ở trang 6 rồi chốt quyết định và các việc tiếp theo ở trang 7–8. Để xuất lại PDF, mở `slides/deck.html`, chọn in theo khổ trang của tài liệu, bật đồ hoạ nền và tắt đầu/chân trang của trình duyệt.

**Trước khi lên:** tải repo về một máy khác (hoặc thư mục mới), chạy theo mục "Chạy trong 3 phút" của `README.md` · `.env` có trên máy demo, đã gọi thử 1 câu trong vòng 1 giờ trước giờ demo · video dự phòng mở được bằng cửa sổ ẩn danh · biết bản chạy thử sẽ làm gì với **1 câu thử lạ** của giám khảo.

Ai nói trang nào (mỗi người ≥1 phần):

| Trang | Người nói |
|---|---|
| | |
