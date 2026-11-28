# Tổng hợp bằng chứng pain

> Guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Cập nhật 27/11 tối: đã có đào data + khảo sát. Phỏng vấn đang hẹn.

Nguồn chính đáp ứng mục **“Đạt ngưỡng ≥1 nguồn”** ở CP3/CP4 là nhật ký hành vi pre-class do BTC cấp (`chat.csv`, `events.csv`). Trong **557** phản hồi của trợ giảng dưới video có trường `moc_trich_dan`, **231 phản hồi (41,5%)** có trường này rỗng. Nhóm ghép sự kiện `agent_replied` với câu hỏi dưới video qua `ref_id` và tính trên dữ liệu từ 13/11/2026, khi trường này bắt đầu xuất hiện. [Cách chọn mẫu và cách đếm](data-mining.md#1-cách-đếm--viết-trước-khi-chạy) · [Script kiểm lại](count.py) · [Năm ví dụ có mã dòng đã ẩn danh](data-mining.md#4-5-ví-dụ-cụ-thể-mã-dòng-đã-ẩn-danh-không-đoán-ai-là-ai)

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ | `evidence/data-mining.md` · script `evidence/count.py` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☐ chưa làm | `evidence/interviews/P1.md`… |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | Chờ xác nhận số người ngoài nhóm trong 21 phiếu học viên L3 | `evidence/survey/questions.md` · `evidence/survey/results.csv` (đã ẩn danh) |

## 2. Số chính

**Đào data** `data/preclass/` (05–25/11/2026) — chi tiết `evidence/data-mining.md`:
- 145/436 (33,3%) học viên có hoạt động đã hỏi trợ giảng dưới video; 1.108 câu trong 21 ngày.
- **231/557 (41,5%)** câu trả lời của trợ giảng **không dẫn mốc nào trong bài** (từ 13/11).
- 177/431 (41,1%) người xem video có tua lùi, 2.602 lần.
- 332/1.108 (30,0%) câu hỏi gửi lúc 22:00–01:59 giờ VN.

**Khảo sát** n = 21 (L3B 15, L3A 6) — `evidence/survey/results.csv`, phiếu R01–R21:
- Khung giờ xem: **18/21 (85,7%)** xem buổi tối (19–22h) hoặc khuya (sau 22h).
- Lần gần nhất gặp đoạn chưa hiểu: 10/21 (47,6%) là hôm nay / tuần này; 7/21 tuần trước; 4/21 lâu hơn.
- Số lần gặp đoạn chưa hiểu trong 1 tuần: trung vị **4 lần**, trung bình 4,2 (từ 0 đến 10).
- Lần gần nhất đã làm gì *(chọn nhiều)*: **16/21 (76,2%)** tua lại video để tìm · 14/21 (66,7%) hỏi ChatGPT / Claude riêng · 10/21 (47,6%) hỏi trợ giảng dưới video · 3/21 hỏi bạn / Discord · 1/21 hỏi TA.
- Câu trả lời của trợ giảng có chỉ đúng đoạn không — trong 12 phiếu trả lời có / không: **8/12 không chỉ đúng đoạn** (5 không chỉ đoạn nào, 3 chỉ sai đoạn) · 4/12 chỉ đúng đoạn. *(7 phiếu "không hỏi trợ giảng", 2 phiếu "không nhớ".)*
- Có mở lại bài để kiểm câu trả lời không: **13/21 (61,9%) "có, nhưng mất công tìm"** · 6/21 không kiểm · 2/21 không nhận được câu trả lời.
- Mất bao lâu: dưới 5 phút 5 · 5–15 phút 4 · **15–30 phút 8** · trên 30 phút 4 → **12/21 (57,1%) mất ≥15 phút**; trung vị nằm ở nhóm 15–30 phút.
- Kết quả: chỉ **5/21 (23,8%) hiểu hẳn** · 11/21 hiểu một phần · 2/21 bỏ qua để lên lớp hỏi · 3/21 bỏ luôn.
- *Mâu thuẫn trong phiếu (giữ nguyên, không xoá):* R11, R13, R14 không chọn "hỏi trợ giảng" ở câu 5 nhưng trả lời câu 6 như đã hỏi; R21 chọn "hỏi trợ giảng" ở câu 5 nhưng câu 6 ghi "không hỏi". Số ở câu 6 tính theo đúng câu trả lời câu 6.

**Phỏng vấn:** chưa có. Bảng sẽ điền khi xong.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | | | | | |
| P2 | | | | | |
| P3 | | | | | |

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. "Hỏi tutor. Trả lời chung chung, nên bỏ luôn và đọc tài liệu" — phiếu khảo sát R03
2. "Đoạn hỏi tutor, hiện câu trả lời không liên quan" — phiếu khảo sát R11
3. "Lời giải thích của tutor nhập nhằng, sai" — phiếu khảo sát R20
4. "Kẹt ở Guardrail Output. Tutor không giải thích cụ thể" — phiếu khảo sát R06
5. "Các khái niệm mới, phức tạp nhưng trợ giảng AI giải thích không sâu" — phiếu khảo sát R18
6. Ví dụ data: câu hỏi `C00955` (12 ký tự, video `Day01/d01-r1-v03`) — trợ giảng trả lời 227 ký tự, không dẫn mốc nào trong bài — `evidence/data-mining.md` mục 4.

## 4. Các nguồn có khớp nhau không

- **Data nói:** 41,5% câu trả lời của trợ giảng không dẫn mốc bài; 41,1% người xem có tua lùi; 30% câu hỏi gửi lúc khuya.
- **Người dùng nói (khảo sát):** 8/12 người đã hỏi trợ giảng cho biết câu trả lời không chỉ đúng đoạn; 16/21 phải tua lại tìm; 13/21 mở lại bài nhưng mất công tìm; 18/21 xem buổi tối / khuya.
- **Khớp:** cả hai nguồn cùng cho thấy câu trả lời thường không trỏ về chỗ trong bài và học viên phải tự tua lại tìm, chủ yếu vào buổi tối.
- **Lệch / điều mới:** khảo sát cho thấy thời gian mất **lớn hơn nhiều** so với ước tính ban đầu (≥15 phút ở 12/21, không phải ~3 phút). Một số lời phàn nàn là về **chất lượng giải thích** ("không sâu", "nhập nhằng, sai", "chung chung"), không chỉ về việc thiếu mã đoạn — kể cả khi đã chỉ đúng đoạn (R12). 14/21 phải hỏi thêm ChatGPT / Claude bên ngoài.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md`: **đúng một phần, phải chỉnh** — vì data và khảo sát cùng xác nhận câu trả lời thường không chỉ ra đoạn bài (41,5% theo data; 8/12 theo khảo sát) và học viên mất nhiều thời gian tua lại tìm (12/21 mất ≥15 phút), chủ yếu khi học buổi tối. Nhưng pain không chỉ là "thiếu mã đoạn": học viên còn phàn nàn câu trả lời chung chung, khó hiểu. Lát cắt giữ nguyên (trả lời kèm mã đoạn + câu trích để tự kiểm), metric cần đo cả "nội dung khớp đoạn được dẫn".

**Điều vẫn chưa biết:** (1) câu trả lời không dẫn mốc là sai hay chỉ thiếu căn cứ — data không có nội dung chat; (2) tiêu chí "≥20% lượt chat bị chấm chưa đạt trong `answers.csv`" ở giả thuyết chưa đếm — `answers.csv` chấm câu **học viên** viết, không chấm câu trả lời của trợ giảng, nên đã dùng `moc_trich_dan` thay; (3) chưa có phỏng vấn để hỏi "vì sao" sâu hơn.

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| Học viên L3 | ____ | ☐ |
| Học viên L3 | ____ | ☐ |
| Học viên L3 | ____ | ☐ |
