package com.example.data.repository

import com.example.data.local.AppDatabase
import com.example.data.model.Question
import com.example.data.model.Quiz
import com.example.data.model.QuizWithQuestions
import com.example.data.model.Student
import com.example.data.model.Submission
import kotlinx.coroutines.flow.Flow
import org.json.JSONObject

class QuizRepository(private val database: AppDatabase) {

    private val studentDao = database.studentDao()
    private val quizDao = database.quizDao()
    private val submissionDao = database.submissionDao()

    // Flow streams for UI
    val allQuizzesFlow: Flow<List<Quiz>> = quizDao.getAllQuizzesFlow()
    val allStudentsFlow: Flow<List<Student>> = studentDao.getAllStudentsFlow()
    val allSubmissionsFlow: Flow<List<Submission>> = submissionDao.getAllSubmissionsFlow()

    fun getSubmissionsForQuizFlow(quizId: Long): Flow<List<Submission>> =
        submissionDao.getSubmissionsForQuizFlow(quizId)

    suspend fun getQuizWithQuestions(quizId: Long): QuizWithQuestions? =
        quizDao.getQuizWithQuestions(quizId)

    suspend fun getActiveQuizzes(): List<Quiz> =
        quizDao.getActiveQuizzes()

    suspend fun insertQuiz(quiz: Quiz, questions: List<Question>): Long {
        val quizId = quizDao.insertQuiz(quiz)
        val questionsWithQuizId = questions.map { it.copy(quizId = quizId) }
        quizDao.insertQuestions(questionsWithQuizId)
        return quizId
    }

    suspend fun setQuizActive(quizId: Long, isActive: Boolean) {
        quizDao.setQuizActive(quizId, isActive)
    }

    suspend fun deleteQuiz(quizId: Long) {
        quizDao.deleteQuiz(quizId)
    }

    suspend fun getAllStudents(): List<Student> = studentDao.getAllStudentsList()

    suspend fun getAllQuizzes(): List<Quiz> = quizDao.getAllQuizzesList()

    suspend fun getAllSubmissions(): List<Submission> = submissionDao.getAllSubmissionsList()

    // Student operations
    private fun normalizeArabic(text: String): String {
        return text.trim()
            .replace(Regex("[\u064B-\u0652\u0670]"), "") // remove tashkeel/diacritics
            .replace(Regex("[أإآٱ]"), "ا")
            .replace('ة', 'ه')
            .replace('ى', 'ي')
            .replace("ـ", "") // tatweel
            .replace(Regex("\\s+"), " ")
            .lowercase()
    }

    suspend fun findStudentFlexibly(username: String): Student? {
        val cleanName = username.trim()
        if (cleanName.isBlank()) return null
        val exact = studentDao.findByUsername(cleanName)
        if (exact != null) return exact

        val targetNorm = normalizeArabic(cleanName)
        val allStudents = studentDao.getAllStudentsList()
        return allStudents.find { normalizeArabic(it.username) == targetNorm }
    }

    suspend fun findStudentByIdentifier(identifier: String): Student? {
        val clean = identifier.trim()
        if (clean.isBlank()) return null
        val byNid = studentDao.findByNationalId(clean)
        if (byNid != null) return byNid
        return findStudentFlexibly(clean)
    }

