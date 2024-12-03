@echo off
setlocal enabledelayedexpansion

:: Проверка наличия виртуального окружения
if not exist "venv\" (
    echo Виртуальное окружение не найдено. Создаем новое...
    
    :: Создание виртуального окружения
    python -m venv venv
    
    :: Активация виртуального окружения
    call venv\Scripts\activate
    
    :: Проверка наличия requirements.txt
    if exist "requirements.txt" (
        echo Установка зависимостей из requirements.txt...
        pip install -r requirements.txt
    ) else (
        echo Файл requirements.txt не найден. Пропускаем установку зависимостей.
    )
) else (
    echo Виртуальное окружение уже существует.
    :: Активация существующего виртуального окружения
    call venv\Scripts\activate
)

:: Проверка наличия main.py
if exist "main.py" (
    echo Запуск бота...
    python bot.py
) else (
    echo Файл bot.py не найден.
    pause
    exit /b 1
)

:: Деактивация виртуального окружения после выполнения
deactivate

pause