Структура проекта
family_notes_app/
├── main.py               Главный файл приложения
├── database.py           Работа с SQLite базой данных (448 строк)
├── pages.py              Страницы приложения (755 строк)
├── widgets.py            Пользовательские виджеты
├── dialogs.py            Диалоговые окна
├── styles.py             Стили оформления
├── requirements.txt      Зависимости Python
├── build_exe.py          Скрипт сборки в EXE


Краткая инструкция по запуску
1. Установка Python 3.13.5
Скачайте с
https://www.python.org/downloads/
и установите (обязательно отметьте "Add Python to PATH")

2. Открытие в PyCharm
File → Open → выберите папку family_notes_app
File → Settings → Project → Python Interpreter

3.Создайте виртуальное окружение с Python 3.13.5
Откройте командную строку или терминал в папке вашего проекта (family_notes_app). Например:

cd путь/к/папке/family_notes_app
Создайте виртуальное окружение командой:

на Windows:
python -m venv venv
на macOS или Linux:
python3 -m venv venv
Активируйте виртуальное окружение:

на Windows:
venv\Scripts\activate
на macOS или Linux:
source venv/bin/activate
После активации окружения установите все зависимости из файла requirements.txt:

pip install -r requirements.txt
Теперь запускайте приложение командой:

python main.py
