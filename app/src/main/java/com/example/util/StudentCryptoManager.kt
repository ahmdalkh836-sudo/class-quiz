package com.example.util

import android.util.Base64
import com.example.data.model.Student
import org.json.JSONArray
import org.json.JSONObject
import java.nio.charset.StandardCharsets
import java.security.MessageDigest
import java.security.SecureRandom
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import javax.crypto.Cipher
import javax.crypto.spec.IvParameterSpec
import javax.crypto.spec.SecretKeySpec

object StudentCryptoManager {

    // Default shared classroom key so teachers can exchange student data out-of-the-box
    const val DEFAULT_KEY: String = "ClassroomQuiz#2026!SecureKey"
    private const val PREFIX = "CRS_ENC_V1:"
    private const val ALGORITHM = "AES/CBC/PKCS5Padding"

    private fun deriveKey(secret: String): SecretKeySpec {
        val digest = MessageDigest.getInstance("SHA-256")
        val keyBytes = digest.digest(secret.toByteArray(StandardCharsets.UTF_8))
        return SecretKeySpec(keyBytes, "AES")
    }

    /**
     * Serializes and encrypts a list of students using AES-256.
     */
    fun encryptStudents(students: List<Student>, secretKey: String = DEFAULT_KEY): String {
        val jsonArray = JSONArray()
        for (s in students) {
            val obj = JSONObject().apply {
                put("username", s.username)
                put("nationalId", s.nationalId)
                put("phone", s.phone)
                put("gradeSection", s.gradeSection)
                put("password", s.password)
                put("notes", s.notes)
                put("createdAt", s.createdAt)
                put("exam1Score", s.exam1Score)
                put("exam2Score", s.exam2Score)
                put("participationScore", s.participationScore)
                put("bonusScore", s.bonusScore)
                put("showGradesToStudent", s.showGradesToStudent)
                put("showNotesToStudent", s.showNotesToStudent)
            }
            jsonArray.put(obj)
        }

        val jsonString = jsonArray.toString()
        val plainBytes = jsonString.toByteArray(StandardCharsets.UTF_8)

        // Generate 16-byte random IV
        val iv = ByteArray(16)
        SecureRandom().nextBytes(iv)

        val keySpec = deriveKey(secretKey.ifBlank { DEFAULT_KEY })
        val cipher = Cipher.getInstance(ALGORITHM)
        cipher.init(Cipher.ENCRYPT_MODE, keySpec, IvParameterSpec(iv))
        val encryptedBytes = cipher.doFinal(plainBytes)

        // Combine IV + EncryptedBytes
        val combined = ByteArray(iv.size + encryptedBytes.size)
        System.arraycopy(iv, 0, combined, 0, iv.size)
        System.arraycopy(encryptedBytes, 0, combined, iv.size, encryptedBytes.size)

        val base64 = Base64.encodeToString(combined, Base64.NO_WRAP)
        return PREFIX + base64
    }

