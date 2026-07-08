"""
step3_tts.py — Chuyển script.txt thành giọng nói bằng F5-TTS
Pipeline: script.txt → F5-TTS → voice.wav
"""

import os
import re
import time
import subprocess
import soundfile as sf
from datetime import datetime

# ===== FIX FFMPEG (không cần cài tay) =====
try:
    import imageio_ffmpeg
    os.environ["PATH"] += os.pathsep + os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
    print(f"✅ ffmpeg: {imageio_ffmpeg.get_ffmpeg_exe()}")
except ImportError:
    print("⚠️  imageio_ffmpeg không có — chạy: pip install imageio[ffmpeg]")

# ===== CẤU HÌNH =====
OUTPUT_DIR   = "C:/hermes-agent/output"
SCRIPT_PATH  = f"{OUTPUT_DIR}/script.txt"
VOICE_PATH   = f"{OUTPUT_DIR}/voice.wav"
SAMPLE_AUDIO = "C:/hermes-agent/voice_sample.wav"   # file giọng mẫu của bạn
SAMPLE_TEXT  = "Xin chào các bạn, hôm nay chúng ta sẽ cùng khám phá những dự án công nghệ thú vị nhất tuần này."

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ===== ĐỌC VÀ LÀM SẠCH SCRIPT =====
def load_script(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Không tìm thấy file script: {path}\nHãy chạy step2_hermes.py trước!")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Bỏ dòng header — xử lý cả chữ hoa lẫn thường
    lines = content.splitlines()
    script_lines = []
    for line in lines:
        stripped = line.strip()
        low = stripped.lower()
        if (low.startswith("ch") and ("đề:" in low or "de:" in low)):
            continue
        if low.startswith("ngày tạo:") or low.startswith("ngay tao:"):
            continue
        if stripped.startswith("="):
            continue
        script_lines.append(line)

    script = "\n".join(script_lines).strip()

    # Bỏ emoji và ký tự đặc biệt (F5-TTS không đọc được emoji)
    script = re.sub(r'[^\w\s\.,!?:;\-\(\)àáâãèéêìíòóôõùúýăđơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]', '', script)
    script = re.sub(r'\n+', ' ', script)        # gộp xuống dòng thành khoảng trắng
    script = re.sub(r' +', ' ', script).strip() # bỏ khoảng trắng thừa

    return script


# ===== KIỂM TRA FILE GIỌNG MẪU =====
def check_voice_sample() -> bool:
    if not os.path.exists(SAMPLE_AUDIO):
        print(f"❌ Không tìm thấy file giọng mẫu: {SAMPLE_AUDIO}")
        print("\n👉 Cách tạo file giọng mẫu:")
        print("   1. Mở Voice Recorder trên Windows")
        print("   2. Đọc đoạn sau rõ ràng, tự nhiên (~8 giây):")
        print('      "Xin chào các bạn, hôm nay chúng ta sẽ cùng khám phá')
        print('       những dự án công nghệ thú vị nhất tuần này."')
        print(f"   3. Lưu thành: {SAMPLE_AUDIO}")
        return False

    # Kiểm tra độ dài file (tối thiểu 3 giây)
    try:
        data, sr = sf.read(SAMPLE_AUDIO)
        duration = len(data) / sr
        if duration < 3:
            print(f"⚠️  File giọng mẫu quá ngắn ({duration:.1f}s). Cần ít nhất 3 giây.")
            return False
        print(f"✅ File giọng mẫu: {SAMPLE_AUDIO} ({duration:.1f}s)")
    except Exception as e:
        print(f"⚠️  Không đọc được file giọng mẫu: {e}")
        return False

    return True


# ===== SINH GIỌNG ĐỌC =====
def generate_voice(script: str) -> str:
    print(f"\n🎙️  Đang sinh giọng đọc...")
    print(f"📄 Text ({len(script)} ký tự):\n{script[:200]}{'...' if len(script) > 200 else ''}\n")

    cmd = [
        "f5-tts_infer-cli",
        "--model",      "F5TTS",
        "--ref_audio",  SAMPLE_AUDIO,
        "--ref_text",   SAMPLE_TEXT,
        "--gen_text",   script,
        "--output_dir", OUTPUT_DIR,
        "--output_file","voice.wav",
    ]

    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    elapsed = round(time.time() - start, 2)

    if result.returncode != 0:
        print("❌ F5-TTS gặp lỗi:")
        print(result.stderr[-1000:])  # in 1000 ký tự cuối của lỗi
        raise RuntimeError("F5-TTS thất bại")

    # F5-TTS đôi khi lưu tên khác, tìm file wav mới nhất
    wav_files = [
        f for f in os.listdir(OUTPUT_DIR)
        if f.endswith(".wav") and f != "voice.wav"
    ]
    if wav_files and not os.path.exists(VOICE_PATH):
        latest = max(wav_files, key=lambda f: os.path.getmtime(os.path.join(OUTPUT_DIR, f)))
        os.rename(os.path.join(OUTPUT_DIR, latest), VOICE_PATH)

    return elapsed


# ===== KIỂM TRA KẾT QUẢ =====
def verify_output() -> float:
    if not os.path.exists(VOICE_PATH):
        raise FileNotFoundError(f"Không tìm thấy file output: {VOICE_PATH}")

    data, sr = sf.read(VOICE_PATH)
    duration = len(data) / sr
    return duration


# ===== MAIN =====
if __name__ == "__main__":
    print("=" * 50)
    print("🎙️  F5-TTS — VOICE GENERATOR")
    print("=" * 50)

    # 1. Kiểm tra file giọng mẫu
    if not check_voice_sample():
        exit(1)

    # 2. Đọc script
    try:
        print(f"\n📂 Đang đọc script: {SCRIPT_PATH}")
        script = load_script(SCRIPT_PATH)
        print(f"✅ Đọc xong — {len(script)} ký tự")
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        exit(1)

    # 3. Sinh giọng
    try:
        elapsed = generate_voice(script)
    except RuntimeError:
        print("\n🔍 Gợi ý fix:")
        print("   1. Thử rút ngắn text (dưới 300 ký tự)")
        print("   2. Kiểm tra file voice_sample.wav hợp lệ")
        print("   3. Chạy: f5-tts_infer-cli --help")
        exit(1)

    # 4. Xác nhận kết quả
    try:
        duration = verify_output()
        print("\n" + "=" * 50)
        print(f"✅ Sinh giọng thành công!")
        print(f"📁 File output  : {VOICE_PATH}")
        print(f"⏱️  Thời lượng  : {duration:.1f} giây")
        print(f"🚀 Thời gian xử lý: {elapsed} giây")
        print("=" * 50)
        print("\n🎯 Sẵn sàng cho Step 4 (Subtitle)!")
    except FileNotFoundError as e:
        print(f"\n❌ {e}")