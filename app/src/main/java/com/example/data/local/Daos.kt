package com.example.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Transaction
import androidx.room.Update
import com.example.data.model.Question
import com.example.data.model.Quiz
import com.example.data.model.QuizWithQuestions
import com.example.data.model.Student
import com.example.data.model.Submission
import kotlinx.coroutines.flow.Flow

@Dao
interface StudentDao {
    @Query("SELECT * FROM students ORDER BY createdAt DESC")
    fun getAllStudentsFlow(): Flow<List<Student>>

    @Query("SELECT * FROM students WHERE LOWER(TRIM(username)) = LOWER(TRIM(:username)) LIMIT 1")
    suspend fun findByUsername(username: String): Student?

    @Query("SELECT * FROM students WHERE id = :id LIMIT 1")
    suspend fun findById(id: Long): Student?

    @Query("SELECT * FROM students WHERE TRIM(nationalId) = TRIM(:nid) AND nationalId != '' LIMIT 1")
    suspend fun findByNationalId(nid: String): Student?

    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insertStudent(student: Student): Long

    @Update
    suspend fun updateStudent(student: Student)

    @Query("DELETE FROM students WHERE id = :id")
    suspend fun deleteStudent(id: Long)

    @Query("UPDATE students SET exam1Score = :exam1, exam2Score = :exam2, participationScore = :participation, bonusScore = :bonus, notes = :notes, showGradesToStudent = :showGrades, showNotesToStudent = :showNotes WHERE id = :id")
    suspend fun updateStudentEvaluation(
        id: Long,
        exam1: Double,
        exam2: Double,
        participation: Double,
        bonus: Double,
        notes: String,
        showGrades: Boolean,
        showNotes: Boolean
    )

    @Query("UPDATE students SET bonusScore = bonusScore + :delta WHERE id = :id")
    suspend fun adjustStudentBonus(id: Long, delta: Double)

    @Query("UPDATE students SET showGradesToStudent = :show")
    suspend fun setAllStudentsGradesVisibility(show: Boolean)

    @Query("UPDATE students SET gradeSection = :gradeSection WHERE id = :id")
    suspend fun updateStudentClassSection(id: Long, gradeSection: String)

    @Query("SELECT COUNT(*) FROM students")
    suspend fun getStudentCount(): Int

    @Query("SELECT * FROM students")
    suspend fun getAllStudentsList(): List<Student>
}

@Dao
interface QuizDao {
    @Query("SELECT * FROM quizzes ORDER BY createdAt DESC")
    fun getAllQuizzesFlow(): Flow<List<Quiz>>

    @Query("SELECT * FROM quizzes WHERE isActive = 1 ORDER BY createdAt DESC")
    suspend fun getActiveQuizzes(): List<Quiz>

    @Query("SELECT * FROM quizzes WHERE id = :id LIMIT 1")
    suspend fun getQuizById(id: Long): Quiz?

    @Transaction
    @Query("SELECT * FROM quizzes WHERE id = :quizId LIMIT 1")
    suspend fun getQuizWithQuestions(quizId: Long): QuizWithQuestions?

    @Transaction
    @Query("SELECT * FROM quizzes WHERE isActive = 1 ORDER BY createdAt DESC")
    suspend fun getAllActiveQuizzesWithQuestions(): List<QuizWithQuestions>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertQuiz(quiz: Quiz): Long

    @Update
    suspend fun updateQuiz(quiz: Quiz)

    @Query("UPDATE quizzes SET isActive = :isActive WHERE id = :quizId")
    suspend fun setQuizActive(quizId: Long, isActive: Boolean)

    @Query("DELETE FROM quizzes WHERE id = :quizId")
    suspend fun deleteQuiz(quizId: Long)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertQuestions(questions: List<Question>)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertQuestion(question: Question): Long

    @Query("DELETE FROM questions WHERE id = :questionId")
    suspend fun deleteQuestion(questionId: Long)

    @Query("SELECT COUNT(*) FROM quizzes")
    suspend fun getQuizCount(): Int

    @Query("SELECT * FROM quizzes ORDER BY createdAt DESC")
    suspend fun getAllQuizzesList(): List<Quiz>
}

@Dao
interface SubmissionDao {
    @Query("SELECT * FROM submissions ORDER BY submittedAt DESC")
    fun getAllSubmissionsFlow(): Flow<List<Submission>>

    @Query("SELECT * FROM submissions ORDER BY submittedAt DESC")
    suspend fun getAllSubmissionsList(): List<Submission>

    @Query("SELECT * FROM submissions WHERE quizId = :quizId ORDER BY submittedAt DESC")
    fun getSubmissionsForQuizFlow(quizId: Long): Flow<List<Submission>>

    @Query("SELECT * FROM submissions WHERE LOWER(TRIM(studentUsername)) = LOWER(TRIM(:username)) ORDER BY submittedAt DESC")
    suspend fun getSubmissionsForStudent(username: String): List<Submission>

    @Query("SELECT * FROM submissions WHERE quizId = :quizId AND LOWER(TRIM(studentUsername)) = LOWER(TRIM(:username)) LIMIT 1")
    suspend fun findSubmission(quizId: Long, username: String): Submission?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertSubmission(submission: Submission): Long

    @Query("DELETE FROM submissions WHERE id = :id")
    suspend fun deleteSubmission(id: Long)

    @Query("DELETE FROM submissions WHERE quizId = :quizId")
    suspend fun deleteSubmissionsForQuiz(quizId: Long)
}
