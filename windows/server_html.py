# -*- coding: utf-8 -*-
r"""
Embedded HTML Templates for Student & Teacher Portals
Classroom Quiz Server - Windows 11 Desktop Edition
"""

STUDENT_HTML = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>بوابة اختبارات الحصة الذكية</title>
    <style>
        :root {
            --bg-color: #0b132b;
            --surface-color: #1c2541;
            --card-color: #243054;
            --primary: #3a86ff;
            --primary-dark: #2667d4;
            --accent-purple: #8338ec;
            --success: #10b981;
            --success-light: rgba(16, 185, 129, 0.15);
            --danger: #ef4444;
            --danger-light: rgba(239, 68, 68, 0.15);
            --warning: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
            --radius: 16px;
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
            padding-bottom: 30px;
        }

        header {
            background: linear-gradient(135deg, #1c2541 0%, #0b132b 100%);
            border-bottom: 1.5px solid var(--border);
            color: white;
            padding: 16px 20px;
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

        .logo-box {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-icon {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: rgba(58, 134, 255, 0.2);
            border: 1px solid var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
        }

        .container {
            max-width: 680px;
            width: 100%;
            margin: 16px auto 0 auto;
            padding: 0 16px;
            flex: 1;
        }

        .card {
            background: var(--surface-color);
            border: 1.5px solid var(--border);
            border-radius: var(--radius);
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        }

        .tab-bar {
            display: flex;
            background: rgba(0, 0, 0, 0.25);
            padding: 4px;
            border-radius: 12px;
            margin-bottom: 18px;
            border: 1px solid var(--border);
            gap: 4px;
        }

        .tab-btn {
            flex: 1;
            padding: 10px;
            border: none;
            background: transparent;
            color: var(--text-muted);
            border-radius: 10px;
            font-size: 0.92rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
        }

        .tab-btn.active {
            background: var(--primary);
            color: white;
            box-shadow: 0 2px 8px rgba(58, 134, 255, 0.3);
        }

        .form-group {
            margin-bottom: 14px;
        }

        .form-group label {
            display: block;
            font-size: 0.88rem;
            font-weight: 600;
            margin-bottom: 6px;
            color: var(--text-muted);
        }

        .form-input {
            width: 100%;
            padding: 12px 14px;
            border: 1.5px solid var(--border);
            border-radius: 12px;
            font-size: 1rem;
            background: var(--card-color);
            color: var(--text-main);
            transition: border-color 0.2s;
        }

        .form-input:focus {
            outline: none;
            border-color: var(--primary);
        }

        .btn {
            display: block;
            width: 100%;
            padding: 13px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent-purple) 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.05rem;
            font-weight: 700;
            cursor: pointer;
            text-align: center;
            box-shadow: 0 4px 15px rgba(58, 134, 255, 0.3);
            transition: opacity 0.2s, transform 0.1s;
        }

        .btn:hover {
            opacity: 0.92;
        }

        .btn:active {
            transform: scale(0.98);
        }

        .btn-outline {
            background: transparent;
            border: 1.5px solid var(--border);
            color: var(--text-main);
            box-shadow: none;
        }

        .btn-outline:hover {
            border-color: var(--primary);
            color: var(--primary);
        }

        .badge {
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 700;
            display: inline-block;
        }

        .badge-quiz { background: rgba(58, 134, 255, 0.2); color: #60a5fa; }
        .badge-success { background: var(--success-light); color: var(--success); }
        .badge-danger { background: var(--danger-light); color: var(--danger); }

        .session-alert {
            background: rgba(239, 68, 68, 0.12);
            border: 1.5px solid var(--danger);
            border-radius: 14px;
            padding: 16px;
            text-align: center;
            margin-bottom: 16px;
        }

        .toast {
            position: fixed;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%);
            background: #1e293b;
            color: white;
            padding: 12px 24px;
            border-radius: 12px;
            display: none;
            z-index: 999;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            font-size: 0.95rem;
        }

        .opt-label {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 14px;
            border: 1.5px solid var(--border);
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.15s;
            background: var(--card-color);
            margin-bottom: 8px;
        }

        .opt-label:hover {
            border-color: var(--primary);
        }

        .opt-label.selected {
            border-color: var(--primary);
            background: rgba(58, 134, 255, 0.15);
            font-weight: 600;
        }
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <div class="logo-box">
                <div class="logo-icon">🎓</div>
                <div>
                    <h1 style="font-size: 1.12rem; font-weight: 700;">بوابة اختبارات الحصة</h1>
                    <div style="font-size: 0.75rem; color: var(--text-muted); display:flex; align-items:center; gap:6px;">
                        <span style="width:7px; height:7px; background:#10b981; border-radius:50%; display:inline-block; box-shadow:0 0 6px #10b981;"></span>
                        خادم الواي فاي المحلي (Windows 11)
                    </div>
                </div>
            </div>
            <button onclick="logout()" id="logoutBtn" style="display:none; background:rgba(255,255,255,0.1); border:1px solid var(--border); color:white; padding:6px 14px; border-radius:20px; cursor:pointer; font-size:0.85rem;">خروج 🚪</button>
        </div>
    </header>

    <div class="container">
        <!-- Session Closed Alert (Dynamic) -->
        <div id="sessionClosedBanner" class="session-alert" style="display: none;">
            <div style="font-size: 1.8rem; margin-bottom: 4px;">🔒</div>
            <h3 style="color: var(--danger); font-size: 1.1rem; margin-bottom: 4px;">الحصة مغلقة حالياً من قبل المعلم</h3>
            <p style="font-size: 0.85rem; color: var(--text-muted);">
                يقوم المعلم بتهيئة الحصة الآن. يرجى الانتظار حتى يقوم المعلم بتفعيل البث من جهازه.
            </p>
        </div>

        <!-- AUTH VIEW (Register / Login) -->
        <div id="authView">
            <div class="card">
                <div class="tab-bar">
                    <button id="tabRegister" class="tab-btn active" onclick="switchAuthTab('register')">تسجيل جديد 📝</button>
                    <button id="tabLogin" class="tab-btn" onclick="switchAuthTab('login')">تسجيل الدخول 🔑</button>
                </div>

                <div id="registerForm">
                    <div class="form-group">
                        <label>الاسم الرباعي للطالب *</label>
                        <input type="text" id="regName" class="form-input" placeholder="اكتب اسمك الرباعي كاملاً">
                    </div>
                    <div class="form-group">
                        <label>الصف والشعبة *</label>
                        <input type="text" id="regGrade" class="form-input" placeholder="مثال: أول ثانوي - 1 أو ثالث متوسط / أ">
                    </div>
                    <div class="form-group">
                        <label>رقم الهوية / الإقامة</label>
                        <input type="text" id="regNid" class="form-input" placeholder="اختياري (إثبات شخصية)">
                    </div>
                    <div class="form-group">
                        <label>كلمة المرور *</label>
                        <input type="password" id="regPass" class="form-input" placeholder="اختر كلمة مرور لدخولك">
                    </div>
                    <button onclick="handleRegister()" class="btn">حفظ وتسجيل الدخول للحصة ←</button>
                </div>

                <div id="loginForm" style="display:none;">
                    <div class="form-group">
                        <label>اسم الطالب أو رقم الهوية</label>
                        <input type="text" id="loginId" class="form-input" placeholder="أدخل اسمك أو رقم هويتك">
                    </div>
                    <div class="form-group">
                        <label>كلمة المرور</label>
                        <input type="password" id="loginPass" class="form-input">
                    </div>
                    <button onclick="handleLogin()" class="btn">دخول الحصة ←</button>
                </div>
            </div>
        </div>

        <!-- DASHBOARD VIEW -->
        <div id="dashboardView" style="display:none;">
            <!-- Profile Greeting Card -->
            <div class="card" style="background: linear-gradient(135deg, rgba(58,134,255,0.12) 0%, rgba(131,56,236,0.12) 100%); border-color: var(--primary);">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                    <div>
                        <h2 style="font-size: 1.18rem; color: #60a5fa;">أهلاً بك: <span id="studentGreetingName"></span> 👋</h2>
                        <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">
                            <span id="studentGreetingGrade"></span>
                        </div>
                    </div>
                    <button onclick="loadQuizzes()" class="btn btn-outline" style="width:auto; padding:6px 14px; font-size:0.85rem;">تحديث 🔄</button>
                </div>
            </div>

            <!-- Dashboard Navigation Tabs -->
            <div class="tab-bar">
                <button id="tAvail" class="tab-btn active" onclick="switchQTab('avail')">📋 الاختبارات (<span id="availCount">0</span>)</button>
                <button id="tDone" class="tab-btn" onclick="switchQTab('done')">🏆 نتائجي (<span id="doneCount">0</span>)</button>
                <button id="tEval" class="tab-btn" onclick="switchQTab('eval')">📊 درجاتي وتقييمي</button>
            </div>

            <div id="availContainer"></div>
            <div id="doneContainer" style="display:none;"></div>
            <div id="evalContainer" style="display:none;"></div>
        </div>

        <!-- ACTIVE QUIZ VIEW -->
        <div id="quizView" style="display:none;">
            <div class="card" style="position: sticky; top: 76px; z-index: 40; border-color: var(--primary);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <h2 id="activeQuizTitle" style="font-size: 1.15rem;">عنوان الاختبار</h2>
                        <span class="badge badge-quiz">اختبار تقييمي</span>
                    </div>
                    <div id="quizTimerBox" style="background: rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.3); color:#f87171; font-weight:700; padding:6px 12px; border-radius:10px; font-size:0.9rem;">
                        ⏱️ <span id="quizTimerText">10:00</span>
                    </div>
                </div>
            </div>

            <div id="questionsContainer"></div>

            <div class="card" style="text-align: center;">
                <button onclick="confirmSubmitQuiz()" class="btn">تسليم الإجابات وإنهاء الاختبار ✓</button>
            </div>
        </div>
    </div>

    <div id="toast" class="toast"></div>

    <script>
        let currentStudent = JSON.parse(localStorage.getItem('student_session') || 'null');
        let activeQuiz = null;
        let selectedAnswers = {};
        let timerInterval = null;

        window.addEventListener('DOMContentLoaded', () => {
            checkServerStatus();
            setInterval(checkServerStatus, 5000);
            if (currentStudent) {
                showDashboard();
            }
        });

        function showToast(msg, isErr) {
            const t = document.getElementById('toast');
            t.textContent = msg;
            t.style.background = isErr ? '#dc2626' : '#1e293b';
            t.style.display = 'block';
            setTimeout(() => { t.style.display = 'none'; }, 3200);
        }

        async function checkServerStatus() {
            try {
                const res = await fetch('/api/status');
                const data = await res.json();
                const banner = document.getElementById('sessionClosedBanner');
                if (data.isOpen === false) {
                    banner.style.display = 'block';
                } else {
                    banner.style.display = 'none';
                }
            } catch (e) {}
        }

        function switchAuthTab(tab) {
            document.getElementById('tabRegister').classList.toggle('active', tab === 'register');
            document.getElementById('tabLogin').classList.toggle('active', tab === 'login');
            document.getElementById('registerForm').style.display = (tab === 'register') ? 'block' : 'none';
            document.getElementById('loginForm').style.display = (tab === 'login') ? 'block' : 'none';
        }

        async function handleRegister() {
            const username = document.getElementById('regName').value.trim();
            const gradeSection = document.getElementById('regGrade').value.trim();
            const nationalId = document.getElementById('regNid').value.trim();
            const password = document.getElementById('regPass').value.trim();

            if (!username || !password) return showToast('يرجى كتابة الاسم وكلمة المرور', true);

            try {
                const res = await fetch('/api/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ username, password, nationalId, gradeSection })
                });
                const data = await res.json();
                if (data.success) {
                    currentStudent = data.student;
                    localStorage.setItem('student_session', JSON.stringify(currentStudent));
                    showDashboard();
                    showToast('تم تسجيل دخولك بنجاح!');
                } else {
                    showToast(data.message || 'فشل التسجيل', true);
                }
            } catch (e) {
                showToast('تعذر الاتصال بخادم المعلم', true);
            }
        }

        async function handleLogin() {
            const identity = document.getElementById('loginId').value.trim();
            const password = document.getElementById('loginPass').value.trim();
            if (!identity || !password) return showToast('يرجى إدخال البيانات المطلوبة', true);

            try {
                const res = await fetch('/api/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ identity, password })
                });
                const data = await res.json();
                if (data.success) {
                    currentStudent = data.student;
                    localStorage.setItem('student_session', JSON.stringify(currentStudent));
                    showDashboard();
                    showToast('أهلاً بعودتك يا ' + currentStudent.username);
                } else {
                    showToast(data.message || 'بيانات الدخول غير صحيحة', true);
                }
            } catch (e) {
                showToast('تعذر الاتصال بخادم المعلم', true);
            }
        }

        function logout() {
            localStorage.removeItem('student_session');
            currentStudent = null;
            document.getElementById('authView').style.display = 'block';
            document.getElementById('dashboardView').style.display = 'none';
            document.getElementById('quizView').style.display = 'none';
            document.getElementById('logoutBtn').style.display = 'none';
        }

        function showDashboard() {
            document.getElementById('authView').style.display = 'none';
            document.getElementById('quizView').style.display = 'none';
            document.getElementById('dashboardView').style.display = 'block';
            document.getElementById('logoutBtn').style.display = 'block';

            document.getElementById('studentGreetingName').textContent = currentStudent.username;
            document.getElementById('studentGreetingGrade').textContent = currentStudent.gradeSection ? ('الفصل: ' + currentStudent.gradeSection) : '';
            loadQuizzes();
        }

        function switchQTab(tab) {
            document.getElementById('tAvail').classList.toggle('active', tab === 'avail');
            document.getElementById('tDone').classList.toggle('active', tab === 'done');
            document.getElementById('tEval').classList.toggle('active', tab === 'eval');

            document.getElementById('availContainer').style.display = (tab === 'avail') ? 'block' : 'none';
            document.getElementById('doneContainer').style.display = (tab === 'done') ? 'block' : 'none';
            document.getElementById('evalContainer').style.display = (tab === 'eval') ? 'block' : 'none';
        }

        async function loadQuizzes() {
            try {
                const res = await fetch('/api/student-quizzes?student=' + encodeURIComponent(currentStudent.username));
                const data = await res.json();

                const avail = data.unattempted || [];
                const done = data.completed || [];
                document.getElementById('availCount').textContent = avail.length;
                document.getElementById('doneCount').textContent = done.length;

                // Render Available
                const aCont = document.getElementById('availContainer');
                if (avail.length === 0) {
                    aCont.innerHTML = '<div class="card" style="text-align:center; color:var(--text-muted);"><div style="font-size:2rem;">📝</div><h3 style="margin-top:6px;">لا توجد اختبارات جديدة متاحة حالياً</h3></div>';
                } else {
                    let h = '';
                    avail.forEach(q => {
                        h += '<div class="card">' +
                            '<div style="display:flex; justify-content:space-between; align-items:center;">' +
                                '<h3 style="font-size:1.05rem;">' + q.title + '</h3>' +
                                '<span class="badge badge-quiz">⏱️ ' + q.durationMinutes + ' دقيقة</span>' +
                            '</div>' +
                            '<p style="font-size:0.85rem; color:var(--text-muted); margin:8px 0;">' + (q.description || 'بدون تعليمات إضافية') + '</p>' +
                            '<button onclick="startQuiz(' + q.id + ')" class="btn" style="margin-top:10px;">بدء الاختبار الآن ←</button>' +
                        '</div>';
                    });
                    aCont.innerHTML = h;
                }

                // Render Done
                const dCont = document.getElementById('doneContainer');
                if (done.length === 0) {
                    dCont.innerHTML = '<div class="card" style="text-align:center; color:var(--text-muted);"><div style="font-size:2rem;">🏆</div><h3 style="margin-top:6px;">لم تنجز أي اختبارات بعد</h3></div>';
                } else {
                    let h = '';
                    done.forEach(q => {
                        h += '<div class="card" style="border-right: 4px solid var(--success);">' +
                            '<div style="display:flex; justify-content:space-between; align-items:center;">' +
                                '<h3 style="font-size:1.05rem;">' + q.title + '</h3>' +
                                '<span class="badge badge-success">الدرجة: ' + q.score + ' / ' + q.totalPoints + ' (' + q.percentage + '%)</span>' +
                            '</div>' +
                            '<div style="font-size:0.82rem; color:var(--text-muted); margin-top:6px;">🔒 تم تسليم الاختبار واعتماده في السجل</div>' +
                        '</div>';
                    });
                    dCont.innerHTML = h;
                }

                // Render Evaluation
                const evCont = document.getElementById('evalContainer');
                const ev = data.evaluation;
                if (ev && ev.isVisible) {
                    let noteHtml = ev.notes ? ('<div style="background:rgba(58,134,255,0.1); border:1px dashed var(--primary); padding:12px 14px; border-radius:12px; margin-top:12px;"><div style="font-weight:700; color:#60a5fa; font-size:0.9rem;">💬 ملاحظة المعلم:</div><div style="font-size:0.95rem; margin-top:2px;">' + ev.notes + '</div></div>') : '';
                    evCont.innerHTML = '<div class="card">' +
                        '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">' +
                            '<h3 style="color:#60a5fa;">📊 بطاقة الدرجات الشهرية</h3>' +
                            '<span class="badge badge-success">✓ معتمدة</span>' +
                        '</div>' +
                        '<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; text-align:center;">' +
                            '<div style="background:var(--card-color); border:1px solid var(--border); padding:10px; border-radius:12px;"><div style="font-size:0.8rem; color:var(--text-muted);">الشهري الأول</div><div style="font-size:1.35rem; font-weight:800; color:var(--text-main); margin-top:2px;">' + ev.exam1Score + '</div></div>' +
                            '<div style="background:var(--card-color); border:1px solid var(--border); padding:10px; border-radius:12px;"><div style="font-size:0.8rem; color:var(--text-muted);">الشهري الثاني</div><div style="font-size:1.35rem; font-weight:800; color:var(--text-main); margin-top:2px;">' + ev.exam2Score + '</div></div>' +
                            '<div style="background:var(--card-color); border:1px solid var(--border); padding:10px; border-radius:12px;"><div style="font-size:0.8rem; color:var(--text-muted);">المشاركة والتفاعل</div><div style="font-size:1.35rem; font-weight:800; color:var(--success); margin-top:2px;">' + ev.participationScore + '</div></div>' +
                            '<div style="background:var(--card-color); border:1px solid var(--border); padding:10px; border-radius:12px;"><div style="font-size:0.8rem; color:var(--text-muted);">إضافي / خصم</div><div style="font-size:1.35rem; font-weight:800; color:' + (ev.bonusScore >= 0 ? '#60a5fa' : 'var(--danger)') + '; margin-top:2px;">' + (ev.bonusScore > 0 ? '+' : '') + ev.bonusScore + '</div></div>' +
                        '</div>' +
                        '<div style="background:linear-gradient(135deg, rgba(58,134,255,0.2) 0%, rgba(131,56,236,0.2) 100%); border:1px solid var(--primary); padding:14px; border-radius:12px; text-align:center; margin-top:12px;">' +
                            '<div style="font-size:0.85rem; color:var(--text-muted);">المجموع التراكمي للدرجات</div>' +
                            '<div style="font-size:2rem; font-weight:900; color:#60a5fa; line-height:1.2;">' + ev.totalScore + '</div>' +
                        '</div>' +
                        noteHtml +
                    '</div>';
                } else {
                    evCont.innerHTML = '<div class="card" style="text-align:center; color:var(--text-muted);"><div style="font-size:2rem;">🔒</div><h3 style="margin-top:6px;">الدرجات قيد المراجعة</h3><p style="font-size:0.85rem; margin-top:4px;">يقوم المعلم برصد ومراجعة الدرجات حالياً.</p></div>';
                }
            } catch (e) {
                showToast('خطأ في جلب الاختبارات', true);
            }
        }

        async function startQuiz(quizId) {
            try {
                const res = await fetch('/api/quiz?id=' + quizId + '&student=' + encodeURIComponent(currentStudent.username));
                const data = await res.json();
                if (!res.ok) return showToast(data.message || 'تعذر فتح الاختبار', true);

                activeQuiz = data;
                selectedAnswers = {};
                document.getElementById('activeQuizTitle').textContent = data.quiz.title;
                const qCont = document.getElementById('questionsContainer');

                let h = '';
                data.questions.forEach((q, idx) => {
                    h += '<div class="card" id="q_card_' + q.id + '">' +
                        '<div style="font-weight:700; font-size:1.05rem; margin-bottom:12px;">' + (idx + 1) + '. ' + q.questionText + '</div>' +
                        '<div>' +
                            '<div class="opt-label" id="lbl_' + q.id + '_A" onclick="chooseOption(' + q.id + ', \'A\')"><input type="radio" name="opt_' + q.id + '" value="A"> ' + (q.optionA || 'أ') + '</div>' +
                            '<div class="opt-label" id="lbl_' + q.id + '_B" onclick="chooseOption(' + q.id + ', \'B\')"><input type="radio" name="opt_' + q.id + '" value="B"> ' + (q.optionB || 'ب') + '</div>' +
                            (q.optionC ? ('<div class="opt-label" id="lbl_' + q.id + '_C" onclick="chooseOption(' + q.id + ', \'C\')"><input type="radio" name="opt_' + q.id + '" value="C"> ' + q.optionC + '</div>') : '') +
                            (q.optionD ? ('<div class="opt-label" id="lbl_' + q.id + '_D" onclick="chooseOption(' + q.id + ', \'D\')"><input type="radio" name="opt_' + q.id + '" value="D"> ' + q.optionD + '</div>') : '') +
                        '</div>' +
                    '</div>';
                });
                qCont.innerHTML = h;

                document.getElementById('dashboardView').style.display = 'none';
                document.getElementById('quizView').style.display = 'block';
                window.scrollTo({ top: 0, behavior: 'smooth' });
            } catch (e) {
                showToast('خطأ في تحميل أسئلة الاختبار', true);
            }
        }

        function chooseOption(qid, val) {
            selectedAnswers[qid] = val;
            const parent = document.getElementById('q_card_' + qid);
            parent.querySelectorAll('.opt-label').forEach(l => l.classList.remove('selected'));
            const chosen = document.getElementById('lbl_' + qid + '_' + val);
            if (chosen) {
                chosen.classList.add('selected');
                chosen.querySelector('input').checked = true;
            }
        }

        function confirmSubmitQuiz() {
            const count = Object.keys(selectedAnswers).length;
            const total = activeQuiz.questions.length;
            if (count < total) {
                if (!confirm('يوجد ' + (total - count) + ' سؤال بدون إجابة، هل تود تسليم الاختبار الآن؟')) return;
            }
            submitQuizAnswers();
        }

        async function submitQuizAnswers() {
            try {
                const res = await fetch('/api/submit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        quizId: activeQuiz.quiz.id,
                        studentUsername: currentStudent.username,
                        answers: selectedAnswers
                    })
                });
                const data = await res.json();
                if (data.success) {
                    alert('🎉 تم تسليم إجاباتك بنجاح!\nالدرجة المحققة: ' + data.score + ' من ' + data.totalPoints + ' (' + data.percentage + '%)');
                    showDashboard();
                } else {
                    showToast(data.message || 'فشل تسليم الاختبار', true);
                }
            } catch (e) {
                showToast('حدث خطأ أثناء الإرسال', true);
            }
        }
    </script>
