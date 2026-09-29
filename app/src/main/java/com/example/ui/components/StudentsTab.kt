package com.example.ui.components

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.model.Student
import com.example.data.model.Submission
import com.example.data.repository.StudentImportResult
import com.example.ui.theme.BrandDanger
import com.example.ui.theme.BrandPrimary
import com.example.ui.theme.BrandSuccess
import com.example.ui.theme.BrandWarning
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun StudentsTab(
    students: List<Student>,
    submissions: List<Submission>,
    searchQuery: String,
    areGradesVisibleGlobally: Boolean = true,
    onSearchQueryChange: (String) -> Unit,
    onResetPassword: (studentId: Long, newPass: String) -> Unit,
    onDeleteStudent: (studentId: Long) -> Unit,
    onSaveEvaluation: (
        studentId: Long,
        exam1: Double,
        exam2: Double,
        participation: Double,
        bonus: Double,
        notes: String,
        showGrades: Boolean,
        showNotes: Boolean,
        gradeSection: String
    ) -> Unit = { _, _, _, _, _, _, _, _, _ -> },
    onQuickAdjustBonus: (studentId: Long, delta: Double) -> Unit = { _, _ -> },
    onToggleGlobalGradesVisibility: (Boolean) -> Unit = {},
    teacherName: String = "",
    onImportStudents: (code: String, password: String, overwrite: Boolean, onDone: (Result<StudentImportResult>) -> Unit) -> Unit = { _, _, _, _ -> },
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    var editingPasswordStudent by remember { mutableStateOf<Student?>(null) }
    var evaluatingStudent by remember { mutableStateOf<Student?>(null) }
    var studentToDelete by remember { mutableStateOf<Student?>(null) }
    var newPasswordText by remember { mutableStateOf("") }

    var showExportAllDialog by remember { mutableStateOf(false) }
    var studentToExportSingle by remember { mutableStateOf<Student?>(null) }
    var showImportDialog by remember { mutableStateOf(false) }

    // Selected Class & Section filter chip (null = All)
    var selectedClassFilter by remember { mutableStateOf<String?>(null) }

    // Filter students by search and class/section
    val filteredStudents = remember(students, searchQuery, selectedClassFilter) {
        var list = students
        val q = searchQuery.trim()
        if (q.isNotBlank()) {
            list = list.filter {
                it.username.contains(q, ignoreCase = true) ||
                it.nationalId.contains(q) ||
                it.phone.contains(q) ||
                it.gradeSection.contains(q, ignoreCase = true)
            }
        }
        if (selectedClassFilter != null) {
            list = list.filter {
                val (className, sectionName) = it.getClassAndSectionDisplay()
                val fullKey = "$className - $sectionName"
                className == selectedClassFilter || fullKey == selectedClassFilter || it.gradeSection.contains(selectedClassFilter!!)
            }
        }
        list
    }

    // Extract all unique classes for top filter chips
    val distinctClasses = remember(students) {
        students.map {
            val (c, s) = it.getClassAndSectionDisplay()
            if (s.isNotBlank() && s != "عام") "$c - $s" else c
        }.distinct().sorted()
    }

    // Group filtered students by Class & Section
    val groupedStudents = remember(filteredStudents) {
        filteredStudents.groupBy {
            val (c, s) = it.getClassAndSectionDisplay()
            if (s.isNotBlank() && s != "عام") "$c - $s" else c
        }
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = 16.dp)
    ) {
        // Global Action Buttons: Export, Import & Global Visibility
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 10.dp, bottom = 6.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Button(
                onClick = { showExportAllDialog = true },
                modifier = Modifier
                    .weight(1f)
                    .testTag("btn_open_export_students"),
                shape = RoundedCornerShape(12.dp),
                enabled = students.isNotEmpty()
            ) {
                Icon(imageVector = Icons.Default.Security, contentDescription = null, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(4.dp))
                Text("سحب مشفر 🔒", fontSize = 11.5.sp, fontWeight = FontWeight.Bold)
            }

            OutlinedButton(
                onClick = { showImportDialog = true },
                modifier = Modifier
                    .weight(1f)
                    .testTag("btn_open_import_students"),
                shape = RoundedCornerShape(12.dp)
            ) {
                Icon(imageVector = Icons.Default.Download, contentDescription = null, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(4.dp))
                Text("استيراد 📥", fontSize = 11.5.sp, fontWeight = FontWeight.Bold)
            }

            FilledTonalButton(
                onClick = { onToggleGlobalGradesVisibility(!areGradesVisibleGlobally) },
                modifier = Modifier
                    .weight(1.2f)
                    .testTag("btn_toggle_global_grades"),
                colors = ButtonDefaults.filledTonalButtonColors(
                    containerColor = if (areGradesVisibleGlobally) BrandSuccess.copy(alpha = 0.15f) else BrandWarning.copy(alpha = 0.15f)
                ),
                shape = RoundedCornerShape(12.dp)
            ) {
                Icon(
                    imageVector = if (areGradesVisibleGlobally) Icons.Default.Visibility else Icons.Default.VisibilityOff,
                    contentDescription = null,
                    modifier = Modifier.size(16.dp),
                    tint = if (areGradesVisibleGlobally) BrandSuccess else BrandWarning
                )
                Spacer(modifier = Modifier.width(4.dp))
                Text(
                    text = if (areGradesVisibleGlobally) "الدرجات: معلنة" else "الدرجات: مخفية",
                    fontSize = 11.5.sp,
                    fontWeight = FontWeight.Bold,
                    color = if (areGradesVisibleGlobally) BrandSuccess else BrandWarning
                )
            }
        }

        // Search Input
        OutlinedTextField(
            value = searchQuery,
            onValueChange = onSearchQueryChange,
            placeholder = { Text("بحث عن اسم طالب، هوية، فصل...") },
            leadingIcon = {
                Icon(imageVector = Icons.Default.Search, contentDescription = "بحث")
            },
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 4.dp)
                .testTag("search_student_input"),
            shape = RoundedCornerShape(14.dp),
            singleLine = true
        )

        // Class & Section Filter Chips
        if (distinctClasses.isNotEmpty()) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState())
                    .padding(vertical = 6.dp),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                FilterChip(
                    selected = selectedClassFilter == null,
                    onClick = { selectedClassFilter = null },
                    label = { Text("الكل (${students.size})", fontSize = 12.sp, fontWeight = FontWeight.Bold) },
                    leadingIcon = {
                        if (selectedClassFilter == null) {
                            Icon(imageVector = Icons.Default.Check, contentDescription = null, modifier = Modifier.size(14.dp))
                        }
                    }
                )

                distinctClasses.forEach { clsName ->
                    val count = students.count {
                        val (c, s) = it.getClassAndSectionDisplay()
                        val fullKey = "$c - $s"
                        c == clsName || fullKey == clsName
                    }
                    FilterChip(
                        selected = selectedClassFilter == clsName,
                        onClick = {
                            selectedClassFilter = if (selectedClassFilter == clsName) null else clsName
                        },
                        label = { Text("$clsName ($count)", fontSize = 12.sp) },
                        leadingIcon = {
                            if (selectedClassFilter == clsName) {
                                Icon(imageVector = Icons.Default.Check, contentDescription = null, modifier = Modifier.size(14.dp))
                            }
                        }
                    )
                }
            }
        }

        if (filteredStudents.isEmpty()) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(32.dp),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Box(
                        modifier = Modifier
                            .size(70.dp)
                            .clip(CircleShape)
                            .background(MaterialTheme.colorScheme.surfaceVariant),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Default.People,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f),
                            modifier = Modifier.size(38.dp)
                        )
                    }
                    Spacer(modifier = Modifier.height(14.dp))
                    Text(
                        text = if (searchQuery.isBlank()) "لم يقم أي طالب بالتسجيل بعد" else "لا توجد نتائج مطابقة للبحث",
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = "عندما يفتح الطالب الرابط ويسجل اسمه، سيظهر هنا فوراً في فصله.",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
                    )
                }
            }
        } else {
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                groupedStudents.forEach { (classSectionTitle, classStudents) ->
                    // Section Header Card
                    item(key = "header_$classSectionTitle") {
                        ClassSectionHeaderCard(
                            title = classSectionTitle,
                            studentCount = classStudents.size,
                            averageScore = classStudents.map { it.totalScore }.average()
                        )
                    }

                    items(classStudents, key = { it.id }) { student ->
                        val studentSubmissions = submissions.count {
                            it.studentUsername.equals(student.username.trim(), ignoreCase = true)
                        }

                        CategorizedStudentCard(
                            student = student,
                            submissionsCount = studentSubmissions,
                            onEvaluate = { evaluatingStudent = student },
                            onQuickBonus = { delta -> onQuickAdjustBonus(student.id, delta) },
                            onEditPassword = {
                                editingPasswordStudent = student
                                newPasswordText = student.password
                            },
                            onDelete = { studentToDelete = student },
                            onExportEncrypted = { studentToExportSingle = student },
                            onCopyPassword = {
                                val clip = ClipData.newPlainText("Student Pass", student.password)
                                (context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).setPrimaryClip(clip)
                                Toast.makeText(context, "تم نسخ كلمة مرور ${student.username}", Toast.LENGTH_SHORT).show()
                            }
                        )
                    }
                }

                item {
                    Spacer(modifier = Modifier.height(30.dp))
                }
            }
        }
    }

    // Evaluation Dialog
    evaluatingStudent?.let { student ->
        StudentEvaluationDialog(
            student = student,
            onSaveEvaluation = { e1, e2, part, bonus, notes, showGrades, showNotes, gradeSec ->
                onSaveEvaluation(student.id, e1, e2, part, bonus, notes, showGrades, showNotes, gradeSec)
                evaluatingStudent = null
            },
            onDismiss = { evaluatingStudent = null }
        )
    }

    // Export All Students Dialog
    if (showExportAllDialog) {
        ExportStudentsDialog(
            students = students,
            teacherName = teacherName,
            onDismiss = { showExportAllDialog = false }
        )
    }

    // Export Single Student Dialog
    studentToExportSingle?.let { singleStudent ->
        ExportStudentsDialog(
            students = listOf(singleStudent),
            teacherName = teacherName,
            onDismiss = { studentToExportSingle = null }
        )
    }

    // Import Students Dialog
    if (showImportDialog) {
        ImportStudentsDialog(
            onImportStudents = onImportStudents,
            onDismiss = { showImportDialog = false }
        )
    }

    // Reset Password Dialog
    editingPasswordStudent?.let { student ->
        AlertDialog(
            onDismissRequest = { editingPasswordStudent = null },
            title = { Text("تعديل كلمة مرور: ${student.username}") },
            text = {
                Column {
                    Text(
                        text = "يمكنك كتابة كلمة مرور جديدة للطالب في حال نسيانها في الفصل:",
                        style = MaterialTheme.typography.bodyMedium
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    OutlinedTextField(
                        value = newPasswordText,
                        onValueChange = { newPasswordText = it },
                        label = { Text("كلمة المرور الجديدة") },
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(10.dp),
                        singleLine = true
                    )
                }
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        if (newPasswordText.isNotBlank()) {
                            onResetPassword(student.id, newPasswordText.trim())
                            editingPasswordStudent = null
                        }
                    }
                ) {
                    Text("حفظ التعديل", fontWeight = FontWeight.Bold)
                }
            },
            dismissButton = {
                TextButton(onClick = { editingPasswordStudent = null }) {
                    Text("إلغاء")
                }
            }
        )
    }

    // Delete Student Dialog
    studentToDelete?.let { student ->
        AlertDialog(
            onDismissRequest = { studentToDelete = null },
            title = { Text("حذف حساب الطالب؟") },
            text = { Text("هل تود حذف الطالب '${student.username}'؟ يمكنه بعد ذلك التسجيل مجدداً كطالب جديد.") },
            confirmButton = {
                TextButton(
                    onClick = {
                        onDeleteStudent(student.id)
                        studentToDelete = null
                    }
                ) {
                    Text("حذف", color = BrandDanger, fontWeight = FontWeight.Bold)
                }
            },
            dismissButton = {
                TextButton(onClick = { studentToDelete = null }) {
                    Text("إلغاء")
                }
            }
        )
    }
}

