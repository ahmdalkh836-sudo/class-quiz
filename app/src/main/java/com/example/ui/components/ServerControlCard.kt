package com.example.ui.components

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.widget.Toast
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.qr.EnlargedQrDialog
import com.example.ui.qr.QrCodeView
import com.example.ui.theme.BrandDanger
import com.example.ui.theme.BrandPrimary
import com.example.ui.theme.BrandSuccess
import com.example.util.NetworkAddressInfo
import com.example.util.NetworkConnectionMode

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ServerControlCard(
    isRunning: Boolean,
    serverUrl: String,
    simplifiedUrl: String,
    currentMode: NetworkConnectionMode,
    availableNetworks: List<NetworkAddressInfo>,
    onModeChange: (NetworkConnectionMode) -> Unit,
    onToggleServer: () -> Unit,
    onRefreshIp: () -> Unit,
    onShowGuide: () -> Unit,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    var showInlineQr by remember { mutableStateOf(false) }
    var showEnlargedQrDialog by remember { mutableStateOf(false) }

    Card(
        modifier = modifier
            .fillMaxWidth()
            .testTag("server_control_card"),
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            // Header: Server Status + Toggle Switch
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
                            .background(
                                if (isRunning) BrandSuccess.copy(alpha = 0.15f)
                                else BrandDanger.copy(alpha = 0.15f)
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = if (isRunning) Icons.Default.Wifi else Icons.Default.WifiOff,
                            contentDescription = "حالة الخادم",
                            tint = if (isRunning) BrandSuccess else BrandDanger,
                            modifier = Modifier.size(24.dp)
                        )
                    }

                    Column {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier
                                    .size(8.dp)
                                    .clip(CircleShape)
                                    .background(if (isRunning) BrandSuccess else BrandDanger)
                            )
                            Spacer(modifier = Modifier.width(6.dp))
                            Text(
                                text = if (isRunning) "خادم الحصة يعمل (نشط)" else "الخادم متوقف",
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold,
                                color = if (isRunning) BrandSuccess else BrandDanger
                            )
                        }
                        Text(
                            text = if (isRunning) {
                                if (currentMode == NetworkConnectionMode.WIFI) "مشاركة عبر راوتر المدرسة/المنزل"
                                else "مشاركة عبر نقطة اتصال هاتفك (Hotspot)"
                            } else "اضغط تشغيل للبدء بربط أجهزة الطلاب",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
                        )
                    }
                }

                Switch(
                    checked = isRunning,
                    onCheckedChange = { onToggleServer() },
                    modifier = Modifier.testTag("server_toggle_switch"),
                    colors = SwitchDefaults.colors(
                        checkedThumbColor = Color.White,
                        checkedTrackColor = BrandSuccess
                    )
                )
            }

            Spacer(modifier = Modifier.height(12.dp))

            // Network Mode Selection: Wi-Fi vs Hotspot
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(12.dp))
                    .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                    .padding(4.dp),
                horizontalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                // Wi-Fi Mode Button
                Surface(
                    onClick = { onModeChange(NetworkConnectionMode.WIFI) },
                    modifier = Modifier.weight(1f),
                    shape = RoundedCornerShape(10.dp),
                    color = if (currentMode == NetworkConnectionMode.WIFI) MaterialTheme.colorScheme.primary else Color.Transparent,
                    contentColor = if (currentMode == NetworkConnectionMode.WIFI) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface
                ) {
                    Row(
                        modifier = Modifier.padding(vertical = 8.dp, horizontal = 6.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center
                    ) {
                        Icon(
                            imageVector = Icons.Default.Router,
                            contentDescription = null,
                            modifier = Modifier.size(16.dp)
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(
                            text = "شبكة Wi-Fi المشتركة",
                            fontSize = 11.5.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }

                // Hotspot Mode Button
                Surface(
                    onClick = { onModeChange(NetworkConnectionMode.HOTSPOT) },
                    modifier = Modifier.weight(1f),
                    shape = RoundedCornerShape(10.dp),
                    color = if (currentMode == NetworkConnectionMode.HOTSPOT) MaterialTheme.colorScheme.primary else Color.Transparent,
                    contentColor = if (currentMode == NetworkConnectionMode.HOTSPOT) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface
                ) {
                    Row(
                        modifier = Modifier.padding(vertical = 8.dp, horizontal = 6.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center
                    ) {
                        Icon(
                            imageVector = Icons.Default.Sensors,
                            contentDescription = null,
                            modifier = Modifier.size(16.dp)
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(
                            text = "نقطة اتصال (Hotspot)",
                            fontSize = 11.5.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }

            if (isRunning) {
                Spacer(modifier = Modifier.height(12.dp))

                // Server URL Banner Card
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(14.dp))
                        .background(MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.45f))
                        .border(
                            width = 1.dp,
                            color = MaterialTheme.colorScheme.primary.copy(alpha = 0.3f),
                            shape = RoundedCornerShape(14.dp)
                        )
                        .padding(horizontal = 14.dp, vertical = 10.dp)
                ) {
                    Column(modifier = Modifier.fillMaxWidth()) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = if (currentMode == NetworkConnectionMode.WIFI)
                                        "رابط دخول الطلاب (عبر راوتر المدرسة):"
                                    else
                                        "رابط دخول الطلاب (عبر الهوتسبوت):",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
                                )
                                Text(
                                    text = serverUrl,
                                    style = MaterialTheme.typography.titleMedium,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.primary
                                )
                                Text(
                                    text = "رابط مبسط: $simplifiedUrl",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.primary.copy(alpha = 0.85f)
                                )
                            }

                            Row {
                                // Copy URL Button
                                IconButton(
                                    onClick = {
                                        val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                                        val clip = ClipData.newPlainText("Classroom URL", serverUrl)
                                        clipboard.setPrimaryClip(clip)
                                        Toast.makeText(context, "تم نسخ رابط الموقع!", Toast.LENGTH_SHORT).show()
                                    },
                                    modifier = Modifier.testTag("copy_url_button")
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.ContentCopy,
                                        contentDescription = "نسخ الرابط",
                                        tint = MaterialTheme.colorScheme.primary
                                    )
                                }

                                // Share URL Button
                                IconButton(
                                    onClick = {
                                        val sendIntent = Intent(Intent.ACTION_SEND).apply {
                                            type = "text/plain"
                                            putExtra(
                                                Intent.EXTRA_TEXT,
                                                "رابط اختبارات الحصة للطلاب: $serverUrl أو $simplifiedUrl (تأكد من الاتصال بنفس شبكة واي فاي المدرسة)"
                                            )
                                        }
                                        context.startActivity(Intent.createChooser(sendIntent, "مشاركة رابط الاختبار"))
                                    },
                                    modifier = Modifier.testTag("share_url_button")
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Share,
                                        contentDescription = "مشاركة الرابط",
                                        tint = MaterialTheme.colorScheme.primary
                                    )
                                }
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(10.dp))

                // Action Bar: Big QR, Inline QR Toggle, Open Browser, Refresh
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Button(
                        onClick = { showEnlargedQrDialog = true },
                        modifier = Modifier
                            .weight(1.3f)
                            .testTag("open_big_qr_button"),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Icon(imageVector = Icons.Default.QrCode2, contentDescription = null, modifier = Modifier.size(18.dp))
                        Spacer(modifier = Modifier.width(6.dp))
                        Text("عرض QR كبير 📱", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    }

                    OutlinedButton(
                        onClick = { showInlineQr = !showInlineQr },
                        modifier = Modifier.weight(1f),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Icon(
                            imageVector = if (showInlineQr) Icons.Default.VisibilityOff else Icons.Default.QrCode,
                            contentDescription = null,
                            modifier = Modifier.size(16.dp)
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        Text(if (showInlineQr) "إخفاء" else "معاينة QR", fontSize = 11.5.sp)
                    }

                    IconButton(
                        onClick = {
                            try {
                                val browserIntent = Intent(Intent.ACTION_VIEW, Uri.parse(serverUrl))
                                context.startActivity(browserIntent)
                            } catch (e: Exception) {
                                Toast.makeText(context, "تعذر فتح المتصفح", Toast.LENGTH_SHORT).show()
                            }
                        },
                        modifier = Modifier
                            .clip(RoundedCornerShape(12.dp))
                            .background(MaterialTheme.colorScheme.surfaceVariant)
                    ) {
                        Icon(imageVector = Icons.Default.OpenInBrowser, contentDescription = "فتح في المتصفح")
                    }

                    IconButton(
                        onClick = onRefreshIp,
                        modifier = Modifier
                            .clip(RoundedCornerShape(12.dp))
                            .background(MaterialTheme.colorScheme.surfaceVariant)
                    ) {
                        Icon(imageVector = Icons.Default.Refresh, contentDescription = "تحديث العنوان")
                    }
                }

                // Inline QR Preview
                AnimatedVisibility(visible = showInlineQr) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(top = 12.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Card(
                            shape = RoundedCornerShape(16.dp),
                            colors = CardDefaults.cardColors(containerColor = Color.White),
                            elevation = CardDefaults.cardElevation(defaultElevation = 3.dp)
                        ) {
                            Column(
                                modifier = Modifier.padding(14.dp),
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {
                                QrCodeView(data = serverUrl, size = 180.dp)
                                Spacer(modifier = Modifier.height(8.dp))
                                Text(
                                    text = "وجه كاميرا هاتف الطالب نحو الرمز للدخول فوراً",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = Color.DarkGray
                                )
                            }
                        }
                    }
                }
            } else {
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "💡 يمكنك الاتصال عبر نفس راوتر المدرسة أو عبر الهوتسبوت",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.65f)
                    )
                    TextButton(onClick = onShowGuide) {
                        Text("طريقة الاتصال ❓", fontSize = 12.sp)
                    }
                }
            }
        }
    }

    if (showEnlargedQrDialog) {
        EnlargedQrDialog(
            directUrl = serverUrl,
            simplifiedUrl = simplifiedUrl,
            networkName = if (currentMode == NetworkConnectionMode.WIFI) "شبكة Wi-Fi المشتركة" else "نقطة اتصال الهاتف (Hotspot)",
            onDismiss = { showEnlargedQrDialog = false }
        )
    }
}