    suspend fun registerStudent(
        username: String,
        password: String,
        nationalId: String = "",
        phone: String = "",
        gradeSection: String = ""
    ): Result<Student> {
        val cleanName = username.trim()
        val cleanNid = nationalId.trim()
        val cleanPhone = phone.trim()
        val cleanPass = password.trim()
        if (cleanName.isBlank()) {
            return Result.failure(IllegalArgumentException("يرجى إدخال اسم الطالب الرباعي"))
        }
        if (cleanPass.isBlank()) {
            return Result.failure(IllegalArgumentException("يرجى إدخال كلمة المرور"))
        }

        var existing = findStudentFlexibly(cleanName)
        if (existing == null && cleanNid.isNotBlank()) {
            existing = studentDao.findByNationalId(cleanNid)
        }

        if (existing != null) {
            // If already registered and password matches, smoothly log the student in
            if (existing.password == cleanPass) {
                return Result.success(existing)
            }
            return Result.failure(IllegalArgumentException("هذا الاسم أو رقم الهوية مسجل بالفعل! إذا كان هذا حسابك، انتقل لتبويب (تسجيل الدخول)، أو راجع المعلم."))
        }

        val student = Student(
            username = cleanName,
            nationalId = cleanNid,
            phone = cleanPhone,
            gradeSection = gradeSection.trim(),
            password = cleanPass,
            createdAt = System.currentTimeMillis()
        )
        val id = studentDao.insertStudent(student)
        return Result.success(student.copy(id = id))
    }

    suspend fun authenticateStudent(identifier: String, password: String): Result<Student> {
        val cleanId = identifier.trim()
        val cleanPass = password.trim()
        val existing = findStudentByIdentifier(cleanId)
            ?: return Result.failure(IllegalArgumentException("الاسم أو رقم الهوية غير مسجل لدى المعلم. يرجى استخدام تبويب (تسجيل جديد) أولاً!"))

        if (existing.password != cleanPass) {
            return Result.failure(IllegalArgumentException("كلمة المرور غير صحيحة! تأكد منها أو اطلب من المعلم إعادة تعيينها لك."))
        }
        return Result.success(existing)
    }

    suspend fun hasStudentSubmittedQuiz(quizId: Long, studentUsername: String): Boolean {
        return submissionDao.findSubmission(quizId, studentUsername.trim()) != null
    }

    suspend fun getStudentQuizzesStatus(username: String): Pair<List<Quiz>, List<Pair<Quiz, Submission>>> {
        val activeQuizzes = quizDao.getActiveQuizzes()
        val studentSubmissions = submissionDao.getSubmissionsForStudent(username.trim())
        val submittedQuizIds = studentSubmissions.map { it.quizId }.toSet()

        val unattempted = activeQuizzes.filter { it.id !in submittedQuizIds }
        val completed = studentSubmissions.mapNotNull { sub ->
            val quiz = quizDao.getQuizById(sub.quizId) ?: Quiz(id = sub.quizId, title = "اختبار منجز", isActive = false)
            Pair(quiz, sub)
        }
        return Pair(unattempted, completed)
    }

    suspend fun updateStudentPassword(studentId: Long, newPass: String) {
        val student = studentDao.findById(studentId) ?: return
        studentDao.updateStudent(student.copy(password = newPass.trim()))
    }

    suspend fun deleteStudent(studentId: Long) {
        studentDao.deleteStudent(studentId)
    }

    suspend fun importStudents(students: List<Student>, overwriteExisting: Boolean = false): StudentImportResult {
        var added = 0
        var updated = 0
        var skipped = 0

        for (st in students) {
            val cleanName = st.username.trim()
            val cleanNid = st.nationalId.trim()
            if (cleanName.isBlank()) continue

            val existing = when {
                cleanNid.isNotBlank() -> studentDao.findByNationalId(cleanNid) ?: studentDao.findByUsername(cleanName)
                else -> studentDao.findByUsername(cleanName)
            }

            if (existing == null) {
                studentDao.insertStudent(st.copy(id = 0))
                added++
            } else if (overwriteExisting) {
                studentDao.updateStudent(
                    existing.copy(
                        nationalId = if (cleanNid.isNotBlank()) cleanNid else existing.nationalId,
                        phone = if (st.phone.isNotBlank()) st.phone else existing.phone,
                        gradeSection = if (st.gradeSection.isNotBlank()) st.gradeSection else existing.gradeSection,
                        password = if (st.password.isNotBlank()) st.password else existing.password,
                        notes = if (st.notes.isNotBlank()) st.notes else existing.notes,
                        exam1Score = if (st.exam1Score > 0) st.exam1Score else existing.exam1Score,
                        exam2Score = if (st.exam2Score > 0) st.exam2Score else existing.exam2Score,
                        participationScore = if (st.participationScore > 0) st.participationScore else existing.participationScore,
                        bonusScore = if (st.bonusScore != 0.0) st.bonusScore else existing.bonusScore,
                        showGradesToStudent = st.showGradesToStudent,
                        showNotesToStudent = st.showNotesToStudent
                    )
                )
                updated++
            } else {
                skipped++
            }
        }
        return StudentImportResult(added = added, updated = updated, skipped = skipped)
    }

