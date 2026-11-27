# Đào data — cách đếm và kết quả

> Guide bước 1.2. Repo chỉ chứa số đã tổng hợp và vài mã dòng ví dụ, không chép lại nguyên file data.
> **Chạy lại:** `python evidence/count.py <đường-dẫn-tới-data/preclass>` (mặc định đọc `data-btc/preclass`, thư mục đã có trong `.gitignore`).

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** `data/preclass/` BTC cấp — `chat.csv`, `events.csv` — từ 05/11 đến 25/11/2026 (21 ngày, Day01–Day13). Giờ trong file là UTC.
- **Đếm gì:**
  - D1: bao nhiêu học viên hỏi trợ giảng dưới video, bao nhiêu câu.
  - D2: trong câu trả lời của trợ giảng, bao nhiêu câu **không dẫn mốc nào trong bài** (khoá `moc_trich_dan` rỗng).
  - D3: bao nhiêu người xem video có **tua lùi** (dấu hiệu tua lại tìm đoạn).
  - D6: phân bố số câu hỏi mỗi học viên (dùng cho persona chi phí).
- **Trên tập nào · lọc gì:**
  - D1: `chat.csv`, `channel = video_question`.
  - D2: `events.csv`, `type = agent_replied`, nối `ref_id` với câu ở D1, chỉ câu do `teaching_assistant` trả lời, và **chỉ dòng có khoá `moc_trich_dan`** trong cột `data` (khoá này chỉ có từ 13/11).
  - D3: `events.csv`, `type = video_seeked`, lọc `to < from`.
- **Mẫu số là gì:**
  - D1: 436 = số học viên có ≥1 dòng `actor = learner` trong `events.csv` (không dùng 721 tài khoản).
  - D2: 557 = số câu trả lời của trợ giảng có khoá `moc_trich_dan` (không dùng cả 1.108 câu).
  - D3: 431 = số học viên có `video_opened`.
- **Script:** [`evidence/count.py`](count.py) — chỉ thư viện chuẩn Python.

## 2. Đọc trước, đếm sau

Đã đọc `README.md`, `column_dictionary.csv`, `event_types.csv` và ~30 dòng đầu `chat.csv`. Các *kiểu* hành vi thấy được trước khi định nghĩa thứ cần đếm:
- Học viên hỏi trợ giảng ngay dưới video (`video_question`) — kênh chiếm gần hết lượt chat (1.108/1.260).
- Trợ giảng trả lời; từ 13/11 có ghi các mốc giây trong bài mà câu trả lời dẫn ra (`moc_trich_dan`) và cờ `missing_context`.
- Học viên tua video, phần lớn là tua lùi.
- Bạn học AI tự xen vào bài giảng rất nhiều lần, học viên ít khi đáp lại.
- **Data không có nội dung câu hỏi / câu trả lời**, chỉ có độ dài (số ký tự).

## 3. Kết quả

| | Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|---|
| D1 | Học viên đã hỏi trợ giảng dưới video | 145 / 436 | 33,3% | 1.108 câu trong 21 ngày |
| D2 | Câu trả lời của trợ giảng **không dẫn mốc nào trong bài** | 231 / 557 | 41,5% | Chỉ từ 13/11 (khi có khoá `moc_trich_dan`) |
| D2b | Trợ giảng tự báo thiếu ngữ cảnh (`missing_context = True`) | 99 / 1.091 | 9,1% | Toàn bộ câu trợ giảng trả lời |
| D3 | Người xem video có tua lùi ít nhất 1 lần | 177 / 431 | 41,1% | 2.602 lần tua lùi |
| D4/D5 | Học viên đáp lại lời bạn học AI | 151 / 13.975 | 1,1% | Dùng cho hướng A4 (đã loại) |
| D6 | Hỏi ít (1–2 câu) / vừa (3–9) / nhiều (≥10) | 56 / 55 / 34 trên 145 | 38,6% / 37,9% / 23,4% | Nhóm hỏi nhiều chiếm 720/1.108 câu (65,0%) |
| — | Câu hỏi gửi lúc 22:00–01:59 giờ VN | 332 / 1.108 | 30,0% | Ủng hộ người dùng chính "tối mới xem" |

## 4. ≥5 ví dụ cụ thể (mã dòng đã ẩn danh, không đoán ai là ai)

Năm câu hỏi dưới video mà câu trả lời của trợ giảng **không dẫn mốc nào trong bài** (D2). Giờ đã đổi sang giờ VN.

| # | Mã chat | Video (transcript) | Độ dài câu hỏi | Độ dài trả lời | Lúc hỏi (VN) |
|---|---|---|---|---|---|
| 1 | `C01187` | `Day06/d06-r1-v01` | 92 ký tự | 600 ký tự | 13/11 11:31 |
| 2 | `C00882` | `Day05/d05-r2-v06` | 18 ký tự | 220 ký tự | 13/11 11:35 |
| 3 | `C00218` | `Day01/d01-r1-v03` | 28 ký tự | 266 ký tự | 13/11 12:58 |
| 4 | `C00955` | `Day01/d01-r1-v03` | 12 ký tự | 227 ký tự | 13/11 12:58 |
| 5 | `C00951` | `Day01/d01-r1-v03` | 25 ký tự | 299 ký tự | 13/11 12:58 |

Ví dụ 4 và 2: câu hỏi rất ngắn (12–18 ký tự) — dạng câu dễ mơ hồ, đúng loại `kho` trong bộ câu thử.

## 5. Giới hạn của data

- Data cho biết học viên **làm gì**, không cho biết **vì sao**. Không có nội dung câu hỏi, nên không biết câu trả lời không dẫn mốc là **sai** hay chỉ **thiếu căn cứ**.
- `moc_trich_dan` chỉ có từ 13/11 → D2 chỉ tính trên 557 câu, chưa chắc đại diện cho cả 21 ngày.
- Tua lùi (D3) có thể vì nhiều lý do (xem lại cho kỹ, lỡ tay), không chắc là "tìm lại đoạn để kiểm câu trả lời".
- Chỉ 436/721 tài khoản có hoạt động; data lệch về phía học viên đã dùng trang pre-class.

→ **Kiểm lại bằng:** phỏng vấn ≥3 học viên L3 (lần gần nhất kẹt khi xem video: làm gì, câu trả lời có chỉ đoạn bài không, mất bao lâu) và khảo sát (`evidence/survey/questions.md`, câu 6 kiểm D2, câu 8 kiểm thời gian mỗi lần).
