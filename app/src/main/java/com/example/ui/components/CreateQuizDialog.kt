package com.example.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.FormatListNumbered
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.example.data.model.Question
import com.example.ui.theme.BrandDanger
import com.example.ui.theme.BrandPrimary
import com.example.ui.theme.BrandSuccess

data class DraftQuestion(
    val id: Long = System.currentTimeMillis() + (0..999).random(),
    var questionText: String = "",
    var questionType: String = "MULTIPLE_CHOICE", // "MULTIPLE_CHOICE", "TRUE_FALSE", "SHORT_ANSWER"
    var optionA: String = "",
    var optionB: String = "",
    var optionC: String = "",
    var optionD: String = "",
    var correctAnswer: String = "A",
    var points: Int = 1
)

@Composable
fun CreateQuizDialog(
    onDismiss: () -> Unit,
    onSave: (title: String, desc: String, duration: Int, type: String, questions: List<Question>) -> Unit
) {
    var title by remember { mutableStateOf("") }
    var description by remember { mutableStateOf("") }
    var durationMinutes by remember { mutableIntStateOf(10) }
    var quizType by remember { mutableStateOf("QUIZ") } // "QUIZ" or "ACTIVITY"

    val draftQuestions = remember {
        mutableStateListOf(
            DraftQuestion(
                questionText = "",
                questionType = "MULTIPLE_CHOICE",
                optionA = "",
                optionB = "",
                optionC = "",
                optionD = "",
                correctAnswer = "A",
                points = 2
            )
        )
    }

    var errorMessage by remember { mutableStateOf<String?>(null) }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Surface(
            modifier = Modifier
                .fillMaxWidth(0.95f)
                .clip(RoundedCornerShape(24.dp)),
            color = MaterialTheme.colorScheme.surface
        ) {
            Column(
                modifier = Modifier
                    .padding(20.dp)
                    .verticalScroll(rememberScrollState())
            ) {
                // Header
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = if (quizType == "QUIZ") "إنشاء اختبار جديد للحصة" else "إنشاء نشاط تفاعلي للحصة",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold
                    )
                    IconButton(onClick = onDismiss) {
                        Icon(imageVector = Icons.Default.Close, contentDescription = "إغلاق")
                    }
                }

                Spacer(modifier = Modifier.height(14.dp))

                // Type Toggle (Quiz vs Activity)
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .background(MaterialTheme.colorScheme.surfaceVariant)
                        .padding(4.dp),
                    horizontalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .clip(RoundedCornerShape(8.dp))
                            .background(if (quizType == "QUIZ") BrandPrimary else Color.Transparent)
                            .clickable { quizType = "QUIZ" }
                            .padding(vertical = 8.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "اختبار / تقييم 📝",
                            fontWeight = FontWeight.Bold,
                            color = if (quizType == "QUIZ") Color.White else MaterialTheme.colorScheme.onSurface
                        )
                    }

                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .clip(RoundedCornerShape(8.dp))
                            .background(if (quizType == "ACTIVITY") BrandPrimary else Color.Transparent)
                            .clickable { quizType = "ACTIVITY" }
                            .padding(vertical = 8.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "نشاط / مشاركة 💡",
                            fontWeight = FontWeight.Bold,
                            color = if (quizType == "ACTIVITY") Color.White else MaterialTheme.colorScheme.onSurface
                        )
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                // Basic Info
                OutlinedTextField(
                    value = title,
                    onValueChange = { title = it },
                    label = { Text("عنوان الاختبار أو النشاط *") },
                    placeholder = { Text("مثال: اختبار قصير في مادة الرياضيات") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .testTag("quiz_title_input"),
                    shape = RoundedCornerShape(12.dp),
                    singleLine = true
                )

                Spacer(modifier = Modifier.height(10.dp))

                OutlinedTextField(
                    value = description,
                    onValueChange = { description = it },
                    label = { Text("تعليمات للطلاب (اختياري)") },
                    placeholder = { Text("مثال: أجب عن الأسئلة بدقة خلال وقت الحصة") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    maxLines = 2
                )

                Spacer(modifier = Modifier.height(10.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    OutlinedTextField(
                        value = durationMinutes.toString(),
                        onValueChange = { durationMinutes = it.toIntOrNull() ?: 0 },
                        label = { Text("مدة الاختبار (بالدقائق)") },
                        modifier = Modifier.weight(1f),
                        shape = RoundedCornerShape(12.dp),
                        singleLine = true
                    )
                }

                Spacer(modifier = Modifier.height(20.dp))
                HorizontalDivider()
                Spacer(modifier = Modifier.height(14.dp))

                // Questions Section Header
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "الأسئلة (${draftQuestions.size})",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )

                    Button(
                        onClick = {
                            draftQuestions.add(
                                DraftQuestion(
                                    questionText = "",
                                    questionType = "MULTIPLE_CHOICE",
                                    correctAnswer = "A",
                                    points = 1
                                )
                            )
                        },
                        shape = RoundedCornerShape(10.dp)
                    ) {
                        Icon(imageVector = Icons.Default.Add, contentDescription = null, modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("إضافة سؤال")
                    }
                }

                Spacer(modifier = Modifier.height(12.dp))

                // Questions List
                draftQuestions.forEachIndexed { index, draft ->
                    QuestionDraftCard(
                        index = index,
                        draft = draft,
                        canDelete = draftQuestions.size > 1,
                        onDelete = { draftQuestions.removeAt(index) },
                        onUpdate = { updated ->
                            draftQuestions[index] = updated
                        }
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                }

                if (errorMessage != null) {
                    Text(
                        text = errorMessage!!,
                        color = BrandDanger,
                        style = MaterialTheme.typography.bodySmall,
                        modifier = Modifier.padding(vertical = 6.dp)
                    )
                }

                Spacer(modifier = Modifier.height(16.dp))

                // Save Button
                Button(
                    onClick = {
                        if (title.isBlank()) {
                            errorMessage = "يرجى كتابة عنوان الاختبار"
                            return@Button
                        }
                        val emptyQ = draftQuestions.find { it.questionText.isBlank() }
                        if (emptyQ != null) {
                            errorMessage = "يرجى ملء نصوص جميع الأسئلة"
                            return@Button
                        }

                        val questions = draftQuestions.map { d ->
                            Question(
                                quizId = 0,
                                questionText = d.questionText.trim(),
                                questionType = d.questionType,
                                optionA = d.optionA.trim(),
                                optionB = d.optionB.trim(),
                                optionC = d.optionC.trim(),
                                optionD = d.optionD.trim(),
                                correctAnswer = d.correctAnswer.trim(),
                                points = if (d.points > 0) d.points else 1
                            )
                        }

                        onSave(title, description, durationMinutes, quizType, questions)
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(50.dp)
                        .testTag("save_quiz_button"),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text(
                        text = "حفظ ونشر في الحصة فوراً ✓",
                        fontWeight = FontWeight.Bold,
                        fontSize = MaterialTheme.typography.titleMedium.fontSize
                    )
                }
            }
        }
    }
}

