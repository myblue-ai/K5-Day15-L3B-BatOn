# Demo BatOn trên VPS

Site [demo.202603027.xyz:8090](http://demo.202603027.xyz:8090/) phục vụ HTTP ở cổng riêng. Backend dùng Python chuẩn trong venv của image Docker và chỉ xuất cổng `127.0.0.1:8091`. Proxy demo dùng `deploy/Caddyfile`. Caddy production và staging đang dùng 80/443.

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

Từ máy ngoài VPS, kiểm tra `curl --fail http://demo.202603027.xyz:8090/health` và mở [video dự phòng](http://demo.202603027.xyz:8090/demo.mp4) trong cửa sổ riêng tư. Hai ca trong video là A1-01 và A1-07, trên agent ở mốc `19c67d3` với DeepInfra. Đối chiếu lại demo khi dùng phiên bản D1.