@Composable
private fun ClassSectionHeaderCard(
    title: String,
    studentCount: Int,
    averageScore: Double
) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 10.dp, bottom = 4.dp),
        shape = RoundedCornerShape(14.dp),
        color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.35f),
        border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.25f))
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 14.dp, vertical = 10.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Default.School,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(20.dp)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary
                )
            }

            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                Surface(
                    shape = RoundedCornerShape(8.dp),
                    color = MaterialTheme.colorScheme.surface
                ) {
                    Text(
                        text = "$studentCount طلاب",
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                        fontSize = 11.5.sp,
                        fontWeight = FontWeight.Bold
                    )
                }

                if (!averageScore.isNaN() && averageScore > 0) {
                    Surface(
                        shape = RoundedCornerShape(8.dp),
                        color = BrandPrimary.copy(alpha = 0.15f)
                    ) {
                        Text(
                            text = "معدل: ${String.format("%.1f", averageScore)}",
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            color = BrandPrimary
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun CategorizedStudentCard(
    student: Student,
    submissionsCount: Int,
    onEvaluate: () -> Unit,
    onQuickBonus: (Double) -> Unit,
    onEditPassword: () -> Unit,
    onDelete: () -> Unit,
    onExportEncrypted: () -> Unit,
    onCopyPassword: () -> Unit
) {
    var showPassword by remember { mutableStateOf(false) }

    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.5.dp)
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            // Student Primary Info Row
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Avatar
                Box(
                    modifier = Modifier
                        .size(44.dp)
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

                Spacer(modifier = Modifier.width(12.dp))

                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = student.username,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )

                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        if (student.nationalId.isNotBlank()) {
                            Text(
                                text = "هوية: ${student.nationalId}",
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.primary
                            )
                        }
                        if (student.gradeSection.isNotBlank()) {
                            Text(
                                text = student.gradeSection,
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
                            )
                        }
                    }
                }

                // Total Score Badge
                Surface(
                    shape = RoundedCornerShape(10.dp),
                    color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.6f),
                    border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.3f))
                ) {
                    Column(
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text("المجموع", fontSize = 10.sp, color = MaterialTheme.colorScheme.primary)
                        Text(
                            text = String.format("%.1f", student.totalScore),
                            fontSize = 15.sp,
                            fontWeight = FontWeight.Black,
                            color = MaterialTheme.colorScheme.primary
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(10.dp))

            // Grades Strip: Exam 1, Exam 2, Participation, Bonus
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(10.dp))
                    .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.35f))
                    .padding(horizontal = 10.dp, vertical = 6.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                GradeMiniItem(label = "شهري 1", value = student.exam1Score)
                GradeMiniItem(label = "شهري 2", value = student.exam2Score)
                GradeMiniItem(label = "مشاركة", value = student.participationScore)
                GradeMiniItem(
                    label = "إضافي",
                    value = student.bonusScore,
                    highlightColor = if (student.bonusScore >= 0) MaterialTheme.colorScheme.primary else BrandDanger
                )

                // Visibility pill
                Icon(
                    imageVector = if (student.showGradesToStudent) Icons.Default.Visibility else Icons.Default.VisibilityOff,
                    contentDescription = if (student.showGradesToStudent) "الدرجات مرئية للطالب" else "الدرجات مخفية",
                    tint = if (student.showGradesToStudent) BrandSuccess else BrandDanger.copy(alpha = 0.7f),
                    modifier = Modifier.size(16.dp)
                )
            }

            if (student.notes.isNotBlank()) {
                Spacer(modifier = Modifier.height(6.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Default.ChatBubbleOutline,
                        contentDescription = null,
                        modifier = Modifier.size(12.dp),
                        tint = MaterialTheme.colorScheme.primary
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(
                        text = student.notes,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.75f),
                        maxLines = 1
                    )
                }
            }

            Spacer(modifier = Modifier.height(10.dp))

            // Quick Actions Strip: Evaluation Button, Quick +1/-1, Password, Export, Delete
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Primary Evaluate & Grade Button
                FilledTonalButton(
                    onClick = onEvaluate,
                    shape = RoundedCornerShape(10.dp),
                    contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp)
                ) {
                    Icon(imageVector = Icons.Default.EditNote, contentDescription = null, modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(4.dp))
                    Text("رصد وتقييم", fontSize = 11.5.sp, fontWeight = FontWeight.Bold)
                }

                // Quick +1 and -1 Points Buttons
                Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                    FilledTonalButton(
                        onClick = { onQuickBonus(1.0) },
                        shape = RoundedCornerShape(8.dp),
                        contentPadding = PaddingValues(horizontal = 8.dp, vertical = 4.dp)
                    ) {
                        Text("+1", fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    }

                    FilledTonalButton(
                        onClick = { onQuickBonus(-1.0) },
                        shape = RoundedCornerShape(8.dp),
                        colors = ButtonDefaults.filledTonalButtonColors(containerColor = BrandDanger.copy(alpha = 0.12f)),
                        contentPadding = PaddingValues(horizontal = 8.dp, vertical = 4.dp)
                    ) {
                        Text("-1", fontSize = 11.sp, color = BrandDanger, fontWeight = FontWeight.Bold)
                    }
                }

                // Tool Buttons: Password, Encrypted Export, Delete
                Row {
                    IconButton(onClick = onCopyPassword, modifier = Modifier.size(32.dp)) {
                        Icon(imageVector = Icons.Default.Key, contentDescription = "نسخ كلمة المرور", modifier = Modifier.size(16.dp))
                    }

                    IconButton(onClick = onExportEncrypted, modifier = Modifier.size(32.dp)) {
                        Icon(imageVector = Icons.Default.Security, contentDescription = "سحب مشفر", tint = BrandPrimary, modifier = Modifier.size(16.dp))
                    }

                    IconButton(onClick = onDelete, modifier = Modifier.size(32.dp)) {
                        Icon(imageVector = Icons.Default.Delete, contentDescription = "حذف", tint = BrandDanger.copy(alpha = 0.7f), modifier = Modifier.size(16.dp))
                    }
                }
            }
        }
    }
}

@Composable
private fun GradeMiniItem(
    label: String,
    value: Double,
    highlightColor: Color = MaterialTheme.colorScheme.onSurface
) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(
            text = label,
            fontSize = 10.sp,
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
        )
        Text(
            text = if (value % 1.0 == 0.0) value.toInt().toString() else String.format("%.1f", value),
            fontSize = 12.sp,
            fontWeight = FontWeight.Bold,
            color = highlightColor
        )
    }
}
