# Demo BatOn trên VPS

Site [demo.202603027.xyz:8090](https://demo.202603027.xyz:8090/) dùng HTTPS và chuyển hướng link HTTP cũ trên cùng cổng. Backend dùng Python chuẩn trong venv của image Docker và chỉ xuất cổng `127.0.0.1:8091`. Proxy demo dùng `deploy/Caddyfile`. Caddy production và staging dùng 80/443.

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
docker compose --env-file .env -f deploy/compose.yaml build agent
docker compose --env-file .env -f deploy/compose.yaml run --rm --no-deps proxy caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
sudo systemctl restart mini-hackathon.service
curl --fail http://127.0.0.1:8091/health
```

Từ máy ngoài VPS, kiểm tra `curl --fail https://demo.202603027.xyz:8090/health` và mở [video dự phòng](https://demo.202603027.xyz:8090/demo.mp4) trong cửa sổ riêng tư. Hai ca trong video là A1-01 và A1-07, trên agent ở mốc `19c67d3` với DeepInfra. Đối chiếu lại demo khi dùng phiên bản D1.

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
