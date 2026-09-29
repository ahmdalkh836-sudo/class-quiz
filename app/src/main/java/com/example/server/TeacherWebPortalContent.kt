package com.example.server

object TeacherWebPortalContent {

    fun getTeacherHtml(): String {
        return """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة تحكم المعلم - Windows 11 & PC</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎓</text></svg>">
    <style>
        :root {
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --primary-light: #eff6ff;
            --success: #16a34a;
            --success-light: #dcfce7;
            --danger: #dc2626;
            --danger-light: #fee2e2;
            --warning: #d97706;
            --warning-light: #fef3c7;
            --bg: #f1f5f9;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --radius: 14px;
        }

        body.dark-mode {
            --primary: #3b82f6;
            --primary-dark: #60a5fa;
            --primary-light: rgba(59, 130, 246, 0.15);
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
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            background: var(--bg);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        header {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
            color: white;
            padding: 14px 24px;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-inner {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo-area {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-area h1 {
            font-size: 1.25rem;
            font-weight: 700;
        }

        .badge-pc {
            background: rgba(255,255,255,0.22);
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .main-container {
            max-width: 1200px;
            width: 100%;
            margin: 20px auto;
            padding: 0 20px;
            flex: 1;
        }

        .top-nav {
            display: flex;
            gap: 10px;
            background: var(--card-bg);
            padding: 6px;
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 20px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        }

        .nav-btn {
            background: transparent;
            border: none;
            padding: 10px 18px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-muted);
            transition: all 0.15s;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .nav-btn:hover {
            background: var(--primary-light);
            color: var(--primary);
        }

        .nav-btn.active {
            background: var(--primary);
            color: white;
        }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        }

        .grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 18px;
        }

        .btn {
            background: var(--primary);
            color: white;
            border: none;
            padding: 9px 16px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            transition: opacity 0.15s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .btn:hover {
            opacity: 0.9;
        }

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
            background: rgba(0,0,0,0.02);
            font-weight: 700;
            color: var(--text-muted);
        }

        .student-row:hover {
            background: rgba(37,99,235,0.03);
        }

        .toast {
            position: fixed;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%);
            background: #0f172a;
            color: white;
            padding: 12px 24px;
            border-radius: 10px;
            display: none;
            z-index: 9999;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        /* Modal Styles */
        .modal-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(15,23,42,0.6);
            backdrop-filter: blur(4px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            padding: 20px;
        }

        .modal-content {
            background: var(--card-bg);
            border-radius: 16px;
            max-width: 600px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            padding: 24px;
            border: 1px solid var(--border);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
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
            font-size: 0.95rem;
            background: var(--card-bg);
            color: var(--text-main);
        }

        .form-input:focus {
            outline: none;
            border-color: var(--primary);
        }
    </style>
</head>
<body>
    <header>
        <div class="header-inner">
            <div class="logo-area">
                <span style="font-size: 1.6rem;">🎓</span>
                <div>
                    <h1>لوحة تحكم المعلم (Windows 11 & PC)</h1>
                    <div style="font-size: 0.78rem; opacity: 0.9;">خادم الاختبارات المدرسية التفاعلية • اتصال شبكي محلي</div>
                </div>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
                <span class="badge-pc">💻 متوافق مع Windows 11</span>
                <button onclick="fetchData()" class="btn btn-outline" style="color: white; border-color: rgba(255,255,255,0.4); padding:6px 12px; font-size:0.82rem;">تحديث البيانات 🔄</button>
            </div>
        </div>
    </header>

    <div class="main-container">
        <!-- Navigation Tabs -->
        <div class="top-nav">
            <button id="navStudents" class="nav-btn active" onclick="switchNav('students')">
                👥 سجل الطلاب والدرجات الشهرية
            </button>
            <button id="navQuizzes" class="nav-btn" onclick="switchNav('quizzes')">
                📝 بنك الاختبارات والأنشطة
            </button>
            <button id="navSubmissions" class="nav-btn" onclick="switchNav('submissions')">
                📊 التسليمات والنتائج الحية
            </button>
            <button id="navWindowsGuide" class="nav-btn" onclick="switchNav('guide')">
                💻 دليل Windows 11 والتثبيت
            </button>
        </div>

        <!-- SECTION 1: Students & Grades -->
        <div id="sectionStudents">
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <h2 style="font-size: 1.2rem;">قائمة الطلاب المسجلين وتقييم الدرجات</h2>
                        <p style="font-size: 0.85rem; color: var(--text-muted);">مقسّمة بحسب الفصول والشعب مع إمكانية رصد درجات الاختبارات الشهرية والمشاركة</p>
                    </div>
                    <div style="display: flex; gap: 10px;">
                        <button id="globalGradesToggleBtn" onclick="toggleGlobalVisibility()" class="btn btn-outline">
                            👁️ إخفاء/إظهار الدرجات للجميع
                        </button>
                    </div>
                </div>
                <div style="margin-top: 14px;">
                    <input type="text" id="studentSearchInput" onkeyup="filterStudentsTable()" placeholder="ابحث باسم الطالب، رقم الهوية، أو الفصل..." class="form-input" style="max-width: 400px;">
                </div>
            </div>

            <div id="studentsContainer"></div>
        </div>

        <!-- SECTION 2: Quizzes -->
        <div id="sectionQuizzes" style="display: none;">
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h2 style="font-size: 1.2rem;">إدارة الاختبارات والأنشطة</h2>
                        <p style="font-size: 0.85rem; color: var(--text-muted);">إنشاء واختيار وتفعيل الاختبارات المتاحة للطلاب في الفصل</p>
                    </div>
                    <button onclick="openCreateQuizModal()" class="btn btn-success">+ إنشاء اختبار جديد من لوحة المفاتيح</button>
                </div>
            </div>
            <div id="quizzesContainer" class="grid-2"></div>
        </div>

        <!-- SECTION 3: Submissions -->
        <div id="sectionSubmissions" style="display: none;">
            <div class="card">
                <h2 style="font-size: 1.2rem;">سجل تسليمات الاختبارات الفورية</h2>
                <p style="font-size: 0.85rem; color: var(--text-muted);">جميع إجابات الطلاب التي تم تسليمها واعتمادها</p>
                <div style="overflow-x: auto; margin-top: 14px;">
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>اسم الطالب</th>
                                <th>عنوان الاختبار</th>
                                <th>الدرجة</th>
                                <th>النسبة</th>
                                <th>وقت التسليم</th>
                            </tr>
                        </thead>
                        <tbody id="submissionsTableBody"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- SECTION 4: Windows 11 Integration Guide -->
        <div id="sectionGuide" style="display: none;">
            <div class="card">
                <h2 style="font-size: 1.25rem; color: var(--primary);">💻 طرق تشغيل البرنامج على Windows 11</h2>
                <p style="font-size: 0.9rem; color: var(--text-muted); margin-top: 4px;">يمكنك استخدام النظام على كمبيوتر أو لابتوب ويندوز 11 بثلاث طرق مريحة:</p>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 20px;">
                    <div style="background: rgba(37,99,235,0.06); border: 1.5px solid var(--primary); border-radius: 12px; padding: 16px;">
                        <h3 style="color: var(--primary); font-size: 1.05rem;">1. لوحة تحكم المتصفح (Edge / Chrome)</h3>
                        <p style="font-size: 0.88rem; margin-top: 8px; color: var(--text-main);">
                            أسهل وأسرع طريقة! ما دمت متصلاً بنفس راوتر المدرسة أو واي فاي الهاتف، يمكنك فتح الرابط <code>http://[IP]:8080/teacher</code> على كمبيوتر ويندوز 11 لإدارة كل شيء بشاشة كاملة وبلوحة مفاتيح سريعة.
                        </p>
                    </div>

                    <div style="background: rgba(22,163,74,0.06); border: 1.5px solid var(--success); border-radius: 12px; padding: 16px;">
                        <h3 style="color: var(--success); font-size: 1.05rem;">2. تثبيت كتطبيق على Windows 11 (PWA)</h3>
                        <p style="font-size: 0.88rem; margin-top: 8px; color: var(--text-main);">
                            في متصفح Microsoft Edge أو Google Chrome على ويندوز 11، اضغط على أيقونة (تثبيت التطبيق / Install App) في شريط العنوان بالأعلى لتثبيته كبرنامج مستقل على شريط المهام وقائمة Start لويندوز 11.
                        </p>
                    </div>

                    <div style="background: rgba(217,119,6,0.06); border: 1.5px solid var(--warning); border-radius: 12px; padding: 16px;">
                        <h3 style="color: var(--warning); font-size: 1.05rem;">3. تشغيل ملف APK على Windows 11</h3>
                        <p style="font-size: 0.88rem; margin-top: 8px; color: var(--text-main);">
                            يدعم ويندوز 11 تشغيل تطبيقات الأندرويد مباشرة عبر Windows Subsystem for Android (WSA) أو عبر محاكيات مثل BlueStacks أو LDPlayer بتثبيت ملف الـ APK الصادر من التطبيق.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Student Evaluation Modal -->
    <div id="evalModal" class="modal-overlay">
        <div class="modal-content">
            <h3 id="modalStudentName" style="font-size: 1.2rem; color: var(--primary); margin-bottom: 16px;">رصد درجات الطالب</h3>
            <input type="hidden" id="modalStudentId">

            <div class="form-group">
                <label>الفصل والشعبة:</label>
                <input type="text" id="modalGradeSection" class="form-input">
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div class="form-group">
                    <label>الاختبار الشهري الأول:</label>
                    <input type="number" step="0.5" id="modalExam1" class="form-input">
                </div>
                <div class="form-group">
                    <label>الاختبار الشهري الثاني:</label>
                    <input type="number" step="0.5" id="modalExam2" class="form-input">
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div class="form-group">
                    <label>درجة المشاركة:</label>
                    <input type="number" step="0.5" id="modalPart" class="form-input">
                </div>
                <div class="form-group">
                    <label>نقاط إضافية / خصم (+/-):</label>
                    <input type="number" step="0.5" id="modalBonus" class="form-input">
                </div>
            </div>

            <div class="form-group">
                <label>ملاحظات المعلم وتوجيهاته للطالب:</label>
                <textarea id="modalNotes" rows="3" class="form-input"></textarea>
            </div>

            <div style="display: flex; gap: 20px; margin: 14px 0;">
                <label style="display: flex; align-items: center; gap: 6px; cursor: pointer;">
                    <input type="checkbox" id="modalShowGrades">
                    <span>إظهار الدرجات للطالب في بوابته</span>
                </label>
                <label style="display: flex; align-items: center; gap: 6px; cursor: pointer;">
                    <input type="checkbox" id="modalShowNotes">
                    <span>إظهار الملاحظات للطالب</span>
                </label>
            </div>

            <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 18px;">
                <button onclick="closeEvalModal()" class="btn btn-outline">إلغاء</button>
                <button onclick="saveStudentEvaluation()" class="btn btn-success">حفظ التقييم والدرجات ✓</button>
            </div>
        </div>
    </div>

    <!-- Create Quiz Modal -->
    <div id="quizModal" class="modal-overlay">
        <div class="modal-content" style="max-width: 700px;">
            <h3 style="font-size: 1.2rem; color: var(--primary); margin-bottom: 16px;">إنشاء اختبار جديد (عبر Windows 11)</h3>
            <div class="form-group">
                <label>عنوان الاختبار:</label>
                <input type="text" id="newQuizTitle" class="form-input" placeholder="مثال: الاختبار الفتري الأول في الرياضيات">
            </div>
            <div class="form-group">
                <label>الوصف أو التعليمات:</label>
                <input type="text" id="newQuizDesc" class="form-input" placeholder="مثال: أجب عن جميع الأسئلة بدقة">
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

            <h4 style="margin: 14px 0 8px 0; font-size: 1rem;">الأسئلة (اختيار من متعدد):</h4>
            <div id="newQuestionsList"></div>
            <button onclick="addQuestionField()" class="btn btn-outline" style="margin-top: 8px;">+ إضافة سؤال آخر</button>

            <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px;">
                <button onclick="closeQuizModal()" class="btn btn-outline">إلغاء</button>
                <button onclick="submitNewQuiz()" class="btn btn-success">حفظ ونشر الاختبار للطلاب ✓</button>
            </div>
        </div>
    </div>

    <div id="toast" class="toast"></div>

    <script>
        let allStudents = [];
        let allQuizzes = [];
        let allSubmissions = [];
        let globalVisibility = true;

        window.addEventListener('DOMContentLoaded', () => {
            fetchData();
        });

        function showToast(msg) {
            const t = document.getElementById('toast');
            t.textContent = msg;
            t.style.display = 'block';
            setTimeout(() => { t.style.display = 'none'; }, 3200);
        }

        function switchNav(nav) {
            ['students', 'quizzes', 'submissions', 'guide'].forEach(n => {
                const sec = document.getElementById('section' + n.charAt(0).toUpperCase() + n.slice(1));
                const btn = document.getElementById('nav' + n.charAt(0).toUpperCase() + n.slice(1));
                if (sec) sec.style.display = (n === nav) ? 'block' : 'none';
                if (btn) {
                    if (n === nav) btn.classList.add('active');
                    else btn.classList.remove('active');
                }
            });
        }

        async function fetchData() {
            try {
                const res = await fetch('/api/teacher/data');
                const data = await res.json();
                allStudents = data.students || [];
                allQuizzes = data.quizzes || [];
                allSubmissions = data.submissions || [];
                globalVisibility = data.areGradesVisibleGlobally !== false;

                updateGlobalVisibilityButton();
                renderStudents(allStudents);
                renderQuizzes(allQuizzes);
                renderSubmissions(allSubmissions);
                showToast('تم تحديث البيانات من الخادم بنجاح');
            } catch (e) {
                showToast('تعذر جلب البيانات من الخادم');
            }
        }

        function updateGlobalVisibilityButton() {
            const btn = document.getElementById('globalGradesToggleBtn');
            if (globalVisibility) {
                btn.innerHTML = '👁️ إخفاء الدرجات عن الجميع';
                btn.className = 'btn btn-outline';
            } else {
                btn.innerHTML = '🔒 إظهار الدرجات للجميع';
                btn.className = 'btn btn-success';
            }
        }

        async function toggleGlobalVisibility() {
            try {
                const res = await fetch('/api/teacher/toggle-visibility', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ visible: !globalVisibility })
                });
                const d = await res.json();
                if (d.success) {
                    globalVisibility = d.visible;
                    updateGlobalVisibilityButton();
                    showToast(globalVisibility ? 'تم إظهار الدرجات لجميع الطلاب' : 'تم إخفاء الدرجات عن جميع الطلاب');
                }
            } catch (e) {
                showToast('حدث خطأ أثناء تعديل الظهور');
            }
        }

        function renderStudents(students) {
            const container = document.getElementById('studentsContainer');
            if (students.length === 0) {
                container.innerHTML = '<div class="card" style="text-align:center; color:var(--text-muted);">لا يوجد طلاب مسجلون بعد.</div>';
                return;
            }

            // Group by Class & Section
            const groups = {};
            students.forEach(s => {
                const key = s.gradeSection ? s.gradeSection : 'بدون فصل محدد';
                if (!groups[key]) groups[key] = [];
                groups[key].push(s);
            });

            let html = '';
            for (const [classTitle, stList] of Object.entries(groups)) {
                html += '<div class="card">' +
                    '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">' +
                        '<h3 style="color:var(--primary); font-size:1.15rem;">🏫 ' + classTitle + ' (' + stList.length + ' طالب)</h3>' +
                    '</div>' +
                    '<div style="overflow-x:auto;">' +
                        '<table>' +
                            '<thead>' +
                                '<tr>' +
                                    '<th>اسم الطالب</th>' +
                                    '<th>الهوية</th>' +
                                    '<th>شهري 1</th>' +
                                    '<th>شهري 2</th>' +
                                    '<th>مشاركة</th>' +
                                    '<th>إضافي</th>' +
                                    '<th>المجموع</th>' +
                                    '<th>الظهور</th>' +
                                    '<th>ملاحظات</th>' +
                                    '<th>إجراءات سريعة</th>' +
                                '</tr>' +
                            '</thead>' +
                            '<tbody>';

                stList.forEach(st => {
                    const total = (st.exam1Score || 0) + (st.exam2Score || 0) + (st.participationScore || 0) + (st.bonusScore || 0);
                    html += '<tr class="student-row">' +
                        '<td style="font-weight:700;">' + st.username + '</td>' +
                        '<td>' + (st.nationalId || '-') + '</td>' +
                        '<td>' + st.exam1Score + '</td>' +
                        '<td>' + st.exam2Score + '</td>' +
                        '<td>' + st.participationScore + '</td>' +
                        '<td>' + (st.bonusScore > 0 ? '+' : '') + st.bonusScore + '</td>' +
                        '<td style="font-weight:800; color:var(--primary);">' + total.toFixed(1) + '</td>' +
                        '<td>' + (st.showGradesToStudent ? '👁️ ظاهر' : '🔒 مخفي') + '</td>' +
                        '<td style="max-width:180px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">' + (st.notes || '-') + '</td>' +
                        '<td>' +
                            '<button onclick="quickBonus(' + st.id + ', 1)" class="btn btn-outline" style="padding:4px 8px; font-size:0.78rem;">+1</button> ' +
                            '<button onclick="quickBonus(' + st.id + ', -1)" class="btn btn-outline" style="padding:4px 8px; font-size:0.78rem; color:var(--danger);">-1</button> ' +
                            '<button onclick="openEvalModal(' + st.id + ')" class="btn" style="padding:4px 10px; font-size:0.78rem;">تعديل الدرجات 📝</button>' +
                        '</td>' +
                    '</tr>';
                });

                html += '</tbody></table></div></div>';
            }
            container.innerHTML = html;
        }

        async function quickBonus(studentId, delta) {
            try {
                const res = await fetch('/api/teacher/bonus', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ studentId, delta })
                });
                if (res.ok) {
                    fetchData();
                    showToast('تم تعديل الدرجة بنجاح');
                }
            } catch (e) {
                showToast('فشل تعديل الدرجة');
            }
        }

        function openEvalModal(studentId) {
            const student = allStudents.find(s => s.id === studentId);
            if (!student) return;

            document.getElementById('modalStudentId').value = student.id;
            document.getElementById('modalStudentName').textContent = 'رصد درجات: ' + student.username;
            document.getElementById('modalGradeSection').value = student.gradeSection || '';
            document.getElementById('modalExam1').value = student.exam1Score || 0;
            document.getElementById('modalExam2').value = student.exam2Score || 0;
            document.getElementById('modalPart').value = student.participationScore || 0;
            document.getElementById('modalBonus').value = student.bonusScore || 0;
            document.getElementById('modalNotes').value = student.notes || '';
            document.getElementById('modalShowGrades').checked = student.showGradesToStudent !== false;
            document.getElementById('modalShowNotes').checked = student.showNotesToStudent !== false;

            document.getElementById('evalModal').style.display = 'flex';
        }

        function closeEvalModal() {
            document.getElementById('evalModal').style.display = 'none';
        }

        async function saveStudentEvaluation() {
            const id = parseInt(document.getElementById('modalStudentId').value);
            const payload = {
                studentId: id,
                gradeSection: document.getElementById('modalGradeSection').value.trim(),
                exam1: parseFloat(document.getElementById('modalExam1').value) || 0,
                exam2: parseFloat(document.getElementById('modalExam2').value) || 0,
                participation: parseFloat(document.getElementById('modalPart').value) || 0,
                bonus: parseFloat(document.getElementById('modalBonus').value) || 0,
                notes: document.getElementById('modalNotes').value.trim(),
                showGrades: document.getElementById('modalShowGrades').checked,
                showNotes: document.getElementById('modalShowNotes').checked
            };

            try {
                const res = await fetch('/api/teacher/evaluate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                if (res.ok) {
                    closeEvalModal();
                    fetchData();
                    showToast('تم حفظ التقييم بنجاح!');
                }
            } catch (e) {
                showToast('فشل حفظ التقييم');
            }
        }

        function renderQuizzes(quizzes) {
            const container = document.getElementById('quizzesContainer');
            if (quizzes.length === 0) {
                container.innerHTML = '<div class="card" style="text-align:center;">لا توجد اختبارات مضافة.</div>';
                return;
            }
            let html = '';
            quizzes.forEach(q => {
                html += '<div class="card">' +
                    '<div style="display:flex; justify-content:space-between; align-items:center;">' +
                        '<h3 style="font-size:1.1rem;">' + q.title + '</h3>' +
                        '<span class="badge-pc" style="background:' + (q.isActive ? 'var(--success-light)' : 'var(--danger-light)') + '; color:' + (q.isActive ? 'var(--success)' : 'var(--danger)') + ';">' + (q.isActive ? 'نشط ومتاح' : 'مغلق') + '</span>' +
                    '</div>' +
                    '<p style="font-size:0.88rem; color:var(--text-muted); margin:8px 0;">' + (q.description || 'بدون تعليمات') + '</p>' +
                    '<div style="display:flex; justify-content:space-between; align-items:center; margin-top:14px;">' +
                        '<span style="font-size:0.82rem; color:var(--text-muted);">⏱️ ' + q.durationMinutes + ' دقيقة</span>' +
                        '<button onclick="toggleQuiz(' + q.id + ', ' + q.isActive + ')" class="btn ' + (q.isActive ? 'btn-danger' : 'btn-success') + '">' + (q.isActive ? 'إغلاق الاختبار 🔒' : 'تفعيل الاختبار 🔓') + '</button>' +
                    '</div>' +
                '</div>';
            });
            container.innerHTML = html;
        }

        async function toggleQuiz(quizId, currentActive) {
            try {
                await fetch('/api/teacher/toggle-quiz', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ quizId, isActive: !currentActive })
                });
                fetchData();
            } catch (e) {
                showToast('فشل تغيير حالة الاختبار');
            }
        }

        function renderSubmissions(submissions) {
            const tbody = document.getElementById('submissionsTableBody');
            if (submissions.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:var(--text-muted);">لا توجد تسليمات حتى الآن.</td></tr>';
                return;
            }
            let html = '';
            submissions.forEach((s, idx) => {
                const dateStr = new Date(s.submittedAt).toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' });
                const pct = s.totalPoints > 0 ? Math.round((s.score * 100) / s.totalPoints) : 100;
                html += '<tr>' +
                    '<td>' + (idx + 1) + '</td>' +
                    '<td style="font-weight:700;">' + s.studentUsername + '</td>' +
                    '<td>' + (s.quizTitle || 'اختبار') + '</td>' +
                    '<td style="font-weight:700; color:var(--primary);">' + s.score + ' / ' + s.totalPoints + '</td>' +
                    '<td>' + pct + '%</td>' +
                    '<td>' + dateStr + '</td>' +
                '</tr>';
            });
            tbody.innerHTML = html;
        }

        // Quiz Creation
        function openCreateQuizModal() {
            document.getElementById('newQuestionsList').innerHTML = '';
            addQuestionField();
            document.getElementById('quizModal').style.display = 'flex';
        }

        function closeQuizModal() {
            document.getElementById('quizModal').style.display = 'none';
        }

        let qCount = 0;
        function addQuestionField() {
            qCount++;
            const list = document.getElementById('newQuestionsList');
            const div = document.createElement('div');
            div.style.cssText = 'background:rgba(0,0,0,0.02); border:1px solid var(--border); border-radius:10px; padding:12px; margin-bottom:10px;';
            div.innerHTML = '<div class="form-group">' +
                '<label>نص السؤال ' + qCount + ':</label>' +
                '<input type="text" class="form-input q-text" placeholder="اكتب السؤال هنا...">' +
            '</div>' +
            '<div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">' +
                '<input type="text" class="form-input q-optA" placeholder="الخيار أ">' +
                '<input type="text" class="form-input q-optB" placeholder="الخيار ب">' +
                '<input type="text" class="form-input q-optC" placeholder="الخيار ج">' +
                '<input type="text" class="form-input q-optD" placeholder="الخيار د">' +
            '</div>' +
            '<div class="form-group" style="margin-top:8px;">' +
                '<label>الإجابة الصحيحة:</label>' +
                '<select class="form-input q-correct">' +
                    '<option value="A">الخيار (أ)</option>' +
                    '<option value="B">الخيار (ب)</option>' +
                    '<option value="C">الخيار (ج)</option>' +
                    '<option value="D">الخيار (د)</option>' +
                '</select>' +
            '</div>';
            list.appendChild(div);
        }

        async function submitNewQuiz() {
            const title = document.getElementById('newQuizTitle').value.trim();
            const desc = document.getElementById('newQuizDesc').value.trim();
            const duration = parseInt(document.getElementById('newQuizDuration').value) || 10;
            const type = document.getElementById('newQuizType').value;

            if (!title) {
                showToast('يرجى كتابة عنوان الاختبار');
                return;
            }

            const questions = [];
            document.querySelectorAll('#newQuestionsList > div').forEach(d => {
                const text = d.querySelector('.q-text').value.trim();
                if (text) {
                    questions.push({
                        questionText: text,
                        optionA: d.querySelector('.q-optA').value.trim() || 'خيار 1',
                        optionB: d.querySelector('.q-optB').value.trim() || 'خيار 2',
                        optionC: d.querySelector('.q-optC').value.trim() || '',
                        optionD: d.querySelector('.q-optD').value.trim() || '',
                        correctAnswer: d.querySelector('.q-correct').value,
                        points: 1,
                        questionType: 'MULTIPLE_CHOICE'
                    });
                }
            });

            if (questions.length === 0) {
                showToast('يرجى إضافة سؤال واحد على الأقل');
                return;
            }

            try {
                const res = await fetch('/api/teacher/create-quiz', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ title, description: desc, durationMinutes: duration, type, questions })
                });
                if (res.ok) {
                    closeQuizModal();
                    fetchData();
                    showToast('تم إنشاء ونشر الاختبار بنجاح!');
                }
            } catch (e) {
                showToast('فشل إنشاء الاختبار');
            }
        }
    </script>
</body>
</html>
        """.trimIndent()
    }
}
