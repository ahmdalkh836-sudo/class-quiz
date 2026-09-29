#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classroom Quiz Server - Windows 11 Desktop Standalone Edition
خادم الاختبارات المدرسية التفاعلية لنظام Windows 11
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

PORT = 8080
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "classroom_data.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            nationalId TEXT,
            phone TEXT,
            gradeSection TEXT,
            password TEXT,
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
            description TEXT,
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
            optionA TEXT,
            optionB TEXT,
            optionC TEXT,
            optionD TEXT,
            correctAnswer TEXT,
            points INTEGER DEFAULT 1,
            FOREIGN KEY (quizId) REFERENCES quizzes(id) ON DELETE CASCADE
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quizId INTEGER,
            studentUsername TEXT,
            score INTEGER,
            totalPoints INTEGER,
            answersJson TEXT,
            submittedAt INTEGER,
            FOREIGN KEY (quizId) REFERENCES quizzes(id) ON DELETE CASCADE
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    c.execute('INSERT OR IGNORE INTO settings (key, value) VALUES ("grades_globally_visible", "1")')

    # Seed starter quiz if empty
    c.execute('SELECT COUNT(*) FROM quizzes')
    if c.fetchone()[0] == 0:
        now = int(time.time() * 1000)
        c.execute('INSERT INTO quizzes (title, description, durationMinutes, isActive, type, createdAt) VALUES (?, ?, ?, ?, ?, ?)',
                  ("اختبار مراجعة الحصة", "اختبار قصير لقياس استيعاب المفاهيم الأساسية", 5, 1, "QUIZ", now))
        qid = c.lastrowid
        questions = [
            (qid, "ما هي وحدة قياس القوة في النظام الدولي؟", "MULTIPLE_CHOICE", "النيوتن (Newton)", "الجول (Joule)", "الواط (Watt)", "الباسكال (Pascal)", "A", 2),
            (qid, "تتحرك الإلكترونات حول النواة في مدارات محددة.", "TRUE_FALSE", "صح", "خطأ", "", "", "TRUE", 1),
            (qid, "أي كوكب هو الأقرب إلى الشمس؟", "MULTIPLE_CHOICE", "الزهرة", "عطارد", "المريخ", "الأرض", "B", 2)
        ]
        c.executemany('INSERT INTO questions (quizId, questionText, questionType, optionA, optionB, optionC, optionD, correctAnswer, points) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', questions)

    conn.commit()
    conn.close()

def get_local_ips():
    ips = []
    try:
        host_name = socket.gethostname()
        for ip in socket.gethostbyname_ex(host_name)[2]:
            if not ip.startswith("127."):
                ips.append(ip)
    except Exception:
        pass
    if not ips:
        ips.append("127.0.0.1")
    return ips

