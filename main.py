import os
import json
import shutil
from datetime import datetime

log_file = f"cleanup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"


def log(message):
    with open(log_file, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%H%M%S")
        f.write(f"[{timestamp}] {message}\n")
    print(message)


try:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    log("📖 Конфигурация загружена")
except FileNotFoundError:
    log("❌ОШИБКА: config.json не найден!")
    exit()
except json.JSONDecodeError:
    log("❌ОШИБКА: config.json повреждён!")
    exit()

path = "."
files = os.listdir(path)
moved_count = 0
skipped_count = 0
error_count = 0

for file in files:
    if (
        file in ["main.py", "config.json"]
        or not os.path.isfile(file)
        or file.endswith(".log")
    ):
        skipped_count += 1
        continue

    moved = False
    for folder, extensions in config.items():
        for ext in extensions:
            if file.endswith(ext):
                try:
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                        log(f"📁 Создана папка: {folder}")

                    shutil.move(file, os.path.join(folder, file))
                    log(f"✅ Переместил {file} в {folder}")
                    moved_count += 1
                    moved = True
                except Exception as e:
                    log(f"❌Ошибка с файлом {file}: {str(e)}")
                    error_count += 1
                break

        if moved:
            break

    if not moved:
        log(f"⏸ Нет правил для: {file}")
        skipped_count += 1

log(
    f"🏁 Уборка завершена! Перемещено: {moved_count}, Пропущено: {skipped_count}, Ошибок: {error_count}"
)