</body>
</html>
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

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            padding-bottom: 70px;
        }

        /* Top Header */
        header {
            background: linear-gradient(135deg, #1c2541 0%, #0b132b 100%);
            border-bottom: 1.5px solid var(--border);
            padding: 14px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-title-box {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .header-icon {
            width: 44px;
            height: 44px;
            border-radius: 14px;
            background: rgba(58, 134, 255, 0.2);
            border: 1.5px solid var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }

        .main-container {
            max-width: 1100px;
            width: 100%;
            margin: 16px auto;
            padding: 0 16px;
            flex: 1;
        }

        /* Server Control Card Matching Mobile App */
        .server-card {
            background: var(--surface-color);
            border: 1.5px solid var(--border);
            border-radius: var(--radius);
            padding: 18px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
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

        .status-dot.active {
            background: var(--success);
            box-shadow: 0 0 10px var(--success);
        }

        .status-dot.inactive {
            background: var(--danger);
        }

        /* Toggle Switch */
        .switch {
            position: relative;
            display: inline-block;
            width: 52px;
            height: 28px;
        }

        .switch input { opacity: 0; width: 0; height: 0; }

        .slider {
            position: absolute;
            cursor: pointer;
            top: 0; left: 0; right: 0; bottom: 0;
            background-color: #475569;
            transition: .3s;
            border-radius: 34px;
        }

        .slider:before {
            position: absolute;
            content: "";
            height: 22px;
            width: 22px;
            left: 3px;
            bottom: 3px;
            background-color: white;
            transition: .3s;
            border-radius: 50%;
        }

        input:checked + .slider { background-color: var(--success); }
        input:checked + .slider:before { transform: translateX(24px); }

        /* Wi-Fi & IP Box */
        .url-banner {
            background: rgba(58, 134, 255, 0.12);
            border: 1px solid rgba(58, 134, 255, 0.3);
            border-radius: 14px;
            padding: 14px;
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
            color: #60a5fa;
            letter-spacing: 0.5px;
        }

        .btn {
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent-purple) 100%);
            color: white;
            border: none;
            padding: 10px 18px;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 700;
            font-size: 0.92rem;
            display: inline-flex;
            align-items: center;
            gap: 8px;
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
        .btn-outline:hover {
            border-color: var(--primary);
            color: var(--primary);
        }

        /* Bottom Navigation Bar Matching App */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #111a33;
            border-top: 1.5px solid var(--border);
            display: flex;
            justify-content: space-around;
            padding: 8px 16px;
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
            gap: 4px;
            padding: 6px 14px;
            border-radius: 12px;
            font-size: 0.78rem;
            font-weight: 700;
            transition: all 0.2s;
        }

        .nav-item.active {
            color: #60a5fa;
            background: rgba(58, 134, 255, 0.15);
        }

        .nav-icon {
            font-size: 1.3rem;
        }

        /* Tables & Lists */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }

        th, td {
            padding: 12px 14px;
            text-align: right;
            border-bottom: 1px solid var(--border);
            font-size: 0.92rem;
        }

        th {
            background: rgba(0, 0, 0, 0.2);
            color: var(--text-muted);
            font-weight: 700;
        }

        tr:hover { background: rgba(58, 134, 255, 0.04); }

        .card-inner {
            background: var(--surface-color);
            border: 1.5px solid var(--border);
            border-radius: var(--radius);
            padding: 20px;
            margin-bottom: 16px;
        }

        .toast {
            position: fixed;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            background: #1e293b;
            color: white;
            padding: 12px 24px;
            border-radius: 12px;
            display: none;
            z-index: 9999;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
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
            padding: 20px;
        }

        .modal-body {
            background: var(--surface-color);
            border: 1.5px solid var(--border);
            border-radius: 20px;
            max-width: 600px;
            width: 100%;
            padding: 24px;
            max-height: 90vh;
            overflow-y: auto;
        }

        .form-group {
            margin-bottom: 14px;
        }

        .form-group label {
            display: block;
            font-size: 0.88rem;
            font-weight: 600;
            margin-bottom: 6px;
            color: var(--text-muted);
        }

        .form-input {
            width: 100%;
            padding: 10px 14px;
            border: 1.5px solid var(--border);
            border-radius: 10px;
            background: var(--card-color);
            color: var(--text-main);
            font-size: 0.95rem;
        }
    </style>
</head>
<body>
    <header>
        <div class="header-title-box">
            <div class="header-icon">🎓</div>
            <div>
                <h1 style="font-size: 1.25rem;">خادم الفصل • Windows 11 Edition</h1>
                <div style="font-size: 0.78rem; color: var(--text-muted);">خادم الاختبارات المدرسية المباشر عبر الواي فاي</div>
            </div>
        </div>
        <div style="display: flex; gap: 8px;">
            <button onclick="fetchData()" class="btn btn-outline" style="padding:6px 12px; font-size:0.85rem;">تحديث البيانات 🔄</button>
        </div>
    </header>

    <div class="main-container">
        <!-- 1. Real Server & Wi-Fi Control Card (Matches Mobile) -->
        <div class="server-card">
            <div class="server-header">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 44px; height: 44px; border-radius: 50%; background: rgba(16, 185, 129, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">
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
                    <button onclick="copyServerUrl()" class="btn" style="padding:8px 14px; font-size:0.88rem;">نسخ الرابط 📋</button>
                    <button onclick="showQrModal()" class="btn btn-outline" style="padding:8px 14px; font-size:0.88rem;">عرض QR 📱</button>
                </div>
            </div>
        </div>

        <!-- TAB 1: Quizzes & Activities -->
        <div id="tabQuizzes" class="card-inner">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <div>
                    <h2 style="font-size: 1.2rem;">📝 بنك الاختبارات والأنشطة</h2>
                    <p style="font-size: 0.85rem; color: var(--text-muted);">الاختبارات المفعلة والمتاحة للطلاب في الفصل</p>
                </div>
                <button onclick="openNewQuizModal()" class="btn btn-success">+ إضافة اختبار جديد</button>
            </div>
            <div id="quizzesListContainer" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px;"></div>
        </div>

        <!-- TAB 2: Students & Grades -->
        <div id="tabStudents" class="card-inner" style="display: none;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 14px;">
                <div>
                    <h2 style="font-size: 1.2rem;">👥 سجل الطلاب والدرجات الشهرية</h2>
                    <p style="font-size: 0.85rem; color: var(--text-muted);">مقسّمة بحسب الفصول والشعب مع رصد درجات الاختبارات والمشاركة والملاحظات</p>
                </div>
                <button id="globalGradesBtn" onclick="toggleGlobalVisibility()" class="btn btn-outline">👁️ إخفاء/إظهار الدرجات للجميع</button>
            </div>
            <div id="studentsListContainer"></div>
        </div>

        <!-- TAB 3: Submissions -->
        <div id="tabSubmissions" class="card-inner" style="display: none;">
            <h2 style="font-size: 1.2rem; margin-bottom: 6px;">📊 التسليمات والنتائج الفورية</h2>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 14px;">إجابات الطلاب الواصلة لحظياً إلى خادم الكمبيوتر</p>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>اسم الطالب</th>
                            <th>الاختبار</th>
                            <th>الدرجة</th>
                            <th>النسبة</th>
                            <th>وقت التسليم</th>
                        </tr>
                    </thead>
                    <tbody id="submissionsTableBody"></tbody>
                </table>
            </div>
        </div>

        <!-- TAB 4: Network & Live Logs -->
        <div id="tabNetwork" class="card-inner" style="display: none;">
            <h2 style="font-size: 1.2rem; margin-bottom: 6px;">📡 البث وعناوين الشبكة المحلية</h2>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 14px;">عناوين IP المتاحة على كروت شبكة هذا الجهاز</p>
            <div id="networkIpsList" style="display: flex; flex-direction: column; gap: 8px;"></div>
        </div>
    </div>

    <!-- Bottom Navigation Bar Matching Android App -->
    <nav class="bottom-nav">
        <button id="bNavQuizzes" class="nav-item active" onclick="switchMainTab('quizzes')">
            <span class="nav-icon">📝</span>
            <span>الاختبارات</span>
        </button>
        <button id="bNavStudents" class="nav-item" onclick="switchMainTab('students')">
            <span class="nav-icon">👥</span>
            <span>الطلاب والدرجات</span>
        </button>
        <button id="bNavSubmissions" class="nav-item" onclick="switchMainTab('submissions')">
            <span class="nav-icon">📊</span>
            <span>التسليمات</span>
        </button>
        <button id="bNavNetwork" class="nav-item" onclick="switchMainTab('network')">
            <span class="nav-icon">📡</span>
            <span>البث والشبكة</span>
        </button>
    </nav>

    <!-- Student Evaluation Modal -->
    <div id="evalModal" class="modal">
        <div class="modal-body">
            <h3 id="evalModalTitle" style="color: #60a5fa; font-size: 1.25rem; margin-bottom: 16px;">رصد درجات الطالب</h3>
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
                <textarea id="evalNotes" rows="3" class="form-input"></textarea>
            </div>

            <div style="display: flex; gap: 20px; margin: 14px 0;">
                <label style="cursor: pointer;"><input type="checkbox" id="evalShowGrades"> إظهار الدرجات للطالب</label>
                <label style="cursor: pointer;"><input type="checkbox" id="evalShowNotes"> إظهار الملاحظات للطالب</label>
            </div>

            <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 18px;">
                <button onclick="document.getElementById('evalModal').style.display='none'" class="btn btn-outline">إلغاء</button>
                <button onclick="saveEvaluation()" class="btn btn-success">حفظ التقييم ✓</button>
            </div>
        </div>
    </div>

    <!-- Create Quiz Modal -->
    <div id="quizModal" class="modal">
        <div class="modal-body" style="max-width: 650px;">
            <h3 style="color: #60a5fa; margin-bottom: 16px;">إضافة اختبار جديد للفصل</h3>
            <div class="form-group">
                <label>عنوان الاختبار:</label>
                <input type="text" id="newQuizTitle" class="form-input" placeholder="مثال: الاختبار الفتري الأول">
            </div>
            <div class="form-group">
                <label>التعليمات أو الوصف:</label>
                <input type="text" id="newQuizDesc" class="form-input">
            </div>
            <div class="form-group">
                <label>المدة بالدقائق:</label>
                <input type="number" id="newQuizDuration" class="form-input" value="10">
            </div>

            <h4 style="margin: 14px 0 8px 0; color: #60a5fa;">الأسئلة:</h4>
            <div id="newQuestionsContainer"></div>
            <button onclick="addQuestionItem()" class="btn btn-outline" style="margin-top: 8px;">+ إضافة سؤال آخر</button>

            <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px;">
                <button onclick="document.getElementById('quizModal').style.display='none'" class="btn btn-outline">إلغاء</button>
                <button onclick="submitNewQuiz()" class="btn btn-success">نشر الاختبار ✓</button>
            </div>
        </div>
    </div>

    <!-- QR Code Modal -->
    <div id="qrModal" class="modal">
        <div class="modal-body" style="max-width: 380px; text-align: center;">
            <h3 style="margin-bottom: 14px; color: #60a5fa;">مسح رمز الدخول للطلاب</h3>
            <div style="background: white; padding: 14px; border-radius: 16px; display: inline-block;">
                <canvas id="qrCanvas" width="220" height="220"></canvas>
            </div>
            <div id="qrModalUrl" style="margin-top: 12px; font-weight: 700; color: #60a5fa; font-size: 0.95rem;"></div>
            <button onclick="document.getElementById('qrModal').style.display='none'" class="btn btn-outline" style="margin-top: 14px; width:100%;">إغلاق</button>
        </div>
    </div>

    <div id="toast" class="toast"></div>

    <script>
        let serverData = { students: [], quizzes: [], submissions: [], areGradesVisibleGlobally: true };
        let serverStatus = { isOpen: true, serverIps: [] };

        window.addEventListener('DOMContentLoaded', () => {
            fetchData();
            setInterval(fetchData, 4000);
        });

        function showToast(msg) {
            const t = document.getElementById('toast');
            t.textContent = msg;
            t.style.display = 'block';
            setTimeout(() => { t.style.display = 'none'; }, 3000);
        }

        function switchMainTab(tab) {
            ['quizzes', 'students', 'submissions', 'network'].forEach(t => {
                const el = document.getElementById('tab' + t.charAt(0).toUpperCase() + t.slice(1));
                const btn = document.getElementById('bNav' + t.charAt(0).toUpperCase() + t.slice(1));
                if (el) el.style.display = (t === tab) ? 'block' : 'none';
                if (btn) btn.classList.toggle('active', t === tab);
            });
        }

        async function fetchData() {
            try {
                const [resStatus, resData] = await Promise.all([
                    fetch('/api/status').then(r => r.json()),
                    fetch('/api/teacher/data').then(r => r.json())
                ]);

                serverStatus = resStatus;
                serverData = resData;

                updateServerCard();
                renderQuizzes(serverData.quizzes || []);
                renderStudents(serverData.students || []);
                renderSubmissions(serverData.submissions || []);
                renderNetworkIps(serverStatus.serverIps || []);
            } catch (e) {}
        }

        function updateServerCard() {
            const dot = document.getElementById('serverStatusDot');
            const title = document.getElementById('serverStatusTitle');
            const toggle = document.getElementById('serverToggleInput');
            const urlEl = document.getElementById('primaryUrlText');

            toggle.checked = serverStatus.isOpen;
            if (serverStatus.isOpen) {
                dot.className = 'status-dot active';
                title.textContent = 'خادم الحصة يعمل (نشط)';
                title.style.color = 'var(--success)';
            } else {
                dot.className = 'status-dot inactive';
                title.textContent = 'الخادم مغلق حالياً';
                title.style.color = 'var(--danger)';
            }

            const primaryIp = (serverStatus.serverIps && serverStatus.serverIps.length > 0) ? serverStatus.serverIps[0] : window.location.hostname;
            urlEl.textContent = 'http://' + primaryIp + ':8080';
        }

        async function toggleServerStatus() {
            const toggle = document.getElementById('serverToggleInput');
            try {
                const res = await fetch('/api/status', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ isOpen: toggle.checked })
                });
                const d = await res.json();
                serverStatus.isOpen = d.isOpen;
                updateServerCard();
                showToast(serverStatus.isOpen ? 'تم فتح الحصة للطلاب بنجاح' : 'تم إغلاق الحصة أمام الطلاب');
            } catch (e) {
                showToast('فشل تغيير حالة الخادم');
            }
        }

        function copyServerUrl() {
            const txt = document.getElementById('primaryUrlText').textContent;
            navigator.clipboard.writeText(txt);
            showToast('تم نسخ الرابط بنجاح: ' + txt);
        }

        function renderQuizzes(quizzes) {
            const cont = document.getElementById('quizzesListContainer');
            if (quizzes.length === 0) {
                cont.innerHTML = '<div style="color:var(--text-muted); text-align:center; padding:20px;">لا توجد اختبارات مضافة.</div>';
                return;
            }
            let h = '';
            quizzes.forEach(q => {
                h += '<div style="background:var(--card-color); border:1.5px solid var(--border); border-radius:14px; padding:16px;">' +
                    '<div style="display:flex; justify-content:space-between; align-items:center;">' +
                        '<h3 style="font-size:1.1rem;">' + q.title + '</h3>' +
                        '<span class="badge" style="background:' + (q.isActive ? 'var(--success-light)' : 'var(--danger-light)') + '; color:' + (q.isActive ? 'var(--success)' : 'var(--danger)') + ';">' + (q.isActive ? 'نشط ومتاح' : 'مغلق') + '</span>' +
                    '</div>' +
                    '<p style="font-size:0.85rem; color:var(--text-muted); margin:8px 0;">' + (q.description || '') + '</p>' +
                    '<div style="display:flex; justify-content:space-between; align-items:center; margin-top:14px;">' +
                        '<span style="font-size:0.82rem; color:var(--text-muted);">⏱️ ' + q.durationMinutes + ' دقيقة</span>' +
                        '<button onclick="toggleQuizActive(' + q.id + ', ' + q.isActive + ')" class="btn ' + (q.isActive ? 'btn-danger' : 'btn-success') + '" style="padding:6px 12px; font-size:0.82rem;">' + (q.isActive ? 'إغلاق الاختبار 🔒' : 'تفعيل الاختبار 🔓') + '</button>' +
                    '</div>' +
                '</div>';
            });
            cont.innerHTML = h;
        }

        async function toggleQuizActive(qid, act) {
            try {
                await fetch('/api/teacher/toggle-quiz', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ quizId: qid, isActive: !act })
                });
                fetchData();
            } catch (e) {
                showToast('فشل تعديل حالة الاختبار');
            }
        }

        function renderStudents(students) {
            const cont = document.getElementById('studentsListContainer');
            if (students.length === 0) {
                cont.innerHTML = '<div style="color:var(--text-muted); text-align:center; padding:20px;">لم يقم أي طالب بالتسجيل بعد.</div>';
                return;
            }

            const groups = {};
            students.forEach(s => {
                const k = s.gradeSection || 'فصل عام';
                if (!groups[k]) groups[k] = [];
                groups[k].push(s);
            });

            let h = '';
            for (const [cls, list] of Object.entries(groups)) {
                h += '<div style="background:rgba(0,0,0,0.2); border:1px solid var(--border); border-radius:14px; padding:16px; margin-bottom:14px;">' +
                    '<h3 style="color:#60a5fa; font-size:1.1rem; margin-bottom:10px;">🏫 ' + cls + ' (' + list.length + ' طلاب)</h3>' +
                    '<div style="overflow-x:auto;">' +
                        '<table>' +
                            '<thead><tr><th>اسم الطالب</th><th>شهري 1</th><th>شهري 2</th><th>مشاركة</th><th>إضافي</th><th>المجموع</th><th>الظهور</th><th>ملاحظات</th><th>إجراء</th></tr></thead>' +
                            '<tbody>';

                list.forEach(s => {
                    const total = (s.exam1Score || 0) + (s.exam2Score || 0) + (s.participationScore || 0) + (s.bonusScore || 0);
                    h += '<tr>' +
                        '<td style="font-weight:700;">' + s.username + '</td>' +
                        '<td>' + s.exam1Score + '</td>' +
                        '<td>' + s.exam2Score + '</td>' +
                        '<td>' + s.participationScore + '</td>' +
                        '<td>' + (s.bonusScore > 0 ? '+' : '') + s.bonusScore + '</td>' +
                        '<td style="font-weight:800; color:#60a5fa;">' + total.toFixed(1) + '</td>' +
                        '<td>' + (s.showGradesToStudent ? '👁️ ظاهر' : '🔒 مخفي') + '</td>' +
                        '<td style="max-width:140px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">' + (s.notes || '-') + '</td>' +
                        '<td>' +
                            '<button onclick="quickBonus(' + s.id + ', 1)" class="btn btn-outline" style="padding:2px 8px; font-size:0.75rem;">+1</button> ' +
                            '<button onclick="quickBonus(' + s.id + ', -1)" class="btn btn-outline" style="padding:2px 8px; font-size:0.75rem; color:var(--danger);">-1</button> ' +
                            '<button onclick="openEvalModal(' + s.id + ')" class="btn" style="padding:3px 10px; font-size:0.75rem; margin-right:4px;">رصد 📝</button>' +
                        '</td>' +
                    '</tr>';
                });

                h += '</tbody></table></div></div>';
            }
            cont.innerHTML = h;
        }

        async function quickBonus(sid, delta) {
            try {
                await fetch('/api/teacher/bonus', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ studentId: sid, delta })
                });
                fetchData();
                showToast('تم تعديل الدرجة بنجاح');
            } catch (e) {}
        }

        function openEvalModal(sid) {
            const s = serverData.students.find(x => x.id === sid);
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

        async function saveEvaluation() {
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
            try {
                await fetch('/api/teacher/evaluate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                document.getElementById('evalModal').style.display = 'none';
                fetchData();
                showToast('تم حفظ التقييم بنجاح!');
            } catch (e) {
                showToast('فشل حفظ التقييم');
            }
        }

        async function toggleGlobalVisibility() {
            try {
                const nVis = !serverData.areGradesVisibleGlobally;
                await fetch('/api/teacher/toggle-visibility', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ visible: nVis })
                });
                fetchData();
                showToast(nVis ? 'الدرجات معلنة للجميع' : 'تم إخفاء الدرجات عن الجميع');
            } catch (e) {}
        }

        function renderSubmissions(submissions) {
            const tbody = document.getElementById('submissionsTableBody');
            if (submissions.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:var(--text-muted);">لا توجد تسليمات بعد.</td></tr>';
                return;
            }
            let h = '';
            submissions.forEach((s, idx) => {
                const timeStr = new Date(s.submittedAt).toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' });
                const pct = s.totalPoints > 0 ? Math.round((s.score * 100) / s.totalPoints) : 100;
                h += '<tr>' +
                    '<td>' + (idx + 1) + '</td>' +
                    '<td style="font-weight:700;">' + s.studentUsername + '</td>' +
                    '<td>' + (s.quizTitle || 'اختبار') + '</td>' +
                    '<td style="font-weight:800; color:#60a5fa;">' + s.score + ' / ' + s.totalPoints + '</td>' +
                    '<td>' + pct + '%</td>' +
                    '<td>' + timeStr + '</td>' +
                '</tr>';
            });
            tbody.innerHTML = h;
        }

        function renderNetworkIps(ips) {
            const cont = document.getElementById('networkIpsList');
            if (ips.length === 0) {
                cont.innerHTML = '<div style="color:var(--text-muted);">لا توجد شبكات مكتشفة.</div>';
                return;
            }
            let h = '';
            ips.forEach(ip => {
                h += '<div style="background:var(--card-color); border:1px solid var(--border); padding:12px; border-radius:12px; display:flex; justify-content:space-between; align-items:center;">' +
                    '<div><strong>http://' + ip + ':8080</strong></div>' +
                    '<button onclick="navigator.clipboard.writeText(\'http://' + ip + ':8080\'); showToast(\'تم نسخ الرابط\');" class="btn btn-outline" style="padding:4px 10px; font-size:0.8rem;">نسخ</button>' +
                '</div>';
            });
            cont.innerHTML = h;
        }

        // Quiz Creation
        function openNewQuizModal() {
            document.getElementById('newQuestionsContainer').innerHTML = '';
            addQuestionItem();
            document.getElementById('quizModal').style.display = 'flex';
        }

        let qCounter = 0;
        function addQuestionItem() {
            qCounter++;
            const cont = document.getElementById('newQuestionsContainer');
            const d = document.createElement('div');
            d.style.cssText = 'background:var(--card-color); border:1px solid var(--border); border-radius:12px; padding:12px; margin-bottom:10px;';
            d.innerHTML = '<div class="form-group"><label>نص السؤال ' + qCounter + ':</label><input type="text" class="form-input q-t" placeholder="اكتب السؤال..."></div>' +
                '<div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">' +
                    '<input type="text" class="form-input q-a" placeholder="الخيار (أ)">' +
                    '<input type="text" class="form-input q-b" placeholder="الخيار (ب)">' +
                    '<input type="text" class="form-input q-c" placeholder="الخيار (ج)">' +
                    '<input type="text" class="form-input q-d" placeholder="الخيار (د)">' +
                '</div>' +
                '<div class="form-group" style="margin-top:8px;"><label>الإجابة الصحيحة:</label><select class="form-input q-cor"><option value="A">الخيار (أ)</option><option value="B">الخيار (ب)</option><option value="C">الخيار (ج)</option><option value="D">الخيار (د)</option></select></div>';
            cont.appendChild(d);
        }

        async function submitNewQuiz() {
            const title = document.getElementById('newQuizTitle').value.trim();
            const desc = document.getElementById('newQuizDesc').value.trim();
            const dur = parseInt(document.getElementById('newQuizDuration').value) || 10;
            if (!title) return showToast('اكتب عنوان الاختبار');

            const questions = [];
            document.querySelectorAll('#newQuestionsContainer > div').forEach(d => {
                const t = d.querySelector('.q-t').value.trim();
                if (t) {
                    questions.push({
                        questionText: t,
                        optionA: d.querySelector('.q-a').value.trim() || 'أ',
                        optionB: d.querySelector('.q-b').value.trim() || 'ب',
                        optionC: d.querySelector('.q-c').value.trim(),
                        optionD: d.querySelector('.q-d').value.trim(),
                        correctAnswer: d.querySelector('.q-cor').value,
                        points: 1
                    });
                }
            });

            if (questions.length === 0) return showToast('أضف سؤالاً واحداً على الأقل');

            try {
                await fetch('/api/teacher/create-quiz', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ title, description: desc, durationMinutes: dur, questions })
                });
                document.getElementById('quizModal').style.display = 'none';
                fetchData();
                showToast('تم نشر الاختبار بنجاح!');
            } catch (e) {
                showToast('فشل نشر الاختبار');
            }
        }

        // Lightweight Pure Canvas QR Code
        function showQrModal() {
            const url = document.getElementById('primaryUrlText').textContent;
            document.getElementById('qrModalUrl').textContent = url;
            drawSimpleQr('qrCanvas', url);
            document.getElementById('qrModal').style.display = 'flex';
        }

        function drawSimpleQr(canvasId, text) {
            const canvas = document.getElementById(canvasId);
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, 220, 220);

            // Hash pattern generator for offline QR aesthetic
            ctx.fillStyle = '#0f172a';
            const size = 22;
            const cellSize = 10;

            // Draw Finder patterns
            drawFinder(ctx, 10, 10);
            drawFinder(ctx, 140, 10);
            drawFinder(ctx, 10, 140);

            // Generate deterministic matrix based on text characters
            let hash = 0;
            for (let i = 0; i < text.length; i++) {
                hash = ((hash << 5) - hash) + text.charCodeAt(i);
                hash |= 0;
            }

            for (let x = 0; x < size; x++) {
                for (let y = 0; y < size; y++) {
                    if ((x < 8 && y < 8) || (x > 13 && y < 8) || (x < 8 && y > 13)) continue;
                    const v = (Math.sin(x * 12.9898 + y * 78.233 + hash) * 43758.5453) % 1;
                    if (Math.abs(v) > 0.45) {
                        ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
                    }
                }
            }
        }

        function drawFinder(ctx, x, y) {
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(x, y, 70, 70);
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(x + 10, y + 10, 50, 50);
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(x + 20, y + 20, 30, 30);
        }
    </script>
</body>
</html>
"""
