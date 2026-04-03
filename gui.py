import os
import json
import shutil
import threading
from typing import Tuple
import customtkinter as ctk
from datetime import datetime

class FileOrganizerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
    
        self.title("File Organizer")
        self.geometry("500x400")

        self.iconbitmap("icon.ico")

        # Заголовок
        self.label = ctk.CTkLabel(self, text = "Уборщик Файлов v5.1", font=("Arial", 20, "bold"))
        self.label.pack(pady = 20)

        # Кнопка запуска
        self.start_button = ctk.CTkButton(self, text = "🚀 Запустить уборку", command=self.start_cleanup_thread)
        self.start_button.pack(pady = 20)

        # Кнопка выбора папки
        self.folder_button = ctk.CTkButton(self, text = "📁 Выбрать папку", command=self.select_folder)
        self.folder_button.pack(pady = 10)

        self.folder_label = ctk.CTkLabel(self, text = "Папка: текущая", text_color="gray")
        self.folder_label.pack(pady = 5)

        # Поле для логов
        self.log_text = ctk.CTkTextbox(self, width = 450, height = 200)
        self.log_text.pack(pady = 20)

        # Настройки
        self.work_path = "."
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H%M%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")

    def select_folder(self):
        folder = ctk.filedialog.askdirectory()
        if folder:
            self.work_path = folder
            self.folder_label.configure(text = f"Папка: {folder}")
            self.log(f"📁 Выбрана папка: {folder}")
    
    def start_cleanup_thread(self):
        thread = threading.Thread(target=self.cleanup_start)
        thread.start()
    
    def cleanup_start(self):
        self.start_button.configure(state = "disabled")
        self.log("🚀 Запуск уборки...")

        moved_count = 0
        skipped_count = 0
        error_count = 0

        try:
            # Загрузка конфига
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            self.log("📖 Конфигурация загружена")
        except FileNotFoundError:
            self.log("❌ОШИБКА: config.json не найден!")
            self.start_button.configure(state = "normal")
            return
        except json.JSONDecodeError:
            self.log("❌ОШИБКА: config.json повреждён!")
            self.start_button.configure(state = "normal")
            return

        files = os.listdir(self.work_path)

        for file in files:
            if file in ["main.py", "gui.py", "config.json", "icon.ico"] or file.endswith(".log"):
                skipped_count += 1
                continue
        
            if not os.path.isfile(os.path.join(self.work_path, file)):
                continue

            moved = False
            for folder, extensions in config.items():
                for ext in extensions:
                    if file.endswith(ext):
                        try:
                            target_folder = os.path.join(self.work_path, folder)
                            if not os.path.exists(target_folder):
                                os.makedirs(target_folder)
                                self.log(f"📁 Создана папка: {folder}")
                            
                            shutil.move(
                                os.path.join(self.work_path, file),
                                os.path.join(target_folder, file)
                            )
                            self.log(f"✅ Переместил {file} в {folder}")
                            moved_count += 1
                            moved = True
                        except Exception as e:
                            self.log(f"❌Ошибка с файлом {file}: {str(e)}")
                            error_count += 1
                        break
                
                if moved:
                    break
            
            if not moved:
                self.log(f"⏸ Нет правил для: {file}")
                skipped_count += 1

        self.log(f"🏁 Готов! Перемещено: {moved_count}, Пропущено: {skipped_count}, Ошибок: {error_count}")
        self.start_button.configure(state = "normal")
    
if __name__ == "__main__":
    app = FileOrganizerGUI()
    app.mainloop()