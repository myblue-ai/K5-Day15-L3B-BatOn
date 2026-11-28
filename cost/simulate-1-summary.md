# Tóm tắt mô phỏng simulate-1@20261128-115039

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| hoi_it | 15 | 1 | 867 | 84 | 1.0 | 1.0 |
| hoi_vua | 22 | 2 | 1731 | 204 | 2.0 | 2.0 |
| hoi_nhieu | 13 | 4 | 3464 | 351 | 4.0 | 4.0 |

Tỉ lệ đạt dùng để tính: 20/22 (91%) — lượt run-2@20261128-092833

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (436 người) | Chi phí / tháng — cơ sở (700 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-4o-mini (vào 0.15 · ra 0.6 $/1M) | $0.00041 (≈ 10 ₫) | $0.00045 (≈ 12 ₫) | $0.00020 (≈ 5 ₫) | $1.77 (≈ 44.966 ₫) | $2.84 (≈ 72.192 ₫) | $4.06 (≈ 103.132 ₫) | $0.0041 (≈ 103 ₫) |
| gpt-6.1-terra (vào 1.0 · ra 5.0 $/1M) | $0.0030 (≈ 75 ₫) | $0.0032 (≈ 83 ₫) | $0.0015 (≈ 37 ₫) | $12.68 (≈ 322.046 ₫) | $20.36 (≈ 517.046 ₫) | $29.08 (≈ 738.637 ₫) | $0.0291 (≈ 739 ₫) |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (2.2) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-5.6-luna. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
- Tỷ giá: 1 USD = 25.400 ₫ (Tỷ giá Vietcombank ngày 25/11/2026).
