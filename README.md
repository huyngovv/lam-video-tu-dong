#  HERMES-AGENT — Tự động tạo video từ văn bản

Pipeline AI tự động: nhập chủ đề → sinh kịch bản → tạo giọng đọc → xuất video.  
Chạy hoàn toàn **local** trên máy tính cá nhân, không tốn chi phí API.

---

## Cấu hình máy tính được test

| Thành phần | Thông số |
|---|---|
| CPU | Intel Core i5-12450HX (12 cores, 2.4GHz) |
| RAM | 16 GB |
| GPU | NVIDIA GeForce RTX (dùng để tăng tốc Ollama) |
| OS | Windows 11 Home 64-bit |

---

## Tổng quan pipeline

```
[Bạn nhập chủ đề]
        ↓
  Step 2 — Hermes3 (Ollama)
  Sinh kịch bản tiếng Việt ~60 giây
        ↓
  Step 3 — F5-TTS
  Chuyển kịch bản thành giọng đọc (voice.wav)
        ↓
  Step 4 — (sắp tới)
  Tạo video HTML 9:16 + caption karaoke + render
        ↓
  [Video thành phẩm]
```

---

## Cấu trúc thư mục

```
C:/hermes-agent/
│
├── step2_hermes.py       # Sinh kịch bản bằng Hermes3
├── step3_tts.py          # Chuyển kịch bản thành giọng đọc F5-TTS
├── test_hermes.py        # Test kết nối Ollama
├── requirements.txt      # Thư viện Python cần cài
├── voice_sample.wav      # File giọng mẫu của bạn (tự thu âm)
│
├── output/
│   ├── script.txt        # Kịch bản mới nhất
│   ├── script_YYYYMMDD_HHMMSS.txt   # Backup kịch bản
│   └── voice.wav         # File giọng đọc đầu ra
│
└── logs/
    └── hermes.log        # Log quá trình chạy
```

---

## Cài đặt

### 1. Cài Python 3.11

Tải tại: https://www.python.org/downloads/release/python-3119/

> Nhớ tick **"Add Python to PATH"** khi cài.

### 2. Cài Ollama và tải model Hermes3

Tải Ollama tại: https://ollama.com/download/windows

Sau khi cài, mở PowerShell và chạy:

```powershell
ollama pull hermes3:latest
```

### 3. Cài các thư viện Python

```powershell
pip install ollama soundfile imageio[ffmpeg]
```

### 4. Cài F5-TTS

```powershell
pip install f5-tts
```

> F5-TTS yêu cầu khoảng 4-6 GB dung lượng khi tải model lần đầu.

---

## Hướng dẫn sử dụng

### Bước 1 — Test kết nối Ollama

```powershell
python test_hermes.py
```

Nếu Hermes trả lời được là kết nối thành công.

### Bước 2 — Sinh kịch bản

```powershell
python step2_hermes.py
```

Chương trình sẽ hỏi chủ đề, ví dụ:

```
 Nhập chủ đề video: Top 3 repo GitHub hot nhất tuần
```

Kịch bản được lưu tại `output/script.txt`.

### Bước 3 — Sinh giọng đọc

Trước tiên cần có file `voice_sample.wav` — file giọng mẫu của bạn (tự thu âm, tối thiểu 3 giây, đọc rõ ràng).

```powershell
python step3_tts.py
```

File giọng đọc được lưu tại `output/voice.wav`.

---

## Cách tạo file giọng mẫu (voice_sample.wav)

1. Mở **Voice Recorder** trên Windows (tìm trong Start Menu)
2. Đọc đoạn sau rõ ràng, tự nhiên, khoảng 8 giây:

   > *"Xin chào các bạn, hôm nay chúng ta sẽ cùng khám phá những dự án công nghệ thú vị nhất tuần này."*

3. Lưu file và copy vào: `C:/hermes-agent/voice_sample.wav`

---

## Ví dụ chủ đề video

**Công nghệ / GitHub:**
- Top 4 repo GitHub trending tuần này
- 5 extension VS Code đáng dùng nhất
- AI phân loại rác bằng camera

**Tài chính:**
- VN-Index hôm nay tăng hay giảm
- 3 cổ phiếu được khối ngoại mua ròng nhiều nhất

**AI News:**
- 5 tin AI nổi bật trong tuần
- Claude vs GPT-4o — so sánh mới nhất

**Gaming:**
- Top game ra mắt tuần này
- Bản cập nhật mới của Elden Ring

**Mẹo điện thoại:**
- 5 mẹo Android ít ai biết
- Cách tăng tốc iPhone không cần reset

---

## Xử lý lỗi thường gặp

| Lỗi | Nguyên nhân | Cách fix |
|---|---|---|
| `ollama: command not found` | Chưa cài Ollama | Tải tại ollama.com |
| `model hermes3 not found` | Chưa pull model | Chạy `ollama pull hermes3:latest` |
| `Script quá ngắn` | Model trả lời lỗi | Restart Ollama, thử lại |
| `Không tìm thấy voice_sample.wav` | Chưa có file giọng mẫu | Thu âm và lưu vào đúng đường dẫn |
| `F5-TTS thất bại` | Text quá dài hoặc file giọng lỗi | Rút ngắn script, kiểm tra voice_sample.wav |

---

## Roadmap — Các bước sắp tới

- [x] Step 2 — Sinh kịch bản bằng Hermes3
- [x] Step 3 — Sinh giọng đọc bằng F5-TTS
- [ ] Step 4 — Tạo HTML composition 9:16 (dark tech style)
- [ ] Step 5 — Inject caption karaoke + render video
- [ ] Step 6 — Tự upload lên Google Drive
- [ ] Step 7 — Telegram Bot để ra lệnh từ điện thoại

---

## Tác giả

**Huy** — HERMES-AGENT project  
Cảm hứng từ: Long Đình (@trolap_bot)
