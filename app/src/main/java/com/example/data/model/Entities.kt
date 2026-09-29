package com.example.data.model

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey
import androidx.room.Embedded
import androidx.room.Relation

@Entity(tableName = "students")
data class Student(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val username: String, // الاسم الرباعي للطالب
    val nationalId: String = "", // رقم الهوية أو الإقامة (إثبات الشخصية)
    val phone: String = "", // رقم التليفون
    val gradeSection: String = "", // الصف الثانوي والشعبة (مثال: أول ثانوي - شعبة 2)
    val password: String, // كلمة المرور التي يختارها الطالب
    val createdAt: Long = System.currentTimeMillis(),
    val notes: String = "", // ملاحظات المعلم
    val exam1Score: Double = 0.0, // درجات الاختبار الشهري الأول
    val exam2Score: Double = 0.0, // درجات الاختبار الشهري الثاني
    val participationScore: Double = 0.0, // درجات المشاركة والتفاعل الصفي
    val bonusScore: Double = 0.0, // درجات إضافية أو خصم (+ / -)
    val showGradesToStudent: Boolean = true, // إظهار أو إخفاء الدرجات لهذا الطالب بعينه
    val showNotesToStudent: Boolean = true // إظهار أو إخفاء الملاحظات لهذا الطالب
) {
    val totalScore: Double
        get() = exam1Score + exam2Score + participationScore + bonusScore

    /**
     * Extracts normalized Class and Section for grouping.
     * Example: "أول ثانوي - 2" -> Pair("أول ثانوي", "شعبة 2")
     */
    fun getClassAndSectionDisplay(): Pair<String, String> {
        val raw = gradeSection.trim()
        if (raw.isBlank()) return Pair("بدون فصل محدد", "عام")
        val delimiters = listOf(" - ", " -", "- ", "-", " / ", "/", "،", ",")
        for (d in delimiters) {
            if (raw.contains(d)) {
                val parts = raw.split(d, limit = 2)
                val c = parts[0].trim().ifBlank { "فصل عام" }
                val s = parts.getOrNull(1)?.trim()?.ifBlank { "عام" } ?: "عام"
                val formattedSection = if (s.startsWith("شعبة") || s.startsWith("فصل")) s else "شعبة $s"
                return Pair(c, formattedSection)
            }
        }
        return Pair(raw, "عام")
    }
}

@Entity(tableName = "quizzes")
data class Quiz(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val title: String,
    val description: String = "",
    val durationMinutes: Int = 10,
    val isActive: Boolean = true, // Whether open for students to take right now
    val type: String = "QUIZ", // "QUIZ" or "ACTIVITY"
    val createdAt: Long = System.currentTimeMillis()
)

@Entity(
    tableName = "questions",
    foreignKeys = [
        ForeignKey(
            entity = Quiz::class,
            parentColumns = ["id"],
            childColumns = ["quizId"],
            onDelete = ForeignKey.CASCADE
        )
    ],
    indices = [Index("quizId")]
)
data class Question(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val quizId: Long,
    val questionText: String,
    val questionType: String = "MULTIPLE_CHOICE", // "MULTIPLE_CHOICE", "TRUE_FALSE", "SHORT_ANSWER"
    val optionA: String = "",
    val optionB: String = "",
    val optionC: String = "",
    val optionD: String = "",
    val correctAnswer: String = "A", // "A", "B", "C", "D", "TRUE", "FALSE", or keyword
    val points: Int = 1
)

@Entity(
    tableName = "submissions",
    foreignKeys = [
        ForeignKey(
            entity = Quiz::class,
            parentColumns = ["id"],
            childColumns = ["quizId"],
            onDelete = ForeignKey.CASCADE
        )
    ],
    indices = [Index("quizId")]
)
data class Submission(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val quizId: Long,
    val studentUsername: String,
    val score: Int,
    val totalPoints: Int,
    val answersJson: String, // JSON map of questionId -> studentAnswer
    val submittedAt: Long = System.currentTimeMillis()
)

data class QuizWithQuestions(
    @Embedded val quiz: Quiz,
    @Relation(
        parentColumn = "id",
        entityColumn = "quizId"
    )
    val questions: List<Question>
)
