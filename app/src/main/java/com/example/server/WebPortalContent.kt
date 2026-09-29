package com.example.server

object WebPortalContent {

    fun getIndexHtml(): String {
        return """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>بوابة اختبارات الحصة الذكية</title>
    <style>
        :root {
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --primary-light: #dbeafe;
            --success: #16a34a;
            --success-light: #dcfce7;
            --danger: #dc2626;
            --danger-light: #fee2e2;
            --warning: #d97706;
            --warning-light: #fef3c7;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --radius: 16px;
        }

        body.dark-mode {
            --primary: #3b82f6;
            --primary-dark: #60a5fa;
            --primary-light: rgba(59, 130, 246, 0.18);
            --success: #22c55e;
            --success-light: rgba(34, 197, 94, 0.18);
            --danger: #ef4444;
            --danger-light: rgba(239, 68, 68, 0.18);
            --warning: #f59e0b;
            --warning-light: rgba(245, 158, 11, 0.18);
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background: var(--bg);
            color: var(--text-main);
            line-height: 1.6;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            padding-bottom: 40px;
            transition: background-color 0.25s, color 0.25s;
        }

        header {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
            color: white;
            padding: 16px;
            box-shadow: 0 4px 20px rgba(37, 99, 235, 0.2);
            position: sticky;
            top: 0;
            z-index: 50;
        }

        .header-content {
            max-width: 680px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header-title {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .header-title h1 {
            font-size: 1.12rem;
            font-weight: 700;
        }

        .offline-badge {
            background: rgba(255,255,255,0.2);
            font-size: 0.73rem;
            padding: 3px 8px;
            border-radius: 20px;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            margin-top: 2px;
        }

        .dot {
            width: 8px;
            height: 8px;
            background: #4ade80;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px #4ade80;
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .theme-toggle-btn {
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.3);
            color: white;
            padding: 6px 10px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .container {
            max-width: 680px;
            width: 100%;
            margin: 16px auto 0 auto;
            padding: 0 16px;
            flex: 1;
        }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            transition: all 0.2s;
        }

        .tab-bar {
            display: flex;
            background: rgba(0,0,0,0.04);
            padding: 4px;
            border-radius: 12px;
            margin-bottom: 18px;
            border: 1px solid var(--border);
        }

        .tab-btn {
            flex: 1;
            padding: 10px 12px;
            border: none;
            background: transparent;
            color: var(--text-muted);
            font-weight: 600;
            font-size: 0.92rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.15s;
            text-align: center;
        }

        .tab-btn.active {
            background: var(--card-bg);
            color: var(--primary);
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        }

        .form-group {
            margin-bottom: 14px;
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        label {
            font-size: 0.88rem;
            font-weight: 600;
            color: var(--text-main);
        }

        input, textarea, select {
            width: 100%;
            padding: 12px 14px;
            border: 1.5px solid var(--border);
            border-radius: 10px;
            font-size: 0.96rem;
            background: var(--card-bg);
            color: var(--text-main);
            outline: none;
            transition: border-color 0.2s;
        }

        input:focus, textarea:focus, select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-light);
        }

        .btn {
            background: var(--primary);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 10px;
            font-size: 0.98rem;
            font-weight: 700;
            cursor: pointer;
            width: 100%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: background 0.2s;
        }

        .btn:hover {
            background: var(--primary-dark);
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .btn-outline {
            background: transparent;
            border: 1.5px solid var(--primary);
            color: var(--primary);
        }

        .btn-outline:hover {
            background: var(--primary-light);
        }

        .btn-sm {
            padding: 8px 14px;
            font-size: 0.88rem;
            width: auto;
            border-radius: 8px;
        }

        .info-box {
            background: #eff6ff;
            border-right: 4px solid var(--primary);
            padding: 12px 14px;
            border-radius: 8px;
            font-size: 0.88rem;
            color: #1e40af;
            margin-bottom: 16px;
        }

        body.dark-mode .info-box {
            background: rgba(59, 130, 246, 0.15);
            color: #93c5fd;
        }

        .quiz-card {
            border: 1.5px solid var(--border);
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 14px;
            background: var(--card-bg);
            display: flex;
            flex-direction: column;
            gap: 10px;
            transition: all 0.2s;
        }

        .quiz-card:hover {
            border-color: var(--primary);
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.08);
        }

        .quiz-card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }

        .badge {
            font-size: 0.74rem;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
            display: inline-block;
        }

        .badge-quiz {
            background: #e0e7ff;
            color: #3730a3;
        }

        .badge-activity {
            background: #fef3c7;
            color: #92400e;
        }

        .badge-success {
            background: var(--success-light);
            color: var(--success);
        }

        .badge-danger {
            background: var(--danger-light);
            color: var(--danger);
        }

        .meta-row {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            font-size: 0.84rem;
            color: var(--text-muted);
        }

        /* Anti-Cheat Internet Alert Banner Modal */
        #antiCheatModal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(15, 23, 42, 0.88);
            backdrop-filter: blur(6px);
            z-index: 99999;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .anti-cheat-card {
            background: var(--card-bg);
            border: 2px solid var(--danger);
            border-radius: 20px;
            max-width: 460px;
            width: 100%;
            padding: 24px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(220, 38, 38, 0.3);
            animation: pulse-border 1.5s infinite;
        }

        @keyframes pulse-border {
            0% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.5); }
            70% { box-shadow: 0 0 0 15px rgba(220, 38, 38, 0); }
            100% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
        }

        /* Active Quiz UI */
        .timer-box {
            background: #fff1f2;
            color: #e11d48;
            font-weight: 700;
            padding: 8px 14px;
            border-radius: 10px;
            border: 1px solid #fecdd3;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.95rem;
        }

        body.dark-mode .timer-box {
            background: rgba(225, 29, 72, 0.15);
            border-color: rgba(225, 29, 72, 0.3);
        }

        .question-card {
            background: var(--card-bg);
            border: 1.5px solid var(--border);
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 16px;
        }

        .question-title {
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 14px;
            color: var(--text-main);
        }

        .options-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .option-label {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 14px;
            border: 1.5px solid var(--border);
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.15s;
            background: rgba(0,0,0,0.02);
            color: var(--text-main);
        }

        .option-label:hover {
            border-color: var(--primary);
            background: var(--primary-light);
        }

        .option-label.selected {
            border-color: var(--primary);
            background: var(--primary-light);
            font-weight: 600;
        }

        .result-banner {
            text-align: center;
            padding: 24px 16px;
            border-radius: 16px;
            margin-bottom: 20px;
        }

        .result-score {
            font-size: 2.8rem;
            font-weight: 800;
            color: var(--primary);
            line-height: 1.1;
            margin: 10px 0;
        }

        .toast {
            position: fixed;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%);
            background: #1e293b;
            color: white;
            padding: 12px 24px;
            border-radius: 30px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.25);
            font-size: 0.95rem;
            z-index: 1000;
            display: none;
            max-width: 90%;
            text-align: center;
        }

        .empty-state {
            text-align: center;
            padding: 36px 16px;
            color: var(--text-muted);
        }

        .empty-icon {
            font-size: 3rem;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>

    <!-- ANTI-CHEAT EXTERNAL INTERNET OVERLAY -->
    <div id="antiCheatModal">
        <div class="anti-cheat-card">
            <div style="font-size: 3.5rem; margin-bottom: 10px;">🚫</div>
            <h2 style="color: var(--danger); font-size: 1.35rem; margin-bottom: 10px;">تنبيه أمني: اتصال إنترنت خارجي!</h2>
            <p style="font-size: 0.94rem; line-height: 1.6; margin-bottom: 14px;">
                تم رصد اتصال هاتفك بالإنترنت الخارجي (بيانات الهاتف 4G/5G أو شبكة أخرى).
            </p>
            <div style="background: var(--danger-light); color: var(--danger); padding: 12px; border-radius: 10px; font-size: 0.88rem; font-weight: 600; margin-bottom: 16px; text-align: right;">
                ⚠️ <strong>قواعد الاختبار العادل:</strong> هذا الاختبار محمي ويتطلب الاتصال الحصري بشبكة بث المعلم بدون إنترنت خارجي لمنع البحث أو تسريب الأسئلة.
            </div>
            <p style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 18px;">
                يرجى <strong>إيقاف بيانات الهاتف (بيانات الجوال)</strong> فوراً وسيعود الاختبار للعمل تلقائياً.
            </p>
            <button onclick="recheckInternetNow()" class="btn" style="background: var(--danger);">
                <span>فحص الاتصال مجدداً 🔄</span>
            </button>
        </div>
    </div>

    <header>
        <div class="header-content">
            <div class="header-title">
                <span style="font-size: 1.5rem;">📚</span>
                <div>
                    <h1>بوابة اختبارات الحصة الذكية</h1>
                    <div class="offline-badge">
                        <span class="dot"></span>
                        <span>بث محلي آمن بدون إنترنت</span>
                    </div>
                </div>
            </div>
            <div class="header-actions">
                <button onclick="toggleNightMode()" class="theme-toggle-btn" id="themeBtn" title="الوضع الليلي">
                    🌙 <span id="themeBtnText">ليلي</span>
                </button>
                <div id="userHeaderActions" style="display: none;">
                    <button onclick="logout()" class="btn btn-outline btn-sm" style="color:white; border-color:white;">خروج</button>
                </div>
            </div>
        </div>
    </header>

    <div class="container">

        <!-- AUTH VIEW: Registration with Full Details / Login -->
        <div id="authView" class="card">
            <div class="tab-bar">
                <button id="tabRegister" class="tab-btn active" onclick="switchAuthTab('register')">تسجيل طالب جديد (لأول مرة)</button>
                <button id="tabLogin" class="tab-btn" onclick="switchAuthTab('login')">تسجيل دخول</button>
            </div>

            <!-- Enhanced Registration Form (Requested by user) -->
            <div id="registerForm">
                <div class="info-box">
                    👋 <strong>التسجيل لأول مرة:</strong> يرجى إدخال بياناتك الرسمية بدقة لتوثيق حضورك واختباراتك وحفظها لدى جهاز المعلم.
                </div>

                <div class="form-group">
                    <label>الاسم الرباعي الصريح للطالب: <span style="color:var(--danger)">*</span></label>
                    <input type="text" id="regName" placeholder="مثال: محمد عبدالله خالد العتيبي" required autocomplete="name">
                </div>

                <div class="form-group">
                    <label>رقم الهوية الوطنية أو الإقامة: <span style="color:var(--danger)">*</span></label>
                    <input type="tel" id="regNationalId" placeholder="10 أرقام (رقم الهوية أو الإقامة)" maxlength="10" required>
                </div>

                <div class="form-group">
                    <label>رقم الهاتف / الجوال: <span style="color:var(--danger)">*</span></label>
                    <input type="tel" id="regPhone" placeholder="مثال: 05xxxxxxxx" maxlength="14" required>
                </div>

                <div class="form-group">
                    <label>الصف والشعبة: <span style="color:var(--danger)">*</span></label>
                    <input type="text" id="regGradeSection" placeholder="مثال: أول ثانوي - شعبة 1" required>
                </div>

                <div class="form-group">
                    <label>اختر كلمة مرور خاصة بحسابك: <span style="color:var(--danger)">*</span></label>
                    <input type="password" id="regPass" placeholder="كلمة مرور تتذكرها للدخول مستقبلاً" required>
                </div>

                <button onclick="handleRegister()" class="btn" id="regBtn">
                    <span>حفظ البيانات وتسجيل الدخول للدروس</span>
                    <span>←</span>
                </button>
            </div>

            <!-- Login Form (Supports Login by Name or National ID) -->
            <div id="loginForm" style="display: none;">
                <div class="info-box" style="background: #f0fdf4; border-color: var(--success); color: #166534;">
                    🔑 ادخل رقم الهوية/الإقامة (أو اسمك الرباعي) مع كلمة المرور التي حددتها سابقاً.
                </div>

                <div class="form-group">
                    <label>رقم الهوية الوطنية أو الاسم الرباعي:</label>
                    <input type="text" id="loginIdentity" placeholder="رقم الهوية أو اسمك المسجل" required onkeypress="if(event.key==='Enter') document.getElementById('loginPass').focus()">
                </div>

                <div class="form-group">
                    <label>كلمة المرور:</label>
                    <input type="password" id="loginPass" placeholder="كلمة المرور الخاصة بك" required onkeypress="if(event.key==='Enter') handleLogin()">
                </div>

                <button onclick="handleLogin()" class="btn" id="loginBtn">
                    <span>تسجيل الدخول</span>
                    <span>←</span>
                </button>
            </div>

            <!-- Active Quizzes Preview (Visible before login) -->
            <div id="authQuizzesPreview" style="margin-top: 22px; border-top: 1.5px dashed var(--border); padding-top: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <h4 style="font-size: 0.96rem; color: var(--primary); font-weight: 700;">📋 الاختبارات والأنشطة المتاحة في هذه الحصة:</h4>
                    <span id="previewCountBadge" class="badge badge-quiz">0 اختبارات</span>
                </div>
                <div id="authQuizzesList" style="display: flex; flex-direction: column; gap: 8px;">
                    <p style="font-size: 0.85rem; color: var(--text-muted);">جاري فحص اختبارات المعلم...</p>
                </div>
                <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 10px; text-align: center;">
                    💡 سجّل اسمك وبياناتك بالأعلى أولاً للبدء في حل هذه الاختبارات وحفظ درجاتك.
                </p>
            </div>
        </div>

        <!-- DASHBOARD VIEW: Student's available tests & Completed results -->
        <div id="dashboardView" style="display: none;">
            <!-- Student Header Profile Banner -->
            <div class="card" style="background: linear-gradient(135deg, rgba(37,99,235,0.08) 0%, rgba(37,99,235,0.18) 100%); border-color: var(--primary);">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <h2 style="font-size: 1.18rem; color: var(--primary);">أهلاً بك: <span id="studentGreetingName"></span> 👋</h2>
                        <div style="font-size: 0.84rem; color: var(--text-muted); display: flex; gap: 10px; margin-top: 4px;">
                            <span id="studentGreetingId"></span>
                            <span id="studentGreetingGrade"></span>
                        </div>
                    </div>
                    <button onclick="loadQuizzes()" class="btn btn-outline btn-sm" style="background:var(--card-bg);">
                        تحديث 🔄
                    </button>
                </div>
            </div>

            <!-- Quizzes Categorized Tabs -->
            <div class="tab-bar">
                <button id="tabAvailableQuizzes" class="tab-btn active" onclick="switchQuizzesTab('available')">
                    📋 الاختبارات (<span id="availableCount">0</span>)
                </button>
                <button id="tabCompletedQuizzes" class="tab-btn" onclick="switchQuizzesTab('completed')">
                    🏆 نتائج الحل (<span id="completedCount">0</span>)
                </button>
                <button id="tabEvaluationGrades" class="tab-btn" onclick="switchQuizzesTab('evaluation')">
                    📊 درجاتي وتقييمي
                </button>
            </div>

            <!-- Available (Unattempted) Quizzes Container -->
            <div id="availableQuizzesContainer"></div>

            <!-- Completed Quizzes Container (Scores & Cannot retake) -->
            <div id="completedQuizzesContainer" style="display: none;"></div>

            <!-- Student Evaluation Card (Monthly Exams, Participation, Bonus, Notes) -->
            <div id="evaluationGradesContainer" style="display: none;"></div>
        </div>

        <!-- QUIZ ACTIVE VIEW: Taking the quiz -->
        <div id="activeQuizView" style="display: none;">
            <div class="card" style="position: sticky; top: 72px; z-index: 40;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h2 id="activeQuizTitle" style="font-size: 1.15rem;">عنوان الاختبار</h2>
                        <span id="activeQuizTypeBadge" class="badge badge-quiz">اختبار تقييمي</span>
                    </div>
                    <div id="quizTimerBox" class="timer-box">
                        <span>⏱️</span>
                        <span id="quizTimerText">--:--</span>
                    </div>
                </div>
            </div>

            <div id="questionsContainer"></div>

            <div class="card" style="text-align: center;">
                <button onclick="confirmSubmitQuiz()" class="btn" id="submitExamBtn">
                    <span>تسليم الإجابات وإنهاء الاختبار</span>
                    <span>✓</span>
                </button>
            </div>
        </div>

        <!-- RESULT VIEW: Score & Feedback -->
        <div id="resultView" style="display: none;">
            <div class="card">
                <div class="result-banner" style="background: var(--success-light); border: 1.5px solid var(--success);">
                    <span style="font-size: 3rem;">🎉</span>
                    <h2 style="color: var(--success); font-size: 1.3rem;">تم تسليم إجاباتك بنجاح!</h2>
                    <p style="color: var(--text-main); font-size: 0.95rem; margin-top: 4px;">
                        تم إرسال نتيجتك وحفظها فوراً في سجل درجات المعلم.
                    </p>
                    <div class="result-score" id="resScore">-- / --</div>
                    <div id="resPercent" style="font-weight: 700; color: var(--success);">النسبة: --%</div>
                </div>

                <div style="background: rgba(0,0,0,0.03); border-radius: 12px; padding: 14px; text-align: center; margin-bottom: 16px;">
                    <p style="font-size: 0.9rem; color: var(--text-muted);">
                        🔒 تم إغلاق الاختبار لك، ولا يمكن إعادة الدخول للحفاظ على سرية الأسئلة.
                    </p>
                </div>

                <button onclick="backToDashboard()" class="btn">
                    <span>العودة إلى لوحة الاختبارات الرئيسية</span>
                    <span>←</span>
                </button>
            </div>
        </div>

    </div>

    <div id="toast" class="toast"></div>

    <script>
        let currentStudent = null;
        let activeQuizData = null;
        let currentAnswers = {};
        let timerInterval = null;
        let timeRemainingSeconds = 0;
        let currentQuizzesTab = 'available';
        let isExternalInternetActive = false;
        let internetCheckInterval = null;

        // Init on load
        window.addEventListener('DOMContentLoaded', () => {
            initNightMode();
            checkSavedSession();
            loadAuthQuizzesPreview();
            startInternetMonitoring();
            startDashboardPolling();
        });

        // Night Mode toggle
        function initNightMode() {
            const savedTheme = localStorage.getItem('portal_theme');
            if (savedTheme === 'dark') {
                document.body.classList.add('dark-mode');
                document.getElementById('themeBtnText').textContent = 'نهاري';
                document.getElementById('themeBtn').innerHTML = '☀️ <span>نهاري</span>';
            }
        }

        function toggleNightMode() {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            localStorage.setItem('portal_theme', isDark ? 'dark' : 'light');
            document.getElementById('themeBtn').innerHTML = isDark ? '☀️ <span>نهاري</span>' : '🌙 <span>ليلي</span>';
        }

        function showToast(msg, isError = false) {
            const t = document.getElementById('toast');
            t.textContent = msg;
            t.style.background = isError ? '#dc2626' : '#1e293b';
            t.style.display = 'block';
            setTimeout(() => { t.style.display = 'none'; }, 3200);
        }

        function switchAuthTab(tab) {
            const tabReg = document.getElementById('tabRegister');
            const tabLog = document.getElementById('tabLogin');
            const regForm = document.getElementById('registerForm');
            const logForm = document.getElementById('loginForm');

            if (tab === 'register') {
                tabReg.classList.add('active');
                tabLog.classList.remove('active');
                regForm.style.display = 'block';
                logForm.style.display = 'none';
            } else {
                tabLog.classList.add('active');
                tabReg.classList.remove('active');
                logForm.style.display = 'block';
                regForm.style.display = 'none';
            }
        }

        function switchQuizzesTab(tab) {
            currentQuizzesTab = tab;
            const tabAvail = document.getElementById('tabAvailableQuizzes');
            const tabComp = document.getElementById('tabCompletedQuizzes');
            const availCont = document.getElementById('availableQuizzesContainer');
            const compCont = document.getElementById('completedQuizzesContainer');

            if (tab === 'available') {
                tabAvail.classList.add('active');
                tabComp.classList.remove('active');
                availCont.style.display = 'block';
                compCont.style.display = 'none';
            } else {
                tabComp.classList.add('active');
                tabAvail.classList.remove('active');
                compCont.style.display = 'block';
                availCont.style.display = 'none';
            }
        }

        function checkSavedSession() {
            const saved = localStorage.getItem('class_student');
            if (saved) {
                try {
                    currentStudent = JSON.parse(saved);
                    if (currentStudent && currentStudent.username) {
                        showDashboard();
                    }
                } catch(e) {
                    localStorage.removeItem('class_student');
                }
            }
        }

        // Real-time external internet check (Anti-Cheat)
        function startInternetMonitoring() {
            // Check immediately
            checkExternalInternet();
            // And periodically
            internetCheckInterval = setInterval(checkExternalInternet, 7000);
        }

        async function checkExternalInternet() {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 1800);
                // Attempt to reach a reliable public internet target with cache disabled
                const probe = await fetch('https://www.google.com/generate_204?' + Date.now(), {
                    method: 'HEAD',
                    mode: 'no-cors',
                    cache: 'no-store',
                    signal: controller.signal
                });
                clearTimeout(timeoutId);
                // If it succeeds, WAN / 4G / 5G is reachable!
                handleExternalInternetDetected(true);
            } catch (err) {
                // In isolated offline classroom hotspot, external DNS / WAN fails completely -> THIS IS EXPECTED!
                handleExternalInternetDetected(false);
            }
        }

        function recheckInternetNow() {
            showToast('جاري التحقق من حالة الاتصال...');
            checkExternalInternet();
        }

        function handleExternalInternetDetected(detected) {
            const modal = document.getElementById('antiCheatModal');
            if (detected) {
                modal.style.display = 'flex';
                if (!isExternalInternetActive && currentStudent) {
                    // Send alert to teacher
                    fetch('/api/cheat-alert', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            studentUsername: currentStudent.username,
                            reason: 'تم رصد اتصال خارجي بالإنترنت (بيانات الهاتف 4G/5G نشطة أثناء الامتحان)'
                        })
                    }).catch(() => {});
                }
                isExternalInternetActive = true;
            } else {
                modal.style.display = 'none';
                if (isExternalInternetActive) {
                    showToast('تم التحقق: أنت الآن في بيئة الاختبار المعزولة بنجاح ✓');
                }
                isExternalInternetActive = false;
            }
        }

        // Registration with complete details
        async function handleRegister() {
            const name = document.getElementById('regName').value.trim();
            const nationalId = document.getElementById('regNationalId').value.trim();
            const phone = document.getElementById('regPhone').value.trim();
            const gradeSection = document.getElementById('regGradeSection').value.trim();
            const pass = document.getElementById('regPass').value.trim();

            if (!name || !nationalId || !phone || !gradeSection || !pass) {
                showToast('يرجى ملء جميع الحقول المطلوبة للتسجيل', true);
                return;
            }

            if (nationalId.length < 9) {
                showToast('يرجى التأكد من صحة رقم الهوية أو الإقامة (10 أرقام)', true);
                return;
            }

            const btn = document.getElementById('regBtn');
            btn.disabled = true;
            btn.innerText = 'جاري تسجيل بياناتك...';

            try {
                const res = await fetch('/api/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        username: name,
                        nationalId: nationalId,
                        phone: phone,
                        gradeSection: gradeSection,
                        password: pass
                    })
                });

                const data = await res.json();
                if (res.ok && data.success) {
                    currentStudent = data.student;
                    localStorage.setItem('class_student', JSON.stringify(currentStudent));
                    showToast('تم تسجيلك بنجاح وحفظ بياناتك لدى المعلم! 🎉');
                    showDashboard();
                } else {
                    const msg = data.message || 'فشل التسجيل، يرجى المحاولة ثانية';
                    showToast(msg, true);
                    if (msg.includes('مسجل بالفعل') || msg.includes('تسجيل الدخول')) {
                        setTimeout(() => {
                            switchAuthTab('login');
                            document.getElementById('loginIdentity').value = nationalId || name;
                        }, 1600);
                    }
                }
            } catch (err) {
                showToast('تعذر الاتصال بالمعلم. تأكد من الاتصال بنقطة بث المعلم (Hotspot).', true);
            } finally {
                btn.disabled = false;
                btn.innerText = 'حفظ البيانات وتسجيل الدخول للدروس ←';
            }
        }

        // Login Handler
        async function handleLogin() {
            const identity = document.getElementById('loginIdentity').value.trim();
            const pass = document.getElementById('loginPass').value.trim();

            if (!identity || !pass) {
                showToast('يرجى كتابة رقم الهوية أو الاسم وكلمة المرور', true);
                return;
            }

            const btn = document.getElementById('loginBtn');
            btn.disabled = true;
            btn.innerText = 'جاري التحقق...';

            try {
                const res = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        identity: identity,
                        username: identity,
                        password: pass
                    })
                });

                const data = await res.json();
                if (res.ok && data.success) {
                    currentStudent = data.student;
                    localStorage.setItem('class_student', JSON.stringify(currentStudent));
                    showToast('أهلاً بعودتك يا ' + currentStudent.username);
                    showDashboard();
                } else {
                    showToast(data.message || 'رقم الهوية أو كلمة المرور غير صحيحة', true);
                }
            } catch (err) {
                showToast('تعذر الاتصال بالخادم، تأكد من الاتصال بنقطة بث المعلم (Hotspot)', true);
            } finally {
                btn.disabled = false;
                btn.innerText = 'تسجيل الدخول ←';
            }
        }

        function logout() {
            localStorage.removeItem('class_student');
            currentStudent = null;
            document.getElementById('userHeaderActions').style.display = 'none';
            document.getElementById('dashboardView').style.display = 'none';
            document.getElementById('activeQuizView').style.display = 'none';
            document.getElementById('resultView').style.display = 'none';
            document.getElementById('authView').style.display = 'block';
            loadAuthQuizzesPreview();
            showToast('تم تسجيل الخروج');
        }

        function showDashboard() {
            document.getElementById('authView').style.display = 'none';
            document.getElementById('activeQuizView').style.display = 'none';
            document.getElementById('resultView').style.display = 'none';
            document.getElementById('dashboardView').style.display = 'block';
            document.getElementById('userHeaderActions').style.display = 'block';

            document.getElementById('studentGreetingName').textContent = currentStudent.username;
            document.getElementById('studentGreetingId').textContent = currentStudent.nationalId ? 'هوية: ' + currentStudent.nationalId : '';
            document.getElementById('studentGreetingGrade').textContent = currentStudent.gradeSection ? '• الصف: ' + currentStudent.gradeSection : '';
            loadQuizzes(false);
        }

        // Preview of quizzes on the login/registration screen
        async function loadAuthQuizzesPreview() {
            const listEl = document.getElementById('authQuizzesList');
            const badgeEl = document.getElementById('previewCountBadge');
            if (!listEl) return;

            try {
                let res = await fetch('/api/student-quizzes');
                let data = await res.json();
                let quizzes = (data.availableQuizzes && data.availableQuizzes.length !== undefined)
                    ? data.availableQuizzes
                    : (data.unattempted || []);

                if (quizzes.length === 0) {
                    try {
                        const fallbackRes = await fetch('/api/quizzes');
                        const fallbackList = await fallbackRes.json();
                        if (Array.isArray(fallbackList)) {
                            quizzes = fallbackList;
                        }
                    } catch (e) {}
                }

                if (badgeEl) {
                    badgeEl.textContent = quizzes.length + ' اختبارات متاحة';
                }

                if (quizzes.length === 0) {
                    listEl.innerHTML = '<p style="font-size:0.85rem; color:var(--text-muted); text-align:center;">لا توجد اختبارات معلنة حالياً. سيعلن المعلم عنها قريباً.</p>';
                } else {
                    let html = '';
                    quizzes.forEach((q, idx) => {
                        const isAct = q.type === 'ACTIVITY';
                        const badgeTxt = isAct ? 'نشاط تفاعلي' : 'اختبار تقييمي';
                        const badgeClass = isAct ? 'badge-activity' : 'badge-quiz';
                        const countTxt = (q.questionCount !== undefined && q.questionCount > 0) ? (q.questionCount + ' أسئلة') : '';
                        html += '<div style="display:flex; justify-content:space-between; align-items:center; background:rgba(0,0,0,0.03); padding:9px 12px; border-radius:10px; border:1px solid var(--border);">' +
                            '<div>' +
                                '<div style="font-weight:600; font-size:0.92rem; color:var(--text-main);">' + (idx + 1) + '. ' + (q.title || 'اختبار') + '</div>' +
                                '<div style="font-size:0.78rem; color:var(--text-muted); margin-top:2px;">⏱️ ' + (q.durationMinutes || 10) + ' دقيقة ' + (countTxt ? '• ❓ ' + countTxt : '') + '</div>' +
                            '</div>' +
                            '<span class="badge ' + badgeClass + '">' + badgeTxt + '</span>' +
                        '</div>';
                    });
                    listEl.innerHTML = html;
                }
            } catch (err) {
                if (listEl) {
                    listEl.innerHTML = '<p style="font-size:0.82rem; color:var(--text-muted);">يرجى التأكد من الاتصال بشبكة وايفاي المعلم (Hotspot).</p>';
                }
            }
        }

        // Automatic periodic polling for student dashboard
        let dashboardPollInterval = null;
        function startDashboardPolling() {
            if (dashboardPollInterval) clearInterval(dashboardPollInterval);
            dashboardPollInterval = setInterval(() => {
                const dash = document.getElementById('dashboardView');
                if (dash && dash.style.display !== 'none' && currentStudent) {
                    loadQuizzes(true);
                }
            }, 7000);
        }

        // Load quizzes categorized into Available and Completed
        async function loadQuizzes(isSilent = false) {
            const availCont = document.getElementById('availableQuizzesContainer');
            const compCont = document.getElementById('completedQuizzesContainer');

            if (!isSilent) {
                availCont.innerHTML = '<div class="empty-state"><div class="empty-icon">⏳</div><h3>جاري فحص الاختبارات...</h3></div>';
                compCont.innerHTML = '<div class="empty-state"><div class="empty-icon">⏳</div><h3>جاري تحميل النتائج...</h3></div>';
            }

            try {
                const studentName = currentStudent ? currentStudent.username : '';
                const res = await fetch('/api/student-quizzes?student=' + encodeURIComponent(studentName));
                const data = await res.json();

                // Robust check across all possible keys
                let available = (data.availableQuizzes && Array.isArray(data.availableQuizzes))
                    ? data.availableQuizzes
                    : (data.unattempted && Array.isArray(data.unattempted) ? data.unattempted : []);

                let completed = (data.completedQuizzes && Array.isArray(data.completedQuizzes))
                    ? data.completedQuizzes
                    : (data.completed && Array.isArray(data.completed) ? data.completed : []);

                // Fallback check to /api/quizzes if student-quizzes returned empty
                if (available.length === 0 && completed.length === 0) {
                    try {
                        const fbRes = await fetch('/api/quizzes?student=' + encodeURIComponent(studentName));
                        const fbList = await fbRes.json();
                        if (Array.isArray(fbList) && fbList.length > 0) {
                            available = fbList.filter(q => !q.isSubmitted);
                            completed = fbList.filter(q => q.isSubmitted);
                        }
                    } catch (e) {}
                }

                document.getElementById('availableCount').textContent = available.length;
                document.getElementById('completedCount').textContent = completed.length;

                // Render Available
                if (available.length === 0) {
                    availCont.innerHTML = `
                        <div class="card empty-state">
                            <div class="empty-icon">📝</div>
                            <h3>لا توجد اختبارات جديدة متاحة حالياً</h3>
                            <p style="font-size:0.88rem; color:var(--text-muted); margin-top:6px;">
                                لقد أتممت جميع الاختبارات الحالية، أو لم يقم المعلم بفتح اختبار جديد بعد.
                            </p>
                            <button onclick="loadQuizzes(false)" class="btn btn-outline btn-sm" style="margin-top:12px;">
                                إعادة الفحص 🔄
                            </button>
                        </div>
                    `;
                } else {
                    let h = '';
                    available.forEach(q => {
                        const isActivity = q.type === 'ACTIVITY';
                        const typeLabel = isActivity ? 'نشاط تفاعلي' : 'اختبار تقييمي';
                        const typeClass = isActivity ? 'badge-activity' : 'badge-quiz';
                        const targetQuizId = q.id || q.quizId;

                        h += '<div class="quiz-card">' +
                            '<div class="quiz-card-header">' +
                                '<div>' +
                                    '<h3 style="font-size:1.05rem; margin-bottom:4px;">' + q.title + '</h3>' +
                                    '<p style="font-size:0.88rem; color:var(--text-muted);">' + (q.description || 'بدون تعليمات إضافية') + '</p>' +
                                '</div>' +
                                '<span class="badge ' + typeClass + '">' + typeLabel + '</span>' +
                            '</div>' +
                            '<div class="meta-row">' +
                                '<span>⏱️ المدة: ' + (q.durationMinutes || 10) + ' دقيقة</span>' +
                                '<span>❓ عدد الأسئلة: ' + (q.questionCount !== undefined ? q.questionCount : 'متعدد') + '</span>' +
                            '</div>' +
                            '<div style="display:flex; justify-content:flex-end; margin-top:4px;">' +
                                '<button onclick="startQuiz(' + targetQuizId + ')" class="btn" style="padding:10px 18px; width:auto;">بدء الاختبار الآن ←</button>' +
                            '</div>' +
                        '</div>';
                    });
                    availCont.innerHTML = h;
                }

                // Render Completed (Locked - cannot retake)
                if (completed.length === 0) {
                    compCont.innerHTML = `
                        <div class="card empty-state">
                            <div class="empty-icon">📊</div>
                            <h3>لم تنجز أي اختبارات بعد</h3>
                            <p style="font-size:0.88rem; color:var(--text-muted); margin-top:6px;">
                                ستظهر هنا جميع درجاتك ونتائجك بعد تسليم أي اختبار للمعلم.
                            </p>
                        </div>
                    `;
                } else {
                    let h = '';
                    completed.forEach(q => {
                        h += '<div class="quiz-card" style="border-right: 4px solid var(--success);">' +
                            '<div class="quiz-card-header">' +
                                '<div>' +
                                    '<h3 style="font-size:1.05rem; margin-bottom:4px;">' + q.title + '</h3>' +
                                    '<span style="font-size:0.82rem; color:var(--text-muted);">تم التسليم: ' + (q.submittedAtFormatted || q.submittedAt || '') + '</span>' +
                                '</div>' +
                                '<span class="badge badge-success">✓ تم التسليم بنجاح</span>' +
                            '</div>' +
                            '<div class="meta-row" style="margin-top:6px;">' +
                                '<span style="font-weight:700; color:var(--primary); font-size:0.95rem;">الدرجة: ' + (q.score !== undefined ? q.score : '') + ' من ' + (q.totalPoints !== undefined ? q.totalPoints : '') + ' (' + (q.percentage !== undefined ? q.percentage : '') + '%)</span>' +
                                '<span>🔒 مكتمل ومغلق</span>' +
                            '</div>' +
                            '<div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px; background:rgba(0,0,0,0.02); padding:8px 12px; border-radius:8px;">' +
                                '<span style="font-size:0.82rem; color:var(--text-muted);">لا يمكن إعادة الاختبار بعد اعتماده</span>' +
                                '<button onclick="alertCompletedQuizNotice()" class="btn btn-outline btn-sm">عرض النتيجة 🔒</button>' +
                            '</div>' +
                        '</div>';
                    });
                    compCont.innerHTML = h;
                }

                // Render Student Evaluation (Monthly Exams, Participation, Bonus, Notes)
                const evalCont = document.getElementById('evaluationGradesContainer');
                if (evalCont && data.evaluation) {
                    const ev = data.evaluation;
                    if (ev.isVisible) {
                        let notesHtml = '';
                        if (ev.notes) {
                            notesHtml = '<div style="background:rgba(37,99,235,0.08); border:1.5px dashed var(--primary); border-radius:12px; padding:12px 14px; margin-top:14px;">' +
                                '<div style="font-weight:700; color:var(--primary); font-size:0.92rem; margin-bottom:4px;">💬 ملاحظة وتوجيه المعلم لك:</div>' +
                                '<div style="font-size:0.95rem; color:var(--text-main);">' + ev.notes + '</div>' +
                            '</div>';
                        }
                        const bonusSign = ev.bonusScore > 0 ? '+' : '';
                        evalCont.innerHTML = '<div class="card" style="border-top: 4px solid var(--primary);">' +
                            '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">' +
                                '<h3 style="font-size:1.1rem; color:var(--primary);">📊 بطاقة التقييم والدرجات الشهرية</h3>' +
                                '<span class="badge badge-success">✓ معتمدة</span>' +
                            '</div>' +
                            '<div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-top:10px;">' +
                                '<div style="background:rgba(0,0,0,0.03); border:1px solid var(--border); border-radius:12px; padding:12px; text-align:center;">' +
                                    '<div style="font-size:0.8rem; color:var(--text-muted);">الاختبار الشهري الأول</div>' +
                                    '<div style="font-size:1.35rem; font-weight:800; color:var(--text-main); margin-top:2px;">' + ev.exam1Score + '</div>' +
                                '</div>' +
                                '<div style="background:rgba(0,0,0,0.03); border:1px solid var(--border); border-radius:12px; padding:12px; text-align:center;">' +
                                    '<div style="font-size:0.8rem; color:var(--text-muted);">الاختبار الشهري الثاني</div>' +
                                    '<div style="font-size:1.35rem; font-weight:800; color:var(--text-main); margin-top:2px;">' + ev.exam2Score + '</div>' +
                                '</div>' +
                                '<div style="background:rgba(0,0,0,0.03); border:1px solid var(--border); border-radius:12px; padding:12px; text-align:center;">' +
                                    '<div style="font-size:0.8rem; color:var(--text-muted);">درجات المشاركة والتفاعل</div>' +
                                    '<div style="font-size:1.35rem; font-weight:800; color:var(--success); margin-top:2px;">' + ev.participationScore + '</div>' +
                                '</div>' +
                                '<div style="background:rgba(0,0,0,0.03); border:1px solid var(--border); border-radius:12px; padding:12px; text-align:center;">' +
                                    '<div style="font-size:0.8rem; color:var(--text-muted);">نقاط إضافية / خصم</div>' +
                                    '<div style="font-size:1.35rem; font-weight:800; color:' + (ev.bonusScore >= 0 ? 'var(--primary)' : 'var(--danger)') + '; margin-top:2px;">' + bonusSign + ev.bonusScore + '</div>' +
                                '</div>' +
                            '</div>' +
                            '<div style="background:linear-gradient(135deg, rgba(37,99,235,0.12) 0%, rgba(37,99,235,0.22) 100%); border-radius:14px; padding:14px; text-align:center; margin-top:12px; border:1px solid var(--primary);">' +
                                '<div style="font-size:0.88rem; font-weight:600; color:var(--primary);">المجموع التراكمي للدرجات</div>' +
                                '<div style="font-size:2.2rem; font-weight:900; color:var(--primary); line-height:1.2;">' + ev.totalScore + '</div>' +
                            '</div>' +
                            notesHtml +
                        '</div>';
                    } else {
                        evalCont.innerHTML = '<div class="card empty-state">' +
                            '<div class="empty-icon">🔒</div>' +
                            '<h3>الدرجات قيد المراجعة</h3>' +
                            '<p style="font-size:0.88rem; color:var(--text-muted); margin-top:6px;">' +
                                'يقوم المعلم حالياً بمراجعة ورصد الدرجات والملاحظات، وستظهر لك فور إتاحتها.' +
                            '</p>' +
                        '</div>';
                    }
                }
            } catch (err) {
                if (!isSilent) {
                    availCont.innerHTML = '<div class="card empty-state" style="color:var(--danger)">⚠️ تعذر الاتصال بالمعلم، تأكد من الاتصال بالشبكة واضغط تحديث.</div>';
                }
            }
        }

        function switchQuizzesTab(tab) {
            currentQuizzesTab = tab;
            const tabAvail = document.getElementById('tabAvailableQuizzes');
            const tabComp = document.getElementById('tabCompletedQuizzes');
            const tabEval = document.getElementById('tabEvaluationGrades');
            const contAvail = document.getElementById('availableQuizzesContainer');
            const contComp = document.getElementById('completedQuizzesContainer');
            const contEval = document.getElementById('evaluationGradesContainer');

            if (tabAvail) tabAvail.classList.remove('active');
            if (tabComp) tabComp.classList.remove('active');
            if (tabEval) tabEval.classList.remove('active');

            if (contAvail) contAvail.style.display = 'none';
            if (contComp) contComp.style.display = 'none';
            if (contEval) contEval.style.display = 'none';

            if (tab === 'available') {
                if (tabAvail) tabAvail.classList.add('active');
                if (contAvail) contAvail.style.display = 'block';
            } else if (tab === 'completed') {
                if (tabComp) tabComp.classList.add('active');
                if (contComp) contComp.style.display = 'block';
            } else if (tab === 'evaluation') {
                if (tabEval) tabEval.classList.add('active');
                if (contEval) contEval.style.display = 'block';
            }
        }

        function alertCompletedQuizNotice() {
            showToast('لقد أكملت هذا الاختبار مسبقاً! غير مسموح بإعادة المحاولة لحفظ سرية الاختبار.');
        }

        async function startQuiz(quizId) {
            if (isExternalInternetActive) {
                document.getElementById('antiCheatModal').style.display = 'flex';
                return;
            }

            try {
                showToast('جاري فتح أسئلة الاختبار...');
                const res = await fetch('/api/quiz?id=' + quizId + '&student=' + encodeURIComponent(currentStudent.username));
                const quiz = await res.json();

                if (!res.ok) {
                    showToast(quiz.message || 'تعذر تحميل الاختبار', true);
                    return;
                }

                if (quiz.error === 'ALREADY_SUBMITTED') {
                    showToast('لقد قمت بحل هذا الاختبار مسبقاً! غير مسموح بالدخول ثانية.', true);
                    loadQuizzes();
                    return;
                }

                activeQuizData = quiz;
                currentAnswers = {};

                document.getElementById('dashboardView').style.display = 'none';
                document.getElementById('activeQuizView').style.display = 'block';

                document.getElementById('activeQuizTitle').textContent = quiz.quiz.title;
                const isActivity = quiz.quiz.type === 'ACTIVITY';
                const badge = document.getElementById('activeQuizTypeBadge');
                badge.textContent = isActivity ? 'نشاط تفاعلي' : 'اختبار تقييمي';
                badge.className = isActivity ? 'badge badge-activity' : 'badge badge-quiz';

                // Setup Timer
                if (quiz.quiz.durationMinutes > 0) {
                    timeRemainingSeconds = quiz.quiz.durationMinutes * 60;
                    startTimer();
                } else {
                    document.getElementById('quizTimerBox').style.display = 'none';
                }

                renderQuestions(quiz.questions);
                window.scrollTo({ top: 0, behavior: 'smooth' });
            } catch (err) {
                showToast('حدث خطأ أثناء فتح الاختبار');
            }
        }

        function startTimer() {
            clearInterval(timerInterval);
            const timerBox = document.getElementById('quizTimerBox');
            timerBox.style.display = 'inline-flex';
            updateTimerDisplay();

            timerInterval = setInterval(() => {
                timeRemainingSeconds--;
                updateTimerDisplay();
                if (timeRemainingSeconds <= 0) {
                    clearInterval(timerInterval);
                    showToast('انتهى وقت الاختبار المحدد! جاري تسليم الإجابات تلقائياً...');
                    submitQuiz();
                }
            }, 1000);
        }

        function updateTimerDisplay() {
            const minutes = Math.floor(timeRemainingSeconds / 60);
            const seconds = timeRemainingSeconds % 60;
            const formatted = (minutes < 10 ? '0' : '') + minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
            document.getElementById('quizTimerText').textContent = formatted;
        }

        function renderQuestions(questions) {
            const container = document.getElementById('questionsContainer');
            let html = '';

            questions.forEach((q, idx) => {
                html += '<div class="question-card" id="qCard_' + q.id + '">' +
                        '<div class="question-title">' +
                            '<span style="color:var(--primary); font-weight:800;">س ' + (idx + 1) + ': </span>' +
                            q.questionText +
                            '<span style="font-size:0.8rem; font-weight:normal; color:var(--text-muted); float:left;">(' + q.points + ' درجات)</span>' +
                        '</div>';

                if (q.questionType === 'MULTIPLE_CHOICE') {
                    const options = [
                        { key: 'A', text: q.optionA },
                        { key: 'B', text: q.optionB },
                        { key: 'C', text: q.optionC },
                        { key: 'D', text: q.optionD }
                    ].filter(o => o.text && o.text.trim().length > 0);

                    html += '<div class="options-list">';
                    options.forEach(opt => {
                        html += '<label class="option-label" id="optLabel_' + q.id + '_' + opt.key + '" onclick="selectOption(' + q.id + ', \'' + opt.key + '\')">' +
                                '<input type="radio" name="question_' + q.id + '" value="' + opt.key + '">' +
                                '<strong style="color:var(--primary); min-width:24px;">(' + opt.key + ')</strong>' +
                                '<span>' + opt.text + '</span>' +
                            '</label>';
                    });
                    html += '</div>';
                } else if (q.questionType === 'TRUE_FALSE') {
                    html += '<div class="options-list">' +
                            '<label class="option-label" id="optLabel_' + q.id + '_TRUE" onclick="selectOption(' + q.id + ', \'TRUE\')">' +
                                '<input type="radio" name="question_' + q.id + '" value="' + opt.key || 'TRUE' + '">' +
                                '<span style="color:var(--success); font-weight:bold; font-size:1.1rem;">✓</span>' +
                                '<span>صح (صحيحة)</span>' +
                            '</label>' +
                            '<label class="option-label" id="optLabel_' + q.id + '_FALSE" onclick="selectOption(' + q.id + ', \'FALSE\')">' +
                                '<input type="radio" name="question_' + q.id + '" value="FALSE">' +
                                '<span style="color:var(--danger); font-weight:bold; font-size:1.1rem;">✗</span>' +
                                '<span>خطأ (غير صحيحة)</span>' +
                            '</label>' +
                        '</div>';
                } else if (q.questionType === 'SHORT_ANSWER') {
                    html += '<textarea rows="3" placeholder="اكتب إجابتك هنا بالتفصيل..." oninput="handleTextInput(' + q.id + ', this.value)"></textarea>';
                }

                html += '</div>';
            });

            container.innerHTML = html;
        }

        function selectOption(questionId, value) {
            currentAnswers[questionId] = value;
            const parent = document.getElementById('qCard_' + questionId);
            const labels = parent.querySelectorAll('.option-label');
            labels.forEach(lbl => lbl.classList.remove('selected'));

            const selectedLbl = document.getElementById('optLabel_' + questionId + '_' + value);
            if (selectedLbl) {
                selectedLbl.classList.add('selected');
                const radio = selectedLbl.querySelector('input[type="radio"]');
                if (radio) radio.checked = true;
            }
        }

        function handleTextInput(questionId, value) {
            currentAnswers[questionId] = value;
        }

        function confirmSubmitQuiz() {
            if (isExternalInternetActive) {
                document.getElementById('antiCheatModal').style.display = 'flex';
                return;
            }

            const unanswered = activeQuizData.questions.filter(q => !currentAnswers[q.id]);
            if (unanswered.length > 0) {
                if (!confirm('يوجد ' + unanswered.length + ' سؤال بدون إجابة، هل أنت متأكد من تسليم الاختبار الآن؟')) {
                    return;
                }
            }
            submitQuiz();
        }

        async function submitQuiz() {
            clearInterval(timerInterval);
            const btn = document.getElementById('submitExamBtn');
            btn.disabled = true;
            btn.innerText = 'جاري إرسال الإجابات إلى المعلم...';

            try {
                const res = await fetch('/api/submit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        quizId: activeQuizData.quiz.id,
                        studentUsername: currentStudent.username,
                        answers: currentAnswers
                    })
                });

                const data = await res.json();
                if (res.ok && data.success) {
                    showResultView(data);
                } else {
                    showToast(data.message || 'حدث خطأ في استلام الإجابة', true);
                    btn.disabled = false;
                    btn.innerText = 'تسليم الإجابات وإنهاء الاختبار ✓';
                }
            } catch (err) {
                showToast('تعذر الإرسال، يرجى المحاولة مجدداً');
                btn.disabled = false;
                btn.innerText = 'تسليم الإجابات وإنهاء الاختبار ✓';
            }
        }

        function showResultView(result) {
            document.getElementById('activeQuizView').style.display = 'none';
            document.getElementById('resultView').style.display = 'block';

            document.getElementById('resScore').textContent = result.score + ' من ' + result.totalPoints;
            document.getElementById('resPercent').textContent = 'النسبة المئوية: ' + result.percentage + '%';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function backToDashboard() {
            document.getElementById('resultView').style.display = 'none';
            document.getElementById('dashboardView').style.display = 'block';
            loadQuizzes();
        }
    </script>
</body>
</html>
        """.trimIndent()
    }
}
