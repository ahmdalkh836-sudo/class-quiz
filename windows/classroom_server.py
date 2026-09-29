#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classroom Quiz Server - Windows 11 Desktop Edition
خادم بث الاختبارات المدرسية المباشر عبر شبكة الواي فاي المحلية
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

from server_html import STUDENT_HTML, TEACHER_HTML

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "classroom_data.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    c.execute('INSERT OR IGNORE INTO settings (key, value) VALUES ("session_open", "1")')
    c.execute('INSERT OR IGNORE INTO settings (key, value) VALUES ("grades_globally_visible", "1")')

    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE COLLATE NOCASE,
            nationalId TEXT DEFAULT '',
            phone TEXT DEFAULT '',
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

    c.execute('''
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT DEFAULT '',
            durationMinutes INTEGER DEFAULT 10,
            isActive INTEGER DEFAULT 1,
            type TEXT DEFAULT 'QUIZ',
            createdAt INTEGER
        )
    ''')

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

    # Seed initial sample quiz if database is new
    c.execute('SELECT COUNT(*) FROM quizzes')
    if c.fetchone()[0] == 0:
        now = int(time.time() * 1000)
        c.execute('''
            INSERT INTO quizzes (title, description, durationMinutes, isActive, type, createdAt)
            VALUES (?, ?, ?, 1, 'QUIZ', ?)
        ''', ("اختبار مراجعة الحصة الأول", "اختبار قصير للتأكد من استيعاب المفاهيم الأساسية", 5, now))
        qid = c.lastrowid
        questions = [
            (qid, "ما هي وحدة قياس القوة في النظام الدولي؟", "MULTIPLE_CHOICE", "النيوتن (Newton)", "الجول (Joule)", "الواط (Watt)", "الباسكال (Pascal)", "A", 2),
            (qid, "تتحرك الإلكترونات حول النواة في مدارات ومستويات طاقة محددة.", "MULTIPLE_CHOICE", "صح", "خطأ", "", "", "A", 1),
            (qid, "أي كوكب هو الأقرب إلى الشمس في المجموعة الشمسية؟", "MULTIPLE_CHOICE", "الزهرة", "عطارد", "المريخ", "الأرض", "B", 2)
        ]
        c.executemany('''
            INSERT INTO questions (quizId, questionText, questionType, optionA, optionB, optionC, optionD, correctAnswer, points)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', questions)

    conn.commit()
    conn.close()

def get_local_ips():
    ips = []
    # Method 1: Connecting dummy socket to detect primary active route
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(("8.8.8.8", 80))
        primary_ip = s.getsockname()[0]
        s.close()
        if primary_ip and not primary_ip.startswith("127."):
            ips.append(primary_ip)
    except Exception:
        pass

    # Method 2: Inspecting all interface addresses via gethostbyname_ex
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

def is_session_open():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT value FROM settings WHERE key="session_open"')
    row = c.fetchone()
    conn.close()
    return (row and row[0] == "1")

def set_session_open(open_status):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('UPDATE settings SET value=? WHERE key="session_open"', ("1" if open_status else "0",))
    conn.commit()
    conn.close()

class ClassroomHandler(http.server.BaseHTTPRequestHandler):

    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

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

        # 3. GET /api/status - Session & Network Status
        if path == '/api/status':
            ips = get_local_ips()
            self.send_json(200, {
                "isOpen": is_session_open(),
                "port": PORT,
                "serverIps": ips
            })
            return

        # 4. GET /api/quizzes - List Open Quizzes
        if path == '/api/quizzes':
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM quizzes WHERE isActive = 1 ORDER BY createdAt DESC')
            quizzes = [dict(row) for row in c.fetchall()]
            for q in quizzes:
                c.execute('SELECT COUNT(*) FROM questions WHERE quizId = ?', (q['id'],))
                q['questionCount'] = c.fetchone()[0]
            conn.close()
            self.send_json(200, quizzes)
            return

        # 5. GET /api/quiz?id=X&student=Y - Questions for Quiz
        if path == '/api/quiz':
            qid = query.get('id', [None])[0]
            student = query.get('student', [''])[0].strip()
            if not qid:
                self.send_json(400, {"message": "رقم الاختبار مطلوب"})
                return

            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            # Prevent retaking
            if student:
                c.execute('SELECT id FROM submissions WHERE quizId = ? AND LOWER(TRIM(studentUsername)) = LOWER(TRIM(?)) LIMIT 1', (qid, student))
                if c.fetchone():
                    conn.close()
                    self.send_json(400, {"error": "ALREADY_SUBMITTED", "message": "لقد قمت بحل هذا الاختبار مسبقاً! غير مسموح بالإعادة."})
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

            self.send_json(200, {
                "quiz": dict(quiz_row),
                "questions": questions
            })
            return

        # 6. GET /api/student-quizzes?student=X - Quizzes Status & Report Card
        if path == '/api/student-quizzes':
            student = query.get('student', [''])[0].strip()
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute('SELECT * FROM quizzes WHERE isActive = 1 ORDER BY createdAt DESC')
            active_quizzes = [dict(r) for r in c.fetchall()]
            for q in active_quizzes:
                c.execute('SELECT COUNT(*) FROM questions WHERE quizId = ?', (q['id'],))
                q['questionCount'] = c.fetchone()[0]

            submitted_qids = set()
            completed = []
            if student:
                c.execute('SELECT * FROM submissions WHERE LOWER(TRIM(studentUsername)) = LOWER(TRIM(?)) ORDER BY submittedAt DESC', (student,))
                for s in c.fetchall():
                    s_dict = dict(s)
                    submitted_qids.add(s_dict['quizId'])
                    c.execute('SELECT title FROM quizzes WHERE id = ?', (s_dict['quizId'],))
                    q_res = c.fetchone()
                    s_dict['title'] = q_res[0] if q_res else "اختبار منجز"
                    pct = round((s_dict['score'] * 100) / s_dict['totalPoints']) if s_dict['totalPoints'] > 0 else 100
                    s_dict['percentage'] = pct
                    completed.append(s_dict)

            unattempted = [q for q in active_quizzes if q['id'] not in submitted_qids]

            # Evaluation & Report card
            c.execute('SELECT value FROM settings WHERE key="grades_globally_visible"')
            grow = c.fetchone()
            glob_visible = (grow and grow[0] == "1")

            c.execute('SELECT * FROM students WHERE LOWER(TRIM(username)) = LOWER(TRIM(?)) LIMIT 1', (student,))
            srow = c.fetchone()
            sdict = dict(srow) if srow else {}

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
                "gradeSection": sdict.get('gradeSection', '')
            }

            conn.close()
            self.send_json(200, {
                "unattempted": unattempted,
                "availableQuizzes": unattempted,
                "completed": completed,
                "completedQuizzes": completed,
                "evaluation": eval_obj
            })
            return

        # 7. GET /api/teacher/data - Live Feed for Windows 11 Teacher Console
        if path == '/api/teacher/data':
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute('SELECT * FROM students ORDER BY createdAt DESC')
            students = [dict(r) for r in c.fetchall()]

            c.execute('SELECT * FROM quizzes ORDER BY createdAt DESC')
            quizzes = [dict(r) for r in c.fetchall()]
            for q in quizzes:
                c.execute('SELECT COUNT(*) FROM questions WHERE quizId = ?', (q['id'],))
                q['questionCount'] = c.fetchone()[0]

            c.execute('''
                SELECT s.*, q.title as quizTitle
                FROM submissions s
                LEFT JOIN quizzes q ON s.quizId = q.id
                ORDER BY s.submittedAt DESC
            ''')
            submissions = [dict(r) for r in c.fetchall()]

            c.execute('SELECT value FROM settings WHERE key="grades_globally_visible"')
            row = c.fetchone()
            glob_vis = (row and row[0] == "1")

            conn.close()
            self.send_json(200, {
                "students": students,
                "quizzes": quizzes,
                "submissions": submissions,
                "areGradesVisibleGlobally": glob_vis,
                "isOpen": is_session_open()
            })
            return

        self.send_error(404, "Page Not Found")

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        data = json.loads(body) if body else {}
        path = urllib.parse.urlparse(self.path).path

        # 1. POST /api/status - Open/Close Session
        if path == '/api/status':
            is_open = bool(data.get('isOpen', True))
            set_session_open(is_open)
            self.send_json(200, {"success": True, "isOpen": is_open})
            return

        # 2. POST /api/register - Student Registration
        if path == '/api/register':
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
            grade_sec = data.get('gradeSection', '').strip()
            nid = data.get('nationalId', '').strip()

            if not username or not password:
                self.send_json(400, {"success": False, "message": "الاسم وكلمة المرور مطلوبة"})
                return

            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            try:
                now = int(time.time() * 1000)
                c.execute('''
                    INSERT INTO students (username, nationalId, gradeSection, password, createdAt)
                    VALUES (?, ?, ?, ?, ?)
                ''', (username, nid, grade_sec, password, now))
                sid = c.lastrowid
                conn.commit()
                conn.close()
                self.send_json(200, {"success": True, "student": {"id": sid, "username": username, "gradeSection": grade_sec, "nationalId": nid}})
            except sqlite3.IntegrityError:
                conn.close()
                self.send_json(400, {"success": False, "message": "هذا الاسم مسجل مسبقاً! انتقل لتبويب تسجيل الدخول."})
            return

        # 3. POST /api/login - Student Login
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
            conn.close()

            if not row or row['password'] != password:
                self.send_json(401, {"success": False, "message": "بيانات الدخول غير صحيحة"})
                return

            self.send_json(200, {
                "success": True,
                "student": {"id": row['id'], "username": row['username'], "gradeSection": row['gradeSection'], "nationalId": row['nationalId']}
            })
            return

        # 4. POST /api/submit - Auto-grade & Record Quiz Answers
        if path == '/api/submit':
            qid = data.get('quizId')
            username = data.get('studentUsername', '').strip()
            answers = data.get('answers', {})

            if not qid or not username:
                self.send_json(400, {"success": False, "message": "بيانات التسليم ناقصة"})
                return

            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()

            # Check if student already submitted
            c.execute('SELECT id FROM submissions WHERE quizId = ? AND LOWER(TRIM(studentUsername)) = LOWER(TRIM(?)) LIMIT 1', (qid, username))
            if c.fetchone():
                conn.close()
                self.send_json(400, {"success": False, "message": "لقد قمت بحل هذا الاختبار مسبقاً!"})
                return

            # Grade questions
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
            conn.commit()
            conn.close()

            pct = round((score * 100) / total_points) if total_points > 0 else 100
            self.send_json(200, {"success": True, "score": score, "totalPoints": total_points, "percentage": pct})
            return

        # 5. POST /api/teacher/evaluate - Record Grades & Notes
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
                    gradeSection = CASE WHEN ? != '' THEN ? ELSE gradeSection END
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
                sid
            ))
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True})
            return

        # 6. POST /api/teacher/bonus - Quick +/- Points
        if path == '/api/teacher/bonus':
            sid = data.get('studentId')
            delta = data.get('delta', 0.0)
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute('UPDATE students SET bonusScore = bonusScore + ? WHERE id = ?', (delta, sid))
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True})
            return

        # 7. POST /api/teacher/create-quiz - Create Quiz & Questions
        if path == '/api/teacher/create-quiz':
            title = data.get('title', 'اختبار').strip()
            desc = data.get('description', '').strip()
            duration = int(data.get('durationMinutes', 10))
            questions = data.get('questions', [])

            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            now = int(time.time() * 1000)
            c.execute('''
                INSERT INTO quizzes (title, description, durationMinutes, isActive, type, createdAt)
                VALUES (?, ?, ?, 1, 'QUIZ', ?)
            ''', (title, desc, duration, now))
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
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True, "quizId": new_qid})
            return

        # 8. POST /api/teacher/toggle-quiz - Activate/Close Quiz
        if path == '/api/teacher/toggle-quiz':
            qid = data.get('quizId')
            is_act = 1 if data.get('isActive') else 0
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute('UPDATE quizzes SET isActive = ? WHERE id = ?', (is_act, qid))
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True})
            return

        # 9. POST /api/teacher/toggle-visibility - Global Grades Visibility
        if path == '/api/teacher/toggle-visibility':
            vis = 1 if data.get('visible', True) else 0
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute('UPDATE settings SET value = ? WHERE key = "grades_globally_visible"', (str(vis),))
            c.execute('UPDATE students SET showGradesToStudent = ?', (vis,))
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True, "visible": bool(vis)})
            return

        self.send_json(404, {"error": "Endpoint Not Found"})

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

def run():
    init_db()
    ips = get_local_ips()
    primary_ip = ips[0]

    # Bind explicitly to 0.0.0.0:8080 so all devices on Wi-Fi can connect
    server_address = ('0.0.0.0', PORT)
    httpd = ThreadedHTTPServer(server_address, ClassroomHandler)

    print("=" * 68)
    print("  ★ خادم الاختبارات المدرسية - Windows 11 Desktop Edition ★")
    print("=" * 68)
    print(f"  [✓] الخادم يعمل الآن بنجاح على العنوان: 0.0.0.0:{PORT}")
    print(f"  [💻] لوحة تحكم المعلم (Windows 11): http://localhost:{PORT}/teacher")
    print("  " + "-" * 64)
    print("  [📱] روابط دخول الطلاب من هواتفهم المتصلة بنفس شبكة الواي فاي:")
    for ip in ips:
        print(f"       -> http://{ip}:{PORT}")
    print("=" * 68)
    print("  جاري فتح لوحة تحكم المعلم تلقائياً في المتصفح...")

    # Auto-open browser on Windows 11
    threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{PORT}/teacher")).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nتم إيقاف الخادم.")
        httpd.server_close()

if __name__ == '__main__':
    run()