    suspend fun updateStudentEvaluation(
        studentId: Long,
        exam1: Double,
        exam2: Double,
        participation: Double,
        bonus: Double,
        notes: String,
        showGrades: Boolean,
        showNotes: Boolean
    ) {
        studentDao.updateStudentEvaluation(
            id = studentId,
            exam1 = exam1,
            exam2 = exam2,
            participation = participation,
            bonus = bonus,
            notes = notes.trim(),
            showGrades = showGrades,
            showNotes = showNotes
        )
    }

    suspend fun adjustStudentBonus(studentId: Long, delta: Double) {
        studentDao.adjustStudentBonus(studentId, delta)
    }

    suspend fun setAllStudentsGradesVisibility(show: Boolean) {
        studentDao.setAllStudentsGradesVisibility(show)
    }

    suspend fun updateStudentClassSection(studentId: Long, gradeSection: String) {
        studentDao.updateStudentClassSection(studentId, gradeSection.trim())
    }

    // Global setting for grades visibility in web portal
    @Volatile
    var areGradesVisibleGlobally: Boolean = true

    // Submission & Grading
    suspend fun submitQuizAnswers(
        quizId: Long,
        studentUsername: String,
        answersMap: Map<Long, String> // questionId -> answer chosen
    ): Result<SubmissionResult> {
        val trimmedUsername = studentUsername.trim()
        // Prevent retaking quiz:
        if (submissionDao.findSubmission(quizId, trimmedUsername) != null) {
            return Result.failure(IllegalArgumentException("لقد قمت بأداء هذا الاختبار بالفعل مسبقاً! غير مسموح بإعادة المحاولة."))
        }

        val quizWithQ = quizDao.getQuizWithQuestions(quizId)
            ?: return Result.failure(IllegalArgumentException("الاختبار غير موجود أو تم حذفه"))

        var totalScore = 0
        var maxPoints = 0
        val resultsObject = JSONObject()

        for (question in quizWithQ.questions) {
            maxPoints += question.points
            val studentAns = (answersMap[question.id] ?: "").trim()
            val isCorrect = when (question.questionType) {
                "MULTIPLE_CHOICE", "TRUE_FALSE" -> {
                    studentAns.equals(question.correctAnswer.trim(), ignoreCase = true)
                }
                "SHORT_ANSWER" -> {
                    // For short answer / activities, award points if answered or matches keyword
                    if (question.correctAnswer.isBlank()) {
                        studentAns.isNotBlank()
                    } else {
                        studentAns.contains(question.correctAnswer.trim(), ignoreCase = true)
                    }
                }
                else -> false
            }

            val questionScore = if (isCorrect) question.points else 0
            totalScore += questionScore

            val qDetail = JSONObject().apply {
                put("questionText", question.questionText)
                put("studentAnswer", studentAns)
                put("correctAnswer", question.correctAnswer)
                put("isCorrect", isCorrect)
                put("pointsAwarded", questionScore)
                put("maxPoints", question.points)
            }
            resultsObject.put(question.id.toString(), qDetail)
        }

        val submission = Submission(
            quizId = quizId,
            studentUsername = studentUsername.trim(),
            score = totalScore,
            totalPoints = if (maxPoints > 0) maxPoints else 1,
            answersJson = resultsObject.toString(),
            submittedAt = System.currentTimeMillis()
        )

        val subId = submissionDao.insertSubmission(submission)
        return Result.success(
            SubmissionResult(
                submissionId = subId,
                quizTitle = quizWithQ.quiz.title,
                studentUsername = studentUsername,
                score = totalScore,
                totalPoints = maxPoints,
                percentage = if (maxPoints > 0) (totalScore * 100) / maxPoints else 100
            )
        )
    }

