package com.example.ui.theme

import androidx.compose.ui.graphics.Color

// Default Brand palette - Teacher Hotspot Classroom Hub
val BrandPrimary = Color(0xFF1E40AF)        // Deep Royal Blue
val BrandPrimaryDark = Color(0xFF172554)
val BrandSecondary = Color(0xFF0284C7)      // Cyan Accent
val BrandTertiary = Color(0xFF0D9488)       // Emerald Teal
val BrandSuccess = Color(0xFF16A34A)        // Green
val BrandWarning = Color(0xFFD97706)        // Amber
val BrandDanger = Color(0xFFDC2626)         // Red

val LightBackground = Color(0xFFF8FAFC)
val LightSurface = Color(0xFFFFFFFF)
val LightSurfaceVariant = Color(0xFFF1F5F9)
val LightOnSurface = Color(0xFF0F172A)
val LightOutline = Color(0xFFCBD5E1)

val DarkBackground = Color(0xFF0B1329)
val DarkSurface = Color(0xFF111C3A)
val DarkSurfaceVariant = Color(0xFF1E293B)
val DarkOnSurface = Color(0xFFF1F5F9)
val DarkOutline = Color(0xFF334155)

enum class AppColorTheme(val title: String, val primary: Color, val secondary: Color) {
    ROYAL_BLUE("الأزرق الملكي", Color(0xFF1E40AF), Color(0xFF0284C7)),
    EMERALD_TEAL("الزمردي التعليمي", Color(0xFF0F766E), Color(0xFF14B8A6)),
    ACADEMIC_PURPLE("البنفسجي الأكاديمي", Color(0xFF6D28D9), Color(0xFF8B5CF6)),
    AMBER_GOLD("الكهرماني الذهبي", Color(0xFFB45309), Color(0xFFF59E0B)),
    CRIMSON_RED("الياقوتي المتميز", Color(0xFFBE123C), Color(0xFFF43F5E))
}
