package com.example.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.example.data.model.Question
import com.example.data.model.Quiz
import com.example.data.model.Student
import com.example.data.model.Submission

@Database(
    entities = [
        Student::class,
        Quiz::class,
        Question::class,
        Submission::class
    ],
    version = 3,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun studentDao(): StudentDao
    abstract fun quizDao(): QuizDao
    abstract fun submissionDao(): SubmissionDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getInstance(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                INSTANCE ?: buildDatabase(context).also { INSTANCE = it }
            }
        }

        private fun buildDatabase(context: Context): AppDatabase {
            val appContext = context.applicationContext
            return try {
                Room.databaseBuilder(
                    appContext,
                    AppDatabase::class.java,
                    "classroom_quiz_server.db"
                )
                .fallbackToDestructiveMigration()
                .build()
            } catch (e: Throwable) {
                // If any integrity or schema issue occurs, delete old db and recreate
                try {
                    appContext.deleteDatabase("classroom_quiz_server.db")
                } catch (_: Throwable) {}
                Room.databaseBuilder(
                    appContext,
                    AppDatabase::class.java,
                    "classroom_quiz_server.db"
                )
                .fallbackToDestructiveMigration()
                .build()
            }
        }
    }
}
