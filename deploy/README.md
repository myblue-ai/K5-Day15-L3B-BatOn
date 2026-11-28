# Demo BatOn trên VPS

Để chạy chat và admin bằng Python trên máy của bạn, dùng [hướng dẫn setup và test local](../docs/local-setup.md).

Site [demo.202603027.xyz:8090](https://demo.202603027.xyz:8090/) dùng HTTPS và chuyển hướng link HTTP cũ trên cùng cổng. Backend dùng Python chuẩn trong venv của image Docker. Cổng `127.0.0.1:8091` phục vụ chat qua proxy demo. Cổng riêng `127.0.0.1:8092` phục vụ quản trị qua SSH tunnel. Caddy production và staging dùng 80/443.

Project trên máy `vps-aiv2` nằm ở `/home/deploy/mini-hackathon`. Unit `mini-hackathon.service` chạy dưới user `deploy`, đọc `.env` quyền 0600 và quản lý hai container của project Compose `mini-hackathon`. Cấu hình web hiện cho phép 4 lượt gọi đồng thời, tổng cộng 120 lượt/giờ cho toàn bộ demo. Video phục vụ từ `replay/demo.mp4`.

```bash
ssh vps-aiv2
cd /home/deploy/mini-hackathon
systemctl status mini-hackathon --no-pager
sudo journalctl -u mini-hackathon -n 50 --no-pager
sudo journalctl -fu mini-hackathon
```

Sau khi đồng bộ các tệp runtime đã cập nhật vào thư mục này, chạy:

```bash
sh deploy/build-agent.sh
docker compose --env-file .env -f deploy/compose.yaml run --rm --no-deps proxy caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
sudo systemctl restart mini-hackathon.service
curl --fail http://127.0.0.1:8091/health
```

Từ máy ngoài VPS, kiểm tra `curl --fail https://demo.202603027.xyz:8090/health` và mở [video dự phòng](https://demo.202603027.xyz:8090/demo.mp4) trong cửa sổ riêng tư. Video ghi hai ca A1-01 và A1-07 trên agent D1 (`93e78d8`) dùng DeepInfra. Hai lượt đánh giá và phép đo token D3 dùng `gpt-5.6-luna`.

## Quản trị model và khoá lượt gọi công khai

Trên máy của bạn, giữ SSH tunnel chạy. Tunnel dùng cổng `18092` trên máy bạn và chuyển tiếp đến cổng `8092` trên VPS. Cổng `8092` trên máy bạn dành cho admin local khi chạy bằng Python.

```bash
ssh -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -L 127.0.0.1:18092:127.0.0.1:8092 vps-aiv2
```

[Mở trang quản trị VPS qua tunnel](http://127.0.0.1:18092/)

Trong cửa sổ PowerShell khác, lấy token VPS vào clipboard rồi dán vào trang admin ở `18092`. Quyền đọc token thuộc người có quyền quản trị VPS. Nếu gặp lỗi token, kiểm tra lại cổng trên thanh địa chỉ và lấy lại token bằng lệnh sau.

```powershell
ssh vps-aiv2 'sudo -n cat /home/deploy/mini-hackathon/runtime-config/admin-token' | Set-Clipboard
```

- **Đổi model.** Điền provider, model, base URL và key. Bấm **Kiểm tra gateway**, rồi **Áp dụng** trong vòng 5 phút. Có thể giữ key bằng cách để trống ô key khi dùng cùng provider và base URL. **Quay lại cấu hình trước** khôi phục phiên bản liền trước. Lượt gọi mới lấy cấu hình từ RAM.
- **Kết thúc demo.** Bấm **Khoá lượt gọi công khai**. Hai endpoint `/api/chat` và `/api/call` trả 503 trước khi gọi model. Các lượt đã bắt đầu có thể hoàn tất. Trạng thái khoá vẫn còn sau restart và có thể mở lại từ admin. Đây là khoá trên BatOn, còn key do gateway quản lý.
- **Xem lưu lượng.** Admin hiển thị số lần mở trang, yêu cầu chat, phản hồi thành công, lượt bị chặn, lỗi và tối đa 100 sự kiện gần đây. Biểu đồ theo 24 khung giờ và bắt đầu gom dữ liệu từ khi tiến trình khởi động. Các bộ đếm và nhật ký trên trang được đặt lại khi restart. Log chỉ chứa loại sự kiện, thời gian, trạng thái và thời lượng.

Kho `runtime-config/` trên VPS lưu token quản trị và hai phiên bản cấu hình model. Hãy giữ thư mục quyền 0700, file quyền 0600 cho user trong container (UID 65532). Khi chưa có bản ghi đã lưu, agent dùng model từ `.env`.

Trang admin cho phép endpoint mặc định của DeepInfra và OpenAI. Để thêm gateway đã dùng cho `gpt-5.6-luna`, khai báo URL HTTPS chính xác trong `MODEL_ALLOWED_BASE_URLS` ở `.env`, phân cách các mục bằng dấu phẩy. Sau đó khởi động lại riêng `mini-hackathon` để nạp danh sách cho phép. Việc đổi cấu hình sang gateway đã được phép diễn ra trực tiếp trong admin. Agent hỗ trợ các gateway nhận `/chat/completions` và trả usage token.

## Chứng chỉ HTTPS

Chứng chỉ Let's Encrypt cho `demo.202603027.xyz` được cấp bằng DNS-01. Bản ghi A trên Cloudflare ở chế độ DNS only. Certbot lưu tài khoản và chứng chỉ trong `acme/` trên VPS. Caddy đọc bản sao chỉ đọc ở `tls/`. Chứng chỉ đã cấp hết hạn ngày 25/02/2027 theo UTC.

Lần cấp này dùng xác thực thủ công. Để gia hạn, chạy các lệnh sau trên VPS khi gần hết hạn, rồi tạo bản ghi TXT `_acme-challenge.demo.202603027.xyz` theo giá trị Certbot đưa ra. Đợi DNS công khai trả đúng giá trị trước khi tiếp tục và xoá bản ghi TXT vừa tạo sau khi cấp xong. [Hướng dẫn Certbot](https://eff-certbot.readthedocs.io/en/stable/using.html#manual)

```bash
cd /home/deploy/mini-hackathon
docker run --rm -it --name mini-hackathon-acme --user "$(id -u):$(id -g)" \
  -v "$PWD/acme:/acme" certbot/certbot:v5.10.0 certonly \
  --config-dir /acme/config --work-dir /acme/work --logs-dir /acme/logs \
  --manual --preferred-challenges dns -d demo.202603027.xyz
```

Sau khi cấp, cài cặp tệp mới, kiểm tra cấu hình rồi khởi động lại dịch vụ BatOn để nạp chứng chỉ.

```bash
live=acme/config/live/demo.202603027.xyz
sudo install -o root -g 65532 -m 640 "$live/fullchain.pem" "$live/privkey.pem" tls/
docker compose --env-file .env -f deploy/compose.yaml run --rm --no-deps proxy caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
sudo systemctl restart mini-hackathon.service
curl --fail https://demo.202603027.xyz:8090/health
```
