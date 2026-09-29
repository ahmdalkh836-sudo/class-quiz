# -*- coding: utf-8 -*-
r"""
Student Web Portal HTML Template for Windows 11 Classroom Server
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
        .tab-btn { flex: 1; padding: 9px; border: none; background: transparent; color: var(--text-muted); border-radius: 9px; font-size: 0.9rem; font-weight: 700; cursor: pointer; }
        .tab-btn.active { background: var(--primary); color: white; }
        .form-group { margin-bottom: 12px; }
        .form-group label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 5px; color: var(--text-muted); }
        .form-input { width: 100%; padding: 11px 13px; border: 1.5px solid var(--border); border-radius: 11px; font-size: 0.95rem; background: var(--card); color: var(--text-main); }
        .form-input:focus { outline: none; border-color: var(--primary); }
        .btn { display: block; width: 100%; padding: 12px; background: linear-gradient(135deg, var(--primary) 0%, #8338ec 100%); color: white; border: none; border-radius: 11px; font-size: 1rem; font-weight: 700; cursor: pointer; text-align: center; }
        .btn-outline { background: transparent; border: 1.5px solid var(--border); color: var(--text-main); }
        .badge { padding: 4px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; display: inline-block; }
        .badge-success { background: rgba(16,185,129,0.15); color: var(--success); }
        .opt-label { display: flex; align-items: center; gap: 10px; padding: 12px 14px; border: 1.5px solid var(--border); border-radius: 11px; cursor: pointer; background: var(--card); margin-bottom: 8px; font-size: 0.95rem; }
        .opt-label.selected { border-color: var(--primary); background: rgba(58,134,255,0.15); font-weight: 700; }
        .toast { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: #1e293b; color: white; padding: 10px 20px; border-radius: 10px; display: none; z-index: 999; }
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="width:38px; height:38px; border-radius:10px; background:rgba(58,134,255,0.2); border:1px solid var(--primary); display:flex; align-items:center; justify-content:center; font-size:1.3rem;">🎓</div>
                <div>
                    <h1 style="font-size: 1.05rem;">بوابة اختبارات الحصة</h1>
                    <div style="font-size: 0.75rem; color: var(--text-muted);">بث مباشر عبر الواي فاي المحلي</div>
                </div>
            </div>
            <button onclick="logout()" id="logoutBtn" style="display:none; background:rgba(255,255,255,0.1); border:1px solid var(--border); color:white; padding:5px 12px; border-radius:16px; cursor:pointer; font-size:0.8rem;">خروج 🚪</button>
        </div>
    </header>

    <div class="container">
        <!-- Session Closed Warning -->
        <div id="sessionClosedBanner" class="card" style="display:none; border-color:var(--danger); background:rgba(239,68,68,0.1); text-align:center;">
            <div style="font-size:1.6rem;">🔒</div>
            <h3 style="color:var(--danger); margin:4px 0;">الحصة مغلقة حالياً من قبل المعلم</h3>
            <p style="font-size:0.85rem; color:var(--text-muted);">يرجى الانتظار حتى يقوم المعلم ببدء وتفعيل الحصة.</p>
        </div>

        <!-- AUTH VIEW -->
        <div id="authView">
            <div class="card">
                <div class="tab-bar">
                    <button id="tabRegister" class="tab-btn active" onclick="switchAuth('register')">تسجيل جديد 📝</button>
                    <button id="tabLogin" class="tab-btn" onclick="switchAuth('login')">تسجيل الدخول 🔑</button>
                </div>

                <div id="registerForm">
                    <div class="form-group"><label>الاسم الرباعي للطالب *</label><input type="text" id="regName" class="form-input" placeholder="اكتب اسمك الرباعي كاملاً"></div>
                    <div class="form-group"><label>الصف والشعبة *</label><input type="text" id="regGrade" class="form-input" placeholder="مثال: أول ثانوي - 1 أو ثالث متوسط / أ"></div>
                    <div class="form-group"><label>رقم الهوية / الإقامة</label><input type="text" id="regNid" class="form-input" placeholder="اختياري"></div>
                    <div class="form-group"><label>كلمة المرور *</label><input type="password" id="regPass" class="form-input" placeholder="اختر كلمة مرور خاصة بك"></div>
                    <button onclick="handleRegister()" class="btn">حفظ وتسجيل الدخول للحصة ←</button>
                </div>

                <div id="loginForm" style="display:none;">
                    <div class="form-group"><label>اسم الطالب أو رقم الهوية</label><input type="text" id="loginId" class="form-input"></div>
                    <div class="form-group"><label>كلمة المرور</label><input type="password" id="loginPass" class="form-input"></div>
                    <button onclick="handleLogin()" class="btn">دخول الحصة ←</button>
                </div>
            </div>
        </div>

        <!-- DASHBOARD VIEW -->
        <div id="dashboardView" style="display:none;">
            <div class="card" style="background: linear-gradient(135deg, rgba(58,134,255,0.12) 0%, rgba(131,56,236,0.12) 100%); border-color: var(--primary);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <h2 style="font-size: 1.15rem; color:#60a5fa;">أهلاً بك: <span id="studentGreetingName"></span> 👋</h2>
                        <div id="studentGreetingGrade" style="font-size: 0.85rem; color: var(--text-muted); margin-top:2px;"></div>
                    </div>
                    <button onclick="loadQuizzes()" class="btn btn-outline" style="width:auto; padding:6px 12px; font-size:0.8rem;">تحديث 🔄</button>
                </div>
            </div>

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
            <div class="card" style="position:sticky; top:70px; z-index:40; border-color:var(--primary); display:flex; justify-content:space-between; align-items:center;">
                <h2 id="activeQuizTitle" style="font-size: 1.1rem;"></h2>
                <div style="background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.3); color:#f87171; font-weight:700; padding:4px 10px; border-radius:8px; font-size:0.88rem;">⏱️ <span id="quizTimerText">10:00</span></div>
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
        let antiCheatEnabled = true;

        window.addEventListener('DOMContentLoaded', () => {
            checkStatus();
            setInterval(checkStatus, 6000);
            if (currentStudent) showDashboard();
        });

        function showToast(m, isErr) {
            const t = document.getElementById('toast');
            t.textContent = m;
            t.style.background = isErr ? '#dc2626' : '#1e293b';
            t.style.display = 'block';
            setTimeout(() => t.style.display = 'none', 3000);
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
            const gradeSection = document.getElementById('regGrade').value.trim();
            const nationalId = document.getElementById('regNid').value.trim();
            const password = document.getElementById('regPass').value.trim();
            if (!username || !password) return showToast('الاسم وكلمة المرور مطلوبة', true);

            try {
                const res = await fetch('/api/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ username, password, nationalId, gradeSection })
                });
                const d = await res.json();
                if (d.success) {
                    currentStudent = d.student;
                    localStorage.setItem('student_session', JSON.stringify(currentStudent));
                    showDashboard();
                } else showToast(d.message || 'فشل التسجيل', true);
            } catch(e) { showToast('تعذر الاتصال بالخادم', true); }
        }

        async function handleLogin() {
            const identity = document.getElementById('loginId').value.trim();
            const password = document.getElementById('loginPass').value.trim();
            if (!identity || !password) return showToast('أدخل البيانات المطلوبة', true);

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
                } else showToast(d.message || 'بيانات غير صحيحة', true);
            } catch(e) { showToast('تعذر الاتصال بالخادم', true); }
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

        function switchQTab(t) {
            ['avail', 'done', 'eval'].forEach(k => {
                document.getElementById('t' + k.charAt(0).toUpperCase() + k.slice(1)).classList.toggle('active', k === t);
                document.getElementById(k + 'Container').style.display = (k === t) ? 'block' : 'none';
            });
        }

        async function loadQuizzes() {
            try {
                const res = await fetch('/api/student-quizzes?student=' + encodeURIComponent(currentStudent.username));
                const d = await res.json();
                const avail = d.unattempted || [];
                const done = d.completed || [];
                document.getElementById('availCount').textContent = avail.length;
                document.getElementById('doneCount').textContent = done.length;

                // Render available
                const aCont = document.getElementById('availContainer');
                if (avail.length === 0) aCont.innerHTML = '<div class="card" style="text-align:center; color:var(--text-muted);"><div style="font-size:1.8rem;">📝</div><h3>لا توجد اختبارات جديدة حالياً</h3></div>';
                else {
                    let h = '';
                    avail.forEach(q => {
                        h += '<div class="card">' +
                            '<div style="display:flex; justify-content:space-between; align-items:center;"><h3 style="font-size:1.05rem;">' + q.title + '</h3><span class="badge" style="background:rgba(58,134,255,0.2); color:#60a5fa;">⏱️ ' + q.durationMinutes + ' د</span></div>' +
                            '<p style="font-size:0.85rem; color:var(--text-muted); margin:6px 0;">' + (q.description || '') + '</p>' +
                            '<button onclick="startQuiz(' + q.id + ')" class="btn" style="margin-top:8px;">بدء الاختبار الآن ←</button>' +
                        '</div>';
                    });
                    aCont.innerHTML = h;
                }

                // Render done
                const dCont = document.getElementById('doneContainer');
                if (done.length === 0) dCont.innerHTML = '<div class="card" style="text-align:center; color:var(--text-muted);"><div style="font-size:1.8rem;">🏆</div><h3>لم تنجز أي اختبارات بعد</h3></div>';
                else {
                    let h = '';
                    done.forEach(q => {
                        h += '<div class="card" style="border-right:4px solid var(--success);">' +
                            '<div style="display:flex; justify-content:space-between; align-items:center;"><h3 style="font-size:1.05rem;">' + q.title + '</h3><span class="badge badge-success">الدرجة: ' + q.score + ' / ' + q.totalPoints + ' (' + q.percentage + '%)</span></div>' +
                            '<div style="font-size:0.8rem; color:var(--text-muted); margin-top:4px;">🔒 تم تسليم الاختبار واعتماده</div>' +
                        '</div>';
                    });
                    dCont.innerHTML = h;
                }

                // Render evaluation
                const evCont = document.getElementById('evalContainer');
                const ev = d.evaluation;
                if (ev && ev.isVisible) {
                    const noteHtml = ev.notes ? ('<div style="background:rgba(58,134,255,0.1); border:1px dashed var(--primary); padding:10px; border-radius:10px; margin-top:10px;"><div style="font-weight:700; color:#60a5fa; font-size:0.85rem;">💬 ملاحظة المعلم:</div><div style="font-size:0.9rem;">' + ev.notes + '</div></div>') : '';
                    evCont.innerHTML = '<div class="card">' +
                        '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;"><h3 style="color:#60a5fa;">📊 بطاقة الدرجات الشهرية</h3><span class="badge badge-success">✓ معتمدة</span></div>' +
                        '<div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; text-align:center;">' +
                            '<div style="background:var(--card); padding:8px; border-radius:10px; border:1px solid var(--border);"><div style="font-size:0.75rem; color:var(--text-muted);">الشهري 1</div><div style="font-size:1.25rem; font-weight:800;">' + ev.exam1Score + '</div></div>' +
                            '<div style="background:var(--card); padding:8px; border-radius:10px; border:1px solid var(--border);"><div style="font-size:0.75rem; color:var(--text-muted);">الشهري 2</div><div style="font-size:1.25rem; font-weight:800;">' + ev.exam2Score + '</div></div>' +
                            '<div style="background:var(--card); padding:8px; border-radius:10px; border:1px solid var(--border);"><div style="font-size:0.75rem; color:var(--text-muted);">المشاركة</div><div style="font-size:1.25rem; font-weight:800; color:var(--success);">' + ev.participationScore + '</div></div>' +
                            '<div style="background:var(--card); padding:8px; border-radius:10px; border:1px solid var(--border);"><div style="font-size:0.75rem; color:var(--text-muted);">إضافي/خصم</div><div style="font-size:1.25rem; font-weight:800; color:' + (ev.bonusScore >= 0 ? '#60a5fa' : 'var(--danger)') + ';">' + (ev.bonusScore > 0 ? '+' : '') + ev.bonusScore + '</div></div>' +
                        '</div>' +
                        '<div style="background:linear-gradient(135deg, rgba(58,134,255,0.2) 0%, rgba(131,56,236,0.2) 100%); border:1px solid var(--primary); padding:10px; border-radius:10px; text-align:center; margin-top:10px;"><div style="font-size:0.8rem; color:var(--text-muted);">المجموع التراكمي</div><div style="font-size:1.8rem; font-weight:900; color:#60a5fa;">' + ev.totalScore + '</div></div>' +
                        noteHtml +
                    '</div>';
                } else {
                    evCont.innerHTML = '<div class="card" style="text-align:center; color:var(--text-muted);"><div style="font-size:1.8rem;">🔒</div><h3>الدرجات قيد المراجعة</h3><p style="font-size:0.85rem; margin-top:4px;">يقوم المعلم برصد ومراجعة الدرجات حالياً.</p></div>';
                }
            } catch(e) { showToast('خطأ في جلب الاختبارات', true); }
        }

        async function startQuiz(quizId) {
            try {
                const res = await fetch('/api/quiz?id=' + quizId + '&student=' + encodeURIComponent(currentStudent.username));
                const d = await res.json();
                if (!res.ok) return showToast(d.message || 'تعذر فتح الاختبار', true);

                activeQuiz = d;
                selectedAnswers = {};
                document.getElementById('activeQuizTitle').textContent = d.quiz.title;
                const qCont = document.getElementById('questionsContainer');

                let h = '';
                d.questions.forEach((q, idx) => {
                    h += '<div class="card" id="q_card_' + q.id + '">' +
                        '<div style="font-weight:700; font-size:1rem; margin-bottom:10px;">' + (idx + 1) + '. ' + q.questionText + '</div>' +
                        '<div>' +
                            '<div class="opt-label" id="lbl_' + q.id + '_A" onclick="pickOpt(' + q.id + ',\'A\')"><input type="radio" name="q_' + q.id + '" value="A"> ' + (q.optionA || 'أ') + '</div>' +
                            '<div class="opt-label" id="lbl_' + q.id + '_B" onclick="pickOpt(' + q.id + ',\'B\')"><input type="radio" name="q_' + q.id + '" value="B"> ' + (q.optionB || 'ب') + '</div>' +
                            (q.optionC ? ('<div class="opt-label" id="lbl_' + q.id + '_C" onclick="pickOpt(' + q.id + ',\'C\')"><input type="radio" name="q_' + q.id + '" value="C"> ' + q.optionC + '</div>') : '') +
                            (q.optionD ? ('<div class="opt-label" id="lbl_' + q.id + '_D" onclick="pickOpt(' + q.id + ',\'D\')"><input type="radio" name="q_' + q.id + '" value="D"> ' + q.optionD + '</div>') : '') +
                        '</div>' +
                    '</div>';
                });
                qCont.innerHTML = h;

                document.getElementById('dashboardView').style.display = 'none';
                document.getElementById('quizView').style.display = 'block';
                window.scrollTo({ top: 0, behavior: 'smooth' });
            } catch(e) { showToast('خطأ في تحميل الاختبار', true); }
        }

        function pickOpt(qid, val) {
            selectedAnswers[qid] = val;
            const card = document.getElementById('q_card_' + qid);
            card.querySelectorAll('.opt-label').forEach(l => l.classList.remove('selected'));
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
            submitQuiz();
        }

        async function submitQuiz() {
            // Anti-cheat: Check if device is using cellular/external network while connected
            if (antiCheatEnabled && navigator.connection && navigator.connection.type === 'cellular') {
                alert('⚠️ تنبيه أمني: تم اكتشاف اتصال بإنترنت شريحة الهاتف (4G/5G). يرجى إيقاف بيانات الهاتف والاتصال فقط بشبكة المعلم لتسليم الإجابات!');
                fetch('/api/cheat-alert', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ student: currentStudent.username, reason: 'استخدام بيانات الهاتف (4G/5G) أثناء حل الاختبار' })
                });
                return;
            }

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
                    alert('🎉 تم تسليم إجاباتك بنجاح!\nالدرجة: ' + d.score + ' من ' + d.totalPoints + ' (' + d.percentage + '%)');
                    showDashboard();
                } else showToast(d.message || 'فشل التسليم', true);
            } catch(e) { showToast('خطأ أثناء تسليم الإجابات', true); }
        }
    </script>
</body>
</html>
"""
