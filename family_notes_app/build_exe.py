import subprocess
import sys
import os

def build():
    try:
        import PyInstaller
    except ImportError:
        print("Устанавливаем PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    app_name = "FamilyNotes"
    main_script = "main.py"
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        f"--name={app_name}",
        "--clean",
        "--noconfirm",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=qrcode",
        "--hidden-import=PIL",
        "--hidden-import=sqlite3",
        main_script
    ]
    
    print("Начинаем сборку...")
    print("Команда:", " ".join(cmd))
    print("-" * 50)
    
    try:
        subprocess.check_call(cmd)
        print("-" * 50)
        print("✅ Сборка завершена успешно!")
        print(f"EXE файл находится в папке: dist/{app_name}.exe")
    except subprocess.CalledProcessError as e:
        print("❌ Ошибка при сборке:", e)
        return False
    
    return True

if __name__ == "__main__":
    build()
