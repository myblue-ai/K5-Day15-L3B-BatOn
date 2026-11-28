# Chạy và kiểm tra BatOn trên máy local

Chạy các lệnh trong thư mục gốc của repo, nơi có `run.py`. Cần Python 3.10 trở lên. Web, trang admin và bộ test đều dùng thư viện chuẩn của Python.

## 1. Kiểm tra bộ câu hỏi và backend

```bash
python run.py check
python -m unittest discover -s tests -v
```

Trên Windows, có thể dùng `py` nếu máy chỉ có Python Launcher. Trên macOS/Linux, dùng `python3` nếu máy không có lệnh `python`.

`run.py check` kiểm bộ câu hỏi, metric và thông tin nhóm. Bộ test admin dùng gateway mô phỏng để kiểm quyền truy cập, kiểm tra rồi áp dụng cấu hình, quay lại bản trước và trạng thái khóa qua restart. Hai lệnh này không gọi API tính phí.

## 2. Chạy web và admin từ `.env`

Dùng `.env` hiện có ở gốc repo. Nếu chưa có, sao chép `.env.example` thành `.env`. Điền `MODEL_PROVIDER` (`deepinfra` hoặc `openai`), `MODEL_NAME` và `API_KEY` của provider. Với gateway tương thích OpenAI có URL riêng, đặt URL đó vào `OPENAI_BASE_URL`. [Hướng dẫn nối model](connect-model.md)

Thêm hoặc bỏ dấu chú thích cho bốn dòng sau trong `.env`.

```dotenv
BIND_HOST=127.0.0.1
PORT=8091
ADMIN_PORT=8092
MODEL_CONFIG_DIR=runtime-config/local
```

Dùng terminal mới nếu trước đó đã đặt `MODEL_PROVIDER=fake` hay biến model khác bằng lệnh shell. Khi một biến đã được đặt trong terminal, nó được ưu tiên hơn giá trị trong `.env`.

**Windows PowerShell**

```powershell
New-Item -ItemType Directory -Force -Path 'runtime-config/local' | Out-Null
$tokenPath = 'runtime-config/local/admin-token'
if (-not (Test-Path -LiteralPath $tokenPath)) {
    python -c "import secrets; print(secrets.token_hex(32))" |
        Set-Content -LiteralPath $tokenPath -Encoding ascii
}
Get-Content -LiteralPath $tokenPath | Set-Clipboard
python codebase/web.py
```

**macOS / Linux**

```bash
umask 077
mkdir -p runtime-config/local
if [ ! -f runtime-config/local/admin-token ]; then
    python3 -c 'import secrets; print(secrets.token_hex(32))' > runtime-config/local/admin-token
fi
python3 codebase/web.py
```

Giữ terminal đang chạy. Mở [phòng học local](http://127.0.0.1:8091/) và [trang admin local](http://127.0.0.1:8092/). Dán token local từ clipboard trên Windows. Trên macOS/Linux, lấy token từ `runtime-config/local/admin-token`. Nếu cổng đang bận, đổi `PORT` hoặc `ADMIN_PORT` trong `.env`.

Admin VPS mở qua SSH tunnel ở cổng `18092` trên máy bạn và dùng token lấy từ VPS. [Cách mở admin VPS](../deploy/README.md#quản-trị-model-và-khoá-lượt-gọi-công-khai)

## 3. Test nhanh trong trình duyệt

| Thao tác | Kết quả mong đợi |
|---|---|
| Đăng nhập admin bằng token | Admin hiển thị đúng provider và model từ `.env` ở lần chạy đầu. |
| Hỏi «Nên đặt temperature ở mức nào cho chatbot hỗ trợ khách hàng, và tại sao?» | Trợ giảng gợi ý mức thấp và dẫn đoạn `L3-D01-P01`. |
| Bấm **Làm mới** trong admin | Lượt mở trang, yêu cầu chat thành công và nhật ký cập nhật theo thao tác vừa làm. |
| Bấm **Khoá lượt gọi công khai**, rồi gửi câu hỏi | Chat báo tạm đóng, API trả `503` và bộ đếm **Đã chặn** tăng. |
| Dừng bằng `Ctrl+C`, chạy lại `python codebase/web.py` trong cùng terminal | Admin vẫn báo đang khóa. Bộ đếm và nhật ký bắt đầu lại. |
| Bấm **Mở lượt gọi công khai**, rồi gửi lại câu hỏi | Chat gọi model đang được cấu hình. |

Có thể gọi API trực tiếp để đối chiếu trạng thái `200` khi mở và `503` khi khoá.

```powershell
curl.exe -fsS http://127.0.0.1:8091/health
'{"message":"Streaming la gi?"}' | curl.exe -sSi -H 'Content-Type: application/json' --data-binary '@-' http://127.0.0.1:8091/api/chat
```

```bash
curl -fsS http://127.0.0.1:8091/health
curl -si -H 'Content-Type: application/json' -d '{"message":"Streaming la gi?"}' http://127.0.0.1:8091/api/chat
```

## 4. Đổi model trong admin

1. Nếu cần nhập một gateway HTTPS riêng, thêm URL chính xác vào `MODEL_ALLOWED_BASE_URLS` trong `.env` trước khi khởi động. Admin đã cho phép URL mặc định của DeepInfra và OpenAI.
2. Đăng nhập admin, điền cấu hình mới và bấm **Kiểm tra gateway**. Nếu thành công, bấm **Áp dụng** trong vòng 5 phút. Có thể bấm **Quay lại cấu hình trước** để khôi phục.

Kiểm tra gateway và chat thật đều dùng token của tài khoản provider. Cấu hình đã áp dụng hoặc trạng thái khoá được ghi vào `runtime-config/local/model.json`. Ở lần khởi động sau, tệp này được ưu tiên hơn các giá trị model trong `.env`. Nếu muốn nạp lại từ `.env` và giữ cấu hình cũ để đối chiếu, chọn một thư mục `MODEL_CONFIG_DIR` mới rồi tạo token trong thư mục đó theo bước 2. Giữ `.env`, token quản trị và `model.json` trên máy local.