class ClassroomHandler(http.server.BaseHTTPRequestHandler):

    def send_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors()
        self.end_headers()

    def send_json(self, status, obj):
        data = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_cors()
        self.end_headers()
        self.wfile.write(data)

    def send_html(self, html_str):
        data = html_str.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_cors()
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path in ['/', '/portal', '/index.html']:
            # Student Portal
            self.send_html(get_student_portal_html())
            return
        elif path in ['/teacher', '/admin', '/teacher.html']:
            # Windows 11 Teacher Console
            self.send_html(get_teacher_portal_html())
            return
        elif path == '/api/health':
            self.send_json(200, {"status": "ok", "platform": "Windows 11 PC"})
            return
        elif path == '/api/teacher/data':
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute('SELECT * FROM students ORDER BY createdAt DESC')
            students = [dict(row) for row in c.fetchall()]

            c.execute('SELECT * FROM quizzes ORDER BY createdAt DESC')
            quizzes = [dict(row) for row in c.fetchall()]

            c.execute('''
                SELECT s.*, q.title as quizTitle
                FROM submissions s
                LEFT JOIN quizzes q ON s.quizId = q.id
                ORDER BY s.submittedAt DESC
            ''')
            submissions = [dict(row) for row in c.fetchall()]

            c.execute('SELECT value FROM settings WHERE key="grades_globally_visible"')
            row = c.fetchone()
            glob_vis = (row and row[0] == "1")

            conn.close()
            self.send_json(200, {
                "students": students,
                "quizzes": quizzes,
                "submissions": submissions,
                "areGradesVisibleGlobally": glob_vis
            })
            return
        elif path == '/api/student-quizzes':
            student_name = query.get('student', [''])[0].strip()
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute('SELECT * FROM quizzes WHERE isActive = 1 ORDER BY createdAt DESC')
            active_quizzes = [dict(row) for row in c.fetchall()]

            submitted_quiz_ids = set()
            completed = []
            if student_name:
                c.execute('SELECT * FROM submissions WHERE LOWER(TRIM(studentUsername)) = LOWER(TRIM(?)) ORDER BY submittedAt DESC', (student_name,))
                for s in c.fetchall():
                    s_dict = dict(s)
                    submitted_quiz_ids.add(s_dict['quizId'])
                    c.execute('SELECT title FROM quizzes WHERE id = ?', (s_dict['quizId'],))
                    qr = c.fetchone()
                    s_dict['title'] = qr[0] if qr else "اختبار منجز"
                    pct = round((s_dict['score'] * 100) / s_dict['totalPoints']) if s_dict['totalPoints'] > 0 else 100
                    s_dict['percentage'] = pct
                    completed.append(s_dict)

            unattempted = [q for q in active_quizzes if q['id'] not in submitted_quiz_ids]

            # Student evaluation
            c.execute('SELECT value FROM settings WHERE key="grades_globally_visible"')
            s_row = c.fetchone()
            glob_vis = (s_row and s_row[0] == "1")

            c.execute('SELECT * FROM students WHERE LOWER(TRIM(username)) = LOWER(TRIM(?)) LIMIT 1', (student_name,))
            st_row = c.fetchone()
            st_dict = dict(st_row) if st_row else {}

            is_visible = glob_vis and (st_dict.get('showGradesToStudent', 1) == 1)
            total_score = (st_dict.get('exam1Score', 0) or 0) + (st_dict.get('exam2Score', 0) or 0) + (st_dict.get('participationScore', 0) or 0) + (st_dict.get('bonusScore', 0) or 0)

            eval_obj = {
                "isVisible": is_visible,
                "exam1Score": st_dict.get('exam1Score', 0.0),
                "exam2Score": st_dict.get('exam2Score', 0.0),
                "participationScore": st_dict.get('participationScore', 0.0),
                "bonusScore": st_dict.get('bonusScore', 0.0),
                "totalScore": round(total_score, 1),
                "notes": st_dict.get('notes', '') if (is_visible and st_dict.get('showNotesToStudent', 1) == 1) else "",
                "hasNotes": bool(st_dict.get('notes')),
                "gradeSection": st_dict.get('gradeSection', '')
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
        elif path == '/api/quiz':
            qid = query.get('id', [None])[0]
            student_name = query.get('student', [''])[0].strip()
            if not qid:
                self.send_json(400, {"message": "رقم الاختبار مفقود"})
                return

            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            # Prevent retake
            c.execute('SELECT id FROM submissions WHERE quizId = ? AND LOWER(TRIM(studentUsername)) = LOWER(TRIM(?)) LIMIT 1', (qid, student_name))
            if c.fetchone():
                conn.close()
                self.send_json(400, {"error": "ALREADY_SUBMITTED", "message": "لقد قمت بحل هذا الاختبار مسبقاً!"})
                return

            c.execute('SELECT * FROM quizzes WHERE id = ?', (qid,))
            quiz = c.fetchone()
            if not quiz:
                conn.close()
                self.send_json(404, {"message": "الاختبار غير موجود"})
                return

            c.execute('SELECT id, questionText, questionType, optionA, optionB, optionC, optionD, points FROM questions WHERE quizId = ?', (qid,))
            questions = [dict(q) for q in c.fetchall()]
            conn.close()

            self.send_json(200, {
                "quiz": dict(quiz),
                "questions": questions
            })
            return

        self.send_error(404, "Page Not Found")

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body) if body else {}
        path = urllib.parse.urlparse(self.path).path

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        if path == '/api/register':
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
            nationalId = data.get('nationalId', '').strip()
            phone = data.get('phone', '').strip()
            gradeSection = data.get('gradeSection', '').strip()

            if not username or not password:
                conn.close()
                self.send_json(400, {"success": False, "message": "الاسم الرباعي وكلمة المرور مطلوبة"})
                return

            try:
                now = int(time.time() * 1000)
                c.execute('''
                    INSERT INTO students (username, nationalId, phone, gradeSection, password, createdAt)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (username, nationalId, phone, gradeSection, password, now))
                sid = c.lastrowid
                conn.commit()
                conn.close()
                self.send_json(200, {"success": True, "student": {"id": sid, "username": username, "nationalId": nationalId, "phone": phone, "gradeSection": gradeSection}})
            except sqlite3.IntegrityError:
                conn.close()
                self.send_json(400, {"success": False, "message": "هذا الطالب مسجل بالفعل! انتقل لتبويب تسجيل الدخول."})
            return

        elif path == '/api/login':
            identity = (data.get('username') or data.get('identity') or '').strip()
            password = data.get('password', '').strip()

            c.execute('''
                SELECT * FROM students
                WHERE LOWER(TRIM(username)) = LOWER(TRIM(?)) OR (TRIM(nationalId) = TRIM(?) AND nationalId != '')
                LIMIT 1
            ''', (identity, identity))
            row = c.fetchone()
            if not row or row[5] != password:
                conn.close()
                self.send_json(401, {"success": False, "message": "بيانات الدخول غير صحيحة"})
                return

            st = {"id": row[0], "username": row[1], "nationalId": row[2], "phone": row[3], "gradeSection": row[4]}
            conn.close()
            self.send_json(200, {"success": True, "student": st})
            return

        elif path == '/api/submit':
            qid = data.get('quizId')
            username = data.get('studentUsername', '').strip()
            answers = data.get('answers', {})

            # Prevent retake
            c.execute('SELECT id FROM submissions WHERE quizId = ? AND LOWER(TRIM(studentUsername)) = LOWER(TRIM(?)) LIMIT 1', (qid, username))
            if c.fetchone():
                conn.close()
                self.send_json(400, {"success": False, "message": "لقد قمت بحل هذا الاختبار مسبقاً!"})
                return

            c.execute('SELECT id, correctAnswer, points, questionType FROM questions WHERE quizId = ?', (qid,))
            q_rows = c.fetchall()
            total_points = 0
            score = 0

            for q in q_rows:
                q_id, correct, pts, q_type = q
                total_points += pts
                st_ans = str(answers.get(str(q_id)) or answers.get(q_id) or '').strip()
                if st_ans.lower() == str(correct).strip().lower():
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

        elif path == '/api/teacher/evaluate':
            sid = data.get('studentId')
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

        elif path == '/api/teacher/bonus':
            sid = data.get('studentId')
            delta = data.get('delta', 0.0)
            c.execute('UPDATE students SET bonusScore = bonusScore + ? WHERE id = ?', (delta, sid))
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True})
            return

        elif path == '/api/teacher/toggle-visibility':
            vis = 1 if data.get('visible', True) else 0
            c.execute('UPDATE settings SET value = ? WHERE key = "grades_globally_visible"', (str(vis),))
            c.execute('UPDATE students SET showGradesToStudent = ?', (vis,))
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True, "visible": bool(vis)})
            return

        elif path == '/api/teacher/toggle-quiz':
            qid = data.get('quizId')
            is_active = 1 if data.get('isActive') else 0
            c.execute('UPDATE quizzes SET isActive = ? WHERE id = ?', (is_active, qid))
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True})
            return

        elif path == '/api/teacher/create-quiz':
            title = data.get('title', 'اختبار')
            desc = data.get('description', '')
            duration = data.get('durationMinutes', 10)
            q_type = data.get('type', 'QUIZ')
            questions = data.get('questions', [])

            now = int(time.time() * 1000)
            c.execute('INSERT INTO quizzes (title, description, durationMinutes, isActive, type, createdAt) VALUES (?, ?, ?, 1, ?, ?)',
                      (title, desc, duration, q_type, now))
            new_qid = c.lastrowid

            q_records = [
                (new_qid, q.get('questionText', ''), q.get('questionType', 'MULTIPLE_CHOICE'),
                 q.get('optionA', ''), q.get('optionB', ''), q.get('optionC', ''), q.get('optionD', ''),
                 q.get('correctAnswer', 'A'), q.get('points', 1))
                for q in questions
            ]
            c.executemany('INSERT INTO questions (quizId, questionText, questionType, optionA, optionB, optionC, optionD, correctAnswer, points) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', q_records)
            conn.commit()
            conn.close()
            self.send_json(200, {"success": True, "quizId": new_qid})
            return

        conn.close()
        self.send_json(404, {"error": "Not Found"})

def get_student_portal_html():
    from server_html import STUDENT_HTML
    return STUDENT_HTML

def get_teacher_portal_html():
    from server_html import TEACHER_HTML
    return TEACHER_HTML

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

def main():
    init_db()
    ips = get_local_ips()
    primary_ip = ips[0]

    server = ThreadedHTTPServer(("0.0.0.0", PORT), ClassroomHandler)

    print("=" * 65)
    print("  خادم الاختبارات المدرسية - نسخة Windows 11 PC")
    print("=" * 65)
    print(f"  [+] الخادم يعمل الآن بنجاح على المنفذ: {PORT}")
    print(f"  [+] لوحة تحكم المعلم (Windows 11): http://localhost:{PORT}/teacher")
    for ip in ips:
        print(f"  [+] رابط دخول الطلاب في الفصل:    http://{ip}:{PORT}")
    print("=" * 65)
    print("  جاري فتح لوحة تحكم المعلم تلقائياً في المتصفح...")

    threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{PORT}/teacher")).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nتم إيقاف الخادم.")
        server.server_close()

if __name__ == '__main__':
    main()
