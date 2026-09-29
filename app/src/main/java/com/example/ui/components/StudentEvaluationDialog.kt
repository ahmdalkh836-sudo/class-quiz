package com.example.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.example.data.model.Student
import com.example.ui.theme.BrandDanger
import com.example.ui.theme.BrandPrimary
import com.example.ui.theme.BrandSuccess
import com.example.ui.theme.BrandWarning

@Composable
fun StudentEvaluationDialog(
    student: Student,
    onSaveEvaluation: (
        exam1: Double,
        exam2: Double,
        participation: Double,
        bonus: Double,
        notes: String,
        showGrades: Boolean,
        showNotes: Boolean,
        gradeSection: String
    ) -> Unit,
    onDismiss: () -> Unit
) {
    var exam1Text by remember { mutableStateOf(if (student.exam1Score > 0) student.exam1Score.toString() else "") }
    var exam2Text by remember { mutableStateOf(if (student.exam2Score > 0) student.exam2Score.toString() else "") }
    var participationText by remember { mutableStateOf(if (student.participationScore > 0) student.participationScore.toString() else "") }
    var bonusScore by remember { mutableStateOf(student.bonusScore) }
    var notesText by remember { mutableStateOf(student.notes) }
    var showGrades by remember { mutableStateOf(student.showGradesToStudent) }
    var showNotes by remember { mutableStateOf(student.showNotesToStudent) }
    var gradeSectionText by remember { mutableStateOf(student.gradeSection) }

    val e1 = exam1Text.toDoubleOrNull() ?: 0.0
    val e2 = exam2Text.toDoubleOrNull() ?: 0.0
    val part = participationText.toDoubleOrNull() ?: 0.0
    val totalScore = e1 + e2 + part + bonusScore

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Card(
            modifier = Modifier
                .fillMaxWidth(0.95f)
                .wrapContentHeight()
                .clip(RoundedCornerShape(24.dp))
                .testTag("student_evaluation_dialog"),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
            elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
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
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        Box(
                            modifier = Modifier
                                .size(42.dp)
                                .clip(CircleShape)
                                .background(BrandPrimary.copy(alpha = 0.12f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = student.username.firstOrNull()?.toString() ?: "ط",
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold,
                                color = BrandPrimary
                            )
                        }

                        Column {
                            Text(
                                text = student.username,
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold
                            )
                            Text(
                                text = if (student.nationalId.isNotBlank()) "هوية: ${student.nationalId}" else "طالب مسجل",
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
                            )
                        }
                    }

                    IconButton(onClick = onDismiss) {
                        Icon(imageVector = Icons.Default.Close, contentDescription = "إغلاق")
                    }
                }

                Spacer(modifier = Modifier.height(14.dp))

                // Class and Section Input
                OutlinedTextField(
                    value = gradeSectionText,
                    onValueChange = { gradeSectionText = it },
                    label = { Text("الفصل والشعبة (مثال: أول ثانوي - 1 أو ثالث متوسط / أ)") },
                    leadingIcon = {
                        Icon(imageVector = Icons.Default.School, contentDescription = null)
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    singleLine = true
                )

                Spacer(modifier = Modifier.height(16.dp))

                // Total Calculated Badge Banner
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.4f))
                        .border(1.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.3f), RoundedCornerShape(16.dp))
                        .padding(14.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Text(
                                text = "المجموع الإجمالي المحسوب:",
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.primary
                            )
                            Text(
                                text = String.format("%.1f", totalScore),
                                style = MaterialTheme.typography.headlineMedium,
                                fontWeight = FontWeight.Black,
                                color = MaterialTheme.colorScheme.primary
                            )
                        }

                        Surface(
                            shape = RoundedCornerShape(10.dp),
                            color = if (showGrades) BrandSuccess.copy(alpha = 0.15f) else BrandDanger.copy(alpha = 0.15f)
                        ) {
                            Text(
                                text = if (showGrades) "👁️ ظاهرة للطالب" else "🔒 مخفية عن الطالب",
                                modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold,
                                color = if (showGrades) BrandSuccess else BrandDanger
                            )
                        }
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                // Grades Input Section
                Text(
                    text = "رصد الدرجات الشهرية والمشاركة:",
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.Bold
                )

                Spacer(modifier = Modifier.height(10.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    OutlinedTextField(
                        value = exam1Text,
                        onValueChange = { exam1Text = it },
                        label = { Text("الشهري الأول") },
                        placeholder = { Text("0") },
                        modifier = Modifier.weight(1f),
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                        shape = RoundedCornerShape(12.dp),
                        singleLine = true
                    )

                    OutlinedTextField(
                        value = exam2Text,
                        onValueChange = { exam2Text = it },
                        label = { Text("الشهري الثاني") },
                        placeholder = { Text("0") },
                        modifier = Modifier.weight(1f),
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                        shape = RoundedCornerShape(12.dp),
                        singleLine = true
                    )
                }

                Spacer(modifier = Modifier.height(10.dp))

                OutlinedTextField(
                    value = participationText,
                    onValueChange = { participationText = it },
                    label = { Text("درجة المشاركة والتفاعل الصفي") },
                    placeholder = { Text("0") },
                    modifier = Modifier.fillMaxWidth(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                    shape = RoundedCornerShape(12.dp),
                    singleLine = true
                )

                Spacer(modifier = Modifier.height(14.dp))

                // Bonus / Deduction Adjustments (+ / -)
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(14.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.45f))
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text("درجات إضافية / خصم:", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                            Text(
                                text = (if (bonusScore > 0) "+$bonusScore" else "$bonusScore"),
                                fontWeight = FontWeight.Black,
                                fontSize = 15.sp,
                                color = if (bonusScore >= 0) MaterialTheme.colorScheme.primary else BrandDanger
                            )
                        }

                        Spacer(modifier = Modifier.height(8.dp))

                        // Quick +/- presets
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(6.dp)
                        ) {
                            FilledTonalButton(
                                onClick = { bonusScore += 1.0 },
                                modifier = Modifier.weight(1f),
                                contentPadding = PaddingValues(horizontal = 4.dp, vertical = 6.dp)
                            ) {
                                Text("+1 مشاركة", fontSize = 11.sp, fontWeight = FontWeight.Bold)
                            }
                            FilledTonalButton(
                                onClick = { bonusScore += 2.0 },
                                modifier = Modifier.weight(1f),
                                contentPadding = PaddingValues(horizontal = 4.dp, vertical = 6.dp)
                            ) {
                                Text("+2 تميز", fontSize = 11.sp, fontWeight = FontWeight.Bold)
                            }
                            FilledTonalButton(
                                onClick = { bonusScore -= 1.0 },
                                modifier = Modifier.weight(1f),
                                colors = ButtonDefaults.filledTonalButtonColors(containerColor = BrandDanger.copy(alpha = 0.15f)),
                                contentPadding = PaddingValues(horizontal = 4.dp, vertical = 6.dp)
                            ) {
                                Text("-1 خصم", fontSize = 11.sp, color = BrandDanger, fontWeight = FontWeight.Bold)
                            }
                            IconButton(
                                onClick = { bonusScore = 0.0 },
                                modifier = Modifier.size(36.dp)
                            ) {
                                Icon(imageVector = Icons.Default.RestartAlt, contentDescription = "تصفير الإضافي", modifier = Modifier.size(18.dp))
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(14.dp))

                // Teacher Notes
                OutlinedTextField(
                    value = notesText,
                    onValueChange = { notesText = it },
                    label = { Text("ملاحظات وتوجيهات المعلم للطالب") },
                    placeholder = { Text("مثال: طالب متميز ومشارك، يحتاج تركيزاً أكثر في المسائل...") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    minLines = 3,
                    maxLines = 5
                )

                Spacer(modifier = Modifier.height(14.dp))

                // Visibility Controls
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(14.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.35f))
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text("إظهار الدرجات لهذا الطالب", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                                Text("يمكن للطالب رؤية درجاته الشهرية في صفحته", fontSize = 11.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f))
                            }
                            Switch(
                                checked = showGrades,
                                onCheckedChange = { showGrades = it }
                            )
                        }

                        HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp), color = MaterialTheme.colorScheme.outline.copy(alpha = 0.2f))

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text("إظهار الملاحظات للطالب", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                                Text("تظهر الملاحظة في بطاقة الطالب الإلكترونية", fontSize = 11.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f))
                            }
                            Switch(
                                checked = showNotes,
                                onCheckedChange = { showNotes = it }
                            )
                        }
                    }
                }

                Spacer(modifier = Modifier.height(20.dp))

                // Save and Cancel Buttons
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    Button(
                        onClick = {
                            onSaveEvaluation(
                                e1,
                                e2,
                                part,
                                bonusScore,
                                notesText,
                                showGrades,
                                showNotes,
                                gradeSectionText
                            )
                            onDismiss()
                        },
                        modifier = Modifier.weight(1.5f),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Icon(imageVector = Icons.Default.Check, contentDescription = null, modifier = Modifier.size(18.dp))
                        Spacer(modifier = Modifier.width(6.dp))
                        Text("حفظ التقييم والدرجات", fontWeight = FontWeight.Bold)
                    }

                    OutlinedButton(
                        onClick = onDismiss,
                        modifier = Modifier.weight(1f),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Text("إلغاء")
                    }
                }
            }
        }
    }
}