    /**
     * Decrypts an encrypted payload string back into a list of students.
     * Can extract the code even if surrounded by instructions from WhatsApp or notes.
     */
    fun decryptStudents(rawInput: String, secretKey: String = DEFAULT_KEY): Result<List<Student>> {
        return try {
            val cleanedCode = extractEncryptedPayload(rawInput)
                ?: return Result.failure(IllegalArgumentException("لم يتم العثور على كود تشفير صالح في النص المدخل!"))

            val combined = Base64.decode(cleanedCode, Base64.DEFAULT)
            if (combined.size < 17) {
                return Result.failure(IllegalArgumentException("كود التشفير تالف أو غير مكتمل."))
            }

            val iv = ByteArray(16)
            val encryptedBytes = ByteArray(combined.size - 16)
            System.arraycopy(combined, 0, iv, 0, 16)
            System.arraycopy(combined, 16, encryptedBytes, 0, encryptedBytes.size)

            val keySpec = deriveKey(secretKey.ifBlank { DEFAULT_KEY })
            val cipher = Cipher.getInstance(ALGORITHM)
            cipher.init(Cipher.DECRYPT_MODE, keySpec, IvParameterSpec(iv))
            val decryptedBytes = cipher.doFinal(encryptedBytes)

            val jsonString = String(decryptedBytes, StandardCharsets.UTF_8)
            val jsonArray = JSONArray(jsonString)

            val students = mutableListOf<Student>()
            for (i in 0 until jsonArray.length()) {
                val obj = jsonArray.getJSONObject(i)
                val username = obj.optString("username", "").trim()
                if (username.isBlank()) continue

                students.add(
                    Student(
                        username = username,
                        nationalId = obj.optString("nationalId", "").trim(),
                        phone = obj.optString("phone", "").trim(),
                        gradeSection = obj.optString("gradeSection", "").trim(),
                        password = obj.optString("password", "123456"),
                        notes = obj.optString("notes", ""),
                        createdAt = obj.optLong("createdAt", System.currentTimeMillis()),
                        exam1Score = obj.optDouble("exam1Score", 0.0),
                        exam2Score = obj.optDouble("exam2Score", 0.0),
                        participationScore = obj.optDouble("participationScore", 0.0),
                        bonusScore = obj.optDouble("bonusScore", 0.0),
                        showGradesToStudent = obj.optBoolean("showGradesToStudent", true),
                        showNotesToStudent = obj.optBoolean("showNotesToStudent", true)
                    )
                )
            }

            if (students.isEmpty()) {
                Result.failure(IllegalArgumentException("الكود المشفر لا يحتوي على أي بيانات طلاب."))
            } else {
                Result.success(students)
            }
        } catch (e: javax.crypto.BadPaddingException) {
            Result.failure(IllegalArgumentException("كلمة المرور غير صحيحة أو كود التشفير تالف!"))
        } catch (e: Throwable) {
            Result.failure(IllegalArgumentException("فشل فك التشفير: ${e.localizedMessage ?: "بيانات غير صالحة"}"))
        }
    }

    /**
     * Extracts the core Base64 payload from raw text.
     */
    private fun extractEncryptedPayload(text: String): String? {
        val trimmed = text.trim()

        // If prefixed with PREFIX
        if (trimmed.contains(PREFIX)) {
            val after = trimmed.substringAfter(PREFIX)
            val token = after.split(Regex("[\\s\\n\\r]+")).firstOrNull { it.isNotBlank() }
            return token?.trim()
        }

        // Search for regex of Base64 token
        val match = Regex("[A-Za-z0-9+/=]{40,}").find(trimmed)
        return match?.value?.trim()
    }

    /**
     * Creates a complete, ready-to-share message with instructions.
     */
    fun createShareableMessage(
        students: List<Student>,
        teacherName: String,
        isCustomKey: Boolean = false,
        customKey: String = ""
    ): String {
        val encryptedPayload = encryptStudents(students, if (isCustomKey) customKey else DEFAULT_KEY)
        val dateStr = SimpleDateFormat("yyyy/MM/dd hh:mm a", Locale.getDefault()).format(Date())
        val teacherDisplay = if (teacherName.isNotBlank()) teacherName else "معلم المادة"

        return buildString {
            appendLine("═══════════════════════════════")
            appendLine("📋 بيانات الطلاب المشفرة - خادم الاختبارات")
            appendLine("═══════════════════════════════")
            appendLine("👤 المعلم: $teacherDisplay")
            appendLine("👥 عدد الطلاب: ${students.size} طالب")
            appendLine("📅 التاريخ: $dateStr")
            if (isCustomKey) {
                appendLine("🔑 كلمة سر فك التشفير: $customKey")
            } else {
                appendLine("🔑 التشفير: مفتاح الفصل الافتراضي (سيتعرف عليه التطبيق تلقائياً)")
            }
            appendLine("───────────────────────────────")
            appendLine("🔒 الكود المشفر (انسخ الكود التالي بالكامل):")
            appendLine(encryptedPayload)
            appendLine("───────────────────────────────")
            appendLine("💡 طريقة وضع البيانات في التطبيق:")
            appendLine("1. افتح تطبيق خادم الاختبارات.")
            appendLine("2. ادخل تبويب (الطلاب) واضغط على (استيراد طلاب مشفرة).")
            appendLine("3. الصق هذا الكود واضغط (استيراد وحفظ).")
        }
    }
}
