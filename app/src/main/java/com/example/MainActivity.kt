package com.example

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
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
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import kotlinx.coroutines.launch
import com.example.ui.components.*
import com.example.ui.qr.EnlargedQrDialog
import com.example.ui.theme.BrandSuccess
import com.example.ui.theme.MyApplicationTheme
import com.example.ui.viewmodel.MainViewModel
import com.example.util.NetworkConnectionMode

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            val viewModel: MainViewModel = viewModel()
            val isDarkMode by viewModel.isDarkMode.collectAsStateWithLifecycle()
            val colorTheme by viewModel.colorTheme.collectAsStateWithLifecycle()

            MyApplicationTheme(darkTheme = isDarkMode, appColorTheme = colorTheme) {
                ClassroomServerMainApp(viewModel = viewModel)
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ClassroomServerMainApp(
    viewModel: MainViewModel = viewModel()
) {
    val isServerRunning by viewModel.isServerRunning.collectAsStateWithLifecycle()
    val serverUrl by viewModel.serverUrl.collectAsStateWithLifecycle()
    val simplifiedUrl by viewModel.simplifiedUrl.collectAsStateWithLifecycle()
    val serverIp by viewModel.serverIp.collectAsStateWithLifecycle()
    val networkMode by viewModel.networkMode.collectAsStateWithLifecycle()
    val availableNetworks by viewModel.availableNetworks.collectAsStateWithLifecycle()

    val quizzes by viewModel.quizzes.collectAsStateWithLifecycle()
    val students by viewModel.students.collectAsStateWithLifecycle()
    val submissions by viewModel.submissions.collectAsStateWithLifecycle()
    val serverLogs by viewModel.serverLogs.collectAsStateWithLifecycle()
    val selectedTab by viewModel.selectedTab.collectAsStateWithLifecycle()
    val searchQuery by viewModel.studentSearchQuery.collectAsStateWithLifecycle()
    val areGradesVisibleGlobally by viewModel.areGradesVisibleGlobally.collectAsStateWithLifecycle()

    val teacherName by viewModel.teacherName.collectAsStateWithLifecycle()
    val teacherPhone by viewModel.teacherPhone.collectAsStateWithLifecycle()
    val teacherSubject by viewModel.teacherSubject.collectAsStateWithLifecycle()
    val isFirstLaunch by viewModel.isFirstLaunch.collectAsStateWithLifecycle()
    val isDarkMode by viewModel.isDarkMode.collectAsStateWithLifecycle()
    val colorTheme by viewModel.colorTheme.collectAsStateWithLifecycle()
    val antiCheatEnabled by viewModel.antiCheatEnabled.collectAsStateWithLifecycle()

    var showGuideDialog by remember { mutableStateOf(false) }
    var showEditProfileDialog by remember { mutableStateOf(false) }
    var showTopBarQrDialog by remember { mutableStateOf(false) }

    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
    val coroutineScope = rememberCoroutineScope()

    // First time welcome dialog
    if (isFirstLaunch || showEditProfileDialog) {
        TeacherOnboardingDialog(
            initialName = teacherName,
            initialPhone = teacherPhone,
            initialSubject = teacherSubject,
            onSave = { name, phone, subject ->
                viewModel.saveTeacherProfile(name, phone, subject)
                showEditProfileDialog = false
            },
            onDismiss = {
                viewModel.dismissFirstLaunch()
                showEditProfileDialog = false
            }
        )
    }

    ModalNavigationDrawer(
        drawerState = drawerState,
        gesturesEnabled = true,
        drawerContent = {
            ModalDrawerSheet(
                modifier = Modifier
                    .width(320.dp)
                    .testTag("main_side_drawer"),
                drawerContainerColor = MaterialTheme.colorScheme.surface,
                drawerTonalElevation = 6.dp
            ) {
                // Drawer Header
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.08f))
                        .padding(horizontal = 18.dp, vertical = 18.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(46.dp)
                                .clip(RoundedCornerShape(14.dp))
                                .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.16f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.School,
                                contentDescription = null,
                                tint = MaterialTheme.colorScheme.primary,
                                modifier = Modifier.size(26.dp)
                            )
                        }

                        IconButton(
                            onClick = { coroutineScope.launch { drawerState.close() } },
                            modifier = Modifier.testTag("drawer_close_button")
                        ) {
                            Icon(
                                imageVector = Icons.Default.Close,
                                contentDescription = "إغلاق القائمة"
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    Text(
                        text = if (teacherName.isNotBlank()) teacherName else "خادم الاختبارات المدرسية",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = if (teacherSubject.isNotBlank()) "مادة: $teacherSubject" else "بث محلي بدون إنترنت",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
                    )
                }

                HorizontalDivider(color = MaterialTheme.colorScheme.outline.copy(alpha = 0.15f))

                Spacer(modifier = Modifier.height(8.dp))

                // Category 1: Classroom & Academics
                Text(
                    text = "إدارة الفصل والدرجات",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.primary,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(horizontal = 18.dp, vertical = 6.dp)
                )

                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Quiz, contentDescription = null) },
                    label = { Text("الاختبارات والأنشطة", fontWeight = FontWeight.SemiBold) },
                    badge = {
                        if (quizzes.isNotEmpty()) {
                            Badge { Text("${quizzes.size}") }
                        }
                    },
                    selected = selectedTab == 0,
                    onClick = {
                        viewModel.setSelectedTab(0)
                        coroutineScope.launch { drawerState.close() }
                    },
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 2.dp)
                )

                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.People, contentDescription = null) },
                    label = { Text("الطلاب والدرجات الشهرية", fontWeight = FontWeight.SemiBold) },
                    badge = {
                        if (students.isNotEmpty()) {
                            Badge { Text("${students.size}") }
                        }
                    },
                    selected = selectedTab == 1,
                    onClick = {
                        viewModel.setSelectedTab(1)
                        coroutineScope.launch { drawerState.close() }
                    },
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 2.dp)
                )

                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Assignment, contentDescription = null) },
                    label = { Text("النتائج والتسليمات", fontWeight = FontWeight.SemiBold) },
                    badge = {
                        if (submissions.isNotEmpty()) {
                            Badge { Text("${submissions.size}") }
                        }
                    },
                    selected = selectedTab == 2,
                    onClick = {
                        viewModel.setSelectedTab(2)
                        coroutineScope.launch { drawerState.close() }
                    },
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 2.dp)
                )

                Spacer(modifier = Modifier.height(6.dp))
                HorizontalDivider(color = MaterialTheme.colorScheme.outline.copy(alpha = 0.12f))

                // Category 2: Network & Live Sharing
                Text(
                    text = "الشبكة والبث المباشر",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.primary,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(horizontal = 18.dp, vertical = 6.dp)
                )

                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.History, contentDescription = null) },
                    label = { Text("سجل العمليات والبث", fontWeight = FontWeight.SemiBold) },
                    selected = selectedTab == 3,
                    onClick = {
                        viewModel.setSelectedTab(3)
                        coroutineScope.launch { drawerState.close() }
                    },
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 2.dp)
                )

                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.HelpOutline, contentDescription = null) },
                    label = { Text("دليل شبكة Wi-Fi والهوتسبوت", fontWeight = FontWeight.SemiBold) },
                    selected = false,
                    onClick = {
                        coroutineScope.launch { drawerState.close() }
                        showGuideDialog = true
                    },
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 2.dp)
                )

                Spacer(modifier = Modifier.height(6.dp))
                HorizontalDivider(color = MaterialTheme.colorScheme.outline.copy(alpha = 0.12f))

                // Category 3: System Settings
                Text(
                    text = "النظام والتخصيص",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.primary,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(horizontal = 18.dp, vertical = 6.dp)
                )

                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Settings, contentDescription = null) },
                    label = { Text("الإعدادات والملف الشخصي", fontWeight = FontWeight.SemiBold) },
                    selected = selectedTab == 4,
                    onClick = {
                        viewModel.setSelectedTab(4)
                        coroutineScope.launch { drawerState.close() }
                    },
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 2.dp)
                )

                Spacer(modifier = Modifier.weight(1f))

                HorizontalDivider(color = MaterialTheme.colorScheme.outline.copy(alpha = 0.15f))

                // Drawer Footer
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 10.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = if (isServerRunning) "🟢 البث يعمل" else "⚪ البث متوقف",
                        style = MaterialTheme.typography.labelSmall,
                        color = if (isServerRunning) BrandSuccess else Color.Gray,
                        fontWeight = FontWeight.Bold
                    )

                    Text(
                        text = if (networkMode == NetworkConnectionMode.WIFI) "🌐 Wi-Fi محلي" else "📡 هوتسبوت",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.primary
                    )
                }
            }
        }
    ) {
        Scaffold(
            modifier = Modifier
                .fillMaxSize()
                .testTag("classroom_main_scaffold"),
            topBar = {
                TopAppBar(
                    navigationIcon = {
                        IconButton(
                            onClick = {
                                coroutineScope.launch {
                                    if (drawerState.isOpen) drawerState.close() else drawerState.open()
                                }
                            },
                            modifier = Modifier.testTag("app_bar_drawer_toggle")
                        ) {
                            Icon(
                                imageVector = Icons.Default.Menu,
                                contentDescription = "القائمة الجانبية",
                                tint = MaterialTheme.colorScheme.primary
                            )
                        }
                    },
                    title = {
                        Column {
                            Text(
                                text = if (teacherName.isNotBlank()) "خادم الفصل • $teacherName" else "خادم الاختبارات المدرسية",
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold,
                                maxLines = 1
                            )
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(
                                    modifier = Modifier
                                        .size(7.dp)
                                        .clip(CircleShape)
                                        .background(if (isServerRunning) BrandSuccess else Color.Gray)
                                )
                                Spacer(modifier = Modifier.width(5.dp))
                                Text(
                                    text = if (isServerRunning) {
                                        if (networkMode == NetworkConnectionMode.WIFI) "نشط: شبكة Wi-Fi المشتركة"
                                        else "نشط: نقطة اتصال (Hotspot)"
                                    } else "الخادم متوقف",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = if (isServerRunning) BrandSuccess else Color.Gray
                                )
                            }
                        }
                    },
                    actions = {
                        // Quick QR Code button in top bar
                        if (isServerRunning) {
                            IconButton(
                                onClick = { showTopBarQrDialog = true },
                                modifier = Modifier.testTag("app_bar_qr_button")
                            ) {
                                Icon(
                                    imageVector = Icons.Default.QrCode2,
                                    contentDescription = "عرض رمز الـ QR للطلاب",
                                    tint = MaterialTheme.colorScheme.primary
                                )
                            }
                        }

                        // Quick Night Mode Toggle Button
                        IconButton(
                            onClick = { viewModel.toggleDarkMode() },
                            modifier = Modifier.testTag("quick_night_mode_btn")
                        ) {
                            Icon(
                                imageVector = if (isDarkMode) Icons.Default.DarkMode else Icons.Default.LightMode,
                                contentDescription = "تبديل الوضع الليلي",
                                tint = if (isDarkMode) Color(0xFFFBBF24) else MaterialTheme.colorScheme.primary
                            )
                        }

                        // Help & Guide Button
                        IconButton(
                            onClick = { showGuideDialog = true },
                            modifier = Modifier.testTag("app_bar_guide_button")
                        ) {
                            Icon(
                                imageVector = Icons.Default.HelpOutline,
                                contentDescription = "دليل الاستخدام",
                                tint = MaterialTheme.colorScheme.primary
                            )
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = MaterialTheme.colorScheme.surface
                    )
                )
            },
            bottomBar = {
                NavigationBar(
                    containerColor = MaterialTheme.colorScheme.surface,
                    tonalElevation = 4.dp
                ) {
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Quiz, contentDescription = null) },
                        label = { Text("الاختبارات", fontSize = 11.sp) },
                        selected = selectedTab == 0,
                        onClick = { viewModel.setSelectedTab(0) }
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.People, contentDescription = null) },
                        label = { Text("الطلاب والدرجات", fontSize = 11.sp) },
                        selected = selectedTab == 1,
                        onClick = { viewModel.setSelectedTab(1) }
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Assignment, contentDescription = null) },
                        label = { Text("التسليمات", fontSize = 11.sp) },
                        selected = selectedTab == 2,
                        onClick = { viewModel.setSelectedTab(2) }
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Wifi, contentDescription = null) },
                        label = { Text("البث والشبكة", fontSize = 11.sp) },
                        selected = selectedTab == 3,
                        onClick = { viewModel.setSelectedTab(3) }
                    )
                }
            }
        ) { innerPadding ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(innerPadding)
                    .background(MaterialTheme.colorScheme.background)
            ) {
                // Server control card is permanently visible at top (hidden in Settings to avoid duplication)
                if (selectedTab != 4) {
                    ServerControlCard(
                        isRunning = isServerRunning,
                        serverUrl = serverUrl,
                        simplifiedUrl = simplifiedUrl,
                        currentMode = networkMode,
                        availableNetworks = availableNetworks,
                        onModeChange = { viewModel.setNetworkMode(it) },
                        onToggleServer = { viewModel.toggleServer() },
                        onRefreshIp = { viewModel.refreshNetworkIp() },
                        onShowGuide = { showGuideDialog = true },
                        modifier = Modifier.padding(horizontal = 14.dp, vertical = 6.dp)
                    )
                }

                // Current Tab View
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .weight(1f)
                ) {
                    when (selectedTab) {
                        0 -> QuizzesTab(
                            quizzes = quizzes,
                            submissions = submissions,
                            onToggleActive = { id, status -> viewModel.toggleQuizActive(id, status) },
                            onDeleteQuiz = { id -> viewModel.deleteQuiz(id) },
                            onCreateQuiz = { title, desc, duration, type, questions ->
                                viewModel.createQuiz(title, desc, duration, type, questions)
                            },
                            onLoadSamples = { viewModel.loadSampleQuizzes() }
                        )
                        1 -> StudentsTab(
                            students = students,
                            submissions = submissions,
                            searchQuery = searchQuery,
                            areGradesVisibleGlobally = areGradesVisibleGlobally,
                            onSearchQueryChange = { viewModel.setStudentSearchQuery(it) },
                            onResetPassword = { id, pass -> viewModel.resetStudentPassword(id, pass) },
                            onDeleteStudent = { id -> viewModel.deleteStudent(id) },
                            onSaveEvaluation = { id, e1, e2, part, bonus, notes, showGrades, showNotes, gradeSec ->
                                viewModel.saveStudentEvaluation(id, e1, e2, part, bonus, notes, showGrades, showNotes, gradeSec)
                            },
                            onQuickAdjustBonus = { id, delta ->
                                viewModel.quickAdjustStudentBonus(id, delta)
                            },
                            onToggleGlobalGradesVisibility = { visible ->
                                viewModel.toggleGlobalGradesVisibility(visible)
                            },
                            teacherName = teacherName,
                            onImportStudents = { code, pass, overwrite, onDone ->
                                viewModel.importEncryptedStudents(code, pass, overwrite, onDone)
                            }
                        )
                        2 -> SubmissionsTab(
                            submissions = submissions,
                            quizzes = quizzes
                        )
                        3 -> LiveLogsTab(
                            logs = serverLogs,
                            onClearLogs = { viewModel.clearLogs() }
                        )
                        4 -> SettingsTab(
                            teacherName = teacherName,
                            teacherPhone = teacherPhone,
                            teacherSubject = teacherSubject,
                            isDarkMode = isDarkMode,
                            colorTheme = colorTheme,
                            antiCheatEnabled = antiCheatEnabled,
                            serverIp = serverIp,
                            serverPort = viewModel.serverPort,
                            onEditTeacherProfile = { showEditProfileDialog = true },
                            onToggleDarkMode = { viewModel.setDarkMode(it) },
                            onSelectColorTheme = { viewModel.setColorTheme(it) },
                            onToggleAntiCheat = { viewModel.setAntiCheatEnabled(it) }
                        )
                    }
                }
            }
        }
    }

    if (showGuideDialog) {
        HotspotGuideDialog(onDismiss = { showGuideDialog = false })
    }

    if (showTopBarQrDialog) {
        EnlargedQrDialog(
            directUrl = serverUrl,
            simplifiedUrl = simplifiedUrl,
            networkName = if (networkMode == NetworkConnectionMode.WIFI) "شبكة Wi-Fi المشتركة" else "نقطة اتصال الهاتف (Hotspot)",
            onDismiss = { showTopBarQrDialog = false }
        )
    }
}
