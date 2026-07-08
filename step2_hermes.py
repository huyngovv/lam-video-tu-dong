"""
step2_hermes.py
HERMES AGENT - Script Generator

Pipeline:
Topic
↓
Hermes3
↓
script.txt

Author: Huy's Hermes Agent
"""

import os
import time
import logging
from datetime import datetime

import ollama

# ==================================================
# CONFIG
# ==================================================

MODEL = "hermes3:latest"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ==================================================
# LOGGING
# ==================================================

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "hermes.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

# ==================================================
# OLLAMA CHECK
# ==================================================

def check_ollama():
    return True

# ==================================================
# PROMPT
# ==================================================

def build_prompt(topic):
    return f"""
Bạn là biên kịch video công nghệ chuyên nghiệp.

Viết kịch bản video ngắn 45-60 giây bằng tiếng Việt.

CHỦ ĐỀ:
{topic}

ĐỊNH DẠNG BẮT BUỘC:

🎯 Hook:
(1-2 câu gây tò mò)

📌 Nội dung:
(3-5 câu giải thích đơn giản, dễ hiểu)

📢 CTA:
(1 câu kêu gọi follow hoặc like)

YÊU CẦU:
- Giọng văn trẻ trung
- Dễ hiểu
- Không dùng bullet point
- Không giải thích ngoài yêu cầu
- Chỉ trả về kịch bản
"""


# ==================================================
# GENERATE SCRIPT
# ==================================================

def generate_script(topic):
    prompt = build_prompt(topic)

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    script = response["message"]["content"].strip()

    if len(script) < 100:
        raise Exception(
            "Script quá ngắn. Có thể model trả lời lỗi."
        )

    return script


# ==================================================
# SAVE SCRIPT
# ==================================================

def save_script(script, topic):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    main_file = os.path.join(
        OUTPUT_DIR,
        "script.txt"
    )

    backup_file = os.path.join(
        OUTPUT_DIR,
        f"script_{timestamp}.txt"
    )

    content = (
        f"CHỦ ĐỀ: {topic}\n"
        f"NGÀY TẠO: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        + "=" * 60
        + "\n\n"
        + script
    )

    with open(main_file, "w", encoding="utf-8") as f:
        f.write(content)

    with open(backup_file, "w", encoding="utf-8") as f:
        f.write(content)

    return main_file, backup_file


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    print("=" * 60)
    print("🎬 HERMES AGENT - SCRIPT GENERATOR")
    print("=" * 60)

    if not check_ollama():
        exit(1)

    print("\n💡 Ví dụ:")
    print("- AI phân loại rác bằng camera")
    print("- Top 3 repo GitHub hot nhất tuần")
    print("- 5 extension VS Code đáng dùng")

    topic = input(
        "\n📥 Nhập chủ đề video: "
    ).strip()

    if not topic:
        topic = "AI phân loại rác bằng camera"

    print("\n🤖 Đang tạo kịch bản...")
    print(f"📌 Chủ đề: {topic}")

    start = time.time()

    try:
        script = generate_script(topic)

        elapsed = round(
            time.time() - start,
            2
        )

        print("\n" + "=" * 60)
        print("📝 KỊCH BẢN")
        print("=" * 60)
        print(script)
        print("=" * 60)

        main_file, backup_file = save_script(
            script,
            topic
        )

        logging.info(
            f"SUCCESS | Topic={topic} | Time={elapsed}s"
        )

        print("\n✅ Thành công")
        print(f"📄 Script: {main_file}")
        print(f"📦 Backup: {backup_file}")
        print(f"⏱️ Thời gian: {elapsed}s")

        print("\n🚀 Hoàn thành Step 2")
        print("➡️ Tiếp theo: Step 3 - F5-TTS")

    except Exception as e:
        logging.error(str(e))

        print("\n❌ Lỗi")
        print(str(e))

        print("\nKiểm tra:")
        print("- ollama list")
        print("- ollama run hermes3:latest")
        print("- Kết nối Ollama")