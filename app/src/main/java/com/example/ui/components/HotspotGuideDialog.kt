package com.example.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.QrCode2
import androidx.compose.material.icons.filled.Router
import androidx.compose.material.icons.filled.Sensors
import androidx.compose.material.icons.filled.Wifi
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.example.ui.theme.BrandPrimary
import com.example.ui.theme.BrandSuccess
import com.example.ui.theme.BrandWarning

@Composable
fun HotspotGuideDialog(
    onDismiss: () -> Unit
) {
    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Surface(
            modifier = Modifier
                .fillMaxWidth(0.94f)
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
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .clip(CircleShape)
                                .background(BrandPrimary.copy(alpha = 0.1f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.Wifi,
                                contentDescription = null,
                                tint = BrandPrimary,
                                modifier = Modifier.size(24.dp)
                            )
                        }
                        Spacer(modifier = Modifier.width(10.dp))
                        Text(
                            text = "دليل الاتصال والمشاركة المدرسية",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold
                        )
                    }

                    IconButton(onClick = onDismiss) {
                        Icon(imageVector = Icons.Default.Close, contentDescription = "إغلاق")
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                // METHOD 1: Local Wi-Fi (No Hotspot needed)
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = BrandSuccess.copy(alpha = 0.08f)),
                    border = androidx.compose.foundation.BorderStroke(1.5.dp, BrandSuccess.copy(alpha = 0.4f))
                ) {
                    Column(modifier = Modifier.padding(14.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(imageVector = Icons.Default.Router, contentDescription = null, tint = BrandSuccess)
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                text = "الخيار الأول: المشاركة عبر شبكة Wi-Fi المشتركة",
                                fontWeight = FontWeight.Bold,
                                color = BrandSuccess,
                                fontSize = 14.sp
                            )
                        }
                        Spacer(modifier = Modifier.height(6.dp))
                        Text(
                            text = "💡 ميزة جديدة ومريحة: لست بحاجة لفتح بث هوتسبوت من هاتفك! إذا كان هاتفك وهواتف الطلاب متصلة بنفس راوتر المدرسة أو المعمل أو المنزل:",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.85f)
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text("1. تأكد أن هاتفك وهواتف الطلاب متصلون بنفس شبكة الواي فاي.", fontSize = 12.sp)
                        Text("2. اختر وضع (شبكة Wi-Fi المشتركة) في بطاقة الخادم أعلى التطبيق.", fontSize = 12.sp)
                        Text("3. اطلب من الطلاب مسح رمز الـ QR أو فتح الرابط المباشر في متصفحهم فوراً.", fontSize = 12.sp)
                    }
                }

                Spacer(modifier = Modifier.height(12.dp))

                // METHOD 2: Hotspot (When no Wi-Fi router is available)
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                ) {
                    Column(modifier = Modifier.padding(14.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(imageVector = Icons.Default.Sensors, contentDescription = null, tint = BrandPrimary)
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                text = "الخيار الثاني: بث نقطة اتصال من هاتفك (Hotspot)",
                                fontWeight = FontWeight.Bold,
                                color = BrandPrimary,
                                fontSize = 14.sp
                            )
                        }
                        Spacer(modifier = Modifier.height(6.dp))
                        Text(
                            text = "استخدم هذا الخيار في حال عدم توفر راوتر أو شبكة واي فاي في الفصل الدراسي:",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.85f)
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text("1. افتح إعدادات هاتفك وشغّل (نقطة اتصال الهواتف المحمولة / Hotspot).", fontSize = 12.sp)
                        Text("2. اطلب من الطلاب الاتصال بشبكة هاتفك بدون الحاجة لباقة إنترنت.", fontSize = 12.sp)
                        Text("3. يفتح الطلاب الرابط أو يمسحون الـ QR كود للدخول فوراً.", fontSize = 12.sp)
                    }
                }

                Spacer(modifier = Modifier.height(12.dp))

                // Easy Access Tip
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = BrandWarning.copy(alpha = 0.08f)),
                    border = androidx.compose.foundation.BorderStroke(1.dp, BrandWarning.copy(alpha = 0.3f))
                ) {
                    Row(
                        modifier = Modifier.padding(14.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(imageVector = Icons.Default.QrCode2, contentDescription = null, tint = BrandWarning, modifier = Modifier.size(28.dp))
                        Spacer(modifier = Modifier.width(10.dp))
                        Column {
                            Text("أسهل وأسرع طريقة للطلاب:", fontWeight = FontWeight.Bold, fontSize = 13.sp, color = BrandWarning)
                            Text(
                                "اضغط زر 'عرض QR كبير 📱' في الشاشة، واطلب من الطلاب توجيه كاميرا هواتفهم نحو الشاشة لفتح الاختبار فوراً بدون كتابة أي أرقام!",
                                fontSize = 11.5.sp,
                                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.8f)
                            )
                        }
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                Button(
                    onClick = onDismiss,
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text("حسناً، فهمت", fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}
