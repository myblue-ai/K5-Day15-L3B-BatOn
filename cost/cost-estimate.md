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

- **Persona** (`cost/personas.yaml`): ≥3 kiểu — tỉ lệ, số phiên / người / tháng, số lượt hỏi / phiên. Nguồn: __
- **Số người dùng thật** 3 kịch bản: thấp __ · cơ sở __ · cao __. Nguồn: __
- **Giá** ≥2 mức model (từ `further-reading/model-prices.md` của repo đề, có link + ngày xem): __ · __
- **Tỉ lệ đạt** dùng để tính: __/__ (__%) — lượt `run-__` (lượt 2)
- Đo token trên model __, tính giá model __ và __

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-__.csv` · run ID __ · __ phiên · seed __

*(dán bảng từ `cost/simulate-N-summary.md`)*

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): __
- Chi phí / người / tháng (cơ sở, model __): __
- **Kết luận một dòng — đáng làm không:** __

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy: model rẻ hơn · cache · cắt ngữ cảnh · giới hạn bước — mỗi cần gạt đổi chi phí bao nhiêu
- Chi phí ngoài model: hosting, lưu trữ, giờ công người duyệt
- Quy mô nào thì bài toán còn đáng làm
