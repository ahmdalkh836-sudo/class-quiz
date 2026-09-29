#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classroom Quiz Server - Windows 11 Desktop Edition
خادم بث الاختبارات المدرسية المباشر عبر شبكة الواي فاي المحلية
يدعم تسجيل المعلم، تسجيل الطلاب وتحديد المرحلة والشعبة، تخصيص وتعديل الاختبارات، والتشفير
"""

import http.server
import socketserver
import sqlite3
import json
import socket
import urllib.parse
import webbrowser
import threading
import sys
import os
import time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from server_html import STUDENT_HTML, TEACHER_HTML
from crypto_helper import encrypt_students_aes, decrypt_students_aes

PORT = 8080
DB_FILE = os.path.join(BASE_DIR, "classroom_data.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # 1. Settings table
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    defaults = [
        ("session_open", "1"),
        ("grades_globally_visible", "1"),
        ("teacher_setup_completed", "0"),
        ("teacher_password", ""),
        ("teacher_username", "admin"),
        ("teacher_name", "الأستاذ / المعلم"),
        ("teacher_subject", "المادة التعليمية"),
        ("teacher_phone", ""),
        ("anti_cheat", "1"),
        ("prevent_retake", "1")
    ]
    for k, v in defaults:
        c.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (k, v))

    # 2. Logs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            message TEXT,
            time TEXT,
            timestamp INTEGER
        )
    ''')

    # 3. Students table
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE COLLATE NOCASE,
            nationalId TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            grade TEXT DEFAULT '',
            section TEXT DEFAULT '',
            gradeSection TEXT DEFAULT '',
            password TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            exam1Score REAL DEFAULT 0.0,
            exam2Score REAL DEFAULT 0.0,
            participationScore REAL DEFAULT 0.0,
            bonusScore REAL DEFAULT 0.0,
            showGradesToStudent INTEGER DEFAULT 1,
            showNotesToStudent INTEGER DEFAULT 1,
            createdAt INTEGER
        )
    ''')

    # 4. Quizzes table
    c.execute('''
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT DEFAULT '',
            durationMinutes INTEGER DEFAULT 10,
            targetGrade TEXT DEFAULT 'الكل',
            targetSection TEXT DEFAULT 'الكل',
            isActive INTEGER DEFAULT 1,
            type TEXT DEFAULT 'QUIZ',
            createdAt INTEGER
        )
    ''')

    # 5. Questions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quizId INTEGER,
            questionText TEXT,
            questionType TEXT DEFAULT 'MULTIPLE_CHOICE',
            optionA TEXT DEFAULT '',
            optionB TEXT DEFAULT '',
            optionC TEXT DEFAULT '',
            optionD TEXT DEFAULT '',
            correctAnswer TEXT DEFAULT 'A',
            points INTEGER DEFAULT 1,
            FOREIGN KEY (quizId) REFERENCES quizzes(id) ON DELETE CASCADE
        )
    ''')

    # 6. Submissions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quizId INTEGER,
            studentUsername TEXT,
            score INTEGER DEFAULT 0,
            totalPoints INTEGER DEFAULT 1,
            answersJson TEXT DEFAULT '{}',
            submittedAt INTEGER,
            FOREIGN KEY (quizId) REFERENCES quizzes(id) ON DELETE CASCADE
        )
    ''')

    # Migration for existing databases
    c.execute("PRAGMA table_info(students)")
    st_cols = [r[1] for r in c.fetchall()]
    if 'grade' not in st_cols:
        c.execute("ALTER TABLE students ADD COLUMN grade TEXT DEFAULT ''")
    if 'section' not in st_cols:
        c.execute("ALTER TABLE students ADD COLUMN section TEXT DEFAULT ''")

    c.execute("PRAGMA table_info(quizzes)")
    qz_cols = [r[1] for r in c.fetchall()]
    if 'targetGrade' not in qz_cols:
        c.execute("ALTER TABLE quizzes ADD COLUMN targetGrade TEXT DEFAULT 'الكل'")
    if 'targetSection' not in qz_cols:
        c.execute("ALTER TABLE quizzes ADD COLUMN targetSection TEXT DEFAULT 'الكل'")

    # Seed initial starter quiz if database is new
    c.execute('SELECT COUNT(*) FROM quizzes')
    if c.fetchone()[0] == 0:
        now = int(time.time() * 1000)
        c.execute('''
            INSERT INTO quizzes (title, description, durationMinutes, targetGrade, targetSection, isActive, type, createdAt)
            VALUES (?, ?, ?, 'الكل', 'الكل', 1, 'QUIZ', ?)
        ''', ("اختبار مراجعة الحصة الأول", "اختبار قصير للتأكد من استيعاب المفاهيم الأساسية", 5, now))
        qid = c.lastrowid
        questions = [
            (qid, "ما هي وحدة قياس القوة في النظام الدولي للوحدات (SI)؟", "MULTIPLE_CHOICE", "النيوتن (Newton)", "الجول (Joule)", "الواط (Watt)", "الباسكال (Pascal)", "A", 2),
            (qid, "تتحرك الإلكترونات حول النواة في مستويات طاقة محددة.", "MULTIPLE_CHOICE", "صح", "خطأ", "", "", "A", 1),
            (qid, "أي كوكب هو الأقرب إلى الشمس في المجموعة الشمسية؟", "MULTIPLE_CHOICE", "الزهرة", "عطارد", "المريخ", "الأرض", "B", 2)
        ]
        c.executemany('''
            INSERT INTO questions (quizId, questionText, questionType, optionA, optionB, optionC, optionD, correctAnswer, points)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', questions)
        add_log_direct(c, "SYSTEM", "تم إنشاء قاعدة البيانات وتهيئة اختبار المراجعة الأولي")

    conn.commit()
    conn.close()

def add_log_direct(cursor, log_type, message):
    now_ts = int(time.time() * 1000)
    time_str = datetime.now().strftime("%H:%M:%S")
    cursor.execute('INSERT INTO logs (type, message, time, timestamp) VALUES (?, ?, ?, ?)',
                   (log_type, message, time_str, now_ts))

def add_log(log_type, message):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    add_log_direct(c, log_type, message)
    conn.commit()
    conn.close()

def get_local_ips():
    ips = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(("8.8.8.8", 80))
        primary = s.getsockname()[0]
        s.close()
        if primary and not primary.startswith("127."):
            ips.append(primary)
    except Exception:
        pass

    try:
        host = socket.gethostname()
        for ip in socket.gethostbyname_ex(host)[2]:
            if not ip.startswith("127.") and ip not in ips:
                ips.append(ip)
    except Exception:
        pass

    if not ips:
        ips.append("127.0.0.1")
    return ips

def get_setting(key, default=""):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT value FROM settings WHERE key=?', (key,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else default

def set_setting(key, value):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, str(value)))
    conn.commit()
    conn.close()

class ClassroomHandler(http.server.BaseHTTPRequestHandler):

    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def send_json(self, status, payload):
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(data)

    def send_html(self, html_content):
        data = html_content.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # 1. Student Portal Page
        if path in ['/', '/portal', '/index.html']:
            self.send_html(STUDENT_HTML)
            return

        # 2. Teacher Windows 11 Dashboard
        if path in ['/teacher', '/admin', '/teacher.html']:
            self.send_html(TEACHER_HTML)
            return

        # 3. GET /api/status
        if path == '/api/status':
            self.send_json(200, {
                "isOpen": (get_setting("session_open", "1") == "1"),
                "antiCheat": (get_setting("anti_cheat", "1") == "1"),
                "preventRetake": (get_setting("prevent_retake", "1") == "1"),
                "port": PORT,
                "serverIps": get_local_ips()
            })
            return

        # 4. GET /api/teacher/auth-status
        if path == '/api/teacher/auth-status':
            is_setup = (get_setting("teacher_setup_completed", "0") == "1")
            pwd = get_setting("teacher_password", "")
            # If password is empty, setup is not done
            has_password = bool(pwd and pwd.strip())
            self.send_json(200, {
                "isSetup": is_setup and has_password,
                "teacherName": get_setting("teacher_name", "الأستاذ / المعلم"),
                "teacherSubject": get_setting("teacher_subject", "المادة التعليمية"),
                "teacherUsername": get_setting("teacher_username", "")
            })
            return

        # 5. GET /api/quizzes
        if path == '/api/quizzes':
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM quizzes WHERE isActive = 1 ORDER BY createdAt DESC')
            quizzes = [dict(r) for r in c.fetchall()]
            for q in quizzes:
                c.execute('SELECT COUNT(*) FROM questions WHERE quizId = ?', (q['id'],))
                q['questionCount'] = c.fetchone()[0]
            conn.close()
            self.send_json(200, quizzes)
            return

        # 6. GET /api/quiz?id=X&student=Y
        if path == '/api/quiz':
            qid = query.get('id', [None])[0]
            student = query.get('student', [''])[0].strip()
            if not qid:
                self.send_json(400, {"message": "رقم الاختبار مطلوب"})
                return

            prevent_retake = (get_setting("prevent_retake", "1") == "1")
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            if student and prevent_retake:
                c.execute('SELECT id FROM submissions WHERE quizId = ? AND LOWER(TRIM(studentUsername)) = LOWER(TRIM(?)) LIMIT 1', (qid, student))
                if c.fetchone():
                    conn.close()
                    self.send_json(400, {"error": "ALREADY_SUBMITTED", "message": "لقد قمت بحل هذا الاختبار مسبقاً! ميزة منع الإعادة مفعلة."})
                    return

            c.execute('SELECT * FROM quizzes WHERE id = ?', (qid,))
            quiz_row = c.fetchone()
            if not quiz_row:
                conn.close()
                self.send_json(404, {"message": "الاختبار غير موجود"})
                return

            c.execute('''
                SELECT id, questionText, questionType, optionA, optionB, optionC, optionD, points
                FROM questions WHERE quizId = ? ORDER BY id ASC
            ''', (qid,))
            questions = [dict(r) for r in c.fetchall()]
            conn.close()

            self.send_json(200, {"quiz": dict(quiz_row), "questions": questions})
            return

        # 7. GET /api/student-quizzes?student=X
        if path == '/api/student-quizzes':
            student = query.get('student', [''])[0].strip()
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute('SELECT * FROM students WHERE LOWER(TRIM(username)) = LOWER(TRIM(?)) LIMIT 1', (student,))
            srow = c.fetchone()
            sdict = dict(srow) if srow else {}
            st_grade = sdict.get('grade', '').strip()
            st_sec = sdict.get('section', '').strip()

            c.execute('SELECT * FROM quizzes WHERE isActive = 1 ORDER BY createdAt DESC')
            all_active = [dict(r) for r in c.fetchall()]

            # Target Grade and Section Filtering
            targeted_quizzes = []
            for q in all_active:
                t_grade = (q.get('targetGrade') or 'الكل').strip()
                t_sec = (q.get('targetSection') or 'الكل').strip()

                grade_match = (t_grade == 'الكل' or not st_grade or t_grade == st_grade)
                sec_match = (t_sec == 'الكل' or not st_sec or t_sec == st_sec)

                if grade_match and sec_match:
                    targeted_quizzes.append(q)

            submitted_qids = set()
            completed = []
            if student:
                c.execute('SELECT * FROM submissions WHERE LOWER(TRIM(studentUsername)) = LOWER(TRIM(?)) ORDER BY submittedAt DESC', (student,))
                for s in c.fetchall():
                    s_dict = dict(s)
                    submitted_qids.add(s_dict['quizId'])
                    c.execute('SELECT title FROM quizzes WHERE id = ?', (s_dict['quizId'],))
                    qr = c.fetchone()
                    s_dict['title'] = qr[0] if qr else "اختبار منجز"
                    pct = round((s_dict['score'] * 100) / s_dict['totalPoints']) if s_dict['totalPoints'] > 0 else 100
                    s_dict['percentage'] = pct
                    completed.append(s_dict)

            unattempted = [q for q in targeted_quizzes if q['id'] not in submitted_qids]

            glob_visible = (get_setting("grades_globally_visible", "1") == "1")
            effective_visible = glob_visible and (sdict.get('showGradesToStudent', 1) == 1)
            total = (sdict.get('exam1Score', 0) or 0) + (sdict.get('exam2Score', 0) or 0) + (sdict.get('participationScore', 0) or 0) + (sdict.get('bonusScore', 0) or 0)

            eval_obj = {
                "isVisible": effective_visible,
                "exam1Score": sdict.get('exam1Score', 0.0),
                "exam2Score": sdict.get('exam2Score', 0.0),
                "participationScore": sdict.get('participationScore', 0.0),
                "bonusScore": sdict.get('bonusScore', 0.0),
                "totalScore": round(total, 1),
                "notes": sdict.get('notes', '') if (effective_visible and sdict.get('showNotesToStudent', 1) == 1) else "",
                "hasNotes": bool(sdict.get('notes')),
                "grade": sdict.get('grade', ''),
                "section": sdict.get('section', ''),
                "gradeSection": sdict.get('gradeSection', '')
            }

            conn.close()
            self.send_json(200, {
                "unattempted": unattempted,
                "completed": completed,
                "evaluation": eval_obj
            })
            return

        # 8. GET /api/teacher/quiz-detail?id=X
        if path == '/api/teacher/quiz-detail':
            qid = query.get('id', [None])[0]
            if not qid:
                self.send_json(400, {"message": "رقم الاختبار مطلوب"})
                return
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM quizzes WHERE id = ?', (qid,))
            q_row = c.fetchone()
            if not q_row:
                conn.close()
                self.send_json(404, {"message": "الاختبار غير موجود"})
                return
            c.execute('SELECT * FROM questions WHERE quizId = ? ORDER BY id ASC', (qid,))
            questions = [dict(r) for r in c.fetchall()]
            conn.close()
            self.send_json(200, {"quiz": dict(q_row), "questions": questions})
            return

        # 9. GET /api/teacher/quiz-submissions?id=X
        if path == '/api/teacher/quiz-submissions':
            qid = query.get('id', [None])[0]
            if not qid:
                self.send_json(400, {"message": "رقم الاختبار مطلوب"})
                return
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM quizzes WHERE id = ?', (qid,))
            q_row = c.fetchone()
            if not q_row:
                conn.close()
                self.send_json(404, {"message": "الاختبار غير موجود"})
                return

            c.execute('SELECT * FROM questions WHERE quizId = ? ORDER BY id ASC', (qid,))
            questions = [dict(r) for r in c.fetchall()]

            c.execute('''
                SELECT sub.*, st.grade, st.section, st.gradeSection, st.nationalId
                FROM submissions sub
                LEFT JOIN students st ON LOWER(TRIM(sub.studentUsername)) = LOWER(TRIM(st.username))
                WHERE sub.quizId = ?
                ORDER BY sub.submittedAt DESC
            ''', (qid,))
            subs = [dict(r) for r in c.fetchall()]
            for s in subs:
                try:
                    s['answers'] = json.loads(s.get('answersJson') or '{}')
                except Exception:
                    s['answers'] = {}

            conn.close()
            self.send_json(200, {
                "quiz": dict(q_row),
                "questions": questions,
                "submissions": subs
            })
            return

        # 10. GET /api/teacher/data - Live Feed for Teacher Console
        if path == '/api/teacher/data':
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute('SELECT * FROM students ORDER BY createdAt DESC')
            students = [dict(r) for r in c.fetchall()]
            for s in students:
                s['totalScore'] = round((s.get('exam1Score', 0) or 0) + (s.get('exam2Score', 0) or 0) + (s.get('participationScore', 0) or 0) + (s.get('bonusScore', 0) or 0), 1)

            c.execute('SELECT * FROM quizzes ORDER BY createdAt DESC')
            quizzes = [dict(r) for r in c.fetchall()]
            for q in quizzes:
                c.execute('SELECT COUNT(*) FROM questions WHERE quizId = ?', (q['id'],))
                q['questionCount'] = c.fetchone()[0]
                c.execute('SELECT COUNT(*) FROM submissions WHERE quizId = ?', (q['id'],))
                q['submissionsCount'] = c.fetchone()[0]

            c.execute('''
                SELECT s.*, q.title as quizTitle, q.type as quizType, q.targetGrade, q.targetSection
                FROM submissions s
                LEFT JOIN quizzes q ON s.quizId = q.id
                ORDER BY s.submittedAt DESC
            ''')
            submissions = [dict(r) for r in c.fetchall()]

            c.execute('SELECT * FROM logs ORDER BY timestamp DESC LIMIT 60')
            logs = [dict(r) for r in c.fetchall()]

            c.execute('SELECT key, value FROM settings')
            settings_dict = dict(c.fetchall())

            conn.close()
            self.send_json(200, {
                "students": students,
                "quizzes": quizzes,
                "submissions": submissions,
                "logs": logs,
                "settings": settings_dict,
                "areGradesVisibleGlobally": (settings_dict.get("grades_globally_visible", "1") == "1"),
                "isOpen": (settings_dict.get("session_open", "1") == "1"),
                "serverIps": get_local_ips(),
                "port": PORT
            })
            return

        self.send_error(404, "Page Not Found")

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        data = json.loads(body) if body else {}
        path = urllib.parse.urlparse(self.path).path

        # 1. POST /api/teacher/setup - First launch setup
        if path == '/api/teacher/setup':
            name = data.get('name', '').strip()
            password = data.get('password', '').strip()
            username = data.get('username', '').strip() or 'admin'
            phone = data.get('phone', '').strip()
            subject = data.get('subject', '').strip() or 'المادة التعليمية'

            if not name:
                self.send_json(400, {"success": False, "message": "اسم الأستاذ إجباري"})
                return
            if not password:
                self.send_json(400, {"success": False, "message": "كلمة المرور إجبارية لحماية لوحة التحكم"})
                return

            set_setting("teacher_name", name)
            set_setting("teacher_password", password)
            set_setting("teacher_username", username)
            set_setting("teacher_phone", phone)
            set_setting("teacher_subject", subject)
            set_setting("teacher_setup_completed", "1")

            add_log("SYSTEM", f"تم إعداد حساب الأستاذ ({name}) وحماية لوحة التحكم بكلمة مرور بنجاح")
            self.send_json(200, {
                "success": True,
                "message": "تم إعداد الحساب بنجاح",
                "teacher": {
                    "name": name,
                    "username": username,
                    "subject": subject,
                    "phone": phone
                }
            })
            return

        # 2. POST /api/teacher/login - Teacher Login
        if path == '/api/teacher/login':
            password = data.get('password', '').strip()
            username = data.get('username', '').strip()
            stored_pwd = get_setting("teacher_password", "")
            stored_user = get_setting("teacher_username", "")

            if not stored_pwd:
                # Setup not completed yet
                self.send_json(400, {"success": False, "needSetup": True, "message": "يجب إعداد حساب الأستاذ أولاً"})
                return

            # If username was specified, verify it if stored is present
            if username and stored_user and username.lower() != stored_user.lower():
                self.send_json(401, {"success": False, "message": "اسم المستخدم أو كلمة المرور غير صحيحة"})
                return

            if password != stored_pwd:
                self.send_json(401, {"success": False, "message": "كلمة المرور غير صحيحة"})
                return

            add_log("SYSTEM", f"تم تسجيل دخول المعلم: {get_setting('teacher_name', 'الأستاذ')}")
            self.send_json(200, {
                "success": True,
                "teacher": {
                    "name": get_setting("teacher_name", "الأستاذ"),
                    "subject": get_setting("teacher_subject", ""),
                    "username": stored_user
                }
            })
            return

        # 3. POST /api/status - Open/Close Session
        if path == '/api/status':
            is_open = bool(data.get('isOpen', True))
            set_setting("session_open", "1" if is_open else "0")
            add_log("SYSTEM", "قام المعلم بفتح الحصة واستقبال الطلاب" if is_open else "قام المعلم بإيقاف استقبال الطلاب مؤقتاً")
            self.send_json(200, {"success": True, "isOpen": is_open})
            return

        # 4. POST /api/register - Student Register (With Grade and Section)
        if path == '/api/register':
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
            grade = data.get('grade', '').strip()
            section = data.get('section', '').strip()
            nid = data.get('nationalId', '').strip()
            phone = data.get('phone', '').strip()

            if not username:
                self.send_json(400, {"success": False, "message": "الاسم الرباعي إجباري"})
                return
            if not password:
                self.send_json(400, {"success": False, "message": "كلمة المرور إجبارية"})
                return
            if not grade or not section:
                # If combined gradeSection is passed
                combo = data.get('gradeSection', '').strip()
                if combo:
                    parts = [p.strip() for p in combo.split('-')]
                    grade = parts[0] if parts else grade
                    section = parts[1] if len(parts) > 1 else section

            if not grade:
                grade = "أول ثانوي"
            if not section:
                section = "شعبة 1"

            grade_sec = f"{grade} - {section}"

            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            try:
                now = int(time.time() * 1000)
                c.execute('''
                    INSERT INTO students (username, nationalId, phone, grade, section, gradeSection, password, createdAt)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (username, nid, phone, grade, section, grade_sec, password, now))
                sid = c.lastrowid
                add_log_direct(c, "STUDENT_JOIN", f"طالب جديد سجل في الفصل: {username} ({grade_sec})")
                conn.commit()
                conn.close()
                self.send_json(200, {
                    "success": True,
                    "student": {
                        "id": sid,
                        "username": username,
                        "grade": grade,
                        "section": section,
                        "gradeSection": grade_sec,
                        "nationalId": nid
                    }
                })
            except sqlite3.IntegrityError:
                conn.close()
                self.send_json(400, {"success": False, "message": "هذا الاسم مسجل مسبقاً! انتقل لتبويب تسجيل الدخول."})
            return

        # 5. POST /api/login - Student Login
        if path == '/api/login':
            identity = (data.get('identity') or data.get('username') or '').strip()
            password = data.get('password', '').strip()

            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('''
                SELECT * FROM students
                WHERE LOWER(TRIM(username)) = LOWER(TRIM(?)) OR (TRIM(nationalId) = TRIM(?) AND nationalId != '')
                LIMIT 1
            ''', (identity, identity))
            row = c.fetchone()
            if not row or row['password'] != password:
                conn.close()
                self.send_json(401, {"success": False, "message": "بيانات الدخول غير صحيحة، تأكد من الاسم أو كلمة المرور"})
                return

            add_log_direct(c, "STUDENT_JOIN", f"تسجيل دخول الطالب: {row['username']} ({row['gradeSection'] or (row['grade'] + ' - ' + row['section'])})")
            conn.commit()
            conn.close()
            self.send_json(200, {
                "success": True,
                "student": {
                    "id": row['id'],
                    "username": row['username'],
                    "grade": row['grade'],
                    "section": row['section'],
                    "gradeSection": row['gradeSection'] or f"{row['grade']} - {row['section']}",
                    "nationalId": row['nationalId']
                }
            })
            return

        # 6. POST /api/submit - Submit Quiz Answers
        if path == '/api/submit':
            qid = data.get('quizId')
            username = data.get('studentUsername', '').strip()
            answers = data.get('answers', {})

            prevent_retake = (get_setting("prevent_retake", "1") == "1")
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()

            if prevent_retake:
                c.execute('SELECT id FROM submissions WHERE quizId = ? AND LOWER(TRIM(studentUsername)) = LOWER(TRIM(?)) LIMIT 1', (qid, username))
                if c.fetchone():
                    conn.close()
                    self.send_json(400, {"success": False, "message": "لقد قمت بحل هذا الاختبار مسبقاً! غير مسموح بإعادة الحل."})
                    return

            c.execute('SELECT id, correctAnswer, points FROM questions WHERE quizId = ?', (qid,))
            q_rows = c.fetchall()
            total_points = 0
            score = 0
            for q_id, correct, pts in q_rows:
                total_points += pts
                st_ans = str(answers.get(str(q_id)) or answers.get(q_id) or '').strip()
                if st_ans.upper() == str(correct).strip().upper():
                    score += pts

            now = int(time.time() * 1000)
            c.execute('''
                INSERT INTO submissions (quizId, studentUsername, score, totalPoints, answersJson, submittedAt)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (qid, username, score, max(1, total_points), json.dumps(answers), now))

            c.execute('SELECT title FROM quizzes WHERE id=?', (qid,))
            qtitle_row = c.fetchone()
            qtitle = qtitle_row[0] if qtitle_row else "الاختبار"
            pct = round((score * 100) / total_points) if total_points > 0 else 100

            add_log_direct(c, "SUBMIT", f"سلّم الطالب {username} إجاباته في {qtitle} وحقق ({score}/{total_points} - {pct}%)")
            conn.commit()
            conn.close()

            self.send_json(200, {"success": True, "score": score, "totalPoints": total_points, "percentage": pct})
            return

        # 7. POST /api/cheat-alert - Anti-Cheat Flag
        if path == '/api/cheat-alert':
            st_name = data.get('student', 'طالب')
            reason = data.get('reason', 'محاولة استخدام إنترنت خارجي')
            add_log("CHEAT_ALERT", f"تنبيه أمني: {st_name} - {reason}")
            self.send_json(200, {"success": True})
            return

        # 8. POST /api/teacher/evaluate - Record Grades & Notes
        if path == '/api/teacher/evaluate':
            sid = data.get('studentId')
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute('''
                UPDATE students SET
                    exam1Score = ?,
                    exam2Score = ?,
                    participationScore = ?,
                    bonusScore = ?,
                    notes = ?,
                    showGradesToStudent = ?,
                    showNotesToStudent = ?,
                    gradeSection = CASE WHEN ? != '' THEN ? ELSE gradeSection END,
                    grade = CASE WHEN ? != '' THEN ? ELSE grade END,
                    section = CASE WHEN ? != '' THEN ? ELSE section END
                WHERE id = ?
            ''', (
                data.get('exam1', 0.0),
                data.get('exam2', 0.0),
                data.get('participation', 0.0),
                data.get('bonus', 0.0),
                data.get('notes', ''),
                1 if data.get('showGrades', True) else 0,
                1 if data.get('showNotes', True) else 0,
                data.get('gradeSection', ''),
                data.get('gradeSection', ''),
                data.get('grade', ''),
                data.get('grade', ''),
                data.get('section', ''),
                data.get('section', ''),
                sid
            ))
            add_log_direct(c, "SYSTEM", f"تم تحديث ورصد درجات الطالب رقم #{sid}")
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True})
            return

        # 9. POST /api/teacher/bonus - Quick +/- Points
        if path == '/api/teacher/bonus':
            sid = data.get('studentId')
            delta = data.get('delta', 0.0)
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute('UPDATE students SET bonusScore = bonusScore + ? WHERE id = ?', (delta, sid))
            c.execute('SELECT username FROM students WHERE id = ?', (sid,))
            row = c.fetchone()
            sname = row[0] if row else f"#{sid}"
            sign = "+" if delta > 0 else ""
            add_log_direct(c, "SYSTEM", f"تعديل سريع لدرجات {sname}: ({sign}{delta} درجات)")
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True})
            return

        # 10. POST /api/teacher/settings - Update Teacher Profile & Anti-Cheat
        if path == '/api/teacher/settings':
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            for k in ['teacher_name', 'teacher_subject', 'teacher_phone', 'teacher_username', 'anti_cheat', 'prevent_retake']:
                if k in data:
                    c.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (k, str(data[k])))
            new_pwd = data.get('teacher_password', '').strip()
            if new_pwd:
                c.execute('INSERT OR REPLACE INTO settings (key, value) VALUES ("teacher_password", ?)', (new_pwd,))
            add_log_direct(c, "SYSTEM", "تم تحديث إعدادات المعلم وخيارات الأمان")
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True})
            return

        # 11. POST /api/teacher/toggle-visibility - Global Grades Visibility
        if path == '/api/teacher/toggle-visibility':
            vis = 1 if data.get('visible', True) else 0
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute('UPDATE settings SET value = ? WHERE key = "grades_globally_visible"', (str(vis),))
            c.execute('UPDATE students SET showGradesToStudent = ?', (vis,))
            add_log_direct(c, "SYSTEM", "تم إعلان ونشر الدرجات لجميع الطلاب" if vis else "تم إخفاء الدرجات عن جميع الطلاب")
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True, "visible": bool(vis)})
            return

        # 12. POST /api/teacher/create-quiz - Create Quiz With Targeting
        if path == '/api/teacher/create-quiz':
            title = data.get('title', 'اختبار').strip()
            desc = data.get('description', '').strip()
            duration = int(data.get('durationMinutes', 10))
            q_type = data.get('type', 'QUIZ')
            target_grade = data.get('targetGrade', 'الكل').strip() or 'الكل'
            target_sec = data.get('targetSection', 'الكل').strip() or 'الكل'
            questions = data.get('questions', [])

            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            now = int(time.time() * 1000)
            c.execute('''
                INSERT INTO quizzes (title, description, durationMinutes, targetGrade, targetSection, isActive, type, createdAt)
                VALUES (?, ?, ?, ?, ?, 1, ?, ?)
            ''', (title, desc, duration, target_grade, target_sec, q_type, now))
            new_qid = c.lastrowid

            q_records = [
                (new_qid, q.get('questionText', ''), q.get('questionType', 'MULTIPLE_CHOICE'),
                 q.get('optionA', ''), q.get('optionB', ''), q.get('optionC', ''), q.get('optionD', ''),
                 q.get('correctAnswer', 'A'), q.get('points', 1))
                for q in questions
            ]
            c.executemany('''
                INSERT INTO questions (quizId, questionText, questionType, optionA, optionB, optionC, optionD, correctAnswer, points)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', q_records)

            add_log_direct(c, "SYSTEM", f"تم إنشاء اختبار جديد: {title} ({target_grade} - {target_sec}) - {len(questions)} سؤال")
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True, "quizId": new_qid})
            return

        # 13. POST /api/teacher/update-quiz - Edit Quiz & Questions
        if path == '/api/teacher/update-quiz':
            qid = data.get('quizId')
            title = data.get('title', 'اختبار').strip()
            desc = data.get('description', '').strip()
            duration = int(data.get('durationMinutes', 10))
            q_type = data.get('type', 'QUIZ')
            target_grade = data.get('targetGrade', 'الكل').strip() or 'الكل'
            target_sec = data.get('targetSection', 'الكل').strip() or 'الكل'
            questions = data.get('questions', [])

            if not qid:
                self.send_json(400, {"success": False, "message": "رقم الاختبار مطلوب للتعديل"})
                return

            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute('''
                UPDATE quizzes SET
                    title = ?, description = ?, durationMinutes = ?,
                    targetGrade = ?, targetSection = ?, type = ?
                WHERE id = ?
            ''', (title, desc, duration, target_grade, target_sec, q_type, qid))

            # Replace questions
            c.execute('DELETE FROM questions WHERE quizId = ?', (qid,))
            q_records = [
                (qid, q.get('questionText', ''), q.get('questionType', 'MULTIPLE_CHOICE'),
                 q.get('optionA', ''), q.get('optionB', ''), q.get('optionC', ''), q.get('optionD', ''),
                 q.get('correctAnswer', 'A'), q.get('points', 1))
                for q in questions
            ]
            c.executemany('''
                INSERT INTO questions (quizId, questionText, questionType, optionA, optionB, optionC, optionD, correctAnswer, points)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', q_records)

            add_log_direct(c, "SYSTEM", f"تم تعديل وحفظ الاختبار #{qid}: {title} ({target_grade} - {target_sec})")
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True, "quizId": qid})
            return

        # 14. POST /api/teacher/toggle-quiz - Toggle Quiz Active
        if path == '/api/teacher/toggle-quiz':
            qid = data.get('quizId')
            is_act = 1 if data.get('isActive') else 0
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute('UPDATE quizzes SET isActive = ? WHERE id = ?', (is_act, qid))
            c.execute('SELECT title FROM quizzes WHERE id = ?', (qid,))
            qrow = c.fetchone()
            qtitle = qrow[0] if qrow else f"#{qid}"
            add_log_direct(c, "SYSTEM", f"{'تفعيل وتدشين' if is_act else 'إغلاق'} الاختبار: {qtitle}")
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True})
            return

        # 15. POST /api/teacher/export-data - Encrypted Export (AES-256)
        if path == '/api/teacher/export-data':
            password = data.get('password', '')
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM students')
            students_list = [dict(r) for r in c.fetchall()]
            conn.close()

            encrypted_code = encrypt_students_aes(students_list, password)
            add_log("SYSTEM", f"تم تصدير نسخة مشفرة (AES-256) لبيانات {len(students_list)} طالب")
            self.send_json(200, {
                "success": True,
                "encryptedCode": encrypted_code,
                "studentCount": len(students_list)
            })
            return

        # 16. POST /api/teacher/import-data - Encrypted Import (AES-256)
        if path == '/api/teacher/import-data':
            encrypted_code = data.get('encryptedCode', '').strip()
            password = data.get('password', '')
            overwrite = bool(data.get('overwrite', False))

            try:
                students = decrypt_students_aes(encrypted_code, password)
            except Exception as e:
                self.send_json(400, {"success": False, "message": f"فشل فك التشفير: تأكد من صحة الكود أو كلمة المرور ({str(e)})"})
                return

            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            added = 0
            updated = 0

            for s in students:
                uname = s.get('username', '').strip()
                if not uname:
                    continue

                gr = s.get('grade', '').strip()
                sec = s.get('section', '').strip()
                gr_sec = s.get('gradeSection', '').strip()
                if not gr_sec and (gr or sec):
                    gr_sec = f"{gr} - {sec}"

                c.execute('SELECT id FROM students WHERE LOWER(TRIM(username)) = LOWER(TRIM(?))', (uname,))
                row = c.fetchone()

                if row:
                    if overwrite:
                        c.execute('''
                            UPDATE students SET
                                nationalId = ?, phone = ?, grade = ?, section = ?, gradeSection = ?, notes = ?,
                                exam1Score = ?, exam2Score = ?, participationScore = ?, bonusScore = ?,
                                showGradesToStudent = ?, showNotesToStudent = ?
                            WHERE id = ?
                        ''', (
                            s.get('nationalId', ''), s.get('phone', ''), gr, sec, gr_sec, s.get('notes', ''),
                            s.get('exam1Score', 0.0), s.get('exam2Score', 0.0), s.get('participationScore', 0.0), s.get('bonusScore', 0.0),
                            s.get('showGradesToStudent', 1), s.get('showNotesToStudent', 1),
                            row[0]
                        ))
                        updated += 1
                else:
                    c.execute('''
                        INSERT INTO students (username, nationalId, phone, grade, section, gradeSection, password, notes, exam1Score, exam2Score, participationScore, bonusScore, showGradesToStudent, showNotesToStudent, createdAt)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        uname, s.get('nationalId', ''), s.get('phone', ''), gr, sec, gr_sec,
                        s.get('password', '123456'), s.get('notes', ''),
                        s.get('exam1Score', 0.0), s.get('exam2Score', 0.0), s.get('participationScore', 0.0), s.get('bonusScore', 0.0),
                        s.get('showGradesToStudent', 1), s.get('showNotesToStudent', 1),
                        s.get('createdAt', int(time.time() * 1000))
                    ))
                    added += 1

            add_log_direct(c, "SYSTEM", f"تم استيراد بيانات وفك تشفير بنجاح (جدد: {added}، محدثون: {updated})")
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True, "added": added, "updated": updated})
            return

        # 17. POST /api/teacher/clear-logs
        if path == '/api/teacher/clear-logs':
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute('DELETE FROM logs')
            add_log_direct(c, "SYSTEM", "تم مسح سجل العمليات")
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True})
            return

        self.send_json(404, {"error": "Endpoint Not Found"})

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

def run():
    init_db()
    ips = get_local_ips()

    # Bind explicitly to 0.0.0.0:8080 so all phones on Wi-Fi connect seamlessly
    server_address = ('0.0.0.0', PORT)
    httpd = ThreadedHTTPServer(server_address, ClassroomHandler)

    print("=" * 68)
    print("  ★ خادم الاختبارات المدرسية - Windows 11 Desktop Edition ★")
    print("=" * 68)
    print(f"  [✓] الخادم يعمل بنجاح على العنوان: 0.0.0.0:{PORT}")
    print(f"  [💻] لوحة تحكم المعلم (Windows 11): http://localhost:{PORT}/teacher")
    print("  " + "-" * 64)
    print("  [📱] روابط دخول الطلاب في الفصل عبر شبكة الواي فاي المحلية:")
    for ip in ips:
        print(f"       -> http://{ip}:{PORT}")
    print("=" * 68)
    print("  جاري فتح لوحة تحكم المعلم تلقائياً في المتصفح...")

    threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{PORT}/teacher")).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nتم إيقاف الخادم.")
        httpd.server_close()

if __name__ == '__main__':
    run()
