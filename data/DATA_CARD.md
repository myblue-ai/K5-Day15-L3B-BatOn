# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử (bài mẫu, thông báo mẫu, đoạn transcript…) để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.

## Dataset 1 · Nhật ký pre-class BTC cấp

| | |
|---|---|
| Dùng để làm gì | Xem học viên hỏi ở kênh nào và xác định video cần đối chiếu khi chuẩn bị bộ câu thử A1. |
| Từ đâu | Gói BTC tại `data/preclass/`. Mô tả và từ điển cột trong `README.md` và `column_dictionary.csv` của gói. |
| Xử lý những bước gì | BTC đã thay mã định danh và bỏ nội dung chat. Đã kiểm số dòng bằng `csv.DictReader`, không tính hàng tiêu đề. Khi tìm câu dưới video, lọc `chat.csv` theo `channel=video_question` và nhóm theo `transcript`. |
| Số dòng / số đoạn | `chat.csv` 1.260 lượt, gồm 1.108 `video_question`, 151 `video_discussion_reply` và 1 `session_question`. `answers.csv` 3.776 dòng, `events.csv` 107.709 dòng. |
| Phiên bản / khoảng ghi nhận | Gói AI20K Level 3–4, khoá 5, Day01–Day13, 05–25/11/2026 theo README của BTC. Thời gian trong CSV là UTC. |
| Nhãn | Thật, BTC đã ẩn danh. |
| Giới hạn | `transcript` chỉ là mã/tên tệp lời giảng. Gói chỉ lưu độ dài câu hỏi và câu trả lời. Số lượt hỏi dùng để mô tả hành vi. |

## Dataset 2 · Video mô phỏng Day01 về LLM API

| | |
|---|---|
| Dùng để làm gì | Căn cứ của tutor và bộ đối chiếu đầu ra cho B3. |
| Từ đâu | Tài liệu AI20K Day01, `docs/optional-llm-api-exercises.md` §2.1–§2.3 và khung `src/optional_llm_api/template.py` của side lab LLM API. |
| Xử lý và kiểm tra | Codex biên soạn lại nội dung ngắn theo chủ đề và gắn mã `L3-D01-P01` đến `L3-D01-P04`. Không dùng seed. Chờ người trong nhóm kiểm tay. |
| Số đoạn / phiên bản | 4 đoạn, bản CP2. [Đoạn bài](a1_demo_lesson.json) |
| Nhãn | Tài liệu biên soạn lại từ học liệu thật, dùng làm video mô phỏng. |
| Giới hạn | Một bài duy nhất. Mã đoạn thuộc bản thử. Giá trong bài dùng cho ví dụ tính toán. |

## Dataset 3 · Câu thử CP2

| | |
|---|---|
| Dùng để làm gì | Thử hỏi đáp theo bài, hỏi lại, dẫn căn cứ và từ chối. [Benchmark](../eval/benchmark.csv) |
| Từ đâu | 4 câu diễn đạt lại từ các câu phản ánh và bài tập có sẵn trong phiếu Day01 §2.1–§2.3. 8 câu Codex tự viết theo lát cắt. |
| Xử lý và kiểm tra | Mỗi câu trỏ nguồn và có điều kiện chấm theo đoạn bài. Câu tự viết không dùng seed. Đã thu 12 phản hồi trong một lượt mô phỏng ChatGPT. Chờ B1 và B3 chấm độc lập. [Output mô phỏng](../eval/README.md#output-mô-phỏng-cp2) |
| Số dòng / nhãn | 12 câu bản CP2, gồm 4 `data_that` từ phiếu học tập và 8 `tu_viet`. |
| Giới hạn | Các câu từ phiếu thực hành đại diện cho nội dung học. Ghi chép phỏng vấn sau này có thể bổ sung cách hỏi tự nhiên dưới video. |
