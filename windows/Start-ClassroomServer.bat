@echo off
chcp 65001 > nul
title خادم الاختبارات المدرسية - Windows 11 PC

echo ==============================================================
echo   تشغيل خادم الاختبارات المدرسية - Windows 11 Desktop
echo ==============================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] تنبيه: لم يتم العثور على بايثون مثبت في النظام.
    echo يمكنك تثبيته بسهولة من متجر مايكروسوفت (Microsoft Store) بالبحث عن Python.
    echo أو تشغيل البرنامج من المتصفح مباشرة عبر شبكة الواي فاي.
    echo.
    pause
    exit /b 1
)

echo [+] جاري تشغيل الخادم وفتح لوحة تحكم المعلم...
python "%~dp0classroom_server.py"

pause
