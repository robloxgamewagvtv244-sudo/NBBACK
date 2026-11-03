# NBBACK ULTIMATE
Bot Discord tiếng Việt: moderation, ticket, XP/level, nhạc qua Lavalink, mini game, logs, giveaway và dashboard web khung cơ bản. Không có ngân hàng/tiền ảo.

## Cài đặt
`pip install -r requirements.txt`
Sao chép `.env.example` thành `.env`, điền `DISCORD_TOKEN`, `DASH_PASSWORD`, `DASH_SECRET`.
Trong Discord Developer Portal bật **Message Content Intent** và **Server Members Intent**.
Mời bot với scopes `bot` và `applications.commands`, cấp quyền cần thiết: Manage Channels, View/Send Messages, Read History, Ban, Kick, Moderate Members, Connect, Speak.

## Chạy
`python bot.py`
Dashboard riêng: `python dashboard.py` rồi mở cổng 8080. Dashboard hiện là trang trạng thái có mật khẩu, chưa tích hợp OAuth Discord hoặc cấu hình server qua web.

## Lệnh
`/ping`, `/setup_logs`, `/setup_welcome`, `/ban`, `/kick`, `/timeout`, `/ticket`, `/rank`, `/leaderboard`, `/guess`, `/coinflip`, `/giveaway`, `/play`, `/stop`.

## Nhạc
Cần Lavalink server riêng và cấu hình `LAVALINK_URI`, `LAVALINK_PASSWORD`. Không có Lavalink thì chức năng nhạc chưa hoạt động.

GitHub chỉ lưu mã nguồn, không tự chạy bot 24/7. Không tải `.env` hoặc token lên GitHub công khai. Dùng hosting chạy tiến trình Python nền và lưu SQLite bền vững.