    suspend fun getStudentPastSubmissions(username: String): List<Submission> {
        return submissionDao.getSubmissionsForStudent(username)
    }

    suspend fun ensureDefaultQuizzes() {
        if (quizDao.getQuizCount() == 0) {
            // Seed starter quiz: "اختبار مراجعة الحصة"
            val quiz1 = Quiz(
                title = "اختبار مراجعة سريع في الحصة",
                description = "اختبار قصير للتأكد من استيعاب المفاهيم الأساسية لدرس اليوم",
                durationMinutes = 5,
                isActive = true,
                type = "QUIZ"
            )
            val questions1 = listOf(
                Question(
                    quizId = 0,
                    questionText = "ما هي وحدة قياس القوة في النظام الدولي؟",
                    questionType = "MULTIPLE_CHOICE",
                    optionA = "النيوتن (Newton)",
                    optionB = "الجول (Joule)",
                    optionC = "الواط (Watt)",
                    optionD = "الباسكال (Pascal)",
                    correctAnswer = "A",
                    points = 2
                ),
                Question(
                    quizId = 0,
                    questionText = "تتحرك الإلكترونات حول النواة في مدارات محددة.",
                    questionType = "TRUE_FALSE",
                    optionA = "صح",
                    optionB = "خطأ",
                    correctAnswer = "TRUE",
                    points = 1
                ),
                Question(
                    quizId = 0,
                    questionText = "أي كوكب هو الأقرب إلى الشمس؟",
                    questionType = "MULTIPLE_CHOICE",
                    optionA = "الزهرة",
                    optionB = "عطارد",
                    optionC = "المريخ",
                    optionD = "الأرض",
                    correctAnswer = "B",
                    points = 2
                ),
                Question(
                    quizId = 0,
                    questionText = "نشاط تأملي: اذكر بإيجاز فكرة واحدة جديدة تعلمتها في حصة اليوم وكيف تفيدك؟",
                    questionType = "SHORT_ANSWER",
                    correctAnswer = "",
                    points = 2
                )
            )
            insertQuiz(quiz1, questions1)

            // Seed an activity
            val quiz2 = Quiz(
                title = "نشاط تفاعلي: لغز وتفكير إبداعي",
                description = "شارك بحلك واختبر سرعتك مع زملائك في الفصل!",
                durationMinutes = 7,
                isActive = true,
                type = "ACTIVITY"
            )
            val questions2 = listOf(
                Question(
                    quizId = 0,
                    questionText = "شيء كلما أخذت منه كَبُر، فما هو؟",
                    questionType = "MULTIPLE_CHOICE",
                    optionA = "الحفرة",
                    optionB = "العمر",
                    optionC = "المال",
                    optionD = "الصندوق",
                    correctAnswer = "A",
                    points = 3
                ),
                Question(
                    quizId = 0,
                    questionText = "الصوت ينتقل في الفراغ أسرع من الهواء.",
                    questionType = "TRUE_FALSE",
                    optionA = "صح",
                    optionB = "خطأ (لا ينتقل في الفراغ)",
                    correctAnswer = "FALSE",
                    points = 2
                )
            )
            insertQuiz(quiz2, questions2)
        }
    }
}

data class SubmissionResult(
    val submissionId: Long,
    val quizTitle: String,
    val studentUsername: String,
    val score: Int,
    val totalPoints: Int,
    val percentage: Int
)

data class StudentImportResult(
    val added: Int,
    val updated: Int,
    val skipped: Int
)

