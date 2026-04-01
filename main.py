import os
import shutil

path = "."
files = os.listdir(path)

for file in files:
    if file == "main.py" or not os.path.isfile(file):
        continue

    if file.endswith(".txt"):
        folder = "Texts"
    elif file.endswith(".jpg") or file.endswith(".png"):
        folder = "Images"
    elif file.endswith(".pdf") or file.endswith(".docx"):
        folder = "Docs"
    else:
        continue

    if not os.path.exists(folder):
        os.makedirs(folder)

    shutil.move(file, os.path.join(folder, file))
    print(f"✅ Переместил {file} в {folder}")

print("🧹 Уборка завершена!")
