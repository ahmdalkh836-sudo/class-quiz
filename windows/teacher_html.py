# -*- coding: utf-8 -*-
r"""
Teacher Web Console HTML Template for Windows 11 Desktop Edition
Includes Sidebar Drawer, Settings, Palette Theme, Anti-Cheat, and Encrypted Sync
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
        }

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
            width: 310px;
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
            background: linear-gradient(135deg, rgba(58,134,255,0.15) 0%, rgba(131,56,236,0.15) 100%);
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
            padding: 10px 14px 4px 14px;
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
            max-width: 1100px;
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
            font-size: 1.12rem;
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
            padding: 6px 12px;
            z-index: 100;
        }

        .nav-item {
            background: transparent;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 3px;
            padding: 5px 12px;
            border-radius: 10px;
            font-size: 0.75rem;
            font-weight: 700;
        }

        .nav-item.active {
            color: var(--primary);
            background: var(--primary-light);
        }

        .card-inner {
            background: var(--surface-color);
            border: 1.5px solid var(--border);
            border-radius: var(--radius);
            padding: 18px;
            margin-bottom: 16px;
        }

        /* Tables & Lists */
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 11px 13px; text-align: right; border-bottom: 1px solid var(--border); font-size: 0.9rem; }
        th { background: rgba(0, 0, 0, 0.2); color: var(--text-muted); font-weight: 700; }
        tr:hover { background: var(--primary-light); }

        /* Chips */
        .chip {
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            border: 1px solid var(--border);
            cursor: pointer;
            background: var(--card-color);
            color: var(--text-muted);
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .chip.active {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }

        /* Palette Swatches */
        .color-circle {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            cursor: pointer;
            border: 2px solid transparent;
            transition: transform 0.15s;
        }

        .color-circle.active {
            border-color: white;
            transform: scale(1.15);
            box-shadow: 0 0 10px rgba(255,255,255,0.4);
        }

        /* Modal Styles */
        .modal {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(11, 19, 43, 0.75);
            backdrop-filter: blur(5px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            padding: 16px;
        }

        .modal-body {
            background: var(--surface-color);
            border: 1.5px solid var(--border);
            border-radius: 20px;
            max-width: 600px;
            width: 100%;
            padding: 22px;
            max-height: 90vh;
            overflow-y: auto;
        }

        .form-group { margin-bottom: 12px; }
        .form-group label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 5px; color: var(--text-muted); }
        .form-input {
            width: 100%;
            padding: 10px 12px;
            border: 1.5px solid var(--border);
            border-radius: 10px;
            background: var(--card-color);
            color: var(--text-main);
            font-size: 0.95rem;
        }

        .badge { padding: 4px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; }
        .toast {
            position: fixed;
            bottom: 80px; left: 50%; transform: translateX(-50%);
            background: #1e293b; color: white; padding: 12px 24px; border-radius: 12px;
            display: none; z-index: 9999; box-shadow: 0 10px 25px rgba(0,0,0,0.5); font-size: 0.92rem;
        }
    </style>
</head>
<body>
    <!-- Top Header -->
    <header>
        <div class="header-title-box">
            <button onclick="toggleDrawer(true)" class="menu-btn" title="القائمة الجانبية">☰</button>
            <div>
                <h1 style="font-size: 1.15rem; font-weight: 700;" id="appHeaderTeacherName">خادم الفصل • Windows 11</h1>
                <div style="font-size: 0.75rem; color: var(--text-muted); display:flex; align-items:center; gap:5px;">
                    <span id="headerStatusDot" class="status-dot active"></span>
                    <span id="headerStatusText">نشط: شبكة Wi-Fi المشتركة</span>
                </div>
            </div>
        </div>

        <div style="display: flex; gap: 8px; align-items: center;">
            <button onclick="showQrModal()" class="btn btn-outline" style="padding:6px 12px; font-size:0.82rem;" title="عرض رمز QR">📱 QR</button>
            <button onclick="toggleDarkMode()" class="btn btn-outline" style="padding:6px 10px;" id="themeToggleIcon" title="تبديل المظهر">🌙</button>
            <button onclick="showGuideModal()" class="btn btn-outline" style="padding:6px 10px;" title="دليل الاستخدام">❓</button>
        </div>
    </header>

    <!-- Sidebar Drawer (Matching Android App) -->
    <div id="drawerOverlay" class="drawer-overlay" onclick="toggleDrawer(false)"></div>
    <div id="sidebarDrawer" class="drawer">
        <div class="drawer-header">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="width: 44px; height: 44px; border-radius: 12px; background: var(--primary-light); border: 1.5px solid var(--primary); display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">
                    🎓
                </div>
                <button onclick="toggleDrawer(false)" style="background:transparent; border:none; color:var(--text-muted); font-size:1.4rem; cursor:pointer;">✕</button>
            </div>
            <div style="margin-top: 10px;">
                <h3 id="drawerTeacherName" style="font-size: 1.08rem; font-weight:700;">الأستاذ / المعلم</h3>
                <div id="drawerTeacherSubject" style="font-size: 0.8rem; color: var(--text-muted);">خادم الاختبارات المدرسية المباشر</div>
            </div>
        </div>

        <div class="drawer-content">
            <div class="drawer-category">إدارة الفصل والدرجات</div>
            <div class="drawer-item" onclick="switchMainTab('quizzes')">
                <span>📝 الاختبارات والأنشطة</span>
                <span class="badge" style="background:var(--primary-light); color:var(--primary);" id="badgeQuizzesCount">0</span>
            </div>
            <div class="drawer-item" onclick="switchMainTab('students')">
                <span>👥 الطلاب والدرجات الشهرية</span>
                <span class="badge" style="background:var(--primary-light); color:var(--primary);" id="badgeStudentsCount">0</span>
            </div>
            <div class="drawer-item" onclick="switchMainTab('submissions')">
                <span>📊 النتائج والتسليمات</span>
                <span class="badge" style="background:var(--primary-light); color:var(--primary);" id="badgeSubmissionsCount">0</span>
            </div>

            <div class="drawer-category" style="margin-top: 8px;">الشبكة والبث المباشر</div>
            <div class="drawer-item" onclick="switchMainTab('logs')">
                <span>📡 سجل العمليات والبث</span>
            </div>
            <div class="drawer-item" onclick="showGuideModal()">
                <span>❓ دليل شبكة Wi-Fi والهوتسبوت</span>
            </div>

            <div class="drawer-category" style="margin-top: 8px;">النظام والتخصيص</div>
            <div class="drawer-item" onclick="switchMainTab('settings')">
                <span>⚙️ الإعدادات والملف الشخصي</span>
            </div>
        </div>

        <div style="padding: 14px 18px; border-top: 1px solid var(--border); font-size: 0.8rem; display:flex; justify-content:space-between; color:var(--text-muted);">
            <span id="drawerStatusText">🟢 البث يعمل</span>
            <span id="drawerIpText">Port: 8080</span>
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

        <!-- ==================== TAB 1: Quizzes ==================== -->
        <div id="tabQuizzes" class="card-inner">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <div>
                    <h2 style="font-size: 1.15rem;">📝 بنك الاختبارات والأنشطة</h2>
                    <p style="font-size: 0.85rem; color: var(--text-muted);">الاختبارات المفعلة والمتاحة للطلاب في الفصل</p>
                </div>
                <button onclick="openNewQuizModal()" class="btn btn-success">+ إضافة اختبار جديد</button>
            </div>
            <div id="quizzesListContainer" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px;"></div>
        </div>

        <!-- ==================== TAB 2: Students & Encrypted Sync ==================== -->
        <div id="tabStudents" class="card-inner" style="display: none;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;">
                <div>
                    <h2 style="font-size: 1.15rem;">👥 سجل الطلاب والدرجات الشهرية</h2>
                    <p style="font-size: 0.85rem; color: var(--text-muted);">مقسّمة بحسب الفصول والشعب مع رصد درجات الاختبارات والمشاركة</p>
                </div>

                <!-- Encrypted Sync Buttons (Required Feature 3) -->
                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                    <button onclick="openExportModal()" class="btn" style="background:var(--primary); font-size:0.85rem;">🔒 سحب مشفر</button>
                    <button onclick="openImportModal()" class="btn btn-outline" style="font-size:0.85rem;">📥 استيراد</button>
                    <button id="globalGradesBtn" onclick="toggleGlobalVisibility()" class="btn btn-outline" style="font-size:0.85rem;">👁️ الدرجات: معلنة</button>
                </div>
            </div>

            <!-- Search and Filter Chips -->
            <div style="margin-bottom: 14px;">
                <input type="text" id="studentSearchInput" onkeyup="filterStudents()" placeholder="ابحث باسم الطالب، الهوية، أو الفصل..." class="form-input" style="margin-bottom: 10px;">
                <div id="classFilterChips" style="display: flex; gap: 8px; overflow-x: auto; padding-bottom: 4px;"></div>
            </div>

            <div id="studentsListContainer"></div>
        </div>

        <!-- ==================== TAB 3: Results & Submissions ==================== -->
        <div id="tabSubmissions" class="card-inner" style="display: none;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div>
                    <h2 style="font-size: 1.15rem;">📊 النتائج والتسليمات</h2>
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

        <!-- ==================== TAB 5: Settings & Profile (Required Feature 2) ==================== -->
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
                        <input type="text" id="settingTeacherSubject" class="form-input" placeholder="مثال: الرياضيات / الفيزياء">
                    </div>
                    <div class="form-group">
                        <label>رقم هاتف التواصل:</label>
                        <input type="text" id="settingTeacherPhone" class="form-input" placeholder="اختياري">
                    </div>
                </div>
                <button onclick="saveTeacherProfile()" class="btn btn-success" style="margin-top: 6px;">حفظ الملف الشخصي ✓</button>
            </div>

            <!-- Appearance & Palette Selection -->
            <div class="card-inner" style="background:var(--card-color); margin-bottom:16px;">
                <h3 style="font-size: 1.05rem; margin-bottom: 8px;">🎨 المظهر والألوان</h3>
                <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 14px;">اختر اللون الأساسي المفضل لواجهة البرنامج والوضع الليلي:</p>

                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <span>الوضع الليلي الداكن (Dark Mode)</span>
                    <label class="switch">
                        <input type="checkbox" id="darkModeToggle" checked onchange="toggleDarkMode()">
                        <span class="slider"></span>
                    </label>
                </div>

                <div style="font-size: 0.88rem; font-weight: 600; margin-bottom: 8px;">الألوان الأساسية:</div>
                <div style="display: flex; gap: 12px; align-items: center;">
                    <div class="color-circle active" style="background: #3a86ff;" onclick="setThemePalette('ROYAL_BLUE')" title="الملكي (Royal Blue)"></div>
                    <div class="color-circle" style="background: #f59e0b;" onclick="setThemePalette('AMBER')" title="الكهرماني (Amber)"></div>
                    <div class="color-circle" style="background: #8b5cf6;" onclick="setThemePalette('PURPLE')" title="البنفسجي (Purple)"></div>
                    <div class="color-circle" style="background: #10b981;" onclick="setThemePalette('EMERALD')" title="الزمردي (Emerald)"></div>
                    <div class="color-circle" style="background: #ef4444;" onclick="setThemePalette('CRIMSON')" title="المرجاني (Crimson)"></div>
                </div>
            </div>

            <!-- Anti-Cheat and Security Settings -->
            <div class="card-inner" style="background:var(--card-color);">
                <h3 style="font-size: 1.05rem; margin-bottom: 8px; color: var(--danger);">🛡️ الأمان ومنع الغش</h3>
                <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 14px;">خيارات حماية الاختبارات وضمان النزاهة داخل الفصل:</p>

                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <div>
                        <div style="font-weight: 700; font-size: 0.95rem;">كشف الإنترنت الخارجي (4G / 5G)</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">حظر الإرسال وتنبيه المعلم فوراً إذا حاول الطالب تشغيل بيانات الهاتف</div>
                    </div>
                    <label class="switch">
                        <input type="checkbox" id="antiCheatToggle" checked onchange="toggleAntiCheat()">
                        <span class="slider"></span>
                    </label>
                </div>

                <hr style="border:0; border-top:1px solid var(--border); margin:12px 0;">

                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 700; font-size: 0.95rem;">منع إعادة الاختبار</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">إغلاق الاختبار نهائياً أمام الطالب بمجرد تسليم الإجابات</div>
                    </div>
                    <label class="switch">
                        <input type="checkbox" id="preventRetakeToggle" checked onchange="togglePreventRetake()">
                        <span class="slider"></span>
                    </label>
                </div>
            </div>
        </div>
    </div>

    <!-- Bottom Navigation Bar -->
    <nav class="bottom-nav">
        <button id="bNavQuizzes" class="nav-item active" onclick="switchMainTab('quizzes')">
            <span style="font-size: 1.3rem;">📝</span>
            <span>الاختبارات</span>
        </button>
        <button id="bNavStudents" class="nav-item" onclick="switchMainTab('students')">
            <span style="font-size: 1.3rem;">👥</span>
            <span>الطلاب والدرجات</span>
        </button>
        <button id="bNavSubmissions" class="nav-item" onclick="switchMainTab('submissions')">
            <span style="font-size: 1.3rem;">📊</span>
            <span>التسليمات</span>
        </button>
        <button id="bNavLogs" class="nav-item" onclick="switchMainTab('logs')">
            <span style="font-size: 1.3rem;">📡</span>
            <span>البث والسجل</span>
        </button>
        <button id="bNavSettings" class="nav-item" onclick="switchMainTab('settings')">
            <span style="font-size: 1.3rem;">⚙️</span>
            <span>الإعدادات</span>
        </button>
    </nav>

    <!-- Modal 1: Export Encrypted Data (Required Feature 3A) -->
    <div id="exportModal" class="modal">
        <div class="modal-body">
            <h3 style="color: var(--primary); font-size: 1.25rem; margin-bottom: 12px;">🔒 سحب وتصدير بيانات الطلاب مشفرة</h3>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
                سيتم تشفير بيانات الطلاب، الفصول، درجات الاختبارات الشهرية، والملاحظات بـ <strong>AES-256</strong> لحفظ سريتها عند النقل بين الأجهزة أو المدارس.
            </p>

            <div class="form-group">
                <label>كلمة مرور التشفير (Password):</label>
                <input type="password" id="exportPassword" class="form-input" placeholder="اتركها فارغة لاستخدام المفتاح القياسي المشترك">
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

    <!-- Modal 2: Import Encrypted Data (Required Feature 3B) -->
    <div id="importModal" class="modal">
        <div class="modal-body">
            <h3 style="color: var(--primary); font-size: 1.25rem; margin-bottom: 12px;">📥 استيراد بيانات الطلاب المشفرة</h3>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
                ارفع ملف النسخة الاحتياطية المشفر (.enc) أو الصق الكود المشفر مباشرة لدمج الطلاب والدرجات في قاعدة البيانات المحلية.
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
                <input type="password" id="importPassword" class="form-input" placeholder="اتركها فارغة إذا استخدمت المفتاح الافتراضي">
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

    <!-- Modal 3: Evaluation Dialog -->
    <div id="evalModal" class="modal">
        <div class="modal-body">
            <h3 id="evalModalTitle" style="color: var(--primary); font-size: 1.2rem; margin-bottom: 14px;">رصد درجات الطالب</h3>
            <input type="hidden" id="evalStudentId">

            <div class="form-group">
                <label>الفصل والشعبة:</label>
                <input type="text" id="evalGradeSection" class="form-input">
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

    <!-- Modal 4: Create Quiz -->
    <div id="quizModal" class="modal">
        <div class="modal-body" style="max-width: 650px;">
            <h3 style="color: var(--primary); font-size: 1.2rem; margin-bottom: 14px;">إنشاء اختبار / نشاط جديد</h3>
            <div class="form-group">
                <label>عنوان الاختبار *:</label>
                <input type="text" id="newQuizTitle" class="form-input" placeholder="مثال: الاختبار الفتري الأول في الرياضيات">
            </div>
            <div class="form-group">
                <label>تعليمات أو وصف:</label>
                <input type="text" id="newQuizDesc" class="form-input" placeholder="اختياري">
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

            <h4 style="margin: 12px 0 8px 0; font-size: 0.95rem;">الأسئلة (اختيار من متعدد):</h4>
            <div id="newQuestionsContainer"></div>
            <button onclick="addQuestionItem()" class="btn btn-outline" style="margin-top: 6px;">+ إضافة سؤال آخر</button>

            <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 18px;">
                <button onclick="closeModal('quizModal')" class="btn btn-outline">إلغاء</button>
                <button onclick="submitNewQuiz()" class="btn btn-success">حفظ ونشر الاختبار للطلاب ✓</button>
            </div>
        </div>
    </div>

    <!-- Modal 5: QR Code Presentation -->
    <div id="qrModal" class="modal">
        <div class="modal-body" style="max-width: 400px; text-align: center;">
            <h3 style="color: var(--primary); margin-bottom: 8px;">مسح رمز QR للدخول 📱</h3>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">وجه كاميرا هاتف الطالب نحو الشاشة للدخول فوراً</p>
            <div style="background: white; padding: 16px; border-radius: 16px; display: inline-block;">
                <canvas id="qrCanvas" width="220" height="220"></canvas>
            </div>
            <div id="qrModalUrl" style="font-size: 0.9rem; font-weight: 700; color: var(--primary); margin-top: 14px; word-break: break-all;"></div>
            <button onclick="closeModal('qrModal')" class="btn btn-outline" style="margin-top: 16px; width: 100%;">إغلاق</button>
        </div>
    </div>

    <!-- Modal 6: Wi-Fi Guide Modal -->
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
        let isDarkMode = true;
        let primaryIp = '127.0.0.1';

        window.addEventListener('DOMContentLoaded', () => {
            fetchData();
            setInterval(fetchData, 5000);
            initTheme();
        });

        function showToast(msg, isErr) {
            const t = document.getElementById('toast');
            t.textContent = msg;
            t.style.background = isErr ? '#dc2626' : '#1e293b';
            t.style.display = 'block';
            setTimeout(() => { t.style.display = 'none'; }, 3000);
        }

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

            // Hide server card in settings tab to avoid clutter
            document.getElementById('topServerCard').style.display = (tab === 'settings') ? 'none' : 'block';
        }

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

        // --- Quizzes Rendering ---
        function renderQuizzes() {
            const cont = document.getElementById('quizzesListContainer');
            const qList = serverData.quizzes || [];
            if (qList.length === 0) {
                cont.innerHTML = '<div style="grid-column:1/-1; text-align:center; padding:30px; color:var(--text-muted);">لا توجد اختبارات مضافة. انقر فوق (+ إضافة اختبار جديد) للبدء.</div>';
                return;
            }
            let h = '';
            qList.forEach(q => {
                h += '<div class="card-inner" style="background:var(--card-color);">' +
                    '<div style="display:flex; justify-content:space-between; align-items:center;">' +
                        '<h3 style="font-size:1.05rem;">' + q.title + '</h3>' +
                        '<span class="badge" style="background:' + (q.isActive ? 'var(--success-light)' : 'var(--danger-light)') + '; color:' + (q.isActive ? 'var(--success)' : 'var(--danger)') + ';">' + (q.isActive ? 'نشط ومتاح' : 'مغلق') + '</span>' +
                    '</div>' +
                    '<p style="font-size:0.85rem; color:var(--text-muted); margin:8px 0;">' + (q.description || 'بدون تعليمات') + '</p>' +
                    '<div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px;">' +
                        '<span style="font-size:0.82rem; color:var(--text-muted);">⏱️ ' + q.durationMinutes + ' دقيقة • ' + (q.questionCount || 0) + ' سؤال</span>' +
                        '<button onclick="toggleQuizActive(' + q.id + ', ' + q.isActive + ')" class="btn ' + (q.isActive ? 'btn-danger' : 'btn-success') + '" style="padding:6px 12px; font-size:0.82rem;">' + (q.isActive ? 'إغلاق 🔒' : 'تفعيل 🔓') + '</button>' +
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

        // --- Students & Class Section Grouping ---
        function renderStudents() {
            const cont = document.getElementById('studentsListContainer');
            const chipsCont = document.getElementById('classFilterChips');
            let students = serverData.students || [];

            // Class Chips
            const classes = [...new Set(students.map(s => s.gradeSection || 'عام'))].filter(Boolean);
            let chipsHtml = '<span class="chip ' + (selectedClassFilter === 'ALL' ? 'active' : '') + '" onclick="filterByClass(\'ALL\')">الكل (' + students.length + ')</span>';
            classes.forEach(c => {
                const count = students.filter(s => (s.gradeSection || 'عام') === c).length;
                chipsHtml += '<span class="chip ' + (selectedClassFilter === c ? 'active' : '') + '" onclick="filterByClass(\'' + c + '\')">' + c + ' (' + count + ')</span>';
            });
            chipsCont.innerHTML = chipsHtml;

            // Search & Class filter
            const query = (document.getElementById('studentSearchInput').value || '').trim().toLowerCase();
            if (query) {
                students = students.filter(s => (s.username || '').toLowerCase().includes(query) || (s.nationalId || '').includes(query) || (s.gradeSection || '').toLowerCase().includes(query));
            }
            if (selectedClassFilter !== 'ALL') {
                students = students.filter(s => (s.gradeSection || 'عام') === selectedClassFilter);
            }

            if (students.length === 0) {
                cont.innerHTML = '<div style="text-align:center; padding:30px; color:var(--text-muted);">لا توجد نتائج مطابقة للطلاب.</div>';
                return;
            }

            // Group by class
            const groups = {};
            students.forEach(s => {
                const k = s.gradeSection || 'فصل عام';
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

        // --- Submissions ---
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
                h += '<tr>' +
                    '<td>' + (idx + 1) + '</td>' +
                    '<td style="font-weight:700;">' + s.studentUsername + '</td>' +
                    '<td>' + (s.quizTitle || 'اختبار') + '</td>' +
                    '<td><span class="badge" style="background:var(--primary-light); color:var(--primary);">' + (s.quizType === 'ACTIVITY' ? 'نشاط' : 'اختبار') + '</span></td>' +
                    '<td style="font-weight:800; color:var(--primary);">' + s.score + ' / ' + s.totalPoints + '</td>' +
                    '<td>' + pct + '%</td>' +
                    '<td>' + dateStr + '</td>' +
                '</tr>';
            });
            tbody.innerHTML = h;
        }

        // --- Live Activity Logs ---
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

        // ==================== FEATURE 3: Encrypted Sync (AES-256) ====================
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
                    alert('🎉 تم استيراد البيانات وفك التشفير بنجاح!\n• الطلاب الجدد المضافون: ' + d.added + '\n• الطلاب المحدثون: ' + d.updated);
                } else {
                    showToast(d.message || 'فشل فك التشفير', true);
                }
            } catch(e) { showToast('تعذر الاتصال بالخادم', true); }
        }

        // ==================== Settings & Teacher Profile ====================
        async function saveTeacherProfile() {
            const name = document.getElementById('settingTeacherName').value.trim();
            const subject = document.getElementById('settingTeacherSubject').value.trim();
            const phone = document.getElementById('settingTeacherPhone').value.trim();

            await fetch('/api/teacher/settings', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ teacher_name: name, teacher_subject: subject, teacher_phone: phone })
            });
            fetchData();
            showToast('تم حفظ الملف الشخصي بنجاح ✓');
        }

        function toggleDarkMode() {
            isDarkMode = !isDarkMode;
            document.body.classList.toggle('light-mode', !isDarkMode);
            document.getElementById('darkModeToggle').checked = isDarkMode;
            document.getElementById('themeToggleIcon').textContent = isDarkMode ? '🌙' : '☀️';
            localStorage.setItem('win_dark_mode', isDarkMode ? '1' : '0');
        }

        function setThemePalette(theme) {
            const colors = {
                'ROYAL_BLUE': { primary: '#3a86ff', dark: '#2667d4' },
                'AMBER': { primary: '#f59e0b', dark: '#d97706' },
                'PURPLE': { primary: '#8b5cf6', dark: '#7c3aed' },
                'EMERALD': { primary: '#10b981', dark: '#059669' },
                'CRIMSON': { primary: '#ef4444', dark: '#dc2626' }
            };
            const pal = colors[theme] || colors['ROYAL_BLUE'];
            document.documentElement.style.setProperty('--primary', pal.primary);
            document.documentElement.style.setProperty('--primary-dark', pal.dark);
            document.documentElement.style.setProperty('--primary-light', pal.primary + '26');
            localStorage.setItem('win_theme_palette', theme);
            showToast('تم تطبيق السمة اللونية بنجاح 🎨');
        }

        function initTheme() {
            const savedDark = localStorage.getItem('win_dark_mode');
            if (savedDark === '0') toggleDarkMode();
            const savedPal = localStorage.getItem('win_theme_palette');
            if (savedPal) setThemePalette(savedPal);
        }

        async function toggleAntiCheat() {
            const chk = document.getElementById('antiCheatToggle').checked;
            await fetch('/api/teacher/settings', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ anti_cheat: chk ? '1' : '0' })
            });
            showToast(chk ? 'تم تفعيل كشف الإنترنت الخارجي' : 'تم تعطيل كشف الإنترنت الخارجي');
        }

        async function togglePreventRetake() {
            const chk = document.getElementById('preventRetakeToggle').checked;
            await fetch('/api/teacher/settings', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ prevent_retake: chk ? '1' : '0' })
            });
            showToast(chk ? 'تم تفعيل قفل إعادة الاختبار' : 'تم السماح بإعادة الاختبار');
        }

        // Server On/Off
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
            navigator.clipboard.writeText(url);
            showToast('تم نسخ الرابط المباشر للطلاب 📋');
        }

        function showQrModal() {
            const url = 'http://' + primaryIp + ':8080';
            document.getElementById('qrModalUrl').textContent = url;
            drawSimpleQr('qrCanvas', url);
            document.getElementById('qrModal').style.display = 'flex';
        }

        function showGuideModal() {
            toggleDrawer(false);
            document.getElementById('guideModal').style.display = 'flex';
        }

        // Simple local QR Code Drawing
        function drawSimpleQr(canvasId, text) {
            const c = document.getElementById(canvasId);
            const ctx = c.getContext('2d');
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, 220, 220);
            ctx.fillStyle = '#0f172a';
            // Simple finder patterns
            const drawBox = (x, y) => {
                ctx.fillRect(x, y, 42, 42);
                ctx.clearRect(x+6, y+6, 30, 30);
                ctx.fillRect(x+12, y+12, 18, 18);
            };
            drawBox(10, 10);
            drawBox(168, 10);
            drawBox(10, 168);
            // Draw pseudo grid based on text hash
            let h = 0;
            for (let i = 0; i < text.length; i++) h = ((h << 5) - h) + text.charCodeAt(i);
            for (let i = 0; i < 22; i++) {
                for (let j = 0; j < 22; j++) {
                    if ((i<6 && j<6) || (i>15 && j<6) || (i<6 && j>15)) continue;
                    if ((h ^ (i * 31 + j * 17)) % 3 === 0) {
                        ctx.fillRect(10 + i * 9, 10 + j * 9, 7, 7);
                    }
                }
            }
        }

        // Evaluation
        function openEvalModal(id) {
            const s = (serverData.students || []).find(x => x.id === id);
            if (!s) return;
            document.getElementById('evalStudentId').value = s.id;
            document.getElementById('evalModalTitle').textContent = 'رصد درجات: ' + s.username;
            document.getElementById('evalGradeSection').value = s.gradeSection || '';
            document.getElementById('evalExam1').value = s.exam1Score || 0;
            document.getElementById('evalExam2').value = s.exam2Score || 0;
            document.getElementById('evalPart').value = s.participationScore || 0;
            document.getElementById('evalBonus').value = s.bonusScore || 0;
            document.getElementById('evalNotes').value = s.notes || '';
            document.getElementById('evalShowGrades').checked = s.showGradesToStudent !== 0;
            document.getElementById('evalShowNotes').checked = s.showNotesToStudent !== 0;
            document.getElementById('evalModal').style.display = 'flex';
        }

        async function saveStudentEvaluation() {
            const payload = {
                studentId: parseInt(document.getElementById('evalStudentId').value),
                gradeSection: document.getElementById('evalGradeSection').value.trim(),
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
            fetchData();
            showToast('تم حفظ التقييم بنجاح!');
        }

        // Create Quiz Modal
        function openNewQuizModal() {
            document.getElementById('newQuestionsContainer').innerHTML = '';
            addQuestionItem();
            document.getElementById('quizModal').style.display = 'flex';
        }

        let qCount = 0;
        function addQuestionItem() {
            qCount++;
            const c = document.getElementById('newQuestionsContainer');
            const d = document.createElement('div');
            d.style.cssText = 'background:var(--card-color); border:1px solid var(--border); border-radius:10px; padding:10px; margin-bottom:8px;';
            d.innerHTML = '<div class="form-group"><label>نص السؤال ' + qCount + ':</label><input type="text" class="form-input q-t"></div>' +
                '<div style="display:grid; grid-template-columns:1fr 1fr; gap:6px;">' +
                    '<input type="text" class="form-input q-a" placeholder="خيار أ">' +
                    '<input type="text" class="form-input q-b" placeholder="خيار ب">' +
                    '<input type="text" class="form-input q-c" placeholder="خيار ج">' +
                    '<input type="text" class="form-input q-d" placeholder="خيار د">' +
                '</div>' +
                '<div class="form-group" style="margin-top:6px;"><label>الإجابة الصحيحة:</label><select class="form-input q-cor"><option value="A">الخيار (أ)</option><option value="B">الخيار (ب)</option><option value="C">الخيار (ج)</option><option value="D">الخيار (د)</option></select></div>';
            c.appendChild(d);
        }

        async function submitNewQuiz() {
            const title = document.getElementById('newQuizTitle').value.trim();
            const desc = document.getElementById('newQuizDesc').value.trim();
            const duration = parseInt(document.getElementById('newQuizDuration').value) || 10;
            const type = document.getElementById('newQuizType').value;
            if (!title) return showToast('يرجى كتابة عنوان الاختبار', true);

            const questions = [];
            document.querySelectorAll('#newQuestionsContainer > div').forEach(d => {
                const t = d.querySelector('.q-t').value.trim();
                if (t) {
                    questions.push({
                        questionText: t,
                        optionA: d.querySelector('.q-a').value.trim() || 'أ',
                        optionB: d.querySelector('.q-b').value.trim() || 'ب',
                        optionC: d.querySelector('.q-c').value.trim() || '',
                        optionD: d.querySelector('.q-d').value.trim() || '',
                        correctAnswer: d.querySelector('.q-cor').value,
                        points: 1
                    });
                }
            });
            if (questions.length === 0) return showToast('يرجى إضافة سؤال واحد على الأقل', true);

            await fetch('/api/teacher/create-quiz', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ title, description: desc, durationMinutes: duration, type, questions })
            });
            closeModal('quizModal');
            fetchData();
            showToast('تم نشر الاختبار بنجاح!');
        }
    </script>
</body>
</html>
"""
