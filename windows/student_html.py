# -*- coding: utf-8 -*-
r"""
Student Web Portal HTML Template for Windows 11 Classroom Server
Supports Student Onboarding (Grade & Section selection), Targeted Quizzes, and Dark UI
"""

STUDENT_HTML = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>بوابة اختبارات الحصة الذكية</title>
    <style>
        :root {
            --bg: #0b132b;
            --surface: #1c2541;
            --card: #243054;
            --primary: #3a86ff;
            --primary-light: rgba(58, 134, 255, 0.15);
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
            --radius: 16px;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }
        body { background-color: var(--bg); color: var(--text-main); min-height: 100vh; padding-bottom: 30px; }
        header { background: linear-gradient(135deg, #1c2541 0%, #0b132b 100%); border-bottom: 1.5px solid var(--border); padding: 14px 20px; position: sticky; top: 0; z-index: 50; }
        .header-content { max-width: 680px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
        .container { max-width: 680px; margin: 16px auto; padding: 0 16px; }
        .card { background: var(--surface); border: 1.5px solid var(--border); border-radius: var(--radius); padding: 18px; margin-bottom: 14px; box-shadow: 0 4px 15px rgba(0,0,0,0.25); }
        .tab-bar { display: flex; background: rgba(0,0,0,0.3); padding: 4px; border-radius: 12px; margin-bottom: 16px; border: 1px solid var(--border); gap: 4px; }
        .tab-btn { flex: 1; padding: 10px; border: none; background: transparent; color: var(--text-muted); border-radius: 9px; font-size: 0.92rem; font-weight: 700; cursor: pointer; transition: all 0.2s; }
        .tab-btn.active { background: var(--primary); color: white; }
        .form-group { margin-bottom: 14px; }
        .form-group label { display: block; font-size: 0.86rem; font-weight: 600; margin-bottom: 6px; color: var(--text-muted); }
        .form-input { width: 100%; padding: 12px 14px; border: 1.5px solid var(--border); border-radius: 11px; font-size: 0.95rem; background: var(--card); color: var(--text-main); }
        .form-input:focus { outline: none; border-color: var(--primary); }
        select.form-input { cursor: pointer; }
        select.form-input option { background: #1c2541; color: #f8fafc; }
        .btn { display: block; width: 100%; padding: 13px; background: linear-gradient(135deg, var(--primary) 0%, #8338ec 100%); color: white; border: none; border-radius: 11px; font-size: 1rem; font-weight: 700; cursor: pointer; text-align: center; transition: opacity 0.2s; }
        .btn:hover { opacity: 0.92; }
        .btn-outline { background: transparent; border: 1.5px solid var(--border); color: var(--text-main); }
        .badge { padding: 4px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; display: inline-block; }
        .badge-primary { background: var(--primary-light); color: var(--primary); }
        .badge-success { background: rgba(16,185,129,0.15); color: var(--success); }
        .badge-warning { background: rgba(245,158,11,0.15); color: var(--warning); }
        .opt-label { display: flex; align-items: center; gap: 10px; padding: 12px 14px; border: 1.5px solid var(--border); border-radius: 11px; cursor: pointer; background: var(--card); margin-bottom: 8px; font-size: 0.95rem; transition: all 0.15s; }
        .opt-label.selected { border-color: var(--primary); background: rgba(58,134,255,0.18); font-weight: 700; }
        .toast { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: #1e293b; color: white; padding: 11px 22px; border-radius: 12px; display: none; z-index: 999; box-shadow: 0 4px 20px rgba(0,0,0,0.5); font-weight: 600; font-size: 0.9rem; }
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="width:38px; height:38px; border-radius:10px; background:rgba(58,134,255,0.2); border:1px solid var(--primary); display:flex; align-items:center; justify-content:center; font-size:1.3rem;">🎓</div>
                <div>
                    <h1 style="font-size: 1.05rem;">بوابة اختبارات الحصة</h1>
                    <div style="font-size: 0.75rem; color: var(--text-muted);">بث مباشر عبر شبكة الواي فاي المحلية</div>
                </div>
            </div>
            <button onclick="logout()" id="logoutBtn" style="display:none; background:rgba(255,255,255,0.1); border:1px solid var(--border); color:white; padding:6px 14px; border-radius:16px; cursor:pointer; font-size:0.82rem; font-weight:600;">خروج 🚪</button>
        </div>
    </header>

    <div class="container">
        <!-- Session Closed Warning -->
        <div id="sessionClosedBanner" class="card" style="display:none; border-color:var(--danger); background:rgba(239,68,68,0.1); text-align:center;">
            <div style="font-size:1.8rem; margin-bottom:4px;">🔒</div>
            <h3 style="color:var(--danger); margin:4px 0;">الحصة مغلقة حالياً من قبل المعلم</h3>
            <p style="font-size:0.85rem; color:var(--text-muted);">يرجى الانتظار حتى يقوم المعلم بفتح واستقبال الطلاب للاختبار.</p>
        </div>

        <!-- AUTH VIEW (Student Onboarding) -->
        <div id="authView">
            <div class="card">
                <div style="text-align: center; margin-bottom: 16px;">
                    <h2 style="font-size: 1.2rem; color: var(--primary);">مرحباً بك في فصل الاختبارات</h2>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">سجل بياناتك ومرحلتك الدراسية للوصول للاختبارات والأنشطة</p>
                </div>

                <div class="tab-bar">
                    <button id="tabRegister" class="tab-btn active" onclick="switchAuth('register')">تسجيل جديد 📝</button>
                    <button id="tabLogin" class="tab-btn" onclick="switchAuth('login')">تسجيل الدخول 🔑</button>
                </div>

                <!-- Registration Form -->
                <div id="registerForm">
                    <div class="form-group">
                        <label>الاسم الرباعي للطالب *</label>
                        <input type="text" id="regName" class="form-input" placeholder="اكتب اسمك الرباعي كاملاً">
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div class="form-group">
                            <label>الصف الدراسي *</label>
                            <select id="regGrade" class="form-input">
                                <option value="أول ثانوي">أول ثانوي</option>
                                <option value="ثاني ثانوي">ثاني ثانوي</option>
                                <option value="ثالث ثانوي">ثالث ثانوي</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>الشعبة *</label>
                            <select id="regSection" class="form-input">
                                <option value="شعبة 1">شعبة 1</option>
                                <option value="شعبة 2">شعبة 2</option>
                                <option value="شعبة 3">شعبة 3</option>
                                <option value="شعبة 4">شعبة 4</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>رقم الهوية / الرقم الأكاديمي (اختياري)</label>
                        <input type="text" id="regNid" class="form-input" placeholder="رقم الهوية الوطنية أو الإقامة">
                    </div>

                    <div class="form-group">
                        <label>كلمة المرور الخاصة بك *</label>
                        <input type="password" id="regPass" class="form-input" placeholder="اختر كلمة مرور لتسجيل دخولك لاحقاً">
                    </div>

                    <button onclick="handleRegister()" class="btn">تأكيد التسجيل ودخول الفصل ←</button>
                </div>

                <!-- Login Form -->
                <div id="loginForm" style="display:none;">
                    <div class="form-group">
                        <label>الاسم الرباعي أو رقم الهوية</label>
                        <input type="text" id="loginId" class="form-input" placeholder="أدخل اسمك أو رقم الهوية المسجل">
                    </div>
                    <div class="form-group">
                        <label>كلمة المرور</label>
                        <input type="password" id="loginPass" class="form-input" placeholder="أدخل كلمة المرور">
                    </div>
                    <button onclick="handleLogin()" class="btn">دخول الفصل ←</button>
                </div>
            </div>
        </div>

        <!-- DASHBOARD VIEW -->
        <div id="dashboardView" style="display:none;">
            <div class="card" style="background: linear-gradient(135deg, rgba(58,134,255,0.14) 0%, rgba(131,56,236,0.14) 100%); border-color: var(--primary);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <h2 style="font-size: 1.15rem; color:#60a5fa;">أهلاً بك: <span id="studentGreetingName"></span> 👋</h2>
                        <div style="display:flex; align-items:center; gap:8px; margin-top:4px;">
                            <span class="badge badge-primary" id="studentGreetingBadge"></span>
                            <span style="font-size: 0.8rem; color: var(--text-muted);" id="studentGreetingId"></span>
                        </div>
                    </div>
                    <button onclick="loadQuizzes()" class="btn btn-outline" style="width:auto; padding:6px 14px; font-size:0.82rem;">تحديث 🔄</button>
                </div>
            </div>

            <div class="tab-bar">
                <button id="tAvail" class="tab-btn active" onclick="switchQTab('avail')">📋 الاختبارات المتاحة (<span id="availCount">0</span>)</button>
                <button id="tDone" class="tab-btn" onclick="switchQTab('done')">🏆 نتائجي (<span id="doneCount">0</span>)</button>
                <button id="tEval" class="tab-btn" onclick="switchQTab('eval')">📊 تقييم المعلم</button>
            </div>

            <div id="availContainer"></div>
            <div id="doneContainer" style="display:none;"></div>
            <div id="evalContainer" style="display:none;"></div>
        </div>

        <!-- ACTIVE QUIZ VIEW -->
        <div id="quizView" style="display:none;">
            <div class="card" style="position:sticky; top:70px; z-index:40; border-color:var(--primary); display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h2 id="activeQuizTitle" style="font-size: 1.05rem;"></h2>
                    <div id="activeQuizTargetInfo" style="font-size:0.75rem; color:var(--text-muted);"></div>
                </div>
                <div style="background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.3); color:#f87171; font-weight:700; padding:5px 12px; border-radius:10px; font-size:0.9rem;">
                    ⏱️ <span id="quizTimerText">10:00</span>
                </div>
            </div>
            <div id="questionsContainer"></div>
            <div class="card" style="text-align:center;">
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
        let timeLeft = 0;
        let antiCheatEnabled = true;

        window.addEventListener('DOMContentLoaded', () => {
            checkStatus();
            setInterval(checkStatus, 6000);
            if (currentStudent) {
                showDashboard();
            }
            setupAntiCheat();
        });

        function showToast(m, isErr) {
            const t = document.getElementById('toast');
            t.textContent = m;
            t.style.background = isErr ? '#dc2626' : '#1e293b';
            t.style.display = 'block';
            setTimeout(() => { t.style.display = 'none'; }, 3000);
        }

        async function checkStatus() {
            try {
                const res = await fetch('/api/status');
                const d = await res.json();
                document.getElementById('sessionClosedBanner').style.display = (d.isOpen === false) ? 'block' : 'none';
                antiCheatEnabled = (d.antiCheat !== false);
            } catch(e) {}
        }

        function switchAuth(t) {
            document.getElementById('tabRegister').classList.toggle('active', t === 'register');
            document.getElementById('tabLogin').classList.toggle('active', t === 'login');
            document.getElementById('registerForm').style.display = (t === 'register') ? 'block' : 'none';
            document.getElementById('loginForm').style.display = (t === 'login') ? 'block' : 'none';
        }

        async function handleRegister() {
            const username = document.getElementById('regName').value.trim();
            const grade = document.getElementById('regGrade').value;
            const section = document.getElementById('regSection').value;
            const nationalId = document.getElementById('regNid').value.trim();
            const password = document.getElementById('regPass').value.trim();

            if (!username) return showToast('الاسم الرباعي إجباري', true);
            if (!password) return showToast('كلمة المرور إجبارية', true);

            try {
                const res = await fetch('/api/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ username, grade, section, nationalId, password })
                });
                const d = await res.json();
                if (d.success) {
                    currentStudent = d.student;
                    localStorage.setItem('student_session', JSON.stringify(currentStudent));
                    showDashboard();
                    showToast('تم التسجيل بنجاح! أهلاً بك');
                } else {
                    showToast(d.message || 'فشل التسجيل', true);
                }
            } catch(e) {
                showToast('تعذر الاتصال بالخادم، تأكد من اتصالك بالواي فاي', true);
            }
        }

        async function handleLogin() {
            const identity = document.getElementById('loginId').value.trim();
            const password = document.getElementById('loginPass').value.trim();
            if (!identity || !password) return showToast('أدخل الاسم وكلمة المرور', true);

            try {
                const res = await fetch('/api/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ identity, password })
                });
                const d = await res.json();
                if (d.success) {
                    currentStudent = d.student;
                    localStorage.setItem('student_session', JSON.stringify(currentStudent));
                    showDashboard();
                    showToast('تم تسجيل الدخول بنجاح');
                } else {
                    showToast(d.message || 'بيانات غير صحيحة', true);
                }
            } catch(e) {
                showToast('تعذر الاتصال بالخادم', true);
            }
        }

        function logout() {
            if (activeQuiz && !confirm('أنت الآن بداخل اختبار! هل ترغب بالخروج وإلغاء الإجابة؟')) {
                return;
            }
            if (timerInterval) clearInterval(timerInterval);
            localStorage.removeItem('student_session');
            currentStudent = null;
            activeQuiz = null;
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
            const gradeInfo = (currentStudent.grade || '') + ' - ' + (currentStudent.section || '');
            document.getElementById('studentGreetingBadge').textContent = gradeInfo.trim() !== '-' ? gradeInfo : (currentStudent.gradeSection || 'فصل عام');
            document.getElementById('studentGreetingId').textContent = currentStudent.nationalId ? ('رقم الهوية: ' + currentStudent.nationalId) : '';

            loadQuizzes();
        }

        function switchQTab(t) {
            ['avail', 'done', 'eval'].forEach(k => {
                document.getElementById('t' + k.charAt(0).toUpperCase() + k.slice(1)).classList.toggle('active', k === t);
                document.getElementById(k + 'Container').style.display = (k === t) ? 'block' : 'none';
            });
        }

        async function loadQuizzes() {
            if (!currentStudent) return;
            try {
                const res = await fetch('/api/student-quizzes?student=' + encodeURIComponent(currentStudent.username));
                const d = await res.json();
                const avail = d.unattempted || [];
                const done = d.completed || [];
                const evalData = d.evaluation || {};

                document.getElementById('availCount').textContent = avail.length;
                document.getElementById('doneCount').textContent = done.length;

                // 1. Available Quizzes
                const aCont = document.getElementById('availContainer');
                if (avail.length === 0) {
                    aCont.innerHTML = '<div class="card" style="text-align:center; padding:30px; color:var(--text-muted);"><div style="font-size:2rem; margin-bottom:8px;">📝</div><h3>لا توجد اختبارات جديدة موجهة لصفك وشعبتك حالياً</h3><p style="font-size:0.85rem; margin-top:4px;">يرجى الانتظار حتى يطرح المعلم الاختبار المخصص لفصلك.</p></div>';
                } else {
                    let h = '';
                    avail.forEach(q => {
                        const targetText = (q.targetGrade === 'الكل' && q.targetSection === 'الكل') ? 'متاح لجميع الصفوف' : ((q.targetGrade || 'الكل') + ' • ' + (q.targetSection || 'الكل'));
                        h += '<div class="card">' +
                            '<div style="display:flex; justify-content:space-between; align-items:center;">' +
                                '<h3 style="font-size:1.1rem; color:var(--primary);">' + q.title + '</h3>' +
                                '<span class="badge badge-primary">' + targetText + '</span>' +
                            '</div>' +
                            '<p style="font-size:0.88rem; color:var(--text-muted); margin:8px 0;">' + (q.description || 'اختبار قصير لمتابعة الفهم والتحصيل') + '</p>' +
                            '<div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px;">' +
                                '<span style="font-size:0.82rem; color:var(--text-muted);">⏱️ المدة: ' + q.durationMinutes + ' دقائق</span>' +
                                '<button onclick="startQuiz(' + q.id + ')" class="btn" style="width:auto; padding:8px 20px; font-size:0.9rem;">بدء الاختبار 🚀</button>' +
                            '</div>' +
                        '</div>';
                    });
                    aCont.innerHTML = h;
                }

                // 2. Completed Quizzes
                const dCont = document.getElementById('doneContainer');
                if (done.length === 0) {
                    dCont.innerHTML = '<div class="card" style="text-align:center; padding:30px; color:var(--text-muted);"><div style="font-size:2rem; margin-bottom:8px;">🏆</div><h3>لم تقم بتسليم أي اختبار بعد</h3></div>';
                } else {
                    let h = '';
                    done.forEach(sub => {
                        const dateStr = new Date(sub.submittedAt).toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' });
                        h += '<div class="card">' +
                            '<div style="display:flex; justify-content:space-between; align-items:center;">' +
                                '<h3 style="font-size:1.05rem;">' + sub.title + '</h3>' +
                                '<span class="badge badge-success">تم التسليم ✓</span>' +
                            '</div>' +
                            '<div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px;">' +
                                '<div><span style="font-size:1.3rem; font-weight:800; color:var(--primary);">' + sub.score + '</span> <span style="font-size:0.85rem; color:var(--text-muted);">/ ' + sub.totalPoints + ' (' + sub.percentage + '%)</span></div>' +
                                '<span style="font-size:0.8rem; color:var(--text-muted);">' + dateStr + '</span>' +
                            '</div>' +
                        '</div>';
                    });
                    dCont.innerHTML = h;
                }

                // 3. Teacher Evaluation & Monthly Grades
                const eCont = document.getElementById('evalContainer');
                if (!evalData.isVisible) {
                    eCont.innerHTML = '<div class="card" style="text-align:center; padding:30px; color:var(--text-muted);"><div style="font-size:2rem; margin-bottom:8px;">🔒</div><h3>درجات التقييم الشهري محجوبة حالياً</h3><p style="font-size:0.85rem; margin-top:4px;">سيتم إعلانها فور اعتمادها ونشرها من قبل المعلم.</p></div>';
                } else {
                    eCont.innerHTML = '<div class="card">' +
                        '<h3 style="font-size:1.15rem; color:var(--primary); margin-bottom:12px;">رصد درجاتك الشهرية المعتمدة</h3>' +
                        '<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:14px;">' +
                            '<div style="background:var(--card); padding:12px; border-radius:10px; border:1px solid var(--border);"><div style="font-size:0.8rem; color:var(--text-muted);">الاختبار الشهري 1:</div><div style="font-size:1.2rem; font-weight:700; color:var(--text-main); margin-top:4px;">' + evalData.exam1Score + '</div></div>' +
                            '<div style="background:var(--card); padding:12px; border-radius:10px; border:1px solid var(--border);"><div style="font-size:0.8rem; color:var(--text-muted);">الاختبار الشهري 2:</div><div style="font-size:1.2rem; font-weight:700; color:var(--text-main); margin-top:4px;">' + evalData.exam2Score + '</div></div>' +
                            '<div style="background:var(--card); padding:12px; border-radius:10px; border:1px solid var(--border);"><div style="font-size:0.8rem; color:var(--text-muted);">درجة المشاركة والتفاعل:</div><div style="font-size:1.2rem; font-weight:700; color:var(--text-main); margin-top:4px;">' + evalData.participationScore + '</div></div>' +
                            '<div style="background:var(--card); padding:12px; border-radius:10px; border:1px solid var(--border);"><div style="font-size:0.8rem; color:var(--text-muted);">درجات إضافية / بونص:</div><div style="font-size:1.2rem; font-weight:700; color:var(--success); margin-top:4px;">+' + evalData.bonusScore + '</div></div>' +
                        '</div>' +
                        '<div style="background:rgba(58,134,255,0.12); border:1.5px solid var(--primary); padding:14px; border-radius:12px; display:flex; justify-content:space-between; align-items:center;">' +
                            '<span style="font-weight:700; font-size:1rem;">المجموع الكلي:</span>' +
                            '<span style="font-size:1.4rem; font-weight:800; color:var(--primary);">' + evalData.totalScore + '</span>' +
                        '</div>' +
                        (evalData.notes ? ('<div style="margin-top:14px; padding:12px; background:var(--card); border-radius:10px; border-left:4px solid var(--warning);"><div style="font-size:0.82rem; font-weight:700; color:var(--warning);">توجيه وملاحظة المعلم:</div><p style="font-size:0.9rem; margin-top:4px;">' + evalData.notes + '</p></div>') : '') +
                    '</div>';
                }
            } catch(e) {}
        }

        // ==================== QUIZ SOLVING ====================
        async function startQuiz(qid) {
            try {
                const res = await fetch('/api/quiz?id=' + qid + '&student=' + encodeURIComponent(currentStudent.username));
                const d = await res.json();
                if (d.error === 'ALREADY_SUBMITTED') {
                    showToast(d.message || 'تم حل هذا الاختبار مسبقاً', true);
                    return;
                }
                if (!d.quiz) return showToast('تعذر تحميل الاختبار', true);

                activeQuiz = d;
                selectedAnswers = {};
                timeLeft = (d.quiz.durationMinutes || 10) * 60;

                document.getElementById('dashboardView').style.display = 'none';
                document.getElementById('quizView').style.display = 'block';
                document.getElementById('activeQuizTitle').textContent = d.quiz.title;
                const tg = (d.quiz.targetGrade === 'الكل' && d.quiz.targetSection === 'الكل') ? 'عام للجميع' : (d.quiz.targetGrade + ' • ' + d.quiz.targetSection);
                document.getElementById('activeQuizTargetInfo').textContent = 'المرحلة: ' + tg + ' • ' + d.questions.length + ' أسئلة';

                renderQuestions(d.questions);
                startTimer();
            } catch(e) {
                showToast('خطأ في تحميل أسئلة الاختبار', true);
            }
        }

        function renderQuestions(questions) {
            const cont = document.getElementById('questionsContainer');
            let h = '';
            questions.forEach((q, idx) => {
                h += '<div class="card" id="qcard_' + q.id + '">' +
                    '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">' +
                        '<span style="font-weight:700; color:var(--primary); font-size:1rem;">السؤال ' + (idx + 1) + '</span>' +
                        '<span class="badge badge-primary">' + q.points + ' درجة</span>' +
                    '</div>' +
                    '<p style="font-size:1.02rem; font-weight:600; line-height:1.6; margin-bottom:14px;">' + q.questionText + '</p>' +
                    '<div class="options-box">';

                const opts = [
                    { key: 'A', text: q.optionA },
                    { key: 'B', text: q.optionB },
                    { key: 'C', text: q.optionC },
                    { key: 'D', text: q.optionD }
                ].filter(o => o.text && o.text.trim() !== '');

                opts.forEach(o => {
                    h += '<div class="opt-label" id="opt_' + q.id + '_' + o.key + '" onclick="selectAnswer(' + q.id + ', \'' + o.key + '\')">' +
                        '<div style="width:24px; height:24px; border-radius:50%; border:1.5px solid var(--border); display:flex; align-items:center; justify-content:center; font-size:0.75rem; font-weight:700;">' + o.key + '</div>' +
                        '<span style="flex:1;">' + o.text + '</span>' +
                    '</div>';
                });

                h += '</div></div>';
            });
            cont.innerHTML = h;
        }

        function selectAnswer(qid, optKey) {
            selectedAnswers[qid] = optKey;
            ['A', 'B', 'C', 'D'].forEach(k => {
                const el = document.getElementById('opt_' + qid + '_' + k);
                if (el) el.classList.toggle('selected', k === optKey);
            });
        }

        function startTimer() {
            if (timerInterval) clearInterval(timerInterval);
            updateTimerDisplay();
            timerInterval = setInterval(() => {
                timeLeft--;
                updateTimerDisplay();
                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    showToast('انتهى وقت الاختبار المحدد! سيتم تسليم الإجابات تلقائياً');
                    submitQuiz(true);
                }
            }, 1000);
        }

        function updateTimerDisplay() {
            const m = Math.floor(timeLeft / 60);
            const s = timeLeft % 60;
            document.getElementById('quizTimerText').textContent = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
        }

        function confirmSubmitQuiz() {
            const totalQ = (activeQuiz.questions || []).length;
            const answeredQ = Object.keys(selectedAnswers).length;
            if (answeredQ < totalQ) {
                if (!confirm('لقد أجبت عن (' + answeredQ + ' من ' + totalQ + ') سؤال فقط! هل أنت متأكد من تسليم الاختبار الآن؟')) {
                    return;
                }
            } else {
                if (!confirm('هل أنت متأكد من رغبتك في تسليم الاختبار وإنهاء الحل؟')) return;
            }
            submitQuiz(false);
        }

        async function submitQuiz(auto) {
            if (timerInterval) clearInterval(timerInterval);
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
                const d = await res.json();
                if (d.success) {
                    alert('تم تسليم إجاباتك بنجاح! 🎉\nالدرجة المحققة: ' + d.score + ' من ' + d.totalPoints + ' (' + d.percentage + '%)');
                    activeQuiz = null;
                    showDashboard();
                } else {
                    showToast(d.message || 'فشل تسليم الإجابات', true);
                }
            } catch(e) {
                showToast('خطأ أثناء إرسال الإجابات، أعد المحاولة', true);
            }
        }

        // ==================== ANTI-CHEAT (4G/5G Cellular Detection) ====================
        function setupAntiCheat() {
            // Check Network Connection API for Cellular (4G/5G)
            if ('connection' in navigator) {
                navigator.connection.addEventListener('change', () => {
                    if (antiCheatEnabled && activeQuiz) {
                        const conn = navigator.connection;
                        if (conn.type === 'cellular' || conn.effectiveType === '4g') {
                            reportCheat('تشغيل بيانات الهاتف المحمول (4G/5G) أثناء الاختبار');
                        }
                    }
                });
            }

            // Window visibility
            document.addEventListener('visibilitychange', () => {
                if (antiCheatEnabled && activeQuiz && document.hidden) {
                    reportCheat('الخروج من صفحة الاختبار أو فتح تطبيق آخر');
                }
            });
        }

        async function reportCheat(reason) {
            try {
                await fetch('/api/cheat-alert', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        student: currentStudent ? currentStudent.username : 'طالب',
                        reason: reason
                    })
                });
                showToast('تنبيه أمني: تم رصد مغادرة الصفحة وإخطار المعلم ⚠️', true);
            } catch(e) {}
        }
    </script>
</body>
</html>
"""
