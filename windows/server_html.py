# -*- coding: utf-8 -*-
"""
Embedded HTML Portals for Windows 11 Desktop Edition
"""

STUDENT_HTML = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>بوابة اختبارات الحصة - خادم Windows 11</title>
    <style>
        :root {
            --primary: #2563eb;
            --primary-light: #eff6ff;
            --success: #16a34a;
            --danger: #dc2626;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --radius: 16px;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }
        body { background: var(--bg); color: var(--text-main); line-height: 1.6; min-height: 100vh; padding-bottom: 40px; }
        header { background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%); color: white; padding: 16px; box-shadow: 0 4px 20px rgba(37,99,235,0.2); }
        .header-content { max-width: 680px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
        .container { max-width: 680px; margin: 16px auto; padding: 0 16px; }
        .card { background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
        .tab-bar { display: flex; background: rgba(0,0,0,0.04); padding: 4px; border-radius: 12px; margin-bottom: 18px; border: 1px solid var(--border); }
        .tab-btn { flex: 1; padding: 10px; border: none; background: transparent; cursor: pointer; font-weight: 600; border-radius: 10px; font-size: 0.95rem; color: var(--text-muted); }
        .tab-btn.active { background: var(--card-bg); color: var(--primary); box-shadow: 0 2px 6px rgba(0,0,0,0.08); }
        .form-group { margin-bottom: 14px; }
        .form-group label { display: block; font-size: 0.88rem; font-weight: 600; margin-bottom: 6px; color: var(--text-muted); }
        .form-input { width: 100%; padding: 12px 14px; border: 1.5px solid var(--border); border-radius: 12px; font-size: 1rem; }
        .btn { display: block; width: 100%; padding: 13px; background: var(--primary); color: white; border: none; border-radius: 12px; font-size: 1.05rem; font-weight: 700; cursor: pointer; text-align: center; }
        .btn-outline { background: transparent; border: 1.5px solid var(--border); color: var(--text-main); }
        .badge { padding: 4px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; }
        .toast { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); background: #1e293b; color: white; padding: 12px 24px; border-radius: 12px; display: none; z-index: 999; }
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <div>
                <h1 style="font-size: 1.15rem;">بوابة اختبارات الحصة 🎓</h1>
                <div style="font-size: 0.75rem; opacity: 0.9;">خادم Windows 11 • بث محلي مباشر</div>
            </div>
            <button onclick="logout()" id="logoutBtn" style="display:none; background:rgba(255,255,255,0.2); border:none; color:white; padding:6px 12px; border-radius:20px; cursor:pointer;">خروج 🚪</button>
        </div>
    </header>

    <div class="container">
        <!-- AUTH VIEW -->
        <div id="authView">
            <div class="card">
                <div class="tab-bar">
                    <button id="tabRegister" class="tab-btn active" onclick="switchAuthTab('register')">تسجيل جديد</button>
                    <button id="tabLogin" class="tab-btn" onclick="switchAuthTab('login')">تسجيل الدخول</button>
                </div>

                <div id="registerForm">
                    <div class="form-group">
                        <label>الاسم الرباعي للطالب *</label>
                        <input type="text" id="regName" class="form-input" placeholder="مثال: أحمد محمد علي حسن">
                    </div>
                    <div class="form-group">
                        <label>رقم الهوية / الإقامة</label>
                        <input type="text" id="regNid" class="form-input" placeholder="اختياري">
                    </div>
                    <div class="form-group">
                        <label>الصف والشعبة</label>
                        <input type="text" id="regGrade" class="form-input" placeholder="مثال: أول ثانوي - شعبة 1">
                    </div>
                    <div class="form-group">
                        <label>كلمة المرور *</label>
                        <input type="password" id="regPass" class="form-input" placeholder="اختر كلمة مرور خاصة بك">
                    </div>
                    <button onclick="handleRegister()" class="btn">حفظ والتسجيل للحصة ←</button>
                </div>

                <div id="loginForm" style="display:none;">
                    <div class="form-group">
                        <label>اسم الطالب أو رقم الهوية</label>
                        <input type="text" id="loginId" class="form-input" placeholder="أدخل اسمك أو رقم الهوية">
                    </div>
                    <div class="form-group">
                        <label>كلمة المرور</label>
                        <input type="password" id="loginPass" class="form-input">
                    </div>
                    <button onclick="handleLogin()" class="btn">تسجيل الدخول ←</button>
                </div>
            </div>
        </div>

        <!-- DASHBOARD VIEW -->
        <div id="dashboardView" style="display:none;">
            <div class="card" style="background: var(--primary-light); border-color: var(--primary);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <h2 style="font-size: 1.15rem; color: var(--primary);">أهلاً بك: <span id="studentNameDisplay"></span> 👋</h2>
                        <div id="studentGradeDisplay" style="font-size: 0.85rem; color: var(--text-muted);"></div>
                    </div>
                    <button onclick="loadQuizzes()" class="btn btn-outline" style="width:auto; padding:6px 14px; font-size:0.85rem; background:white;">تحديث 🔄</button>
                </div>
            </div>

            <div class="tab-bar">
                <button id="tAvail" class="tab-btn active" onclick="switchQTab('avail')">الاختبارات المتاحة (<span id="availCount">0</span>)</button>
                <button id="tDone" class="tab-btn" onclick="switchQTab('done')">نتائج الحل (<span id="doneCount">0</span>)</button>
                <button id="tEval" class="tab-btn" onclick="switchQTab('eval')">درجاتي وتقييمي 📊</button>
            </div>

            <div id="availContainer"></div>
            <div id="doneContainer" style="display:none;"></div>
            <div id="evalContainer" style="display:none;"></div>
        </div>

        <!-- ACTIVE QUIZ VIEW -->
        <div id="quizView" style="display:none;">
            <div class="card">
                <h2 id="activeQuizTitle" style="font-size: 1.2rem;"></h2>
                <div id="questionsContainer" style="margin-top: 14px;"></div>
                <button onclick="submitQuizAnswers()" class="btn" style="margin-top: 16px;">تسليم الإجابات وإنهاء الاختبار ✓</button>
            </div>
        </div>
    </div>

    <div id="toast" class="toast"></div>

    <script>
        let currentStudent = JSON.parse(localStorage.getItem('win_student') || 'null');
        let activeQuiz = null;
        let selectedAnswers = {};

        window.addEventListener('DOMContentLoaded', () => {
            if (currentStudent) showDashboard();
        });

        function showToast(msg) {
            const t = document.getElementById('toast');
            t.textContent = msg;
            t.style.display = 'block';
            setTimeout(() => { t.style.display = 'none'; }, 3000);
        }

        function switchAuthTab(tab) {
            document.getElementById('tabRegister').classList.toggle('active', tab === 'register');
            document.getElementById('tabLogin').classList.toggle('active', tab === 'login');
            document.getElementById('registerForm').style.display = (tab === 'register') ? 'block' : 'none';
            document.getElementById('loginForm').style.display = (tab === 'login') ? 'block' : 'none';
        }

        async function handleRegister() {
            const username = document.getElementById('regName').value.trim();
            const password = document.getElementById('regPass').value.trim();
            const nationalId = document.getElementById('regNid').value.trim();
            const gradeSection = document.getElementById('regGrade').value.trim();

            if (!username || !password) return showToast('يرجى كتابة الاسم وكلمة المرور');

            try {
                const res = await fetch('/api/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ username, password, nationalId, gradeSection })
                });
                const data = await res.json();
                if (data.success) {
                    currentStudent = data.student;
                    localStorage.setItem('win_student', JSON.stringify(currentStudent));
                    showDashboard();
                } else {
                    showToast(data.message || 'فشل التسجيل');
                }
            } catch (e) {
                showToast('تعذر الاتصال بالخادم');
            }
        }

        async function handleLogin() {
            const identity = document.getElementById('loginId').value.trim();
            const password = document.getElementById('loginPass').value.trim();
            if (!identity || !password) return showToast('يرجى إدخال البيانات');

            try {
                const res = await fetch('/api/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ identity, password })
                });
                const data = await res.json();
                if (data.success) {
                    currentStudent = data.student;
                    localStorage.setItem('win_student', JSON.stringify(currentStudent));
                    showDashboard();
                } else {
                    showToast(data.message || 'بيانات الدخول غير صحيحة');
                }
            } catch (e) {
                showToast('تعذر الاتصال بالخادم');
            }
        }

        function logout() {
            localStorage.removeItem('win_student');
            currentStudent = null;
            document.getElementById('authView').style.display = 'block';
            document.getElementById('dashboardView').style.display = 'none';
            document.getElementById('logoutBtn').style.display = 'none';
        }

        function showDashboard() {
            document.getElementById('authView').style.display = 'none';
            document.getElementById('quizView').style.display = 'none';
            document.getElementById('dashboardView').style.display = 'block';
            document.getElementById('logoutBtn').style.display = 'block';
            document.getElementById('studentNameDisplay').textContent = currentStudent.username;
            document.getElementById('studentGradeDisplay').textContent = currentStudent.gradeSection ? ('الصف: ' + currentStudent.gradeSection) : '';
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
                    aCont.innerHTML = '<div class="card" style="text-align:center; color:var(--text-muted);">لا توجد اختبارات جديدة متاحة حالياً.</div>';
                } else {
                    let h = '';
                    avail.forEach(q => {
                        h += '<div class="card">' +
                            '<div style="display:flex; justify-content:space-between; align-items:center;">' +
                                '<h3 style="font-size:1.05rem;">' + q.title + '</h3>' +
                                '<span class="badge" style="background:#e0e7ff; color:#3730a3;">⏱️ ' + q.durationMinutes + ' دقيقة</span>' +
                            '</div>' +
                            '<p style="font-size:0.85rem; color:var(--text-muted); margin:6px 0;">' + (q.description || '') + '</p>' +
                            '<button onclick="startQuiz(' + q.id + ')" class="btn" style="margin-top:10px;">بدء الاختبار الآن ←</button>' +
                        '</div>';
                    });
                    aCont.innerHTML = h;
                }

                // Render Completed
                const dCont = document.getElementById('doneContainer');
                if (done.length === 0) {
                    dCont.innerHTML = '<div class="card" style="text-align:center; color:var(--text-muted);">لم تنجز أي اختبارات بعد.</div>';
                } else {
                    let h = '';
                    done.forEach(q => {
                        h += '<div class="card" style="border-right: 4px solid var(--success);">' +
                            '<div style="display:flex; justify-content:space-between; align-items:center;">' +
                                '<h3 style="font-size:1.05rem;">' + q.title + '</h3>' +
                                '<span class="badge" style="background:#dcfce7; color:#16a34a;">الدرجة: ' + q.score + ' / ' + q.totalPoints + ' (' + q.percentage + '%)</span>' +
                            '</div>' +
                            '<div style="font-size:0.8rem; color:var(--text-muted); margin-top:6px;">🔒 تم تسليم الاختبار واعتماده</div>' +
                        '</div>';
                    });
                    dCont.innerHTML = h;
                }

                // Render Evaluation
                const evCont = document.getElementById('evalContainer');
                const ev = data.evaluation;
                if (ev && ev.isVisible) {
                    let noteHtml = ev.notes ? ('<div style="background:rgba(37,99,235,0.08); padding:10px 14px; border-radius:10px; margin-top:10px;">💬 <strong>ملاحظة المعلم:</strong> ' + ev.notes + '</div>') : '';
                    evCont.innerHTML = '<div class="card">' +
                        '<h3 style="color:var(--primary); margin-bottom:12px;">📊 بطاقة الدرجات الشهرية</h3>' +
                        '<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; text-align:center;">' +
                            '<div style="background:#f1f5f9; padding:10px; border-radius:10px;"><div style="font-size:0.8rem; color:var(--text-muted);">الشهري الأول</div><div style="font-size:1.3rem; font-weight:800;">' + ev.exam1Score + '</div></div>' +
                            '<div style="background:#f1f5f9; padding:10px; border-radius:10px;"><div style="font-size:0.8rem; color:var(--text-muted);">الشهري الثاني</div><div style="font-size:1.3rem; font-weight:800;">' + ev.exam2Score + '</div></div>' +
                            '<div style="background:#f1f5f9; padding:10px; border-radius:10px;"><div style="font-size:0.8rem; color:var(--text-muted);">المشاركة</div><div style="font-size:1.3rem; font-weight:800; color:var(--success);">' + ev.participationScore + '</div></div>' +
                            '<div style="background:#f1f5f9; padding:10px; border-radius:10px;"><div style="font-size:0.8rem; color:var(--text-muted);">إضافي / خصم</div><div style="font-size:1.3rem; font-weight:800;">' + (ev.bonusScore > 0 ? '+' : '') + ev.bonusScore + '</div></div>' +
                        '</div>' +
                        '<div style="background:var(--primary-light); padding:12px; border-radius:10px; text-align:center; margin-top:12px; font-weight:800; color:var(--primary); font-size:1.2rem;">المجموع الكلي: ' + ev.totalScore + '</div>' +
                        noteHtml +
                    '</div>';
                } else {
                    evCont.innerHTML = '<div class="card" style="text-align:center; color:var(--text-muted);">🔒 الدرجات قيد المراجعة حالياً من قبل المعلم.</div>';
                }
            } catch (e) {
                showToast('خطأ في جلب الاختبارات');
            }
        }

        async function startQuiz(quizId) {
            try {
                const res = await fetch('/api/quiz?id=' + quizId + '&student=' + encodeURIComponent(currentStudent.username));
                const data = await res.json();
                if (!res.ok) return showToast(data.message || 'تعذر فتح الاختبار');

                activeQuiz = data;
                selectedAnswers = {};
                document.getElementById('activeQuizTitle').textContent = data.quiz.title;
                const qCont = document.getElementById('questionsContainer');

                let h = '';
                data.questions.forEach((q, idx) => {
                    h += '<div style="background:rgba(0,0,0,0.02); border:1px solid var(--border); border-radius:12px; padding:14px; margin-bottom:12px;">' +
                        '<div style="font-weight:700; font-size:1.02rem; margin-bottom:10px;">' + (idx + 1) + '. ' + q.questionText + '</div>' +
                        '<div style="display:flex; flex-direction:column; gap:8px;">' +
                            '<label style="display:flex; align-items:center; gap:8px; padding:8px 12px; border:1px solid var(--border); border-radius:8px; cursor:pointer;"><input type="radio" name="q_' + q.id + '" value="A" onchange="pickAns(' + q.id + ', \'A\')"> ' + (q.optionA || 'أ') + '</label>' +
                            '<label style="display:flex; align-items:center; gap:8px; padding:8px 12px; border:1px solid var(--border); border-radius:8px; cursor:pointer;"><input type="radio" name="q_' + q.id + '" value="B" onchange="pickAns(' + q.id + ', \'B\')"> ' + (q.optionB || 'ب') + '</label>' +
                            (q.optionC ? ('<label style="display:flex; align-items:center; gap:8px; padding:8px 12px; border:1px solid var(--border); border-radius:8px; cursor:pointer;"><input type="radio" name="q_' + q.id + '" value="C" onchange="pickAns(' + q.id + ', \'C\')"> ' + q.optionC + '</label>') : '') +
                            (q.optionD ? ('<label style="display:flex; align-items:center; gap:8px; padding:8px 12px; border:1px solid var(--border); border-radius:8px; cursor:pointer;"><input type="radio" name="q_' + q.id + '" value="D" onchange="pickAns(' + q.id + ', \'D\')"> ' + q.optionD + '</label>') : '') +
                        '</div>' +
                    '</div>';
                });
                qCont.innerHTML = h;

                document.getElementById('dashboardView').style.display = 'none';
                document.getElementById('quizView').style.display = 'block';
            } catch (e) {
                showToast('خطأ في تحميل الاختبار');
            }
        }

        function pickAns(qid, val) {
            selectedAnswers[qid] = val;
        }

        async function submitQuizAnswers() {
            if (!confirm('هل أنت متأكد من تسليم إجاباتك؟')) return;
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
                    alert('تم تسليم الاختبار بنجاح! درجتك: ' + data.score + ' من ' + data.totalPoints + ' (' + data.percentage + '%)');
                    showDashboard();
                } else {
                    showToast(data.message || 'فشل التسليم');
                }
            } catch (e) {
                showToast('خطأ في إرسال الإجابات');
            }
        }
    </script>
