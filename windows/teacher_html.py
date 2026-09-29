# -*- coding: utf-8 -*-
r"""
Teacher Web Console HTML Template for Windows 11 Desktop Edition
Includes Teacher Auth (First Launch Setup & Login), Quiz Targeting & Editing,
Submission Details with Student Answers, Sidebar Drawer, Settings & Themes,
Anti-Cheat, and Encrypted Sync (AES-256)
"""

TEACHER_HTML = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>خادم الاختبارات المدرسية - Windows 11 Desktop Edition</title>
    <style>
        :root {
            --bg-color: #0b132b;
            --surface-color: #1c2541;
            --card-color: #243054;
            --primary: #3a86ff;
            --primary-dark: #2667d4;
            --primary-light: rgba(58, 134, 255, 0.15);
            --accent-purple: #8338ec;
            --success: #10b981;
            --success-light: rgba(16, 185, 129, 0.15);
            --danger: #ef4444;
            --danger-light: rgba(239, 68, 68, 0.15);
            --warning: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
            --radius: 18px;
        }

        body.light-mode {
            --bg-color: #f1f5f9;
            --surface-color: #ffffff;
            --card-color: #f8fafc;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            padding-bottom: 74px;
            transition: background 0.3s, color 0.3s;
        }

        /* Top Header */
        header {
            background: linear-gradient(135deg, var(--surface-color) 0%, var(--bg-color) 100%);
            border-bottom: 1.5px solid var(--border);
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 90;
        }

        .header-title-box {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .menu-btn {
            background: rgba(58, 134, 255, 0.15);
            border: 1px solid var(--border);
            color: var(--primary);
            font-size: 1.3rem;
            width: 42px;
            height: 42px;
            border-radius: 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }
        .menu-btn:hover { background: var(--primary); color: white; }

        /* Sidebar Drawer */
        .drawer-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(4px);
            z-index: 200;
            display: none;
        }

        .drawer {
            position: fixed;
            top: 0; right: 0; bottom: 0;
            width: 320px;
            background: var(--surface-color);
            border-left: 1.5px solid var(--border);
            z-index: 201;
            display: flex;
            flex-direction: column;
            transform: translateX(100%);
            transition: transform 0.25s ease-out;
            box-shadow: -4px 0 25px rgba(0,0,0,0.5);
        }

        .drawer.open {
            transform: translateX(0);
        }

        .drawer-header {
            background: linear-gradient(135deg, rgba(58,134,255,0.18) 0%, rgba(131,56,236,0.18) 100%);
            padding: 20px;
            border-bottom: 1px solid var(--border);
        }

        .drawer-content {
            padding: 12px;
            overflow-y: auto;
            flex: 1;
        }

        .drawer-category {
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--primary);
            padding: 12px 14px 4px 14px;
        }

        .drawer-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 11px 14px;
            border-radius: 12px;
            color: var(--text-main);
            text-decoration: none;
            cursor: pointer;
            margin-bottom: 4px;
            font-size: 0.92rem;
            font-weight: 600;
            transition: all 0.15s;
        }

        .drawer-item:hover, .drawer-item.active {
            background: var(--primary-light);
            color: var(--primary);
        }

        /* Server Control Card */
        .main-container {
            max-width: 1120px;
            width: 100%;
            margin: 16px auto;
            padding: 0 16px;
            flex: 1;
        }

        .server-card {
            background: var(--surface-color);
            border: 1.5px solid var(--border);
            border-radius: var(--radius);
            padding: 18px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        }

        .server-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .status-dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            display: inline-block;
        }

        .status-dot.active { background: var(--success); box-shadow: 0 0 10px var(--success); }
        .status-dot.inactive { background: var(--danger); }

        /* Switch */
        .switch { position: relative; display: inline-block; width: 50px; height: 26px; }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider {
            position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
            background-color: #475569; transition: .3s; border-radius: 34px;
        }
        .slider:before {
            position: absolute; content: ""; height: 20px; width: 20px; left: 3px; bottom: 3px;
            background-color: white; transition: .3s; border-radius: 50%;
        }
        input:checked + .slider { background-color: var(--success); }
        input:checked + .slider:before { transform: translateX(24px); }

        .url-banner {
            background: var(--primary-light);
            border: 1px solid rgba(58, 134, 255, 0.3);
            border-radius: 14px;
            padding: 12px 16px;
            margin-top: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }

        .url-text {
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--primary);
            letter-spacing: 0.5px;
        }

        .btn {
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent-purple) 100%);
            color: white;
            border: none;
            padding: 9px 16px;
            border-radius: 11px;
            cursor: pointer;
            font-weight: 700;
            font-size: 0.9rem;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: opacity 0.15s;
        }

        .btn:hover { opacity: 0.92; }
        .btn-success { background: var(--success); }
        .btn-danger { background: var(--danger); }
        .btn-warning { background: var(--warning); color: #000; }
        .btn-outline {
            background: transparent;
            border: 1.5px solid var(--border);
            color: var(--text-main);
        }
        .btn-outline:hover { border-color: var(--primary); color: var(--primary); }

        /* Bottom Nav */
        .bottom-nav {
            position: fixed;
            bottom: 0; left: 0; right: 0;
            background: var(--surface-color);
            border-top: 1.5px solid var(--border);
            display: flex;
            justify-content: space-around;
            padding: 8px 10px;
            z-index: 80;
        }

        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 0.76rem;
            color: var(--text-muted);
            cursor: pointer;
            font-weight: 600;
            gap: 4px;
            padding: 4px 8px;
            border-radius: 10px;
            transition: all 0.2s;
        }

        .nav-item.active {
            color: var(--primary);
            font-weight: 700;
            background: var(--primary-light);
        }

        /* Chips & Modals */
        .chip {
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            border: 1px solid var(--border);
            background: var(--card-color);
            color: var(--text-muted);
            white-space: nowrap;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            transition: all 0.2s;
        }

        .chip.active {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }

        .card-inner {
            background: var(--surface-color);
            border: 1.5px solid var(--border);
            border-radius: var(--radius);
            padding: 18px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .badge {
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 700;
            display: inline-block;
        }

        .form-group { margin-bottom: 14px; }
        .form-group label { display: block; font-size: 0.86rem; font-weight: 600; margin-bottom: 6px; color: var(--text-muted); }
        .form-input {
            width: 100%;
            padding: 11px 14px;
            border: 1.5px solid var(--border);
            border-radius: 11px;
            font-size: 0.95rem;
            background: var(--card-color);
            color: var(--text-main);
        }
        .form-input:focus { outline: none; border-color: var(--primary); }
        select.form-input option { background: #1c2541; color: #f8fafc; }

        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem; }
        th { text-align: right; padding: 12px 14px; color: var(--text-muted); border-bottom: 1.5px solid var(--border); font-size: 0.84rem; font-weight: 700; }
        td { padding: 12px 14px; border-bottom: 1px solid var(--border); color: var(--text-main); }
        tr:hover td { background: rgba(58, 134, 255, 0.05); }

        .modal {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.75);
            backdrop-filter: blur(5px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 300;
            padding: 16px;
        }

        .modal-body {
            background: var(--surface-color);
            border: 1.5px solid var(--border);
            border-radius: var(--radius);
            max-width: 680px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            padding: 22px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        }

        .toast {
            position: fixed;
            bottom: 84px;
            left: 50%;
            transform: translateX(-50%);
            background: #1e293b;
            color: white;
            padding: 12px 24px;
            border-radius: 12px;
            display: none;
            z-index: 999;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            font-weight: 600;
            font-size: 0.92rem;
        }

        /* Palette dots */
        .color-dot {
            width: 32px; height: 32px; border-radius: 50%; cursor: pointer; border: 2.5px solid transparent;
            display: inline-block; transition: transform 0.2s;
        }
        .color-dot:hover { transform: scale(1.15); }
        .color-dot.active { border-color: white; box-shadow: 0 0 12px rgba(255,255,255,0.8); }

        /* Auth Container Overlay */
        .auth-container-fullscreen {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: var(--bg-color);
            z-index: 500;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 16px;
        }
        .auth-box {
            background: var(--surface-color);
            border: 1.5px solid var(--border);
            border-radius: 20px;
            padding: 28px 24px;
            max-width: 460px;
            width: 100%;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }
    </style>
</head>
<body>

    <!-- ==================== TEACHER AUTH OVERLAY (First Launch Setup / Login) ==================== -->
    <div id="teacherAuthOverlay" class="auth-container-fullscreen" style="display: none;">
        <!-- 1. First Time Setup Card -->
        <div id="teacherSetupCard" class="auth-box" style="display: none;">
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="width: 54px; height: 54px; border-radius: 16px; background: var(--primary-light); border: 1.5px solid var(--primary); display: inline-flex; align-items: center; justify-content: center; font-size: 1.8rem; margin-bottom: 10px;">
                    🛡️
                </div>
                <h2 style="font-size: 1.3rem; color: var(--primary);">تهيئة حساب الأستاذ لأول مرة</h2>
                <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">قم بإنشاء بيانات حسابك وكلمة المرور لحماية لوحة التحكم</p>
            </div>

            <div class="form-group">
                <label>اسم الأستاذ / المعلم * (إجباري)</label>
                <input type="text" id="setupTeacherName" class="form-input" placeholder="مثال: أ. أحمد الخالدي">
            </div>

            <div class="form-group">
                <label>كلمة المرور لحماية لوحة التحكم * (إجباري)</label>
                <input type="password" id="setupTeacherPassword" class="form-input" placeholder="اختر كلمة مرور قوية">
            </div>

            <div class="form-group">
                <label>المادة التعليمية (اختياري)</label>
                <input type="text" id="setupTeacherSubject" class="form-input" placeholder="مثال: الفيزياء / الرياضيات">
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div class="form-group">
                    <label>اسم المستخدم (اختياري)</label>
                    <input type="text" id="setupTeacherUsername" class="form-input" placeholder="admin">
                </div>
                <div class="form-group">
                    <label>رقم الهاتف (اختياري)</label>
                    <input type="text" id="setupTeacherPhone" class="form-input" placeholder="05xxxxxxxx">
                </div>
            </div>

            <button onclick="handleTeacherSetup()" class="btn" style="width: 100%; padding: 13px; font-size: 1rem; margin-top: 8px;">
                حفظ وبدء تشغيل الخادم 🚀
            </button>
        </div>

        <!-- 2. Subsequent Login Card -->
        <div id="teacherLoginCard" class="auth-box" style="display: none;">
            <div style="text-align: center; margin-bottom: 22px;">
                <div style="width: 54px; height: 54px; border-radius: 16px; background: var(--primary-light); border: 1.5px solid var(--primary); display: inline-flex; align-items: center; justify-content: center; font-size: 1.8rem; margin-bottom: 10px;">
                    🔐
                </div>
                <h2 style="font-size: 1.3rem; color: var(--primary);">تسجيل دخول المعلم</h2>
                <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">لوحة تحكم خادم الفصل - Windows 11 Desktop Edition</p>
                <div id="loginGreetingTeacher" style="font-size: 0.95rem; font-weight: 700; color: #60a5fa; margin-top: 6px;"></div>
            </div>

            <div class="form-group">
                <label>كلمة المرور:</label>
                <input type="password" id="loginTeacherPassword" class="form-input" placeholder="أدخل كلمة المرور الخاصة بك">
            </div>

            <button onclick="handleTeacherLogin()" class="btn" style="width: 100%; padding: 13px; font-size: 1rem; margin-top: 8px;">
                دخول لوحة التحكم 🔑
            </button>
        </div>
    </div>

    <!-- Header -->
    <header>
        <div class="header-title-box">
            <button class="menu-btn" onclick="toggleDrawer(true)" title="فتح القائمة الجانبية">☰</button>
            <div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span id="headerStatusDot" class="status-dot active"></span>
                    <h1 style="font-size: 1.15rem; font-weight: 800; letter-spacing: -0.3px;">خادم الاختبارات المدرسية</h1>
                </div>
                <div id="appHeaderTeacherName" style="font-size: 0.78rem; color: var(--text-muted); font-weight: 500;">
                    خادم الفصل • Windows 11 Desktop
                </div>
            </div>
        </div>

        <div style="display: flex; align-items: center; gap: 10px;">
            <button onclick="openNewQuizModal()" class="btn btn-success" style="padding: 7px 14px; font-size: 0.85rem;">
                + اختبار جديد
            </button>
            <button onclick="handleTeacherLogout()" class="btn btn-outline" style="padding: 7px 12px; font-size: 0.82rem;" title="تسجيل الخروج">
                خروج 🚪
            </button>
        </div>
    </header>

    <!-- Sidebar Drawer Overlay & Drawer -->
    <div class="drawer-overlay" id="drawerOverlay" onclick="toggleDrawer(false)"></div>
    <div class="drawer" id="sidebarDrawer">
        <div class="drawer-header">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 44px; height: 44px; border-radius: 50%; background: var(--primary); display: flex; align-items: center; justify-content: center; font-size: 1.3rem; color: white;">
                        👨‍🏫
                    </div>
                    <div>
                        <div id="drawerTeacherName" style="font-weight: 800; font-size: 1.05rem;">الأستاذ / المعلم</div>
                        <div id="drawerTeacherSubject" style="font-size: 0.78rem; color: var(--text-muted);">المادة التعليمية</div>
                    </div>
                </div>
                <button onclick="toggleDrawer(false)" style="background: transparent; border: none; color: var(--text-muted); font-size: 1.3rem; cursor: pointer;">✕</button>
            </div>
            <div style="display: flex; gap: 8px;">
                <span class="badge" style="background: rgba(16, 185, 129, 0.2); color: var(--success); font-size: 0.75rem;" id="drawerStatusText">🟢 البث يعمل</span>
                <span class="badge" style="background: var(--primary-light); color: var(--primary); font-size: 0.75rem;" id="drawerIpText">0.0.0.0:8080</span>
            </div>
        </div>

        <div class="drawer-content">
            <div class="drawer-category">إدارة الفصل والدرجات</div>
            <div class="drawer-item active" onclick="switchMainTab('quizzes')">
                <span>📝 الاختبارات والأنشطة</span>
                <span class="badge" id="badgeQuizzesCount" style="background: var(--primary-light); color: var(--primary);">0</span>
            </div>
            <div class="drawer-item" onclick="switchMainTab('students')">
                <span>👥 الطلاب والدرجات الشهرية</span>
                <span class="badge" id="badgeStudentsCount" style="background: var(--primary-light); color: var(--primary);">0</span>
            </div>
            <div class="drawer-item" onclick="switchMainTab('submissions')">
                <span>📊 النتائج والتسليمات الحية</span>
                <span class="badge" id="badgeSubmissionsCount" style="background: var(--primary-light); color: var(--primary);">0</span>
            </div>

            <div class="drawer-category">الشبكة والبث المباشر</div>
            <div class="drawer-item" onclick="switchMainTab('logs')">
                <span>📡 سجل النشاط والبث المباشر</span>
            </div>
            <div class="drawer-item" onclick="showQrModal()">
                <span>📱 عرض كود QR للطلاب</span>
            </div>
            <div class="drawer-item" onclick="showGuideModal()">
                <span>📶 دليل شبكة Wi-Fi والهوتسبوت</span>
            </div>

            <div class="drawer-category">نقل وتشفير البيانات (AES-256)</div>
            <div class="drawer-item" onclick="openExportModal()">
                <span>🔒 سحب مشفر لبيانات الطلاب</span>
            </div>
            <div class="drawer-item" onclick="openImportModal()">
                <span>📥 استيراد بيانات مشفرة</span>
            </div>

            <div class="drawer-category">النظام والتخصيص</div>
            <div class="drawer-item" onclick="switchMainTab('settings')">
                <span>⚙️ الإعدادات والملف الشخصي</span>
            </div>
            <div class="drawer-item" style="color: var(--danger);" onclick="handleTeacherLogout()">
                <span>🚪 تسجيل الخروج من اللوحة</span>
            </div>
        </div>
    </div>

    <!-- Main Container -->
    <div class="main-container">
        <!-- 1. Real Server & Wi-Fi Control Card -->
        <div class="server-card" id="topServerCard">
            <div class="server-header">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 44px; height: 44px; border-radius: 50%; background: var(--success-light); display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">
                        📶
                    </div>
                    <div>
                        <div style="display: flex; align-items: center; gap: 6px;">
                            <span id="serverStatusDot" class="status-dot active"></span>
                            <strong id="serverStatusTitle" style="color: var(--success); font-size: 1.05rem;">خادم الحصة يعمل (نشط)</strong>
                        </div>
                        <div id="serverStatusSub" style="font-size: 0.82rem; color: var(--text-muted);">
                            المشاركة عبر شبكة Wi-Fi المشتركة للكمبيوتر
                        </div>
                    </div>
                </div>

                <label class="switch">
                    <input type="checkbox" id="serverToggleInput" checked onchange="toggleServerStatus()">
                    <span class="slider"></span>
                </label>
            </div>

            <!-- Student Direct Access URL -->
            <div class="url-banner">
                <div>
                    <div style="font-size: 0.82rem; color: var(--text-muted);">رابط دخول الطلاب في متصفح الهاتف:</div>
                    <div class="url-text" id="primaryUrlText">http://192.168.1.X:8080</div>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button onclick="copyServerUrl()" class="btn" style="padding:7px 14px; font-size:0.85rem;">نسخ الرابط 📋</button>
                    <button onclick="showQrModal()" class="btn btn-outline" style="padding:7px 14px; font-size:0.85rem;">عرض QR 📱</button>
                </div>
            </div>
        </div>

        <!-- ==================== TAB 1: Quizzes & Targeting & Editing ==================== -->
        <div id="tabQuizzes" class="card-inner">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 14px;">
                <div>
                    <h2 style="font-size: 1.15rem;">📝 بنك وتخصيص الاختبارات والأنشطة</h2>
                    <p style="font-size: 0.85rem; color: var(--text-muted);">حدد المرحلة والشعبة المستهدفة لكل اختبار، مع إمكانية تعديل الأسئلة والخيارات في أي وقت</p>
                </div>
                <button onclick="openNewQuizModal()" class="btn btn-success">+ إضافة اختبار جديد</button>
            </div>

            <!-- Filter Chips for Quizzes (Grade and Section) -->
            <div style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 16px; background: var(--card-color); padding: 12px; border-radius: 12px; border: 1px solid var(--border);">
                <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                    <span style="font-size: 0.82rem; font-weight: 700; color: var(--primary);">تصفية حسب الصف:</span>
                    <span class="chip active" id="qGradeFilterAll" onclick="filterQuizByGrade('الكل')">جميع الصفوف</span>
                    <span class="chip" id="qGradeFilterG1" onclick="filterQuizByGrade('أول ثانوي')">أول ثانوي</span>
                    <span class="chip" id="qGradeFilterG2" onclick="filterQuizByGrade('ثاني ثانوي')">ثاني ثانوي</span>
                    <span class="chip" id="qGradeFilterG3" onclick="filterQuizByGrade('ثالث ثانوي')">ثالث ثانوي</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                    <span style="font-size: 0.82rem; font-weight: 700; color: var(--primary);">تصفية حسب الشعبة:</span>
                    <span class="chip active" id="qSecFilterAll" onclick="filterQuizBySection('الكل')">جميع الشعب</span>
                    <span class="chip" id="qSecFilterS1" onclick="filterQuizBySection('شعبة 1')">شعبة 1</span>
                    <span class="chip" id="qSecFilterS2" onclick="filterQuizBySection('شعبة 2')">شعبة 2</span>
                    <span class="chip" id="qSecFilterS3" onclick="filterQuizBySection('شعبة 3')">شعبة 3</span>
                    <span class="chip" id="qSecFilterS4" onclick="filterQuizBySection('شعبة 4')">شعبة 4</span>
                </div>
            </div>

            <div id="quizzesListContainer" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(330px, 1fr)); gap: 14px;"></div>
        </div>

        <!-- ==================== TAB 2: Students & Encrypted Sync ==================== -->
        <div id="tabStudents" class="card-inner" style="display: none;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;">
                <div>
                    <h2 style="font-size: 1.15rem;">👥 سجل الطلاب والدرجات الشهرية</h2>
                    <p style="font-size: 0.85rem; color: var(--text-muted);">مقسّمة بحسب الفصول والشعب مع رصد درجات الاختبارات والمشاركة</p>
                </div>

                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                    <button onclick="openExportModal()" class="btn" style="background:var(--primary); font-size:0.85rem;">🔒 سحب مشفر</button>
                    <button onclick="openImportModal()" class="btn btn-outline" style="font-size:0.85rem;">📥 استيراد</button>
                    <button id="globalGradesBtn" onclick="toggleGlobalVisibility()" class="btn btn-outline" style="font-size:0.85rem;">👁️ الدرجات: معلنة</button>
                </div>
            </div>

            <!-- Search and Filter Chips -->
            <div style="margin-bottom: 14px;">
                <input type="text" id="studentSearchInput" onkeyup="filterStudents()" placeholder="ابحث باسم الطالب، الهوية، أو الفصل والشعبة..." class="form-input" style="margin-bottom: 10px;">
                <div id="classFilterChips" style="display: flex; gap: 8px; overflow-x: auto; padding-bottom: 4px;"></div>
            </div>

            <div id="studentsListContainer"></div>
        </div>

        <!-- ==================== TAB 3: Results & Submissions ==================== -->
        <div id="tabSubmissions" class="card-inner" style="display: none;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div>
                    <h2 style="font-size: 1.15rem;">📊 النتائج والتسليمات الحية</h2>
                    <p style="font-size: 0.85rem; color: var(--text-muted);">إجابات الطلاب الواصلة لحظياً إلى خادم الكمبيوتر</p>
                </div>
                <div style="display: flex; gap: 6px;">
                    <span class="chip active" id="subFilterAll" onclick="filterSubmissions('ALL')">الكل</span>
                    <span class="chip" id="subFilterQuiz" onclick="filterSubmissions('QUIZ')">اختبارات تقييمية</span>
                    <span class="chip" id="subFilterAct" onclick="filterSubmissions('ACTIVITY')">أنشطة صفية</span>
                </div>
            </div>

            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>اسم الطالب</th>
                            <th>الصف والشعبة</th>
                            <th>الاختبار</th>
                            <th>النوع</th>
                            <th>الدرجة</th>
                            <th>النسبة</th>
                            <th>وقت التسليم</th>
                        </tr>
                    </thead>
                    <tbody id="submissionsTableBody"></tbody>
                </table>
            </div>
            <div id="submissionsEmptyState" style="display: none; text-align: center; padding: 40px 20px; color: var(--text-muted);">
                <div style="font-size: 3rem; margin-bottom: 10px;">📊</div>
                <h3>لا توجد أي تسليمات حتى الآن</h3>
                <p style="font-size: 0.85rem; margin-top: 4px;">ستظهر هنا إجابات الطلاب ودرجاتهم فور تسليم أي اختبار.</p>
            </div>
        </div>

        <!-- ==================== TAB 4: Live Activity Logs ==================== -->
        <div id="tabLogs" class="card-inner" style="display: none;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <div>
                    <h2 style="font-size: 1.15rem;">📡 سجل النشاط والبث المباشر</h2>
                    <p style="font-size: 0.85rem; color: var(--text-muted);">متابعة فورية للأحداث (انضمام، تسليم، محاولات غش، سحب بيانات)</p>
                </div>
                <button onclick="clearLogs()" class="btn btn-outline" style="font-size:0.85rem;">مسح السجل 🗑️</button>
            </div>
            <div id="liveLogsContainer" style="display: flex; flex-direction: column; gap: 8px;"></div>
        </div>

        <!-- ==================== TAB 5: Settings & Profile ==================== -->
        <div id="tabSettings" class="card-inner" style="display: none;">
            <h2 style="font-size: 1.25rem; margin-bottom: 6px;">⚙️ الإعدادات والملف الشخصي</h2>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 18px;">التحكم في بيانات المعلم، الوضع الليلي، ألوان البرنامج، وحماية الاختبارات من الغش</p>

            <!-- Teacher Profile Card -->
            <div class="card-inner" style="background:var(--card-color); margin-bottom:16px;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 14px;">
                    <div style="width: 46px; height: 46px; border-radius: 50%; background: var(--primary-light); border:1.5px solid var(--primary); display:flex; align-items:center; justify-content:center; font-size:1.4rem;">
                        👤
                    </div>
                    <div>
                        <h3 style="font-size: 1.05rem;">بيانات المعلم والتخصص</h3>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">تظهر هذه البيانات للطلاب في رأس صفحة الاختبارات</div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px;">
                    <div class="form-group">
                        <label>اسم المعلم:</label>
                        <input type="text" id="settingTeacherName" class="form-input" placeholder="مثال: أ. أحمد الخالدي">
                    </div>
                    <div class="form-group">
                        <label>المادة التعليمية:</label>
                        <input type="text" id="settingTeacherSubject" class="form-input" placeholder="مثال: فيزياء 1">
                    </div>
                    <div class="form-group">
                        <label>رقم هاتف التواصل (اختياري):</label>
                        <input type="text" id="settingTeacherPhone" class="form-input" placeholder="05xxxxxxxx">
                    </div>
                    <div class="form-group">
                        <label>تغيير كلمة المرور للوحة التحكم:</label>
                        <input type="password" id="settingTeacherPassword" class="form-input" placeholder="اتركها فارغة إذا لم ترغب بتغييرها">
                    </div>
                </div>
                <button onclick="saveTeacherSettings()" class="btn btn-success" style="margin-top: 6px;">حفظ بيانات المعلم ✓</button>
            </div>

            <!-- Appearance & Themes -->
            <div class="card-inner" style="background:var(--card-color); margin-bottom:16px;">
                <h3 style="font-size: 1.05rem; margin-bottom: 10px;">🎨 المظهر والسمات (Theme)</h3>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <div>
                        <div style="font-weight: 600;">الوضع الليلي (Dark Mode):</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">مريح للعين أثناء الحصة وعرض الشاشة</div>
                    </div>
                    <label class="switch">
                        <input type="checkbox" id="darkModeToggle" checked onchange="toggleDarkMode()">
                        <span class="slider"></span>
                    </label>
                </div>

                <div>
                    <label style="display:block; font-size: 0.85rem; font-weight:600; color:var(--text-muted); margin-bottom:8px;">لون التمييز الرئيسي (Accent Color):</label>
                    <div style="display: flex; gap: 12px;">
                        <span class="color-dot active" style="background:#3a86ff;" onclick="setThemeColor('#3a86ff')" title="أزرق ويندوز"></span>
                        <span class="color-dot" style="background:#10b981;" onclick="setThemeColor('#10b981')" title="أخضر زمردي"></span>
                        <span class="color-dot" style="background:#8338ec;" onclick="setThemeColor('#8338ec')" title="بنفسجي ملكي"></span>
                        <span class="color-dot" style="background:#f59e0b;" onclick="setThemeColor('#f59e0b')" title="كهرماني"></span>
                        <span class="color-dot" style="background:#ef4444;" onclick="setThemeColor('#ef4444')" title="أحمر ياقوتي"></span>
                    </div>
                </div>
            </div>

            <!-- Anti-Cheat Options -->
            <div class="card-inner" style="background:var(--card-color);">
                <h3 style="font-size: 1.05rem; margin-bottom: 10px;">🛡️ خيارات الأمان ومنع الغش</h3>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div>
                        <div style="font-weight: 600;">كشف شبكة الهاتف الخارجية (4G/5G):</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">تنبيه المعلم فوراً عند محاولة تشغيل شريحة البيانات أو مغادرة الصفحة</div>
                    </div>
                    <label class="switch">
                        <input type="checkbox" id="antiCheatToggle" checked onchange="saveTeacherSettings()">
                        <span class="slider"></span>
                    </label>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 600;">منع إعادة الاختبار:</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">السماح للطالب بحل الاختبار لمرة واحدة فقط لكل حساب مسجل</div>
                    </div>
                    <label class="switch">
                        <input type="checkbox" id="preventRetakeToggle" checked onchange="saveTeacherSettings()">
                        <span class="slider"></span>
                    </label>
                </div>
            </div>
        </div>
    </div>

    <!-- Bottom Navigation Bar -->
    <div class="bottom-nav">
        <div class="nav-item active" id="bNavQuizzes" onclick="switchMainTab('quizzes')">
            <span style="font-size:1.2rem;">📝</span>
            <span>الاختبارات</span>
        </div>
        <div class="nav-item" id="bNavStudents" onclick="switchMainTab('students')">
            <span style="font-size:1.2rem;">👥</span>
            <span>الطلاب والدرجات</span>
        </div>
        <div class="nav-item" id="bNavSubmissions" onclick="switchMainTab('submissions')">
            <span style="font-size:1.2rem;">📊</span>
            <span>التسليمات</span>
        </div>
        <div class="nav-item" id="bNavLogs" onclick="switchMainTab('logs')">
            <span style="font-size:1.2rem;">📡</span>
            <span>السجل الحي</span>
        </div>
        <div class="nav-item" id="bNavSettings" onclick="switchMainTab('settings')">
            <span style="font-size:1.2rem;">⚙️</span>
            <span>الإعدادات</span>
        </div>
    </div>

    <!-- ==================== MODAL 1: Export Encrypted Data ==================== -->
    <div id="exportModal" class="modal">
        <div class="modal-body">
            <h3 style="color: var(--primary); font-size: 1.25rem; margin-bottom: 12px;">🔒 سحب وتصدير بيانات الطلاب مشفرة (AES-256)</h3>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
                سيتم تشفير بيانات جميع الطلاب وفصولهم وشعبهم والدرجات الشهرية والملاحظات باستخدام خوارزمية التشفير العسكري AES-256 واشتقاق المفاتيح PBKDF2 لنقلها بأمان إلى جهازك.
            </p>

            <div class="form-group">
                <label>كلمة مرور التشفير الخاصة بك:</label>
                <input type="password" id="exportPassword" class="form-input" placeholder="اكتب كلمة مرور لحماية الملف المشفر">
            </div>

            <div id="exportResultArea" style="display: none; margin-top: 14px;">
                <label style="font-size: 0.85rem; font-weight: 600; color: var(--success);">تم إنشاء الكود المشفر بنجاح:</label>
                <textarea id="exportedCipherCode" class="form-input" rows="4" readonly style="font-family: monospace; font-size: 0.82rem; margin-top: 4px;"></textarea>
                <div style="display: flex; gap: 8px; margin-top: 10px;">
                    <button onclick="copyExportedCode()" class="btn" style="flex:1;">نسخ الكود 📋</button>
                    <button onclick="downloadExportedFile()" class="btn btn-success" style="flex:1;">تحميل كملف (.enc) 💾</button>
                </div>
            </div>

            <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 18px;">
                <button onclick="closeModal('exportModal')" class="btn btn-outline">إغلاق</button>
                <button onclick="executeEncryptedExport()" class="btn" id="btnRunExport">بدء التشفير والتصدير 🔒</button>
            </div>
        </div>
    </div>

    <!-- ==================== MODAL 2: Import Encrypted Data ==================== -->
    <div id="importModal" class="modal">
        <div class="modal-body">
            <h3 style="color: var(--primary); font-size: 1.25rem; margin-bottom: 12px;">📥 استيراد بيانات الطلاب المشفرة</h3>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
                ارفع ملف النسخة الاحتياطية المشفر (.enc) أو الصق الكود المشفر لدمج الطلاب والدرجات في قاعدة البيانات المحلية.
            </p>

            <div class="form-group">
                <label>رفع ملف مشفر (.enc):</label>
                <input type="file" id="importFileInput" accept=".enc,.txt" class="form-input" onchange="handleFileSelected(event)">
            </div>

            <div class="form-group">
                <label>أو الصق الكود المشفر هنا:</label>
                <textarea id="importCodeInput" class="form-input" rows="3" placeholder="CRS_ENC_V1:..."></textarea>
            </div>

            <div class="form-group">
                <label>كلمة المرور المستخدمة أثناء التشفير:</label>
                <input type="password" id="importPassword" class="form-input" placeholder="أدخل كلمة المرور لفك التشفير">
            </div>

            <div style="display: flex; align-items: center; gap: 8px; margin: 12px 0;">
                <input type="checkbox" id="importOverwriteCheck">
                <label for="importOverwriteCheck" style="font-size: 0.88rem; cursor: pointer;">استبدال بيانات الطلاب الموجودة مسبقاً في حال تشابه الأسماء</label>
            </div>

            <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 18px;">
                <button onclick="closeModal('importModal')" class="btn btn-outline">إلغاء</button>
                <button onclick="executeEncryptedImport()" class="btn btn-success" id="btnRunImport">فك التشفير واستيراد البيانات 📥</button>
            </div>
        </div>
    </div>

    <!-- ==================== MODAL 3: Student Evaluation Dialog ==================== -->
    <div id="evalModal" class="modal">
        <div class="modal-body">
            <h3 id="evalModalTitle" style="color: var(--primary); font-size: 1.2rem; margin-bottom: 14px;">رصد درجات الطالب</h3>
            <input type="hidden" id="evalStudentId">

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div class="form-group">
                    <label>الصف الدراسي:</label>
                    <select id="evalGrade" class="form-input">
                        <option value="أول ثانوي">أول ثانوي</option>
                        <option value="ثاني ثانوي">ثاني ثانوي</option>
                        <option value="ثالث ثانوي">ثالث ثانوي</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>الشعبة:</label>
                    <select id="evalSection" class="form-input">
                        <option value="شعبة 1">شعبة 1</option>
                        <option value="شعبة 2">شعبة 2</option>
                        <option value="شعبة 3">شعبة 3</option>
                        <option value="شعبة 4">شعبة 4</option>
                    </select>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div class="form-group">
                    <label>الاختبار الشهري الأول:</label>
                    <input type="number" step="0.5" id="evalExam1" class="form-input">
                </div>
                <div class="form-group">
                    <label>الاختبار الشهري الثاني:</label>
                    <input type="number" step="0.5" id="evalExam2" class="form-input">
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div class="form-group">
                    <label>درجة المشاركة:</label>
                    <input type="number" step="0.5" id="evalPart" class="form-input">
                </div>
                <div class="form-group">
                    <label>نقاط إضافية / خصم (+/-):</label>
                    <input type="number" step="0.5" id="evalBonus" class="form-input">
                </div>
            </div>

            <div class="form-group">
                <label>ملاحظة وتوجيه المعلم للطالب:</label>
                <textarea id="evalNotes" rows="2" class="form-input"></textarea>
            </div>

            <div style="display: flex; gap: 20px; margin: 12px 0;">
                <label style="cursor: pointer;"><input type="checkbox" id="evalShowGrades"> إظهار الدرجات للطالب</label>
                <label style="cursor: pointer;"><input type="checkbox" id="evalShowNotes"> إظهار الملاحظة للطالب</label>
            </div>

            <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 16px;">
                <button onclick="closeModal('evalModal')" class="btn btn-outline">إلغاء</button>
                <button onclick="saveStudentEvaluation()" class="btn btn-success">حفظ التقييم ✓</button>
            </div>
        </div>
    </div>

    <!-- ==================== MODAL 4: Create or Edit Quiz (Targeting & Questions) ==================== -->
    <div id="quizModal" class="modal">
        <div class="modal-body" style="max-width: 720px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
                <h3 id="quizModalMainTitle" style="color: var(--primary); font-size: 1.25rem;">إنشاء اختبار / نشاط جديد</h3>
                <span id="quizModalModeBadge" class="badge" style="background:var(--primary-light); color:var(--primary);">جديد</span>
            </div>
            <input type="hidden" id="editingQuizId" value="">

            <div class="form-group">
                <label>عنوان الاختبار *:</label>
                <input type="text" id="newQuizTitle" class="form-input" placeholder="مثال: الاختبار الفتري الأول - فيزياء">
            </div>

            <div class="form-group">
                <label>تعليمات أو وصف:</label>
                <input type="text" id="newQuizDesc" class="form-input" placeholder="مثال: مدة الاختبار 10 دقائق، يتكون من 5 أسئلة">
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div class="form-group">
                    <label>المدة بالدقائق:</label>
                    <input type="number" id="newQuizDuration" class="form-input" value="10">
                </div>
                <div class="form-group">
                    <label>نوع الاختبار:</label>
                    <select id="newQuizType" class="form-input">
                        <option value="QUIZ">اختبار تقييمي</option>
                        <option value="ACTIVITY">نشاط صفي تفاعلي</option>
                    </select>
                </div>
            </div>

            <!-- Quiz Targeting: Grade and Section (Required Feature 3) -->
            <div style="background: var(--card-color); border: 1.5px solid var(--border); border-radius: 12px; padding: 14px; margin-bottom: 14px;">
                <div style="font-weight: 700; color: var(--primary); font-size: 0.95rem; margin-bottom: 8px;">🎯 استهداف وتخصيص الفصول والشعب:</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div class="form-group" style="margin-bottom:0;">
                        <label>الصف المستهدف:</label>
                        <select id="newQuizTargetGrade" class="form-input">
                            <option value="الكل">متاح لجميع الصفوف (الكل)</option>
                            <option value="أول ثانوي">أول ثانوي فقط</option>
                            <option value="ثاني ثانوي">ثاني ثانوي فقط</option>
                            <option value="ثالث ثانوي">ثالث ثانوي فقط</option>
                        </select>
                    </div>
                    <div class="form-group" style="margin-bottom:0;">
                        <label>الشعبة المستهدفة:</label>
                        <select id="newQuizTargetSection" class="form-input">
                            <option value="الكل">متاح لجميع الشعب (الكل)</option>
                            <option value="شعبة 1">شعبة 1 فقط</option>
                            <option value="شعبة 2">شعبة 2 فقط</option>
                            <option value="شعبة 3">شعبة 3 فقط</option>
                            <option value="شعبة 4">شعبة 4 فقط</option>
                        </select>
                    </div>
                </div>
                <div style="font-size:0.78rem; color:var(--text-muted); margin-top:6px;">يظهر هذا الاختبار للطلاب المطابقين للصف والشعبة المحددة فقط.</div>
            </div>

            <h4 style="margin: 14px 0 8px 0; font-size: 1rem; color: var(--primary);">الأسئلة والخيارات:</h4>
            <div id="newQuestionsContainer"></div>
            <button onclick="addQuestionItem()" class="btn btn-outline" style="margin-top: 8px; width: 100%;">+ إضافة سؤال جديد</button>

            <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 20px;">
                <button onclick="closeModal('quizModal')" class="btn btn-outline">إلغاء</button>
                <button onclick="submitQuizForm()" class="btn btn-success" id="btnSaveQuizAction">حفظ ونشر الاختبار للطلاب ✓</button>
            </div>
        </div>
    </div>

    <!-- ==================== MODAL 5: Quiz Details & Submissions Table with Answers ==================== -->
    <div id="quizDetailsModal" class="modal">
        <div class="modal-body" style="max-width: 820px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:14px;">
                <div>
                    <h3 id="qdModalTitle" style="color: var(--primary); font-size: 1.25rem;">تفاصيل ونتائج الاختبار</h3>
                    <div id="qdModalSub" style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;"></div>
                </div>
                <button onclick="closeModal('quizDetailsModal')" class="btn btn-outline" style="padding:4px 10px; font-size:0.85rem;">✕ إغلاق</button>
            </div>

            <!-- Stats Bar -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin-bottom: 16px;">
                <div style="background:var(--card-color); padding:12px; border-radius:12px; border:1px solid var(--border); text-align:center;">
                    <div style="font-size:0.78rem; color:var(--text-muted);">إجمالي التسليمات</div>
                    <div id="qdStatSubCount" style="font-size:1.4rem; font-weight:800; color:var(--primary); margin-top:2px;">0</div>
                </div>
                <div style="background:var(--card-color); padding:12px; border-radius:12px; border:1px solid var(--border); text-align:center;">
                    <div style="font-size:0.78rem; color:var(--text-muted);">متوسط الدرجات</div>
                    <div id="qdStatAverage" style="font-size:1.4rem; font-weight:800; color:var(--success); margin-top:2px;">0%</div>
                </div>
                <div style="background:var(--card-color); padding:12px; border-radius:12px; border:1px solid var(--border); text-align:center;">
                    <div style="font-size:0.78rem; color:var(--text-muted);">أعلى درجة</div>
                    <div id="qdStatMax" style="font-size:1.4rem; font-weight:800; color:#60a5fa; margin-top:2px;">0</div>
                </div>
                <div style="background:var(--card-color); padding:12px; border-radius:12px; border:1px solid var(--border); text-align:center;">
                    <div style="font-size:0.78rem; color:var(--text-muted);">أدنى درجة</div>
                    <div id="qdStatMin" style="font-size:1.4rem; font-weight:800; color:var(--warning); margin-top:2px;">0</div>
                </div>
            </div>

            <!-- Submissions Table -->
            <h4 style="font-size:1rem; margin-bottom:8px; color:var(--text-main);">الطلاب الذين سلموا إجاباتهم:</h4>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>اسم الطالب</th>
                            <th>الصف والشعبة</th>
                            <th>الدرجة</th>
                            <th>النسبة</th>
                            <th>وقت التسليم</th>
                            <th>عرض الإجابات</th>
                        </tr>
                    </thead>
                    <tbody id="qdTableBody"></tbody>
                </table>
            </div>
            <div id="qdEmptyState" style="display:none; text-align:center; padding:30px; color:var(--text-muted);">لم يقم أي طالب بتسليم هذا الاختبار حتى الآن.</div>

            <!-- Expanded Answers Viewer Box -->
            <div id="qdAnswersBox" style="display:none; margin-top:18px; background:var(--card-color); border:1.5px solid var(--primary); border-radius:14px; padding:16px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <h4 style="color:var(--primary); font-size:1.05rem;" id="qdAnswersStudentTitle">إجابات الطالب بالتفصيل</h4>
                    <button onclick="document.getElementById('qdAnswersBox').style.display='none'" class="btn btn-outline" style="padding:2px 8px; font-size:0.75rem;">إخفاء ✕</button>
                </div>
                <div id="qdAnswersList" style="display:flex; flex-direction:column; gap:10px;"></div>
            </div>
        </div>
    </div>

    <!-- ==================== MODAL 6: QR Code Presentation ==================== -->
    <div id="qrModal" class="modal">
        <div class="modal-body" style="max-width: 400px; text-align: center;">
            <h3 style="color: var(--primary); margin-bottom: 8px;">مسح رمز QR للدخول 📱</h3>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">وجه كاميرا هاتف الطالب نحو الشاشة للدخول فوراً</p>
            <div style="background: white; padding: 16px; border-radius: 16px; display: inline-block;">
                <canvas id="qrCanvas" width="220" height="220"></canvas>
            </div>
            <div id="qrModalUrl" style="font-size: 0.95rem; font-weight: 700; color: var(--primary); margin-top: 14px; word-break: break-all;"></div>
            <button onclick="closeModal('qrModal')" class="btn btn-outline" style="margin-top: 16px; width: 100%;">إغلاق</button>
        </div>
    </div>

    <!-- ==================== MODAL 7: Wi-Fi Guide Modal ==================== -->
    <div id="guideModal" class="modal">
        <div class="modal-body" style="max-width: 580px;">
            <h3 style="color: var(--primary); font-size: 1.2rem; margin-bottom: 12px;">📡 دليل المشاركة والاتصال بالفصل</h3>
            <div style="background: var(--primary-light); border:1px solid rgba(58,134,255,0.3); border-radius:12px; padding:14px; margin-bottom:12px;">
                <h4 style="color:var(--primary); margin-bottom:4px;">1. شبكة Wi-Fi المشتركة (الموصى بها):</h4>
                <p style="font-size:0.85rem; line-height:1.5;">إذا كان لابتوب المعلم وهواتف الطلاب متصلين بنفس راوتر المدرسة أو المعمل، يدخل الطلاب مباشرة على رابط الـ IP دون الحاجة لبث هوتسبوت.</p>
            </div>
            <div style="background: var(--card-color); border:1px solid var(--border); border-radius:12px; padding:14px;">
                <h4 style="color:#60a5fa; margin-bottom:4px;">2. نقطة اتصال الهاتف (Hotspot):</h4>
                <p style="font-size:0.85rem; line-height:1.5;">في حال عدم توفر راوتر، شغل نقطة اتصال الهواتف المحمولة من لابتوب ويندوز 11 أو الهاتف، ليتصل الطلاب بالشبكة ويفتحوا الاختبارات بدون إنترنت خارجي.</p>
            </div>
            <button onclick="closeModal('guideModal')" class="btn btn-outline" style="margin-top:16px; width:100%;">فهمت ذلك ✓</button>
        </div>
    </div>

    <div id="toast" class="toast"></div>

    <script>
        let serverData = { students: [], quizzes: [], submissions: [], logs: [], settings: {} };
        let currentTab = 'quizzes';
        let selectedClassFilter = 'ALL';
        let currentSubFilter = 'ALL';
        let selectedQuizGradeFilter = 'الكل';
        let selectedQuizSectionFilter = 'الكل';
        let primaryIp = '127.0.0.1';
        let activeQuizDetails = null;

        window.addEventListener('DOMContentLoaded', () => {
            checkAuthAndInit();
            setInterval(() => {
                if (isTeacherLoggedIn()) {
                    fetchData();
                }
            }, 5000);
            initTheme();
        });

        function showToast(msg, isErr) {
            const t = document.getElementById('toast');
            t.textContent = msg;
            t.style.background = isErr ? '#dc2626' : '#1e293b';
            t.style.display = 'block';
            setTimeout(() => { t.style.display = 'none'; }, 3000);
        }

        // ==================== TEACHER AUTH LOGIC ====================
        function isTeacherLoggedIn() {
            return localStorage.getItem('teacher_logged_in') === 'true';
        }

        async function checkAuthAndInit() {
            try {
                const res = await fetch('/api/teacher/auth-status');
                const d = await res.json();

                if (!d.isSetup) {
                    // First Launch Setup
                    document.getElementById('teacherAuthOverlay').style.display = 'flex';
                    document.getElementById('teacherSetupCard').style.display = 'block';
                    document.getElementById('teacherLoginCard').style.display = 'none';
                    return;
                }

                if (!isTeacherLoggedIn()) {
                    // Subsequent Launch Login
                    document.getElementById('teacherAuthOverlay').style.display = 'flex';
                    document.getElementById('teacherSetupCard').style.display = 'none';
                    document.getElementById('teacherLoginCard').style.display = 'block';
                    document.getElementById('loginGreetingTeacher').textContent = 'مرحباً، ' + (d.teacherName || 'الأستاذ');
                    return;
                }

                // Authenticated
                document.getElementById('teacherAuthOverlay').style.display = 'none';
                fetchData();
            } catch(e) {
                fetchData();
            }
        }

        async function handleTeacherSetup() {
            const name = document.getElementById('setupTeacherName').value.trim();
            const password = document.getElementById('setupTeacherPassword').value.trim();
            const subject = document.getElementById('setupTeacherSubject').value.trim();
            const username = document.getElementById('setupTeacherUsername').value.trim() || 'admin';
            const phone = document.getElementById('setupTeacherPhone').value.trim();

            if (!name) return showToast('اسم الأستاذ إجباري', true);
            if (!password) return showToast('كلمة المرور إجبارية لحماية الخادم', true);

            try {
                const res = await fetch('/api/teacher/setup', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ name, password, subject, username, phone })
                });
                const d = await res.json();
                if (d.success) {
                    localStorage.setItem('teacher_logged_in', 'true');
                    document.getElementById('teacherAuthOverlay').style.display = 'none';
                    showToast('تم إعداد حساب الأستاذ بنجاح!');
                    fetchData();
                } else {
                    showToast(d.message || 'فشل إعداد الحساب', true);
                }
            } catch(e) {
                showToast('خطأ أثناء إعداد الحساب', true);
            }
        }

        async function handleTeacherLogin() {
            const password = document.getElementById('loginTeacherPassword').value.trim();
            if (!password) return showToast('أدخل كلمة المرور', true);

            try {
                const res = await fetch('/api/teacher/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ password })
                });
                const d = await res.json();
                if (d.success) {
                    localStorage.setItem('teacher_logged_in', 'true');
                    document.getElementById('teacherAuthOverlay').style.display = 'none';
                    showToast('تم تسجيل الدخول بنجاح! أهلاً بك');
                    fetchData();
                } else {
                    showToast(d.message || 'كلمة المرور غير صحيحة', true);
                }
            } catch(e) {
                showToast('تعذر الاتصال بالخادم', true);
            }
        }

        function handleTeacherLogout() {
            if (confirm('هل ترغب بتسجيل الخروج من لوحة التحكم؟')) {
                localStorage.removeItem('teacher_logged_in');
                location.reload();
            }
        }

        // ==================== NAVIGATION & MODALS ====================
        function toggleDrawer(open) {
            document.getElementById('sidebarDrawer').classList.toggle('open', open);
            document.getElementById('drawerOverlay').style.display = open ? 'block' : 'none';
        }

        function closeModal(id) {
            document.getElementById(id).style.display = 'none';
        }

        function switchMainTab(tab) {
            currentTab = tab;
            toggleDrawer(false);

            ['quizzes', 'students', 'submissions', 'logs', 'settings'].forEach(t => {
                const el = document.getElementById('tab' + t.charAt(0).toUpperCase() + t.slice(1));
                if (el) el.style.display = (t === tab) ? 'block' : 'none';

                const bNav = document.getElementById('bNav' + t.charAt(0).toUpperCase() + t.slice(1));
                if (bNav) bNav.classList.toggle('active', t === tab);
            });

            document.getElementById('topServerCard').style.display = (tab === 'settings') ? 'none' : 'block';
        }

        // ==================== FETCH & RENDER ====================
        async function fetchData() {
            try {
                const res = await fetch('/api/teacher/data');
                const d = await res.json();
                serverData = d;
                renderAll();
            } catch(e) {}
        }

        function renderAll() {
            // Update counts in drawer
            document.getElementById('badgeQuizzesCount').textContent = (serverData.quizzes || []).length;
            document.getElementById('badgeStudentsCount').textContent = (serverData.students || []).length;
            document.getElementById('badgeSubmissionsCount').textContent = (serverData.submissions || []).length;

            // Header and profile
            const tName = serverData.settings.teacher_name || 'خادم الفصل • Windows 11';
            const tSub = serverData.settings.teacher_subject || 'بث مباشر عبر الواي فاي';
            document.getElementById('appHeaderTeacherName').textContent = tName;
            document.getElementById('drawerTeacherName').textContent = tName;
            document.getElementById('drawerTeacherSubject').textContent = tSub;
            document.getElementById('settingTeacherName').value = serverData.settings.teacher_name || '';
            document.getElementById('settingTeacherSubject').value = serverData.settings.teacher_subject || '';
            document.getElementById('settingTeacherPhone').value = serverData.settings.teacher_phone || '';

            // Status
            const isOpen = serverData.isOpen !== false;
            document.getElementById('serverToggleInput').checked = isOpen;
            document.getElementById('serverStatusDot').className = 'status-dot ' + (isOpen ? 'active' : 'inactive');
            document.getElementById('headerStatusDot').className = 'status-dot ' + (isOpen ? 'active' : 'inactive');
            document.getElementById('serverStatusTitle').textContent = isOpen ? 'خادم الحصة يعمل (نشط)' : 'الخادم متوقف مؤقتاً';
            document.getElementById('serverStatusTitle').style.color = isOpen ? 'var(--success)' : 'var(--danger)';
            document.getElementById('drawerStatusText').textContent = isOpen ? '🟢 البث يعمل' : '⚪ البث متوقف';

            // IPs
            if (serverData.serverIps && serverData.serverIps.length > 0) {
                primaryIp = serverData.serverIps[0];
                const fullUrl = 'http://' + primaryIp + ':8080';
                document.getElementById('primaryUrlText').textContent = fullUrl;
                document.getElementById('drawerIpText').textContent = primaryIp + ':8080';
            }

            // Anti-cheat & prevent retake toggles
            document.getElementById('antiCheatToggle').checked = (serverData.settings.anti_cheat !== '0');
            document.getElementById('preventRetakeToggle').checked = (serverData.settings.prevent_retake !== '0');

            // Render components
            renderQuizzes();
            renderStudents();
            renderSubmissions();
            renderLogs();
        }

        // ==================== QUIZZES (Targeting, Filtering & Editing) ====================
        function filterQuizByGrade(grade) {
            selectedQuizGradeFilter = grade;
            ['All', 'G1', 'G2', 'G3'].forEach(k => {
                const el = document.getElementById('qGradeFilter' + k);
                if (el) el.classList.remove('active');
            });
            if (grade === 'الكل') document.getElementById('qGradeFilterAll').classList.add('active');
            else if (grade === 'أول ثانوي') document.getElementById('qGradeFilterG1').classList.add('active');
            else if (grade === 'ثاني ثانوي') document.getElementById('qGradeFilterG2').classList.add('active');
            else if (grade === 'ثالث ثانوي') document.getElementById('qGradeFilterG3').classList.add('active');
            renderQuizzes();
        }

        function filterQuizBySection(sec) {
            selectedQuizSectionFilter = sec;
            ['All', 'S1', 'S2', 'S3', 'S4'].forEach(k => {
                const el = document.getElementById('qSecFilter' + k);
                if (el) el.classList.remove('active');
            });
            if (sec === 'الكل') document.getElementById('qSecFilterAll').classList.add('active');
            else if (sec === 'شعبة 1') document.getElementById('qSecFilterS1').classList.add('active');
            else if (sec === 'شعبة 2') document.getElementById('qSecFilterS2').classList.add('active');
            else if (sec === 'شعبة 3') document.getElementById('qSecFilterS3').classList.add('active');
            else if (sec === 'شعبة 4') document.getElementById('qSecFilterS4').classList.add('active');
            renderQuizzes();
        }

        function renderQuizzes() {
            const cont = document.getElementById('quizzesListContainer');
            let qList = serverData.quizzes || [];

            // Apply Grade & Section filters
            if (selectedQuizGradeFilter !== 'الكل') {
                qList = qList.filter(q => q.targetGrade === selectedQuizGradeFilter || q.targetGrade === 'الكل');
            }
            if (selectedQuizSectionFilter !== 'الكل') {
                qList = qList.filter(q => q.targetSection === selectedQuizSectionFilter || q.targetSection === 'الكل');
            }

            if (qList.length === 0) {
                cont.innerHTML = '<div style="grid-column:1/-1; text-align:center; padding:30px; color:var(--text-muted);"><div style="font-size:2rem; margin-bottom:8px;">📝</div>لا توجد اختبارات مطابقة للتصفية. انقر فوق (+ إضافة اختبار جديد) للبدء.</div>';
                return;
            }

            let h = '';
            qList.forEach(q => {
                const tg = q.targetGrade || 'الكل';
                const ts = q.targetSection || 'الكل';
                const targetDisplay = (tg === 'الكل' && ts === 'الكل') ? 'متاح للجميع' : (tg + ' • ' + ts);
                const subCount = q.submissionsCount || 0;

                h += '<div class="card-inner" style="background:var(--card-color); display:flex; flex-direction:column; justify-content:space-between;">' +
                    '<div>' +
                        '<div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">' +
                            '<h3 style="font-size:1.08rem; color:var(--text-main); font-weight:700;">' + q.title + '</h3>' +
                            '<span class="badge" style="background:' + (q.isActive ? 'var(--success-light)' : 'var(--danger-light)') + '; color:' + (q.isActive ? 'var(--success)' : 'var(--danger)') + ';">' + (q.isActive ? 'نشط ومتاح' : 'مغلق') + '</span>' +
                        '</div>' +
                        '<div style="display:flex; gap:6px; flex-wrap:wrap; margin-bottom:10px;">' +
                            '<span class="badge" style="background:var(--primary-light); color:var(--primary);">🎯 ' + targetDisplay + '</span>' +
                            '<span class="badge" style="background:rgba(255,255,255,0.08); color:var(--text-muted);">' + (q.type === 'ACTIVITY' ? 'نشاط صفي' : 'اختبار تقييمي') + '</span>' +
                        '</div>' +
                        '<p style="font-size:0.85rem; color:var(--text-muted); line-height:1.4; margin-bottom:12px;">' + (q.description || 'بدون وصف إضافي') + '</p>' +
                    '</div>' +
                    '<div>' +
                        '<div style="display:flex; justify-content:space-between; align-items:center; font-size:0.82rem; color:var(--text-muted); margin-bottom:12px; border-top:1px solid var(--border); padding-top:8px;">' +
                            '<span>⏱️ ' + q.durationMinutes + ' دقيقة • ' + (q.questionCount || 0) + ' سؤال</span>' +
                            '<span style="font-weight:700; color:' + (subCount > 0 ? 'var(--success)' : 'var(--text-muted)') + ';">📥 ' + subCount + ' تسليم</span>' +
                        '</div>' +
                        '<div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:6px;">' +
                            '<button onclick="openQuizDetailsModal(' + q.id + ')" class="btn btn-outline" style="padding:6px; font-size:0.78rem; justify-content:center;">النتائج 📊</button>' +
                            '<button onclick="openEditQuizModal(' + q.id + ')" class="btn" style="padding:6px; font-size:0.78rem; justify-content:center; background:var(--primary);">تعديل ✏️</button>' +
                            '<button onclick="toggleQuizActive(' + q.id + ', ' + q.isActive + ')" class="btn ' + (q.isActive ? 'btn-danger' : 'btn-success') + '" style="padding:6px; font-size:0.78rem; justify-content:center;">' + (q.isActive ? 'إغلاق 🔒' : 'تفعيل 🔓') + '</button>' +
                        '</div>' +
                    '</div>' +
                '</div>';
            });
            cont.innerHTML = h;
        }

        async function toggleQuizActive(id, curr) {
            await fetch('/api/teacher/toggle-quiz', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ quizId: id, isActive: !curr })
            });
            fetchData();
        }

        // ==================== CREATE & EDIT QUIZ MODAL ====================
        let questionCounter = 0;

        function openNewQuizModal() {
            document.getElementById('editingQuizId').value = '';
            document.getElementById('quizModalMainTitle').textContent = 'إنشاء اختبار / نشاط جديد';
            document.getElementById('quizModalModeBadge').textContent = 'جديد';
            document.getElementById('btnSaveQuizAction').textContent = 'حفظ ونشر الاختبار للطلاب ✓';

            document.getElementById('newQuizTitle').value = '';
            document.getElementById('newQuizDesc').value = '';
            document.getElementById('newQuizDuration').value = '10';
            document.getElementById('newQuizType').value = 'QUIZ';
            document.getElementById('newQuizTargetGrade').value = 'الكل';
            document.getElementById('newQuizTargetSection').value = 'الكل';

            document.getElementById('newQuestionsContainer').innerHTML = '';
            questionCounter = 0;
            addQuestionItem();
            document.getElementById('quizModal').style.display = 'flex';
        }

        async function openEditQuizModal(qid) {
            try {
                const res = await fetch('/api/teacher/quiz-detail?id=' + qid);
                const d = await res.json();
                if (!d.quiz) return showToast('تعذر جلب تفاصيل الاختبار', true);

                document.getElementById('editingQuizId').value = d.quiz.id;
                document.getElementById('quizModalMainTitle').textContent = 'تعديل الاختبار: ' + d.quiz.title;
                document.getElementById('quizModalModeBadge').textContent = 'تعديل #' + d.quiz.id;
                document.getElementById('btnSaveQuizAction').textContent = 'تحديث وحفظ التعديلات ✓';

                document.getElementById('newQuizTitle').value = d.quiz.title || '';
                document.getElementById('newQuizDesc').value = d.quiz.description || '';
                document.getElementById('newQuizDuration').value = d.quiz.durationMinutes || 10;
                document.getElementById('newQuizType').value = d.quiz.type || 'QUIZ';
                document.getElementById('newQuizTargetGrade').value = d.quiz.targetGrade || 'الكل';
                document.getElementById('newQuizTargetSection').value = d.quiz.targetSection || 'الكل';

                const cont = document.getElementById('newQuestionsContainer');
                cont.innerHTML = '';
                questionCounter = 0;

                const questions = d.questions || [];
                if (questions.length === 0) {
                    addQuestionItem();
                } else {
                    questions.forEach(q => {
                        addQuestionItem(q);
                    });
                }

                document.getElementById('quizModal').style.display = 'flex';
            } catch(e) {
                showToast('خطأ أثناء فتح وضع التعديل', true);
            }
        }

        function addQuestionItem(data = null) {
            questionCounter++;
            const idx = questionCounter;
            const cont = document.getElementById('newQuestionsContainer');

            const qText = data ? (data.questionText || '') : '';
            const opA = data ? (data.optionA || '') : '';
            const opB = data ? (data.optionB || '') : '';
            const opC = data ? (data.optionC || '') : '';
            const opD = data ? (data.optionD || '') : '';
            const correct = data ? (data.correctAnswer || 'A') : 'A';
            const pts = data ? (data.points || 1) : 1;

            const div = document.createElement('div');
            div.className = 'card-inner';
            div.style.background = 'var(--card-color)';
            div.style.marginBottom = '12px';
            div.id = 'qBox_' + idx;
            div.innerHTML =
                '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">' +
                    '<span style="font-weight:700; color:var(--primary); font-size:0.92rem;">السؤال #' + idx + '</span>' +
                    '<button onclick="removeQuestionItem(' + idx + ')" style="background:transparent; border:none; color:var(--danger); cursor:pointer; font-weight:700;">حذف ✕</button>' +
                '</div>' +
                '<div class="form-group">' +
                    '<label>نص السؤال:</label>' +
                    '<input type="text" class="form-input q-text" value="' + qText.replace(/"/g, '&quot;') + '" placeholder="اكتب نص السؤال هنا...">' +
                '</div>' +
                '<div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">' +
                    '<div class="form-group"><label>الخيار أ (A):</label><input type="text" class="form-input q-optA" value="' + opA.replace(/"/g, '&quot;') + '"></div>' +
                    '<div class="form-group"><label>الخيار ب (B):</label><input type="text" class="form-input q-optB" value="' + opB.replace(/"/g, '&quot;') + '"></div>' +
                    '<div class="form-group"><label>الخيار ج (C):</label><input type="text" class="form-input q-optC" value="' + opC.replace(/"/g, '&quot;') + '"></div>' +
                    '<div class="form-group"><label>الخيار د (D):</label><input type="text" class="form-input q-optD" value="' + opD.replace(/"/g, '&quot;') + '"></div>' +
                '</div>' +
                '<div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">' +
                    '<div class="form-group">' +
                        '<label>الإجابة الصحيحة:</label>' +
                        '<select class="form-input q-correct">' +
                            '<option value="A"' + (correct === 'A' ? ' selected' : '') + '>الخيار أ (A)</option>' +
                            '<option value="B"' + (correct === 'B' ? ' selected' : '') + '>الخيار ب (B)</option>' +
                            '<option value="C"' + (correct === 'C' ? ' selected' : '') + '>الخيار ج (C)</option>' +
                            '<option value="D"' + (correct === 'D' ? ' selected' : '') + '>الخيار د (D)</option>' +
                        '</select>' +
                    '</div>' +
                    '<div class="form-group">' +
                        '<label>الدرجة المستحقة:</label>' +
                        '<input type="number" class="form-input q-pts" value="' + pts + '" min="1">' +
                    '</div>' +
                '</div>';
            cont.appendChild(div);
        }

        function removeQuestionItem(idx) {
            const el = document.getElementById('qBox_' + idx);
            if (el) el.remove();
        }

        async function submitQuizForm() {
            const editingId = document.getElementById('editingQuizId').value;
            const title = document.getElementById('newQuizTitle').value.trim();
            const desc = document.getElementById('newQuizDesc').value.trim();
            const duration = parseInt(document.getElementById('newQuizDuration').value) || 10;
            const type = document.getElementById('newQuizType').value;
            const targetGrade = document.getElementById('newQuizTargetGrade').value;
            const targetSection = document.getElementById('newQuizTargetSection').value;

            if (!title) return showToast('عنوان الاختبار إجباري', true);

            const qBoxes = document.querySelectorAll('#newQuestionsContainer > div');
            if (qBoxes.length === 0) return showToast('أضف سؤالاً واحداً على الأقل', true);

            const questions = [];
            for (const b of qBoxes) {
                const text = b.querySelector('.q-text').value.trim();
                const a = b.querySelector('.q-optA').value.trim();
                const opb = b.querySelector('.q-optB').value.trim();
                const c = b.querySelector('.q-optC').value.trim();
                const d = b.querySelector('.q-optD').value.trim();
                const cor = b.querySelector('.q-correct').value;
                const pts = parseInt(b.querySelector('.q-pts').value) || 1;

                if (!text) return showToast('أكمل نص جميع الأسئلة', true);
                if (!a || !opb) return showToast('يجب توفير الخيار أ وب على الأقل لكل سؤال', true);

                questions.push({
                    questionText: text,
                    optionA: a, optionB: opb, optionC: c, optionD: d,
                    correctAnswer: cor,
                    points: pts
                });
            }

            const url = editingId ? '/api/teacher/update-quiz' : '/api/teacher/create-quiz';
            const payload = {
                quizId: editingId ? parseInt(editingId) : undefined,
                title, description: desc, durationMinutes: duration, type,
                targetGrade, targetSection, questions
            };

            try {
                const res = await fetch(url, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                const resData = await res.json();
                if (resData.success) {
                    closeModal('quizModal');
                    showToast(editingId ? 'تم تعديل وحفظ الاختبار بنجاح!' : 'تم نشر الاختبار للطلاب بنجاح!');
                    fetchData();
                } else {
                    showToast(resData.message || 'فشلت العملية', true);
                }
            } catch(e) {
                showToast('خطأ أثناء حفظ الاختبار', true);
            }
        }

        // ==================== QUIZ DETAILS & SUBMISSIONS VIEW ====================
        async function openQuizDetailsModal(qid) {
            try {
                const res = await fetch('/api/teacher/quiz-submissions?id=' + qid);
                const d = await res.json();
                activeQuizDetails = d;

                document.getElementById('qdModalTitle').textContent = 'نتائج: ' + d.quiz.title;
                const tg = d.quiz.targetGrade || 'الكل';
                const ts = d.quiz.targetSection || 'الكل';
                document.getElementById('qdModalSub').textContent = 'المرحلة: ' + ((tg === 'الكل' && ts === 'الكل') ? 'جميع الصفوف والشعب' : (tg + ' - ' + ts)) + ' • المدة: ' + d.quiz.durationMinutes + ' دقيقة • ' + (d.questions || []).length + ' أسئلة';

                const subs = d.submissions || [];
                document.getElementById('qdStatSubCount').textContent = subs.length;

                if (subs.length > 0) {
                    const totalPoints = subs[0].totalPoints || 1;
                    const scores = subs.map(s => s.score);
                    const avg = scores.reduce((a, b) => a + b, 0) / subs.length;
                    const maxScore = Math.max(...scores);
                    const minScore = Math.min(...scores);
                    const avgPct = Math.round((avg * 100) / totalPoints);

                    document.getElementById('qdStatAverage').textContent = avgPct + '%';
                    document.getElementById('qdStatMax').textContent = maxScore + ' / ' + totalPoints;
                    document.getElementById('qdStatMin').textContent = minScore + ' / ' + totalPoints;
                } else {
                    document.getElementById('qdStatAverage').textContent = '0%';
                    document.getElementById('qdStatMax').textContent = '0';
                    document.getElementById('qdStatMin').textContent = '0';
                }

                // Render Submissions Table
                const tbody = document.getElementById('qdTableBody');
                const empty = document.getElementById('qdEmptyState');
                document.getElementById('qdAnswersBox').style.display = 'none';

                if (subs.length === 0) {
                    tbody.innerHTML = '';
                    empty.style.display = 'block';
                } else {
                    empty.style.display = 'none';
                    let h = '';
                    subs.forEach((s, idx) => {
                        const pct = s.totalPoints > 0 ? Math.round((s.score * 100) / s.totalPoints) : 100;
                        const timeStr = new Date(s.submittedAt).toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' });
                        const classText = s.gradeSection || ((s.grade || '') + ' - ' + (s.section || '')) || 'عام';

                        h += '<tr>' +
                            '<td style="font-weight:700;">' + s.studentUsername + '</td>' +
                            '<td><span class="badge" style="background:var(--primary-light); color:var(--primary);">' + classText + '</span></td>' +
                            '<td style="font-weight:800; color:var(--primary);">' + s.score + ' / ' + s.totalPoints + '</td>' +
                            '<td>' + pct + '%</td>' +
                            '<td>' + timeStr + '</td>' +
                            '<td><button onclick="viewStudentAnswersDetail(' + idx + ')" class="btn btn-outline" style="padding:4px 8px; font-size:0.75rem;">عرض الإجابات 🔍</button></td>' +
                        '</tr>';
                    });
                    tbody.innerHTML = h;
                }

                document.getElementById('quizDetailsModal').style.display = 'flex';
            } catch(e) {
                showToast('خطأ أثناء جلب نتائج الاختبار', true);
            }
        }

        function viewStudentAnswersDetail(subIdx) {
            if (!activeQuizDetails) return;
            const sub = activeQuizDetails.submissions[subIdx];
            const questions = activeQuizDetails.questions || [];
            const stAnswers = sub.answers || {};

            document.getElementById('qdAnswersStudentTitle').textContent = 'إجابات الطالب: ' + sub.studentUsername + ' (' + sub.score + ' / ' + sub.totalPoints + ')';

            let h = '';
            questions.forEach((q, qidx) => {
                const studentChoice = (stAnswers[String(q.id)] || stAnswers[q.id] || '').toUpperCase();
                const isCorrect = (studentChoice === (q.correctAnswer || '').toUpperCase());

                const optsMap = {
                    'A': q.optionA,
                    'B': q.optionB,
                    'C': q.optionC,
                    'D': q.optionD
                };

                h += '<div style="background:var(--surface-color); border:1px solid var(--border); border-radius:10px; padding:12px;">' +
                    '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">' +
                        '<span style="font-weight:700; font-size:0.9rem;">السؤال ' + (qidx + 1) + ': ' + q.questionText + '</span>' +
                        '<span class="badge" style="background:' + (isCorrect ? 'var(--success-light)' : 'var(--danger-light)') + '; color:' + (isCorrect ? 'var(--success)' : 'var(--danger)') + ';">' + (isCorrect ? 'إجابة صحيحة ✓' : 'إجابة خاطئة ✕') + '</span>' +
                    '</div>' +
                    '<div style="font-size:0.85rem; margin-top:4px;">' +
                        '<div>إجابة الطالب: <strong>(' + (studentChoice || 'لم يجب') + ') ' + (optsMap[studentChoice] || '') + '</strong></div>' +
                        (!isCorrect ? ('<div style="color:var(--success); margin-top:2px;">الإجابة النموذجية: <strong>(' + q.correctAnswer + ') ' + (optsMap[q.correctAnswer] || '') + '</strong></div>') : '') +
                    '</div>' +
                '</div>';
            });

            document.getElementById('qdAnswersList').innerHTML = h;
            document.getElementById('qdAnswersBox').style.display = 'block';
        }

        // ==================== STUDENTS & CLASS GROUPING ====================
        function renderStudents() {
            const cont = document.getElementById('studentsListContainer');
            const chipsCont = document.getElementById('classFilterChips');
            let students = serverData.students || [];

            // Group Chips
            const classes = [...new Set(students.map(s => s.gradeSection || ((s.grade || '') + ' - ' + (s.section || '')) || 'عام'))].filter(Boolean);
            let chipsHtml = '<span class="chip ' + (selectedClassFilter === 'ALL' ? 'active' : '') + '" onclick="filterByClass(\'ALL\')">الكل (' + students.length + ')</span>';
            classes.forEach(c => {
                const count = students.filter(s => (s.gradeSection || ((s.grade || '') + ' - ' + (s.section || '')) || 'عام') === c).length;
                chipsHtml += '<span class="chip ' + (selectedClassFilter === c ? 'active' : '') + '" onclick="filterByClass(\'' + c + '\')">' + c + ' (' + count + ')</span>';
            });
            chipsCont.innerHTML = chipsHtml;

            // Search query filter
            const query = (document.getElementById('studentSearchInput').value || '').trim().toLowerCase();
            if (query) {
                students = students.filter(s =>
                    (s.username || '').toLowerCase().includes(query) ||
                    (s.nationalId || '').includes(query) ||
                    (s.gradeSection || '').toLowerCase().includes(query) ||
                    (s.grade || '').toLowerCase().includes(query) ||
                    (s.section || '').toLowerCase().includes(query)
                );
            }
            if (selectedClassFilter !== 'ALL') {
                students = students.filter(s => (s.gradeSection || ((s.grade || '') + ' - ' + (s.section || '')) || 'عام') === selectedClassFilter);
            }

            if (students.length === 0) {
                cont.innerHTML = '<div style="text-align:center; padding:30px; color:var(--text-muted);"><div style="font-size:2rem; margin-bottom:8px;">👥</div>لا توجد نتائج مطابقة للطلاب المسجلين.</div>';
                return;
            }

            // Group by class
            const groups = {};
            students.forEach(s => {
                const k = s.gradeSection || ((s.grade || '') + ' - ' + (s.section || '')) || 'فصل عام';
                if (!groups[k]) groups[k] = [];
                groups[k].push(s);
            });

            let h = '';
            for (const [classTitle, stList] of Object.entries(groups)) {
                const avg = stList.reduce((acc, x) => acc + (x.totalScore || 0), 0) / stList.length;
                h += '<div class="card-inner" style="background:var(--card-color); margin-bottom:14px;">' +
                    '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">' +
                        '<div style="font-weight:700; color:var(--primary); font-size:1.02rem;">🏫 ' + classTitle + ' (' + stList.length + ' طالب)</div>' +
                        '<span class="badge" style="background:var(--primary-light); color:var(--primary);">معدل الفصل: ' + avg.toFixed(1) + '</span>' +
                    '</div>' +
                    '<div style="overflow-x:auto;">' +
                        '<table>' +
                            '<thead>' +
                                '<tr><th>اسم الطالب</th><th>الهوية</th><th>شهري 1</th><th>شهري 2</th><th>مشاركة</th><th>إضافي</th><th>المجموع</th><th>الظهور</th><th>إجراءات</th></tr>' +
                            '</thead>' +
                            '<tbody>';

                stList.forEach(s => {
                    const total = (s.exam1Score || 0) + (s.exam2Score || 0) + (s.participationScore || 0) + (s.bonusScore || 0);
                    h += '<tr>' +
                        '<td style="font-weight:700;">' + s.username + '</td>' +
                        '<td>' + (s.nationalId || '-') + '</td>' +
                        '<td>' + s.exam1Score + '</td>' +
                        '<td>' + s.exam2Score + '</td>' +
                        '<td>' + s.participationScore + '</td>' +
                        '<td>' + (s.bonusScore > 0 ? '+' : '') + s.bonusScore + '</td>' +
                        '<td style="font-weight:800; color:var(--primary);">' + total.toFixed(1) + '</td>' +
                        '<td>' + (s.showGradesToStudent ? '👁️' : '🔒') + '</td>' +
                        '<td>' +
                            '<button onclick="quickBonus(' + s.id + ', 1)" class="btn btn-outline" style="padding:3px 7px; font-size:0.75rem;">+1</button> ' +
                            '<button onclick="quickBonus(' + s.id + ', -1)" class="btn btn-outline" style="padding:3px 7px; font-size:0.75rem; color:var(--danger);">-1</button> ' +
                            '<button onclick="openEvalModal(' + s.id + ')" class="btn" style="padding:4px 8px; font-size:0.75rem;">رصد 📝</button>' +
                        '</td>' +
                    '</tr>';
                });

                h += '</tbody></table></div></div>';
            }
            cont.innerHTML = h;
        }

        function filterStudents() { renderStudents(); }
        function filterByClass(cls) { selectedClassFilter = cls; renderStudents(); }

        async function quickBonus(id, delta) {
            await fetch('/api/teacher/bonus', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ studentId: id, delta })
            });
            fetchData();
        }

        function openEvalModal(id) {
            const s = (serverData.students || []).find(x => x.id === id);
            if (!s) return;
            document.getElementById('evalStudentId').value = s.id;
            document.getElementById('evalModalTitle').textContent = 'رصد درجات: ' + s.username;
            document.getElementById('evalGrade').value = s.grade || 'أول ثانوي';
            document.getElementById('evalSection').value = s.section || 'شعبة 1';
            document.getElementById('evalExam1').value = s.exam1Score || 0;
            document.getElementById('evalExam2').value = s.exam2Score || 0;
            document.getElementById('evalPart').value = s.participationScore || 0;
            document.getElementById('evalBonus').value = s.bonusScore || 0;
            document.getElementById('evalNotes').value = s.notes || '';
            document.getElementById('evalShowGrades').checked = (s.showGradesToStudent !== 0);
            document.getElementById('evalShowNotes').checked = (s.showNotesToStudent !== 0);
            document.getElementById('evalModal').style.display = 'flex';
        }

        async function saveStudentEvaluation() {
            const sid = document.getElementById('evalStudentId').value;
            const gr = document.getElementById('evalGrade').value;
            const sec = document.getElementById('evalSection').value;
            const grSec = gr + ' - ' + sec;

            const payload = {
                studentId: parseInt(sid),
                grade: gr,
                section: sec,
                gradeSection: grSec,
                exam1: parseFloat(document.getElementById('evalExam1').value) || 0,
                exam2: parseFloat(document.getElementById('evalExam2').value) || 0,
                participation: parseFloat(document.getElementById('evalPart').value) || 0,
                bonus: parseFloat(document.getElementById('evalBonus').value) || 0,
                notes: document.getElementById('evalNotes').value.trim(),
                showGrades: document.getElementById('evalShowGrades').checked,
                showNotes: document.getElementById('evalShowNotes').checked
            };

            await fetch('/api/teacher/evaluate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            closeModal('evalModal');
            showToast('تم حفظ ورصد درجات الطالب بنجاح');
            fetchData();
        }

        async function toggleGlobalVisibility() {
            const curr = serverData.areGradesVisibleGlobally !== false;
            await fetch('/api/teacher/toggle-visibility', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ visible: !curr })
            });
            fetchData();
            showToast(curr ? 'تم إخفاء الدرجات عن جميع الطلاب' : 'تم إعلان الدرجات للجميع');
        }

        // ==================== SUBMISSIONS ====================
        function filterSubmissions(type) {
            currentSubFilter = type;
            ['All', 'Quiz', 'Act'].forEach(k => {
                document.getElementById('subFilter' + k).classList.toggle('active', (k === 'All' && type === 'ALL') || (k === 'Quiz' && type === 'QUIZ') || (k === 'Act' && type === 'ACTIVITY'));
            });
            renderSubmissions();
        }

        function renderSubmissions() {
            const tbody = document.getElementById('submissionsTableBody');
            const empty = document.getElementById('submissionsEmptyState');
            let subs = serverData.submissions || [];

            if (currentSubFilter !== 'ALL') {
                subs = subs.filter(s => (s.quizType || 'QUIZ') === currentSubFilter);
            }

            if (subs.length === 0) {
                tbody.innerHTML = '';
                empty.style.display = 'block';
                return;
            }
            empty.style.display = 'none';

            let h = '';
            subs.forEach((s, idx) => {
                const dateStr = new Date(s.submittedAt).toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' });
                const pct = s.totalPoints > 0 ? Math.round((s.score * 100) / s.totalPoints) : 100;
                const tg = s.targetGrade || 'الكل';
                const ts = s.targetSection || 'الكل';
                const targetText = (tg === 'الكل' && ts === 'الكل') ? 'عام' : (tg + ' - ' + ts);

                h += '<tr>' +
                    '<td>' + (idx + 1) + '</td>' +
                    '<td style="font-weight:700;">' + s.studentUsername + '</td>' +
                    '<td><span class="badge" style="background:var(--primary-light); color:var(--primary);">' + targetText + '</span></td>' +
                    '<td>' + (s.quizTitle || 'اختبار') + '</td>' +
                    '<td><span class="badge" style="background:rgba(255,255,255,0.08); color:var(--text-muted);">' + (s.quizType === 'ACTIVITY' ? 'نشاط' : 'اختبار') + '</span></td>' +
                    '<td style="font-weight:800; color:var(--primary);">' + s.score + ' / ' + s.totalPoints + '</td>' +
                    '<td>' + pct + '%</td>' +
                    '<td>' + dateStr + '</td>' +
                '</tr>';
            });
            tbody.innerHTML = h;
        }

        // ==================== LIVE ACTIVITY LOGS ====================
        function renderLogs() {
            const cont = document.getElementById('liveLogsContainer');
            const logs = serverData.logs || [];
            if (logs.length === 0) {
                cont.innerHTML = '<div style="text-align:center; padding:20px; color:var(--text-muted);">لا توجد أحداث مسجلة بعد.</div>';
                return;
            }
            let h = '';
            logs.forEach(l => {
                const icon = l.type === 'CHEAT_ALERT' ? '⚠️' : (l.type === 'STUDENT_JOIN' ? '👤' : (l.type === 'SUBMIT' ? '📝' : '🟢'));
                const color = l.type === 'CHEAT_ALERT' ? 'var(--danger)' : 'var(--text-main)';
                h += '<div style="background:var(--card-color); border:1px solid var(--border); border-radius:10px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center;">' +
                    '<div style="display:flex; align-items:center; gap:8px;">' +
                        '<span>' + icon + '</span>' +
                        '<span style="color:' + color + '; font-size:0.9rem; font-weight:600;">' + l.message + '</span>' +
                    '</div>' +
                    '<span style="font-size:0.75rem; color:var(--text-muted);">' + l.time + '</span>' +
                '</div>';
            });
            cont.innerHTML = h;
        }

        async function clearLogs() {
            await fetch('/api/teacher/clear-logs', { method: 'POST' });
            fetchData();
        }

        // ==================== ENCRYPTED SYNC (AES-256) ====================
        function openExportModal() {
            document.getElementById('exportResultArea').style.display = 'none';
            document.getElementById('btnRunExport').style.display = 'inline-block';
            document.getElementById('exportPassword').value = '';
            document.getElementById('exportModal').style.display = 'flex';
        }

        async function executeEncryptedExport() {
            const pass = document.getElementById('exportPassword').value;
            try {
                const res = await fetch('/api/teacher/export-data', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ password: pass })
                });
                const d = await res.json();
                if (d.success) {
                    document.getElementById('exportedCipherCode').value = d.encryptedCode;
                    document.getElementById('exportResultArea').style.display = 'block';
                    document.getElementById('btnRunExport').style.display = 'none';
                    showToast('تم تشفير بيانات ' + d.studentCount + ' طالب بنجاح!');
                }
            } catch(e) { showToast('فشل التصدير المشفر', true); }
        }

        function copyExportedCode() {
            const el = document.getElementById('exportedCipherCode');
            el.select();
            document.execCommand('copy');
            showToast('تم نسخ الكود المشفر للحافظة 📋');
        }

        function downloadExportedFile() {
            const code = document.getElementById('exportedCipherCode').value;
            const blob = new Blob([code], { type: 'text/plain;charset=utf-8' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = 'students_backup_' + new Date().toISOString().slice(0,10) + '.enc';
            a.click();
        }

        function openImportModal() {
            document.getElementById('importCodeInput').value = '';
            document.getElementById('importPassword').value = '';
            document.getElementById('importFileInput').value = '';
            document.getElementById('importModal').style.display = 'flex';
        }

        function handleFileSelected(e) {
            const file = e.target.files[0];
            if (!file) return;
            const r = new FileReader();
            r.onload = ev => {
                document.getElementById('importCodeInput').value = ev.target.result;
            };
            r.readAsText(file);
        }

        async function executeEncryptedImport() {
            const code = document.getElementById('importCodeInput').value.trim();
            const pass = document.getElementById('importPassword').value;
            const overwrite = document.getElementById('importOverwriteCheck').checked;
            if (!code) return showToast('يرجى اختيار ملف أو لصق كود مشفر', true);

            try {
                const res = await fetch('/api/teacher/import-data', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ encryptedCode: code, password: pass, overwrite: overwrite })
                });
                const d = await res.json();
                if (d.success) {
                    closeModal('importModal');
                    fetchData();
                    showToast('تم فك التشفير واستيراد ' + (d.added + d.updated) + ' طالب بنجاح!');
                } else {
                    showToast(d.message || 'فشل فك التشفير', true);
                }
            } catch(e) {
                showToast('خطأ أثناء فك التشفير', true);
            }
        }

        // ==================== SETTINGS & THEMES ====================
        async function saveTeacherSettings() {
            const name = document.getElementById('settingTeacherName').value.trim();
            const subject = document.getElementById('settingTeacherSubject').value.trim();
            const phone = document.getElementById('settingTeacherPhone').value.trim();
            const newPwd = document.getElementById('settingTeacherPassword').value.trim();
            const antiCheat = document.getElementById('antiCheatToggle').checked ? '1' : '0';
            const preventRetake = document.getElementById('preventRetakeToggle').checked ? '1' : '0';

            const payload = {
                teacher_name: name,
                teacher_subject: subject,
                teacher_phone: phone,
                anti_cheat: antiCheat,
                prevent_retake: preventRetake
            };
            if (newPwd) payload.teacher_password = newPwd;

            try {
                await fetch('/api/teacher/settings', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                showToast('تم حفظ الإعدادات بنجاح');
                fetchData();
            } catch(e) {
                showToast('خطأ أثناء حفظ الإعدادات', true);
            }
        }

        function initTheme() {
            const savedTheme = localStorage.getItem('theme_mode') || 'dark';
            if (savedTheme === 'light') {
                document.body.classList.add('light-mode');
                document.getElementById('darkModeToggle').checked = false;
            }
            const savedColor = localStorage.getItem('theme_color') || '#3a86ff';
            setThemeColor(savedColor, false);
        }

        function toggleDarkMode() {
            const isDark = document.getElementById('darkModeToggle').checked;
            document.body.classList.toggle('light-mode', !isDark);
            localStorage.setItem('theme_mode', isDark ? 'dark' : 'light');
        }

        function setThemeColor(color, save = true) {
            document.documentElement.style.setProperty('--primary', color);
            document.documentElement.style.setProperty('--primary-light', color + '26');
            if (save) localStorage.setItem('theme_color', color);

            document.querySelectorAll('.color-dot').forEach(d => {
                d.classList.toggle('active', d.style.background === color || d.getAttribute('style').includes(color));
            });
        }

        // ==================== SERVER CONTROL & QR ====================
        async function toggleServerStatus() {
            const isChecked = document.getElementById('serverToggleInput').checked;
            await fetch('/api/status', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ isOpen: isChecked })
            });
            fetchData();
        }

        function copyServerUrl() {
            const url = document.getElementById('primaryUrlText').textContent;
            navigator.clipboard.writeText(url).then(() => {
                showToast('تم نسخ الرابط للحافظة 📋');
            });
        }

        function showQrModal() {
            const url = document.getElementById('primaryUrlText').textContent;
            document.getElementById('qrModalUrl').textContent = url;
            drawSimpleQr(url);
            document.getElementById('qrModal').style.display = 'flex';
        }

        function showGuideModal() {
            document.getElementById('guideModal').style.display = 'flex';
        }

        function drawSimpleQr(text) {
            const canvas = document.getElementById('qrCanvas');
            const ctx = canvas.getContext('2d');
            const size = canvas.width;
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, size, size);

            // Clean, stylized visual QR pattern representation
            ctx.fillStyle = '#0b132b';
            const s = 14;
            // Top-Right finder
            ctx.fillRect(s*2, s*2, s*4, s*4);
            ctx.clearRect(s*2.5, s*2.5, s*3, s*3);
            ctx.fillRect(s*3, s*3, s*2, s*2);

            // Top-Left finder
            ctx.fillRect(size - s*6, s*2, s*4, s*4);
            ctx.clearRect(size - s*5.5, s*2.5, s*3, s*3);
            ctx.fillRect(size - s*5, s*3, s*2, s*2);

            // Bottom-Right finder
            ctx.fillRect(s*2, size - s*6, s*4, s*4);
            ctx.clearRect(s*2.5, size - s*5.5, s*3, s*3);
            ctx.fillRect(s*3, size - s*5, s*2, s*2);

            // Data matrix pattern based on string hash
            let h = 0;
            for (let i = 0; i < text.length; i++) h = (h * 31 + text.charCodeAt(i)) & 0xffffffff;
            for (let x = 6; x < size / s - 6; x++) {
                for (let y = 2; y < size / s - 2; y++) {
                    if ((x + y + h) % 3 === 0 || (x * y + h) % 5 === 0) {
                        ctx.fillRect(x * s, y * s, s - 2, s - 2);
                    }
                }
            }
        }
    </script>
</body>
</html>
"""
