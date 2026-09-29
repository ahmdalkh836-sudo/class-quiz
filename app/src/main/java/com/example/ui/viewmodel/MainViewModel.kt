package com.example.ui.viewmodel

import android.app.Application
import android.content.Context
import android.net.nsd.NsdManager
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.local.AppDatabase
import com.example.data.model.Question
import com.example.data.model.Quiz
import com.example.data.model.Student
import com.example.data.model.Submission
import com.example.data.repository.QuizRepository
import com.example.server.ClassroomWebServer
import com.example.server.ServerLogEvent
import com.example.ui.theme.AppColorTheme
import com.example.util.NetworkAddressInfo
import com.example.util.NetworkConnectionMode
import com.example.util.NetworkHelper
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class MainViewModel(application: Application) : AndroidViewModel(application) {

    private val prefs = application.getSharedPreferences("classroom_settings", Context.MODE_PRIVATE)

    val repository: QuizRepository
    private var webServer: ClassroomWebServer? = null
    private var mdnsListener: NsdManager.RegistrationListener? = null

    private val _isServerRunning = MutableStateFlow(false)
    val isServerRunning: StateFlow<Boolean> = _isServerRunning.asStateFlow()

    private val _networkMode = MutableStateFlow(
        try {
            NetworkConnectionMode.valueOf(
                prefs.getString("network_mode", NetworkConnectionMode.WIFI.name) ?: NetworkConnectionMode.WIFI.name
            )
        } catch (_: Exception) {
            NetworkConnectionMode.WIFI
        }
    )
    val networkMode: StateFlow<NetworkConnectionMode> = _networkMode.asStateFlow()

    private val _availableNetworks = MutableStateFlow<List<NetworkAddressInfo>>(emptyList())
    val availableNetworks: StateFlow<List<NetworkAddressInfo>> = _availableNetworks.asStateFlow()

    val serverPort = 8080

    private val _serverIp = MutableStateFlow(NetworkHelper.resolveIpForMode(_networkMode.value))
    val serverIp: StateFlow<String> = _serverIp.asStateFlow()

    val serverUrl: StateFlow<String> = _serverIp.combine(_isServerRunning) { ip, _ ->
        "http://$ip:$serverPort"
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "http://192.168.43.1:$serverPort")

    val simplifiedUrl: StateFlow<String> = MutableStateFlow(NetworkHelper.getSimplifiedUrl(serverPort)).asStateFlow()

    private val _areGradesVisibleGlobally = MutableStateFlow(prefs.getBoolean("grades_globally_visible", true))
    val areGradesVisibleGlobally: StateFlow<Boolean> = _areGradesVisibleGlobally.asStateFlow()

    private val _serverLogs = MutableStateFlow<List<ServerLogEvent>>(emptyList())
    val serverLogs: StateFlow<List<ServerLogEvent>> = _serverLogs.asStateFlow()

    private val _selectedTab = MutableStateFlow(0)
    val selectedTab: StateFlow<Int> = _selectedTab.asStateFlow()

    private val _studentSearchQuery = MutableStateFlow("")
    val studentSearchQuery: StateFlow<String> = _studentSearchQuery.asStateFlow()

    // Teacher Profile & Preferences
    private val _teacherName = MutableStateFlow(prefs.getString("teacher_name", "") ?: "")
    val teacherName: StateFlow<String> = _teacherName.asStateFlow()

    private val _teacherPhone = MutableStateFlow(prefs.getString("teacher_phone", "") ?: "")
    val teacherPhone: StateFlow<String> = _teacherPhone.asStateFlow()

    private val _teacherSubject = MutableStateFlow(prefs.getString("teacher_subject", "") ?: "")
    val teacherSubject: StateFlow<String> = _teacherSubject.asStateFlow()

    private val _isFirstLaunch = MutableStateFlow(
        prefs.getBoolean("is_first_launch", true) && (prefs.getString("teacher_name", "") ?: "").isBlank()
    )
    val isFirstLaunch: StateFlow<Boolean> = _isFirstLaunch.asStateFlow()

    private val _isDarkMode = MutableStateFlow(prefs.getBoolean("is_dark_mode", false))
    val isDarkMode: StateFlow<Boolean> = _isDarkMode.asStateFlow()

    private val _colorTheme = MutableStateFlow(
        try {
            AppColorTheme.valueOf(
                prefs.getString("color_theme", AppColorTheme.ROYAL_BLUE.name) ?: AppColorTheme.ROYAL_BLUE.name
            )
        } catch (_: Exception) {
            AppColorTheme.ROYAL_BLUE
        }
    )
    val colorTheme: StateFlow<AppColorTheme> = _colorTheme.asStateFlow()

    private val _antiCheatEnabled = MutableStateFlow(prefs.getBoolean("anti_cheat_enabled", true))
    val antiCheatEnabled: StateFlow<Boolean> = _antiCheatEnabled.asStateFlow()

    val quizzes: StateFlow<List<Quiz>>
    val students: StateFlow<List<Student>>
    val submissions: StateFlow<List<Submission>>

    init {
        val db = AppDatabase.getInstance(application)
        repository = QuizRepository(db)
        repository.areGradesVisibleGlobally = _areGradesVisibleGlobally.value

        quizzes = repository.allQuizzesFlow.stateIn(
            viewModelScope,
            SharingStarted.WhileSubscribed(5000),
            emptyList()
        )

        students = repository.allStudentsFlow.stateIn(
            viewModelScope,
            SharingStarted.WhileSubscribed(5000),
            emptyList()
        )

        submissions = repository.allSubmissionsFlow.stateIn(
            viewModelScope,
            SharingStarted.WhileSubscribed(5000),
            emptyList()
        )

        viewModelScope.launch(Dispatchers.IO) {
            repository.ensureDefaultQuizzes()
        }

        refreshNetworkIp()
        initWebServer()

        // Register local mDNS service for school.local
        mdnsListener = NetworkHelper.registerMdnsService(application, serverPort)
    }

    private fun initWebServer() {
        webServer = ClassroomWebServer(repository, port = serverPort) { event ->
            viewModelScope.launch {
                val updated = listOf(event) + _serverLogs.value
                _serverLogs.value = updated.take(150)
            }
        }
        // Auto-start server so it's ready as soon as the teacher opens the app
        startServer()
    }

    fun startServer() {
        refreshNetworkIp()
        webServer?.start()
        _isServerRunning.value = true
    }

    fun stopServer() {
        webServer?.stop()
        _isServerRunning.value = false
    }

    fun toggleServer() {
        if (_isServerRunning.value) {
            stopServer()
        } else {
            startServer()
        }
    }

    fun setNetworkMode(mode: NetworkConnectionMode) {
        _networkMode.value = mode
        prefs.edit().putString("network_mode", mode.name).apply()
        refreshNetworkIp()
    }

    fun refreshNetworkIp() {
        val networks = NetworkHelper.getAvailableNetworkAddresses()
        _availableNetworks.value = networks
        val ip = NetworkHelper.resolveIpForMode(_networkMode.value)
        _serverIp.value = ip
    }

    fun setSelectedTab(index: Int) {
        _selectedTab.value = index
    }

    fun setStudentSearchQuery(query: String) {
        _studentSearchQuery.value = query
    }

    fun toggleQuizActive(quizId: Long, currentStatus: Boolean) {
        viewModelScope.launch(Dispatchers.IO) {
            repository.setQuizActive(quizId, !currentStatus)
        }
    }

    fun deleteQuiz(quizId: Long) {
        viewModelScope.launch(Dispatchers.IO) {
            repository.deleteQuiz(quizId)
        }
    }

    fun createQuiz(
        title: String,
        description: String,
        durationMinutes: Int,
        type: String,
        questions: List<Question>
    ) {
        viewModelScope.launch(Dispatchers.IO) {
            val quiz = Quiz(
                title = title.trim(),
                description = description.trim(),
                durationMinutes = durationMinutes,
                type = type,
                isActive = true
            )
            repository.insertQuiz(quiz, questions)
        }
    }

    fun resetStudentPassword(studentId: Long, newPassword: String) {
        viewModelScope.launch(Dispatchers.IO) {
            repository.updateStudentPassword(studentId, newPassword)
        }
    }

    fun deleteStudent(studentId: Long) {
        viewModelScope.launch(Dispatchers.IO) {
            repository.deleteStudent(studentId)
        }
    }

    fun saveStudentEvaluation(
        studentId: Long,
        exam1: Double,
        exam2: Double,
        participation: Double,
        bonus: Double,
        notes: String,
        showGrades: Boolean,
        showNotes: Boolean,
        gradeSection: String
    ) {
        viewModelScope.launch(Dispatchers.IO) {
            repository.updateStudentEvaluation(
                studentId = studentId,
                exam1 = exam1,
                exam2 = exam2,
                participation = participation,
                bonus = bonus,
                notes = notes,
                showGrades = showGrades,
                showNotes = showNotes
            )
            if (gradeSection.isNotBlank()) {
                repository.updateStudentClassSection(studentId, gradeSection)
            }
        }
    }

    fun quickAdjustStudentBonus(studentId: Long, delta: Double) {
        viewModelScope.launch(Dispatchers.IO) {
            repository.adjustStudentBonus(studentId, delta)
        }
    }

    fun toggleGlobalGradesVisibility(visible: Boolean) {
        _areGradesVisibleGlobally.value = visible
        prefs.edit().putBoolean("grades_globally_visible", visible).apply()
        repository.areGradesVisibleGlobally = visible
        viewModelScope.launch(Dispatchers.IO) {
            repository.setAllStudentsGradesVisibility(visible)
        }
    }

    fun importEncryptedStudents(
        encryptedCode: String,
        password: String,
        overwriteExisting: Boolean,
        onResult: (Result<com.example.data.repository.StudentImportResult>) -> Unit
    ) {
        viewModelScope.launch(Dispatchers.IO) {
            val decryptRes = com.example.util.StudentCryptoManager.decryptStudents(encryptedCode, password)
            if (decryptRes.isFailure) {
                withContext(Dispatchers.Main) {
                    onResult(Result.failure(decryptRes.exceptionOrNull() ?: Exception("فشل فك التشفير")))
                }
                return@launch
            }
            val studentsList = decryptRes.getOrNull() ?: emptyList()
            val importStats = repository.importStudents(studentsList, overwriteExisting)
            withContext(Dispatchers.Main) {
                onResult(Result.success(importStats))
            }
        }
    }

    fun loadSampleQuizzes() {
        viewModelScope.launch(Dispatchers.IO) {
            repository.ensureDefaultQuizzes()
        }
    }

    fun clearLogs() {
        _serverLogs.value = emptyList()
    }

    fun saveTeacherProfile(name: String, phone: String, subject: String) {
        _teacherName.value = name.trim()
        _teacherPhone.value = phone.trim()
        _teacherSubject.value = subject.trim()
        _isFirstLaunch.value = false
        prefs.edit()
            .putString("teacher_name", _teacherName.value)
            .putString("teacher_phone", _teacherPhone.value)
            .putString("teacher_subject", _teacherSubject.value)
            .putBoolean("is_first_launch", false)
            .apply()
    }

    fun dismissFirstLaunch() {
        _isFirstLaunch.value = false
        prefs.edit().putBoolean("is_first_launch", false).apply()
    }

    fun toggleDarkMode() {
        setDarkMode(!_isDarkMode.value)
    }

    fun setDarkMode(enabled: Boolean) {
        _isDarkMode.value = enabled
        prefs.edit().putBoolean("is_dark_mode", enabled).apply()
    }

    fun setColorTheme(theme: AppColorTheme) {
        _colorTheme.value = theme
        prefs.edit().putString("color_theme", theme.name).apply()
    }

    fun setAntiCheatEnabled(enabled: Boolean) {
        _antiCheatEnabled.value = enabled
        prefs.edit().putBoolean("anti_cheat_enabled", enabled).apply()
    }

    override fun onCleared() {
        super.onCleared()
        webServer?.stop()
        NetworkHelper.unregisterMdnsService(getApplication(), mdnsListener)
    }
}
