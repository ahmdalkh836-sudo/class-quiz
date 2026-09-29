package com.example.server

import android.util.Log
import com.example.data.repository.QuizRepository
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.BufferedInputStream
import java.io.ByteArrayOutputStream
import java.io.InputStream
import java.io.OutputStream
import java.net.Inet4Address
import java.net.InetAddress
import java.net.NetworkInterface
import java.net.ServerSocket
import java.net.Socket
import java.net.URLDecoder
import java.nio.charset.StandardCharsets

data class ServerLogEvent(
    val id: Long = System.currentTimeMillis() + (0..999).random(),
    val timestamp: Long = System.currentTimeMillis(),
    val type: String, // "INFO", "STUDENT_JOIN", "SUBMISSION", "ERROR"
    val message: String
)

class ClassroomWebServer(
    private val repository: QuizRepository,
    private val port: Int = 8080,
    private val onLogEvent: (ServerLogEvent) -> Unit
) {
    private val TAG = "ClassroomWebServer"
    private var serverSocket: ServerSocket? = null
    private var serverJob: Job? = null
    private val serverScope = CoroutineScope(Dispatchers.IO)

    @Volatile
    var isRunning: Boolean = false
        private set

    fun start() {
        if (isRunning) return

        serverJob = serverScope.launch {
            try {
                serverSocket = ServerSocket(port, 50, InetAddress.getByName("0.0.0.0"))
                isRunning = true
                val ip = getLocalIpAddress()
                log("INFO", "تم تشغيل خادم الاختبارات بنجاح على العنوان: http://$ip:$port")

                while (isActive && isRunning) {
                    try {
                        val client = serverSocket?.accept() ?: break
                        serverScope.launch {
                            handleClient(client)
                        }
                    } catch (e: Exception) {
                        if (!isRunning) break
                        Log.e(TAG, "Socket accept error", e)
                    }
                }
            } catch (e: Exception) {
                log("ERROR", "فشل بدء الخادم: ${e.message}")
                Log.e(TAG, "Error starting server", e)
                isRunning = false
            }
        }
    }

    fun stop() {
        isRunning = false
        try {
            serverSocket?.close()
        } catch (e: Exception) {
            Log.e(TAG, "Error closing server socket", e)
        }
        serverJob?.cancel()
        serverSocket = null
        log("INFO", "تم إيقاف خادم الاختبارات")
    }

    private suspend fun handleClient(socket: Socket) {
        withContext(Dispatchers.IO) {
            try {
                socket.soTimeout = 12000 // 12 second read timeout
                val input = BufferedInputStream(socket.getInputStream())
                val output = socket.getOutputStream()

                val requestLine = readHttpLine(input) ?: return@withContext
                val parts = requestLine.split(" ")
                if (parts.size < 2) return@withContext

                val method = parts[0].uppercase().trim()
                val fullPath = parts[1].trim()

                // Parse Headers
                val headers = mutableMapOf<String, String>()
                var contentLength = 0
                while (true) {
                    val line = readHttpLine(input) ?: break
                    if (line.isEmpty()) break
                    val colonIdx = line.indexOf(':')
                    if (colonIdx > 0) {
                        val key = line.substring(0, colonIdx).trim().lowercase()
                        val value = line.substring(colonIdx + 1).trim()
                        headers[key] = value
                        if (key == "content-length") {
                            contentLength = value.toIntOrNull() ?: 0
                        }
                    }
                }

                // Handle CORS preflight early
                if (method == "OPTIONS") {
                    sendOptionsResponse(output)
                    return@withContext
                }

                // Read body accurately by raw bytes (handles Arabic and all UTF-8 characters properly)
                val body = if (contentLength > 0) {
                    val maxAllowed = minOf(contentLength, 2 * 1024 * 1024)
                    val bodyBytes = ByteArray(maxAllowed)
                    var totalRead = 0
                    while (totalRead < maxAllowed) {
                        val count = input.read(bodyBytes, totalRead, maxAllowed - totalRead)
                        if (count == -1) break
                        totalRead += count
                    }
                    String(bodyBytes, 0, totalRead, StandardCharsets.UTF_8)
                } else ""

                val (path, queryParams) = parsePathAndQuery(fullPath)
                routeRequest(method, path, queryParams, body, output)

            } catch (e: Exception) {
                Log.e(TAG, "Error handling client request", e)
            } finally {
                try {
                    socket.close()
                } catch (_: Exception) {}
            }
        }
    }

    private fun readHttpLine(input: InputStream): String? {
        val baos = ByteArrayOutputStream()
        var c: Int
        var hasReadAny = false
        while (true) {
            c = input.read()
            if (c == -1) {
                return if (hasReadAny) baos.toString(StandardCharsets.UTF_8.name()) else null
            }
            hasReadAny = true
            if (c == '\n'.code) {
                break
            }
            if (c != '\r'.code) {
                baos.write(c)
            }
        }
        return baos.toString(StandardCharsets.UTF_8.name())
    }

    private suspend fun routeRequest(
        method: String,
        path: String,
        query: Map<String, String>,
        body: String,
        out: OutputStream
    ) {
        when {
            // Teacher Web Console for Windows 11 / PC
            (method == "GET" && (path == "/teacher" || path == "/admin" || path == "/teacher.html")) -> {
                val html = TeacherWebPortalContent.getTeacherHtml()
                sendResponse(out, 200, "OK", "text/html; charset=UTF-8", html)
            }

            // Teacher API: Get All Data
            (method == "GET" && path == "/api/teacher/data") -> {
                val students = repository.getAllStudents()
                val quizzes = repository.getAllQuizzes()
                val submissions = repository.getAllSubmissions()

                val res = JSONObject().apply {
                    put("areGradesVisibleGlobally", repository.areGradesVisibleGlobally)

                    val studentsArr = JSONArray()
                    students.forEach { s ->
                        studentsArr.put(JSONObject().apply {
                            put("id", s.id)
                            put("username", s.username)
                            put("nationalId", s.nationalId)
                            put("phone", s.phone)
                            put("gradeSection", s.gradeSection)
                            put("notes", s.notes)
                            put("exam1Score", s.exam1Score)
                            put("exam2Score", s.exam2Score)
                            put("participationScore", s.participationScore)
                            put("bonusScore", s.bonusScore)
                            put("totalScore", s.totalScore)
                            put("showGradesToStudent", s.showGradesToStudent)
                            put("showNotesToStudent", s.showNotesToStudent)
                            put("createdAt", s.createdAt)
                        })
                    }
                    put("students", studentsArr)

                    val quizzesArr = JSONArray()
                    quizzes.forEach { q ->
                        quizzesArr.put(JSONObject().apply {
                            put("id", q.id)
                            put("title", q.title)
                            put("description", q.description)
                            put("durationMinutes", q.durationMinutes)
                            put("isActive", q.isActive)
                            put("type", q.type)
                        })
                    }
                    put("quizzes", quizzesArr)

                    val submissionsArr = JSONArray()
                    submissions.forEach { sub ->
                        val q = quizzes.find { it.id == sub.quizId }
                        submissionsArr.put(JSONObject().apply {
                            put("id", sub.id)
                            put("quizId", sub.quizId)
                            put("quizTitle", q?.title ?: "اختبار")
                            put("studentUsername", sub.studentUsername)
                            put("score", sub.score)
                            put("totalPoints", sub.totalPoints)
                            put("submittedAt", sub.submittedAt)
                        })
                    }
                    put("submissions", submissionsArr)
                }
                sendJsonResponse(out, 200, res)
            }

            // Teacher API: Evaluate Student
            (method == "POST" && path == "/api/teacher/evaluate") -> {
                try {
                    val json = JSONObject(body)
                    val studentId = json.optLong("studentId", 0L)
                    val exam1 = json.optDouble("exam1", 0.0)
                    val exam2 = json.optDouble("exam2", 0.0)
                    val part = json.optDouble("participation", 0.0)
                    val bonus = json.optDouble("bonus", 0.0)
                    val notes = json.optString("notes", "")
                    val showGrades = json.optBoolean("showGrades", true)
                    val showNotes = json.optBoolean("showNotes", true)
                    val gradeSection = json.optString("gradeSection", "")

                    repository.updateStudentEvaluation(studentId, exam1, exam2, part, bonus, notes, showGrades, showNotes)
                    if (gradeSection.isNotBlank()) {
                        repository.updateStudentClassSection(studentId, gradeSection)
                    }
                    sendJsonResponse(out, 200, JSONObject().put("success", true))
                } catch (e: Exception) {
                    sendJsonResponse(out, 400, JSONObject().put("success", false).put("message", e.message))
                }
            }

            // Teacher API: Quick Bonus
            (method == "POST" && path == "/api/teacher/bonus") -> {
                try {
                    val json = JSONObject(body)
                    val studentId = json.optLong("studentId", 0L)
                    val delta = json.optDouble("delta", 0.0)
                    repository.adjustStudentBonus(studentId, delta)
                    sendJsonResponse(out, 200, JSONObject().put("success", true))
                } catch (e: Exception) {
                    sendJsonResponse(out, 400, JSONObject().put("success", false))
                }
            }

            // Teacher API: Toggle Global Visibility
            (method == "POST" && path == "/api/teacher/toggle-visibility") -> {
                try {
                    val json = JSONObject(body)
                    val visible = json.optBoolean("visible", true)
                    repository.areGradesVisibleGlobally = visible
                    repository.setAllStudentsGradesVisibility(visible)
                    sendJsonResponse(out, 200, JSONObject().put("success", true).put("visible", visible))
                } catch (e: Exception) {
                    sendJsonResponse(out, 400, JSONObject().put("success", false))
                }
            }

            // Teacher API: Toggle Quiz Active State
            (method == "POST" && path == "/api/teacher/toggle-quiz") -> {
                try {
                    val json = JSONObject(body)
                    val quizId = json.optLong("quizId", 0L)
                    val isActive = json.optBoolean("isActive", true)
                    repository.setQuizActive(quizId, isActive)
                    sendJsonResponse(out, 200, JSONObject().put("success", true))
                } catch (e: Exception) {
                    sendJsonResponse(out, 400, JSONObject().put("success", false))
                }
            }

            // Teacher API: Create Quiz with Questions
            (method == "POST" && path == "/api/teacher/create-quiz") -> {
                try {
                    val json = JSONObject(body)
                    val title = json.optString("title", "اختبار")
                    val desc = json.optString("description", "")
                    val duration = json.optInt("durationMinutes", 10)
                    val type = json.optString("type", "QUIZ")
                    val questionsJson = json.optJSONArray("questions") ?: JSONArray()

                    val quiz = com.example.data.model.Quiz(
                        title = title,
                        description = desc,
                        durationMinutes = duration,
                        type = type,
                        isActive = true
                    )
                    val questionsList = mutableListOf<com.example.data.model.Question>()
                    for (i in 0 until questionsJson.length()) {
                        val qObj = questionsJson.getJSONObject(i)
                        questionsList.add(
                            com.example.data.model.Question(
                                quizId = 0L,
                                questionText = qObj.optString("questionText", ""),
                                questionType = qObj.optString("questionType", "MULTIPLE_CHOICE"),
                                optionA = qObj.optString("optionA", ""),
                                optionB = qObj.optString("optionB", ""),
                                optionC = qObj.optString("optionC", ""),
                                optionD = qObj.optString("optionD", ""),
                                correctAnswer = qObj.optString("correctAnswer", "A"),
                                points = qObj.optInt("points", 1)
                            )
                        )
                    }

                    val newQuizId = repository.insertQuiz(quiz, questionsList)
                    sendJsonResponse(out, 200, JSONObject().put("success", true).put("quizId", newQuizId))
                } catch (e: Exception) {
                    sendJsonResponse(out, 400, JSONObject().put("success", false).put("message", e.message))
                }
            }

            // Static web portal
            (method == "GET" && (path == "/" || path == "/portal" || path == "/index.html")) -> {
                val html = WebPortalContent.getIndexHtml()
                sendResponse(out, 200, "OK", "text/html; charset=UTF-8", html)
            }

            // Health ping
            (method == "GET" && path == "/api/health") -> {
                sendJsonResponse(out, 200, JSONObject().put("status", "ok").put("server", "ClassroomServer"))
            }

            // Register Student
            (method == "POST" && path == "/api/register") -> {
                try {
                    val json = JSONObject(body)
                    val username = json.optString("username", "").trim()
                    val password = json.optString("password", "").trim()
                    val nationalId = json.optString("nationalId", "").trim()
                    val phone = json.optString("phone", "").trim()
                    val gradeSection = json.optString("gradeSection", "").trim()

                    val result = repository.registerStudent(username, password, nationalId, phone, gradeSection)
                    result.onSuccess { student ->
                        val infoStr = if (student.nationalId.isNotBlank()) " (هوية: ${student.nationalId})" else ""
                        log("STUDENT_JOIN", "طالب جديد سجل حسابه لأول مرة: ${student.username}$infoStr")
                        val res = JSONObject().apply {
                            put("success", true)
                            put("student", JSONObject().apply {
                                put("id", student.id)
                                put("username", student.username)
                                put("nationalId", student.nationalId)
                                put("phone", student.phone)
                                put("gradeSection", student.gradeSection)
                            })
                        }
                        sendJsonResponse(out, 200, res)
                    }.onFailure { err ->
                        sendJsonResponse(out, 400, JSONObject().put("success", false).put("message", err.message))
                    }
                } catch (e: Exception) {
                    sendJsonResponse(out, 400, JSONObject().put("success", false).put("message", "بيانات التسجيل غير صالحة"))
                }
            }

            // Login Student
            (method == "POST" && path == "/api/login") -> {
                try {
                    val json = JSONObject(body)
                    val username = (if (json.has("username")) json.optString("username") else json.optString("identifier")).trim()
                    val password = json.optString("password", "").trim()

                    val result = repository.authenticateStudent(username, password)
                    result.onSuccess { student ->
                        log("INFO", "تسجيل دخول الطالب: ${student.username}")
                        val res = JSONObject().apply {
                            put("success", true)
                            put("student", JSONObject().apply {
                                put("id", student.id)
                                put("username", student.username)
                                put("nationalId", student.nationalId)
                                put("phone", student.phone)
                                put("gradeSection", student.gradeSection)
                            })
                        }
                        sendJsonResponse(out, 200, res)
                    }.onFailure { err ->
                        sendJsonResponse(out, 401, JSONObject().put("success", false).put("message", err.message))
                    }
                } catch (e: Exception) {
                    sendJsonResponse(out, 400, JSONObject().put("success", false).put("message", "خطأ في تسجيل الدخول"))
                }
            }

            // Student Quizzes (Unattempted vs Completed)
            (method == "GET" && path == "/api/student-quizzes") -> {
                val studentName = query["student"] ?: ""
                val (unattempted, completed) = repository.getStudentQuizzesStatus(studentName)

                val res = JSONObject().apply {
                    val unattemptedArr = JSONArray()
                    unattempted.forEach { q ->
                        val full = repository.getQuizWithQuestions(q.id)
                        unattemptedArr.put(JSONObject().apply {
                            put("id", q.id)
                            put("title", q.title)
                            put("description", q.description)
                            put("durationMinutes", q.durationMinutes)
                            put("type", q.type)
                            put("isActive", q.isActive)
                            put("questionCount", full?.questions?.size ?: 0)
                        })
                    }
                    put("unattempted", unattemptedArr)
                    put("availableQuizzes", unattemptedArr)

                    val completedArr = JSONArray()
                    val sdf = java.text.SimpleDateFormat("yyyy/MM/dd hh:mm a", java.util.Locale.getDefault())
                    completed.forEach { (q, sub) ->
                        completedArr.put(JSONObject().apply {
                            put("quizId", q.id)
                            put("id", q.id)
                            put("title", q.title)
                            put("score", sub.score)
                            put("totalPoints", sub.totalPoints)
                            val pct = if (sub.totalPoints > 0) (sub.score * 100) / sub.totalPoints else 0
                            put("percentage", pct)
                            put("submittedAt", sub.submittedAt)
                            put("submittedAtFormatted", sdf.format(java.util.Date(sub.submittedAt)))
                        })
                    }
                    put("completed", completedArr)
                    put("completedQuizzes", completedArr)

                    val studentObj = if (studentName.isNotBlank()) repository.findStudentFlexibly(studentName) else null
                    val isGloballyVisible = repository.areGradesVisibleGlobally
                    val isStudentVisible = studentObj?.showGradesToStudent ?: true
                    val effectiveVisible = isGloballyVisible && isStudentVisible

                    val evalObj = JSONObject().apply {
                        put("isVisible", effectiveVisible)
                        put("exam1Score", studentObj?.exam1Score ?: 0.0)
                        put("exam2Score", studentObj?.exam2Score ?: 0.0)
                        put("participationScore", studentObj?.participationScore ?: 0.0)
                        put("bonusScore", studentObj?.bonusScore ?: 0.0)
                        put("totalScore", studentObj?.totalScore ?: 0.0)
                        put("notes", if (effectiveVisible && (studentObj?.showNotesToStudent ?: true)) (studentObj?.notes ?: "") else "")
                        put("hasNotes", !(studentObj?.notes.isNullOrBlank()))
                        put("gradeSection", studentObj?.gradeSection ?: "")
                    }
                    put("evaluation", evalObj)
                }
                sendJsonResponse(out, 200, res)
            }

            // List Active Quizzes
            (method == "GET" && path == "/api/quizzes") -> {
                val studentUsername = query["student"] ?: ""
                val activeQuizzes = repository.getActiveQuizzes()
                val pastSubmissions = if (studentUsername.isNotBlank()) {
                    repository.getStudentPastSubmissions(studentUsername)
                } else emptyList()

                val array = JSONArray()
                for (quiz in activeQuizzes) {
                    val full = repository.getQuizWithQuestions(quiz.id)
                    val pastSub = pastSubmissions.find { it.quizId == quiz.id }

                    val item = JSONObject().apply {
                        put("id", quiz.id)
                        put("title", quiz.title)
                        put("description", quiz.description)
                        put("durationMinutes", quiz.durationMinutes)
                        put("type", quiz.type)
                        put("questionCount", full?.questions?.size ?: 0)
                        put("isSubmitted", pastSub != null)
                        put("lastScore", if (pastSub != null) "${pastSub.score}/${pastSub.totalPoints}" else "")
                    }
                    array.put(item)
                }
                sendJsonStringResponse(out, 200, array.toString())
            }

            // Get Single Quiz Questions (WITHOUT leaking answers to students, with anti-retake check)
            (method == "GET" && path == "/api/quiz") -> {
                val quizId = query["id"]?.toLongOrNull() ?: 0L
                val student = query["student"] ?: ""

                // Strict check: If student already submitted, DO NOT allow opening questions!
                if (student.isNotBlank() && repository.hasStudentSubmittedQuiz(quizId, student)) {
                    val errMsg = "لقد قمت بأداء هذا الاختبار وحلّه مسبقاً! غير مسموح بإعادة المحاولة لحفظ سرية الأسئلة."
                    sendJsonResponse(
                        out,
                        403,
                        JSONObject().put("error", errMsg).put("message", errMsg)
                    )
                    return
                }

                val fullQuiz = repository.getQuizWithQuestions(quizId)
                if (fullQuiz != null && fullQuiz.quiz.isActive) {
                    val res = JSONObject().apply {
                        put("quiz", JSONObject().apply {
                            put("id", fullQuiz.quiz.id)
                            put("title", fullQuiz.quiz.title)
                            put("description", fullQuiz.quiz.description)
                            put("durationMinutes", fullQuiz.quiz.durationMinutes)
                            put("type", fullQuiz.quiz.type)
                        })
                        val qArray = JSONArray()
                        fullQuiz.questions.forEach { q ->
                            val qObj = JSONObject().apply {
                                put("id", q.id)
                                put("questionText", q.questionText)
                                put("questionType", q.questionType)
                                put("optionA", q.optionA)
                                put("optionB", q.optionB)
                                put("optionC", q.optionC)
                                put("optionD", q.optionD)
                                put("points", q.points)
                                // DO NOT expose q.correctAnswer
                            }
                            qArray.put(qObj)
                        }
                        put("questions", qArray)
                    }
                    sendJsonResponse(out, 200, res)
                } else {
                    val notFoundMsg = "هذا الاختبار غير متاح حالياً أو قام المعلم بإغلاقه مؤقتاً."
                    sendJsonResponse(out, 404, JSONObject().put("error", notFoundMsg).put("message", notFoundMsg))
                }
            }

            // Anti-Cheat External Internet Alert
            (method == "POST" && path == "/api/cheat-alert") -> {
                try {
                    val json = JSONObject(body)
                    val student = json.optString("student", "غير معروف")
                    val nationalId = json.optString("nationalId", "")
                    val reason = json.optString("reason", "اتصال بإنترنت خارجي (4G/5G)")
                    val idStr = if (nationalId.isNotBlank()) " - هوية: $nationalId" else ""
                    log("SECURITY_ALERT", "⚠️ تنبيه غش: تم رصد اتصال بالإنترنت لدى الطالب ($student$idStr) - السبب: $reason")
                    sendJsonResponse(out, 200, JSONObject().put("status", "logged"))
                } catch (_: Exception) {
                    sendJsonResponse(out, 200, JSONObject().put("status", "ignored"))
                }
            }

            // Submit Quiz Answers
            (method == "POST" && path == "/api/submit") -> {
                try {
                    val json = JSONObject(body)
                    val quizId = json.optLong("quizId", 0L)
                    val studentName = json.optString("studentUsername", "").trim()
                    val answersJson = json.optJSONObject("answers") ?: JSONObject()

                    val answersMap = mutableMapOf<Long, String>()
                    val keys = answersJson.keys()
                    while (keys.hasNext()) {
                        val key = keys.next()
                        val qId = key.toLongOrNull() ?: continue
                        answersMap[qId] = answersJson.optString(key, "")
                    }

                    val submissionResult = repository.submitQuizAnswers(quizId, studentName, answersMap)
                    submissionResult.onSuccess { sub ->
                        log(
                            "SUBMISSION",
                            "قام الطالب ${sub.studentUsername} بتسليم اختبار '${sub.quizTitle}' وحصل على: ${sub.score}/${sub.totalPoints} (%${sub.percentage})"
                        )
                        val res = JSONObject().apply {
                            put("success", true)
                            put("quizTitle", sub.quizTitle)
                            put("score", sub.score)
                            put("totalPoints", sub.totalPoints)
                            put("percentage", sub.percentage)
                        }
                        sendJsonResponse(out, 200, res)
                    }.onFailure { err ->
                        sendJsonResponse(out, 400, JSONObject().put("success", false).put("message", err.message))
                    }
                } catch (e: Exception) {
                    sendJsonResponse(out, 400, JSONObject().put("success", false).put("message", "خطأ في تسليم الإجابات"))
                }
            }

            else -> {
                sendResponse(out, 404, "Not Found", "text/plain", "Page Not Found")
            }
        }
    }

    private fun sendOptionsResponse(out: OutputStream) {
        val header = "HTTP/1.1 204 No Content\r\n" +
                "Access-Control-Allow-Origin: *\r\n" +
                "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n" +
                "Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With, Accept\r\n" +
                "Access-Control-Max-Age: 86400\r\n" +
                "Content-Length: 0\r\n" +
                "Connection: close\r\n\r\n"
        out.write(header.toByteArray(StandardCharsets.UTF_8))
        out.flush()
    }

    private fun sendResponse(
        out: OutputStream,
        statusCode: Int,
        statusText: String,
        contentType: String,
        body: String
    ) {
        val bodyBytes = body.toByteArray(StandardCharsets.UTF_8)
        val header = "HTTP/1.1 $statusCode $statusText\r\n" +
                "Content-Type: $contentType\r\n" +
                "Content-Length: ${bodyBytes.size}\r\n" +
                "Access-Control-Allow-Origin: *\r\n" +
                "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n" +
                "Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With, Accept\r\n" +
                "Connection: close\r\n\r\n"
        out.write(header.toByteArray(StandardCharsets.UTF_8))
        out.write(bodyBytes)
        out.flush()
    }

    private fun sendJsonResponse(out: OutputStream, statusCode: Int, json: JSONObject) {
        sendJsonStringResponse(out, statusCode, json.toString())
    }

    private fun sendJsonStringResponse(out: OutputStream, statusCode: Int, jsonString: String) {
        sendResponse(out, statusCode, if (statusCode == 200) "OK" else "Error", "application/json; charset=UTF-8", jsonString)
    }

    private fun parsePathAndQuery(fullPath: String): Pair<String, Map<String, String>> {
        val questionIdx = fullPath.indexOf('?')
        if (questionIdx == -1) return Pair(fullPath, emptyMap())

        val path = fullPath.substring(0, questionIdx)
        val queryString = fullPath.substring(questionIdx + 1)
        val params = mutableMapOf<String, String>()

        for (param in queryString.split("&")) {
            val pair = param.split("=")
            if (pair.size == 2) {
                try {
                    val k = URLDecoder.decode(pair[0], "UTF-8")
                    val v = URLDecoder.decode(pair[1], "UTF-8")
                    params[k] = v
                } catch (_: Exception) {}
            }
        }
        return Pair(path, params)
    }

    private fun log(type: String, message: String) {
        onLogEvent(ServerLogEvent(type = type, message = message))
    }

    companion object {
        fun getLocalIpAddress(preferMode: com.example.util.NetworkConnectionMode = com.example.util.NetworkConnectionMode.WIFI): String {
            return com.example.util.NetworkHelper.resolveIpForMode(preferMode)
        }
    }
}
