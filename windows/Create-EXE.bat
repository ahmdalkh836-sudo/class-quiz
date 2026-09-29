@echo off
chcp 65001 > nul
title تحويل خادم الاختبارات إلى ملف EXE مستقل لويندوز 11

echo ==============================================================
echo   بناء ملف EXE تنفيذي مستقل لخادم الاختبارات (Windows 11)
echo ==============================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] بايثون غير مثبت. يرجى تثبيت Python 3 من python.org أو Microsoft Store أولاً.
    pause
    exit /b 1
)

echo [1/3] تثبيت أداة PyInstaller لتحويل الكود إلى ملف EXE...
pip install pyinstaller

echo.
echo [2/3] جاري تجميع ملف ClassroomServer.exe المستقل...
pyinstaller --onefile --noconsole --name "ClassroomQuizServer" "%~dp0classroom_server.py"

echo.
echo ==============================================================
echo [3/3] تم إنشاء ملف EXE بنجاح!
echo ستجد الملف داخل مجلد: dist\ClassroomQuizServer.exe
echo يمكنك نقله إلى أي جهاز كمبيوتر أو لابتوب ويندوز 11 وتشغيله مباشرة دون أي متطلبات!
echo ==============================================================
echo.
pause
