package com.example.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext

@Composable
fun MyApplicationTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    appColorTheme: AppColorTheme = AppColorTheme.ROYAL_BLUE,
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit,
) {
    val primaryColor = appColorTheme.primary
    val secondaryColor = appColorTheme.secondary

    val darkScheme = darkColorScheme(
        primary = secondaryColor,
        onPrimary = Color(0xFF0F172A),
        primaryContainer = primaryColor.copy(alpha = 0.4f),
        onPrimaryContainer = Color(0xFFDBEAFE),
        secondary = secondaryColor,
        onSecondary = Color(0xFF0F172A),
        tertiary = BrandTertiary,
        background = DarkBackground,
        surface = DarkSurface,
        surfaceVariant = DarkSurfaceVariant,
        onBackground = DarkOnSurface,
        onSurface = DarkOnSurface,
        outline = DarkOutline
    )

    val lightScheme = lightColorScheme(
        primary = primaryColor,
        onPrimary = Color.White,
        primaryContainer = primaryColor.copy(alpha = 0.12f),
        onPrimaryContainer = primaryColor,
        secondary = secondaryColor,
        onSecondary = Color.White,
        tertiary = BrandTertiary,
        background = LightBackground,
        surface = LightSurface,
        surfaceVariant = LightSurfaceVariant,
        onBackground = LightOnSurface,
        onSurface = LightOnSurface,
        outline = LightOutline
    )

    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> darkScheme
        else -> lightScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}