</body>
</html>
"""

TEACHER_HTML = \"\"\"<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة تحكم المعلم - Windows 11 PC</title>
    <style>
        :root {
            --primary: #2563eb;
            --success: #16a34a;
            --danger: #dc2626;
            --bg: #f1f5f9;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --radius: 14px;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background: var(--bg); color: var(--text-main); min-height: 100vh; }
        header { background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%); color: white; padding: 14px 24px; display: flex; justify-content: space-between; align-items: center; }
        .main-container { max-width: 1200px; margin: 20px auto; padding: 0 20px; }
        .top-nav { display: flex; gap: 10px; background: var(--card-bg); padding: 6px; border-radius: 12px; border: 1px solid var(--border); margin-bottom: 20px; }
        .nav-btn { background: transparent; border: none; padding: 10px 18px; border-radius: 10px; cursor: pointer; font-size: 0.95rem; font-weight: 600; color: var(--text-muted); }
        .nav-btn.active { background: var(--primary); color: white; }
        .card { background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; margin-bottom: 20px; }
        .btn { background: var(--primary); color: white; border: none; padding: 9px 16px; border-radius: 10px; cursor: pointer; font-weight: 600; font-size: 0.9rem; }
        .btn-success { background: var(--success); }
        .btn-outline { background: transparent; border: 1.5px solid var(--border); color: var(--text-main); }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 12px 14px; text-align: right; border-bottom: 1px solid var(--border); font-size: 0.92rem; }
        th { background: rgba(0,0,0,0.02); font-weight: 700; color: var(--text-muted); }
        .modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(15,23,42,0.6); display: none; align-items: center; justify-content: center; z-index: 1000; }
        .modal-body { background: white; border-radius: 16px; max-width: 600px; width: 100%; padding: 24px; max-height: 90vh; overflow-y: auto; }
        .form-group { margin-bottom: 12px; }
        .form-group label { display: block; font-size: 0.88rem; font-weight: 600; margin-bottom: 6px; }
        .form-input { width: 100%; padding: 10px 12px; border: 1.5px solid var(--border); border-radius: 10px; }
        .toast { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); background: #0f172a; color: white; padding: 12px 24px; border-radius: 10px; display: none; }
    </style>
</head>
<body>
    <header>
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 1.6rem;">🎓</span>
            <div>
                <h1 style="font-size: 1.25rem;">خادم الاختبارات المدرسية - Windows 11 Desktop Edition</h1>
                <div style="font-size: 0.78rem; opacity: 0.9;">يعمل محلياً على جهاز الكمبيوتر مباشرة</div>
            </div>
        </div>
        <button onclick="fetchData()" class="btn btn-outline" style="color:white; border-color:rgba(255,255,255,0.4);">تحديث 🔄</button>
    </header>

    <div class="main-container">
        <div class="top-nav">
            <button id="navSt" class="nav-btn active" onclick="tab('st')">👥 الطلاب والدرجات الشهرية</button>
            <button id="navQz" class="nav-btn" onclick="tab('qz')">📝 بنك الاختبارات والأنشطة</button>
            <button id="navSb" class="nav-btn" onclick="tab('sb')">📊 التسليمات والنتائج</button>
        </div>

        <!-- STUDENTS -->
        <div id="secSt">
            <div class="card" style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2>سجل الطلاب والتقييم</h2>
                    <p style="font-size: 0.85rem; color: var(--text-muted);">رصد درجات الاختبارات الشهرية والمشاركة</p>
                </div>
                <button id="globBtn" onclick="toggleGlobVis()" class="btn btn-outline">👁️ إخفاء/إظهار الدرجات للجميع</button>
            </div>
            <div id="stTableCont"></div>
        </div>

        <!-- QUIZZES -->
        <div id="secQz" style="display: none;">
            <div class="card" style="display: flex; justify-content: space-between; align-items: center;">
                <h2>بنك الاختبارات</h2>
                <button onclick="openNewQuizModal()" class="btn btn-success">+ اختبار جديد</button>
            </div>
            <div id="qzList"></div>
        </div>

        <!-- SUBMISSIONS -->
        <div id="secSb" style="display: none;">
            <div class="card">
                <h2>التسليمات الفورية</h2>
                <table>
                    <thead>
                        <tr><th>#</th><th>اسم الطالب</th><th>عنوان الاختبار</th><th>الدرجة</th><th>النسبة</th></tr>
                    </thead>
                    <tbody id="sbList"></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- EVAL MODAL -->
    <div id="evalModal" class="modal">
        <div class="modal-body">
            <h3 id="mTitle" style="color: var(--primary); margin-bottom: 14px;">رصد درجات الطالب</h3>
            <input type="hidden" id="mId">
            <div class="form-group"><label>الفصل والشعبة:</label><input type="text" id="mGrade" class="form-input"></div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div class="form-group"><label>الشهري 1:</label><input type="number" step="0.5" id="mE1" class="form-input"></div>
                <div class="form-group"><label>الشهري 2:</label><input type="number" step="0.5" id="mE2" class="form-input"></div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div class="form-group"><label>المشاركة:</label><input type="number" step="0.5" id="mPart" class="form-input"></div>
                <div class="form-group"><label>إضافي / خصم (+/-):</label><input type="number" step="0.5" id="mBonus" class="form-input"></div>
            </div>
            <div class="form-group"><label>ملاحظة المعلم:</label><textarea id="mNotes" class="form-input" rows="2"></textarea></div>
            <div style="display: flex; gap: 20px; margin: 12px 0;">
                <label><input type="checkbox" id="mShowG"> إظهار الدرجات للطالب</label>
                <label><input type="checkbox" id="mShowN"> إظهار الملاحظة للطالب</label>
            </div>
            <div style="display: flex; justify-content: flex-end; gap: 10px;">
                <button onclick="document.getElementById('evalModal').style.display='none'" class="btn btn-outline">إلغاء</button>
                <button onclick="saveEval()" class="btn btn-success">حفظ التقييم ✓</button>
            </div>
        </div>
    </div>

    <div id="toast" class="toast"></div>

    <script>
        let data = { students: [], quizzes: [], submissions: [] };
        let globVis = true;

        window.addEventListener('DOMContentLoaded', fetchData);

        function showToast(m) {
            const t = document.getElementById('toast');
            t.textContent = m;
            t.style.display = 'block';
            setTimeout(() => t.style.display = 'none', 3000);
        }

        function tab(t) {
            ['st', 'qz', 'sb'].forEach(k => {
                document.getElementById('sec' + k.toUpperCase().charAt(0) + k.slice(1)).style.display = (k === t) ? 'block' : 'none';
                document.getElementById('nav' + k.toUpperCase().charAt(0) + k.slice(1)).classList.toggle('active', k === t);
            });
        }

        async function fetchData() {
            try {
                const res = await fetch('/api/teacher/data');
                data = await res.json();
                globVis = data.areGradesVisibleGlobally !== false;
                render();
            } catch (e) {
                showToast('خطأ في جلب البيانات');
            }
        }

        function render() {
            // Render students
            const cont = document.getElementById('stTableCont');
            if (data.students.length === 0) {
                cont.innerHTML = '<div class="card" style="text-align:center;">لا يوجد طلاب بعد.</div>';
            } else {
                let h = '<div class="card"><table><thead><tr><th>اسم الطالب</th><th>الصف</th><th>شهري 1</th><th>شهري 2</th><th>مشاركة</th><th>إضافي</th><th>المجموع</th><th>الظهور</th><th>إجراء</th></tr></thead><tbody>';
                data.students.forEach(s => {
                    const total = (s.exam1Score || 0) + (s.exam2Score || 0) + (s.participationScore || 0) + (s.bonusScore || 0);
                    h += '<tr><td style="font-weight:700;">' + s.username + '</td><td>' + (s.gradeSection || '-') + '</td><td>' + s.exam1Score + '</td><td>' + s.exam2Score + '</td><td>' + s.participationScore + '</td><td>' + (s.bonusScore > 0 ? '+' : '') + s.bonusScore + '</td><td style="font-weight:800; color:var(--primary);">' + total.toFixed(1) + '</td><td>' + (s.showGradesToStudent ? '👁️' : '🔒') + '</td><td><button onclick="openEval(' + s.id + ')" class="btn" style="padding:4px 10px; font-size:0.8rem;">رصد 📝</button></td></tr>';
                });
                h += '</tbody></table></div>';
                cont.innerHTML = h;
            }

            // Render quizzes
            const qzCont = document.getElementById('qzList');
            let qh = '';
            data.quizzes.forEach(q => {
                qh += '<div class="card" style="display:flex; justify-content:space-between; align-items:center;"><div><h3>' + q.title + '</h3><div style="font-size:0.85rem; color:var(--text-muted);">⏱️ ' + q.durationMinutes + ' دقيقة</div></div><button onclick="toggleQ(' + q.id + ', ' + q.isActive + ')" class="btn ' + (q.isActive ? 'btn-danger' : 'btn-success') + '">' + (q.isActive ? 'إغلاق الاختبار 🔒' : 'تفعيل الاختبار 🔓') + '</button></div>';
            });
            qzCont.innerHTML = qh;

            // Render submissions
            const sbBody = document.getElementById('sbList');
            let sh = '';
            data.submissions.forEach((s, i) => {
                const pct = s.totalPoints > 0 ? Math.round((s.score * 100) / s.totalPoints) : 100;
                sh += '<tr><td>' + (i+1) + '</td><td style="font-weight:700;">' + s.studentUsername + '</td><td>' + (s.quizTitle || 'اختبار') + '</td><td style="font-weight:700; color:var(--primary);">' + s.score + ' / ' + s.totalPoints + '</td><td>' + pct + '%</td></tr>';
            });
            sbBody.innerHTML = sh || '<tr><td colspan="5" style="text-align:center;">لا توجد تسليمات بعد.</td></tr>';
        }

        function openEval(id) {
            const s = data.students.find(x => x.id === id);
            if (!s) return;
            document.getElementById('mId').value = s.id;
            document.getElementById('mTitle').textContent = 'رصد درجات: ' + s.username;
            document.getElementById('mGrade').value = s.gradeSection || '';
            document.getElementById('mE1').value = s.exam1Score || 0;
            document.getElementById('mE2').value = s.exam2Score || 0;
            document.getElementById('mPart').value = s.participationScore || 0;
            document.getElementById('mBonus').value = s.bonusScore || 0;
            document.getElementById('mNotes').value = s.notes || '';
            document.getElementById('mShowG').checked = s.showGradesToStudent !== 0;
            document.getElementById('mShowN').checked = s.showNotesToStudent !== 0;
            document.getElementById('evalModal').style.display = 'flex';
        }

        async function saveEval() {
            const payload = {
                studentId: parseInt(document.getElementById('mId').value),
                gradeSection: document.getElementById('mGrade').value.trim(),
                exam1: parseFloat(document.getElementById('mE1').value) || 0,
                exam2: parseFloat(document.getElementById('mE2').value) || 0,
                participation: parseFloat(document.getElementById('mPart').value) || 0,
                bonus: parseFloat(document.getElementById('mBonus').value) || 0,
                notes: document.getElementById('mNotes').value.trim(),
                showGrades: document.getElementById('mShowG').checked,
                showNotes: document.getElementById('mShowN').checked
            };
            await fetch('/api/teacher/evaluate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            document.getElementById('evalModal').style.display = 'none';
            fetchData();
            showToast('تم حفظ التقييم بنجاح!');
        }

        async function toggleQ(id, act) {
            await fetch('/api/teacher/toggle-quiz', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ quizId: id, isActive: !act })
            });
            fetchData();
        }

        async function toggleGlobVis() {
            await fetch('/api/teacher/toggle-visibility', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ visible: !globVis })
            });
            fetchData();
            showToast('تم تحديث حالة الظهور للجميع');
        }
    </script>
</body>
</html>
\"\"\"

