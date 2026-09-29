package com.example

import com.example.data.model.Student
import com.example.util.StudentCryptoManager
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [36])
class StudentCryptoManagerTest {

    @Test
    fun testEncryptAndDecryptStudents() {
        val testStudents = listOf(
            Student(id = 1, username = "أحمد محمد", password = "pass123", nationalId = "1001", phone = "0501111111", gradeSection = "أول ثانوي أ"),
            Student(id = 2, username = "سارة علي", password = "pass456", nationalId = "1002", phone = "0502222222", gradeSection = "أول ثانوي ب")
        )

        val encryptedPayload = StudentCryptoManager.encryptStudents(
            students = testStudents,
            secretKey = "SecretKey123"
        )

        assertNotNull(encryptedPayload)
        assertTrue(encryptedPayload.startsWith("CRS_ENC_V1:"))

        val result = StudentCryptoManager.decryptStudents(
            rawInput = encryptedPayload,
            secretKey = "SecretKey123"
        )

        assertTrue(result.isSuccess)
        val decryptedStudents = result.getOrNull()
        assertNotNull(decryptedStudents)
        assertEquals(2, decryptedStudents!!.size)
        assertEquals("أحمد محمد", decryptedStudents[0].username)
        assertEquals("pass123", decryptedStudents[0].password)
        assertEquals("سارة علي", decryptedStudents[1].username)
    }

    @Test
    fun testDefaultKeyAndShareableMessage() {
        val testStudents = listOf(
            Student(id = 3, username = "عمر فاروق", password = "9988", nationalId = "1003", phone = "", gradeSection = "ثالث")
        )

        val shareMessage = StudentCryptoManager.createShareableMessage(
            students = testStudents,
            teacherName = "أستاذ خالد"
        )

        assertTrue(shareMessage.contains("بيانات الطلاب المشفرة"))
        assertTrue(shareMessage.contains("أستاذ خالد"))

        // Decrypt from the full shareable message containing WhatsApp instructions
        val result = StudentCryptoManager.decryptStudents(
            rawInput = shareMessage,
            secretKey = ""
        )

        assertTrue(result.isSuccess)
        val decrypted = result.getOrNull()
        assertNotNull(decrypted)
        assertEquals(1, decrypted!!.size)
        assertEquals("عمر فاروق", decrypted[0].username)
        assertEquals("9988", decrypted[0].password)
    }
}
