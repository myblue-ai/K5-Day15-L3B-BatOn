# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## Chạy thử CP3 · C4

Ngày 28/11/2026, `python run.py simulate --try 10` hoàn tất **10/10 phiên**, không có lỗi. Run ID `simulate-try@20261128-015055`, seed **42**. Model đo token là `deepseek-ai/DeepSeek-V4.1-Flash-1017` qua DeepInfra.

| Persona | Phiên | Lượt hỏi | Token vào / phiên | Token ra / phiên |
|---|---:|---:|---:|---:|
| Hỏi ít | 4 | 4 | 1.015 | 158 |
| Hỏi vừa | 5 | 10 | 2.037 | 413 |
| Hỏi nhiều | 1 | 4 | 4.073 | 418 |

Tổng gồm **18 lượt hỏi**, **18.319 token vào** và **3.114 token ra**. Theo đơn giá trong `personas.yaml`, lượng token đo được tương ứng trung bình **0,00046 USD/phiên** nếu tính giá `gpt-4o-mini` và **0,0034 USD/phiên** nếu tính giá `gpt-6.1-terra`.

Chi phí/task thành công còn trống. Lượt đánh giá đã chấm dùng `gpt-5.6-luna`, còn lượt mô phỏng này đo trên DeepSeek. Khung mô phỏng giữ số liệu thử chi tiết trong `cost/simulate-try.csv`, `cost/simulate-try-summary.md` và `traces/simulate-try.jsonl` ở máy chạy.

## 1. Đầu vào

| Nhóm học viên | Tỉ trọng trong 145 người đã hỏi | Phiên/người/tháng | Câu/phiên |
|---|---:|---:|---:|
| Hỏi ít | 39% (56 người) | 3 | 1 |
| Hỏi vừa | 38% (55 người) | 8 | 2 |
| Hỏi nhiều | 23% (34 người) | 16 | 4 |

Tỉ trọng lấy từ log 21 ngày. Số phiên và số câu mỗi phiên là giả định mô phỏng *(tự ước tính)*, có tham khảo trung vị 4 lần gặp chỗ chưa hiểu mỗi tuần trong khảo sát 21 học viên. [Nguồn và cấu hình](personas.yaml)

| Kịch bản | Số người giả định dùng tutor | Phiên/tháng theo cơ cấu trên |
|---|---:|---:|
| Thấp · học viên có hoạt động trong log | 436 | ≈3.440 |
| Cơ sở · quy mô lớp L3 | 700 | 5.523 |
| Cao · quy mô khoá | 1.000 | 7.890 |

Mỗi người dùng trung bình 0,39 × 3 + 0,38 × 8 + 0,23 × 16 = **7,89 phiên/tháng** theo giả định. Trong kỳ quan sát, 145/436 học viên có hoạt động đã dùng tutor. Cả ba kịch bản chi phí đều giả định toàn bộ số người ở dòng tương ứng sẽ sử dụng.

Hai mức giá chuẩn cho mỗi triệu token vào/ra là **0,15/0,60 USD** cho `gpt-4o-mini` và **1,00/5,00 USD** cho `gpt-6.1-terra`. Cùng một lượng token đo trên model chạy thật được tính lại theo hai bảng giá. [Bảng giá chung BTC ngày 25/11/2026](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/further-reading/model-prices.md)

## 2. Kết quả mô phỏng

Đang chờ bản D1 và `eval/run-2.csv` chấm đủ cột `pass`. Chọn đúng model đã đánh giá, chạy `python run.py simulate --rate-from eval/run-2.csv` với 50 phiên, seed 42. Ghi model đo token, run ID đánh giá, run ID mô phỏng và bảng từ `cost/simulate-N-summary.md` vào đây.

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| gpt-4o-mini | Chờ đo | — | — | — | — | — |
| gpt-6.1-terra | Chờ đo | — | — | — | — | — |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Nhóm ước tính khoảng 160 giờ học viên gặp khó mỗi tháng trên 436 người có hoạt động, tương đương **22 phút/người/tháng**. Thời gian tutor thực sự tiết kiệm cần đo qua người dùng. [Cách tính và giới hạn ở §2](../spec.md)
- Khi có lượt 2, đối chiếu chi phí/người/tháng với 22 phút này và ghi quyết định triển khai, thử tiếp hoặc dừng.

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy: model rẻ hơn · cache · cắt ngữ cảnh · giới hạn bước — mỗi cần gạt đổi chi phí bao nhiêu
- Chi phí ngoài model: hosting, lưu trữ, giờ công người duyệt
- Quy mô nào thì bài toán còn đáng làm