@Composable
private fun QuestionDraftCard(
    index: Int,
    draft: DraftQuestion,
    canDelete: Boolean,
    onDelete: () -> Unit,
    onUpdate: (DraftQuestion) -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(14.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
        )
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "سؤال رقم ${index + 1}",
                    fontWeight = FontWeight.Bold,
                    color = BrandPrimary
                )

                if (canDelete) {
                    IconButton(onClick = onDelete) {
                        Icon(
                            imageVector = Icons.Default.Delete,
                            contentDescription = "حذف السؤال",
                            tint = BrandDanger,
                            modifier = Modifier.size(20.dp)
                        )
                    }
                }
            }

            // Question Type Selector
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 6.dp),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                listOf(
                    "MULTIPLE_CHOICE" to "اختيار من متعدد",
                    "TRUE_FALSE" to "صح أم خطأ",
                    "SHORT_ANSWER" to "سؤال مقالي / نشاط"
                ).forEach { (typeKey, label) ->
                    val isSelected = draft.questionType == typeKey
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .clip(RoundedCornerShape(8.dp))
                            .background(if (isSelected) BrandPrimary else MaterialTheme.colorScheme.surface)
                            .border(1.dp, if (isSelected) BrandPrimary else MaterialTheme.colorScheme.outline, RoundedCornerShape(8.dp))
                            .clickable {
                                onUpdate(draft.copy(questionType = typeKey))
                            }
                            .padding(vertical = 6.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = label,
                            style = MaterialTheme.typography.labelSmall,
                            fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal,
                            color = if (isSelected) Color.White else MaterialTheme.colorScheme.onSurface
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            OutlinedTextField(
                value = draft.questionText,
                onValueChange = { onUpdate(draft.copy(questionText = it)) },
                label = { Text("نص السؤال *") },
                placeholder = { Text("اكتب السؤال هنا...") },
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(10.dp)
            )

            Spacer(modifier = Modifier.height(8.dp))

            if (draft.questionType == "MULTIPLE_CHOICE") {
                Text(
                    text = "الخيارات (حدد الخيار الصحيح بالدائرة):",
                    style = MaterialTheme.typography.labelMedium,
                    fontWeight = FontWeight.SemiBold,
                    modifier = Modifier.padding(top = 4.dp, bottom = 4.dp)
                )

                // Option A
                Row(verticalAlignment = Alignment.CenterVertically) {
                    RadioButton(
                        selected = draft.correctAnswer == "A",
                        onClick = { onUpdate(draft.copy(correctAnswer = "A")) }
                    )
                    OutlinedTextField(
                        value = draft.optionA,
                        onValueChange = { onUpdate(draft.copy(optionA = it)) },
                        label = { Text("الخيار (A)") },
                        modifier = Modifier.weight(1f),
                        shape = RoundedCornerShape(8.dp),
                        singleLine = true
                    )
                }

                // Option B
                Row(verticalAlignment = Alignment.CenterVertically) {
                    RadioButton(
                        selected = draft.correctAnswer == "B",
                        onClick = { onUpdate(draft.copy(correctAnswer = "B")) }
                    )
                    OutlinedTextField(
                        value = draft.optionB,
                        onValueChange = { onUpdate(draft.copy(optionB = it)) },
                        label = { Text("الخيار (B)") },
                        modifier = Modifier.weight(1f),
                        shape = RoundedCornerShape(8.dp),
                        singleLine = true
                    )
                }

                // Option C
                Row(verticalAlignment = Alignment.CenterVertically) {
                    RadioButton(
                        selected = draft.correctAnswer == "C",
                        onClick = { onUpdate(draft.copy(correctAnswer = "C")) }
                    )
                    OutlinedTextField(
                        value = draft.optionC,
                        onValueChange = { onUpdate(draft.copy(optionC = it)) },
                        label = { Text("الخيار (C)") },
                        modifier = Modifier.weight(1f),
                        shape = RoundedCornerShape(8.dp),
                        singleLine = true
                    )
                }

                // Option D
                Row(verticalAlignment = Alignment.CenterVertically) {
                    RadioButton(
                        selected = draft.correctAnswer == "D",
                        onClick = { onUpdate(draft.copy(correctAnswer = "D")) }
                    )
                    OutlinedTextField(
                        value = draft.optionD,
                        onValueChange = { onUpdate(draft.copy(optionD = it)) },
                        label = { Text("الخيار (D)") },
                        modifier = Modifier.weight(1f),
                        shape = RoundedCornerShape(8.dp),
                        singleLine = true
                    )
                }
            } else if (draft.questionType == "TRUE_FALSE") {
                Text(
                    text = "الإجابة الصحيحة:",
                    style = MaterialTheme.typography.labelMedium,
                    fontWeight = FontWeight.SemiBold,
                    modifier = Modifier.padding(top = 4.dp, bottom = 4.dp)
                )

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .clip(RoundedCornerShape(8.dp))
                            .background(if (draft.correctAnswer == "TRUE") BrandSuccess else MaterialTheme.colorScheme.surface)
                            .border(1.dp, if (draft.correctAnswer == "TRUE") BrandSuccess else MaterialTheme.colorScheme.outline, RoundedCornerShape(8.dp))
                            .clickable { onUpdate(draft.copy(correctAnswer = "TRUE")) }
                            .padding(vertical = 10.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "✓ صح",
                            fontWeight = FontWeight.Bold,
                            color = if (draft.correctAnswer == "TRUE") Color.White else MaterialTheme.colorScheme.onSurface
                        )
                    }

                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .clip(RoundedCornerShape(8.dp))
                            .background(if (draft.correctAnswer == "FALSE") BrandDanger else MaterialTheme.colorScheme.surface)
                            .border(1.dp, if (draft.correctAnswer == "FALSE") BrandDanger else MaterialTheme.colorScheme.outline, RoundedCornerShape(8.dp))
                            .clickable { onUpdate(draft.copy(correctAnswer = "FALSE")) }
                            .padding(vertical = 10.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "✗ خطأ",
                            fontWeight = FontWeight.Bold,
                            color = if (draft.correctAnswer == "FALSE") Color.White else MaterialTheme.colorScheme.onSurface
                        )
                    }
                }
            } else {
                Text(
                    text = "سيكتب الطالب إجابته بالتفصيل في خانة مخصصة في المتصفح.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f),
                    modifier = Modifier.padding(vertical = 6.dp)
                )
            }
        }
    }
}
