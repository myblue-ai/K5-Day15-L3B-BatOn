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
| Xử lý và kiểm tra | Codex biên soạn lại nội dung ngắn theo chủ đề và gắn mã `L3-D01-P01` đến `L3-D01-P04`. Học liệu được soạn trực tiếp, không dùng seed, và đã dùng trong hai lượt đánh giá. [Báo cáo đánh giá](../eval/report.md) |
| Số đoạn / phiên bản | 4 đoạn, bản CP2. [Đoạn bài](a1_demo_lesson.json) |
| Nhãn | Tài liệu biên soạn lại từ học liệu thật, dùng làm video mô phỏng. |
| Giới hạn | Một bài duy nhất. Mã đoạn thuộc bản thử. Giá trong bài dùng cho ví dụ tính toán. |

## Dataset 3 · Câu thử CP2 và CP3

| | |
|---|---|
| Dùng để làm gì | Thử hỏi đáp theo bài, hỏi lại, dẫn căn cứ và từ chối. [Benchmark](../eval/benchmark.csv) |
| Từ đâu | 5 câu chuyển thể từ đề thực hành Day01 §2.1–§2.3, 3 câu chuyển thể từ chủ đề cụ thể trong khảo sát R06 (Guardrail Output), R15 (Docker) và R21 (chi phí token), 14 câu tự viết theo lát cắt. |
| Xử lý và kiểm tra | Mỗi câu ghi nguồn và điều kiện chấm. Câu tự viết không dùng seed. CP2 có 12 phản hồi mô phỏng ChatGPT, trong đó 5 được B1 và B3 đối chiếu. CP3 bổ sung 10 câu và đã chạy lượt 1 với 22 đầu vào. Khi rà lại nguồn, giữ nguyên đầu vào, đáp án và tiêu chí đã chạy. [Hồ sơ đánh giá](../eval/README.md) |
| Số dòng / nhãn | CP2 có 12 câu. CP3 có 22 câu gồm 5 `data_that`, 3 `nguoi_dung`, 14 `tu_viet`. Có 5 câu `[ngoai_bai]` và 3 câu `[tan_cong]`. |
| Giới hạn | Câu có nguồn từ khảo sát là câu chuyển thể từ tình huống người dùng mô tả. Số token trong A1-14 do nhóm đặt. Câu có nguồn từ đề thực hành kiểm nội dung học liệu, còn lời hỏi tự nhiên dưới video có thể được bổ sung qua phỏng vấn. |
