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

Phép thử CP3 không dùng để tính chi phí/task thành công vì đo token trên DeepSeek. Phép đo D3 dùng cùng model `gpt-5.6-luna` với lượt đánh giá 2. [Kết quả D3](#2-kết-quả-mô-phỏng)

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

Ngày 28/11/2026, `python run.py simulate --rate-from eval/run-2.csv` hoàn tất **50/50 phiên**, **0 phiên lỗi**, seed **42**. Run ID mô phỏng `simulate-1@20261128-115039`. **Đo token trên `gpt-5.6-luna`** (cùng model và code với lượt 2), **tính giá theo `gpt-4o-mini` và `gpt-6.1-terra`**. Tỉ lệ đạt lấy từ lượt 2 `run-2@20261128-092833`: **20/22 (91%)**. [Bảng gốc](simulate-1-summary.md) · [Số theo phiên](simulate-1.csv)

| Persona | Phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên |
|---|---:|---:|---:|---:|
| Hỏi ít | 15 | 1 | 867 | 84 |
| Hỏi vừa | 22 | 2 | 1.731 | 204 |
| Hỏi nhiều | 13 | 4 | 3.464 | 351 |

Tổng gồm **111 lượt hỏi**, **96.112 token vào** và **10.318 token ra**, trung bình 2,2 lượt hỏi/phiên.

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp (436) | / tháng — cơ sở (700) | / tháng — cao (1.000) | / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|
| gpt-4o-mini | $0.00041 (≈ 10 ₫) | **$0.00045 (≈ 12 ₫)** | $1.77 (≈ 44.966 ₫) | $2.84 (≈ 72.192 ₫) | $4.06 (≈ 103.132 ₫) | $0.0041 (≈ 103 ₫) |
| gpt-6.1-terra | $0.0030 (≈ 75 ₫) | **$0.0032 (≈ 83 ₫)** | $12.68 (≈ 322.046 ₫) | $20.36 (≈ 517.046 ₫) | $29.08 (≈ 738.637 ₫) | $0.0291 (≈ 739 ₫) |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**. Chi phí / câu hỏi đạt là $0.00020 (gpt-4o-mini) và $0.0015 (gpt-6.1-terra). Tỷ giá 1 USD = 25.400 ₫.

Giới hạn: mỗi hãng tách token khác nhau nên số token thật trên `gpt-4o-mini` / `gpt-6.1-terra` có thể lệch so với số đo trên `gpt-5.6-luna`. Tỉ lệ đạt 91% đo trên 22 câu thử, không phải trên phiên thật. Chưa tính hosting, lưu trữ và giờ công TA.

## 3. So với impact

- Nhóm ước tính khoảng 160 giờ học viên gặp khó mỗi tháng trên 436 người có hoạt động, tương đương **22 phút/người/tháng**. Thời gian tutor thực sự tiết kiệm cần đo qua người dùng. [Cách tính và giới hạn ở §2](../spec.md)
- Ở kịch bản cơ sở, chi phí model là **$0.0041 (≈ 103 ₫)/người/tháng** với `gpt-4o-mini` và **$0.029 (≈ 739 ₫)/người/tháng** với `gpt-6.1-terra`. Kể cả kịch bản cao dùng model mạnh, tổng chỉ ≈ **$29/tháng** cho 1.000 người.
- **Đáng làm không:** đáng thử tiếp. Chi phí model không phải điểm nghẽn — dưới 1.000 ₫/người/tháng so với khoảng 22 phút gặp khó/người/tháng. Điều quyết định là chất lượng (lượt 2 còn 2/22 câu trượt) và thời gian tiết kiệm thật, cần đo qua người dùng trước khi triển khai rộng.

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy: model rẻ hơn · cache · cắt ngữ cảnh · giới hạn bước — mỗi cần gạt đổi chi phí bao nhiêu
- Chi phí ngoài model: hosting, lưu trữ, giờ công người duyệt
- Quy mô nào thì bài toán còn đáng làm
