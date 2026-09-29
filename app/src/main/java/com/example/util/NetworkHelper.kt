package com.example.util

import android.content.Context
import android.net.nsd.NsdManager
import android.net.nsd.NsdServiceInfo
import android.util.Log
import java.net.Inet4Address
import java.net.NetworkInterface

enum class NetworkConnectionMode {
    WIFI,       // الجميع متصل بنفس شبكة الواي فاي (راوتر المدرسة أو المنزل بدون هوتسبوت)
    HOTSPOT     // بث نقطة اتصال خاصة من هاتف المعلم
}

data class NetworkAddressInfo(
    val ip: String,
    val interfaceName: String,
    val mode: NetworkConnectionMode,
    val title: String,
    val subtitle: String
)

object NetworkHelper {
    private const val TAG = "NetworkHelper"
    const val DEFAULT_PORT = 8080
    const val MDNS_HOSTNAME = "school.local"

    /**
     * Inspects all active network interfaces on the device and categorizes them.
     */
    fun getAvailableNetworkAddresses(): List<NetworkAddressInfo> {
        val results = mutableListOf<NetworkAddressInfo>()
        try {
            val interfaces = NetworkInterface.getNetworkInterfaces() ?: return emptyList()

            while (interfaces.hasMoreElements()) {
                val nif = interfaces.nextElement() ?: continue
                if (nif.isLoopback || !nif.isUp) continue

                val name = nif.name.lowercase()
                val addresses = nif.inetAddresses ?: continue

                while (addresses.hasMoreElements()) {
                    val addr = addresses.nextElement() ?: continue
                    if (addr is Inet4Address && !addr.isLoopbackAddress) {
                        val host = addr.hostAddress ?: continue
                        if (host.startsWith("127.")) continue

                        val isHotspot = host.startsWith("192.168.43.") ||
                                host.startsWith("192.168.44.") ||
                                name.contains("ap") ||
                                name.contains("softap")

                        val mode = if (isHotspot) NetworkConnectionMode.HOTSPOT else NetworkConnectionMode.WIFI
                        val title = if (mode == NetworkConnectionMode.WIFI) {
                            "شبكة Wi-Fi المشتركة"
                        } else {
                            "نقطة اتصال الهاتف (Hotspot)"
                        }

                        val subtitle = if (mode == NetworkConnectionMode.WIFI) {
                            "متصل بنفس راوتر المدرسة أو المنزل بدون بث نت ($name)"
                        } else {
                            "بث شبكة خاصة من هاتفك للطلاب ($name)"
                        }

                        results.add(
                            NetworkAddressInfo(
                                ip = host,
                                interfaceName = name,
                                mode = mode,
                                title = title,
                                subtitle = subtitle
                            )
                        )
                    }
                }
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error enumerating interfaces", e)
        }

        // Put Wi-Fi first, then Hotspot
        return results.sortedWith(compareBy({ it.mode != NetworkConnectionMode.WIFI }, { it.ip }))
    }

    /**
     * Detects the best IP according to desired mode.
     */
    fun resolveIpForMode(preferredMode: NetworkConnectionMode): String {
        val all = getAvailableNetworkAddresses()
        if (all.isEmpty()) return "192.168.43.1"

        val matching = all.firstOrNull { it.mode == preferredMode }
        if (matching != null) return matching.ip

        return all.first().ip
    }

    /**
     * Returns a simplified mDNS URL or direct IP URL.
     */
    fun getSimplifiedUrl(port: Int = DEFAULT_PORT): String {
        return "http://$MDNS_HOSTNAME:$port"
    }

    /**
     * Registers local mDNS service so Apple devices (Safari) and mDNS-compatible
     * Android/PC browsers can navigate to http://school.local:8080 directly!
     */
    fun registerMdnsService(context: Context, port: Int = DEFAULT_PORT): NsdManager.RegistrationListener? {
        return try {
            val nsdManager = context.getSystemService(Context.NSD_SERVICE) as? NsdManager ?: return null
            val serviceInfo = NsdServiceInfo().apply {
                serviceName = "school"
                serviceType = "_http._tcp."
                setPort(port)
            }

            val listener = object : NsdManager.RegistrationListener {
                override fun onServiceRegistered(NsdServiceInfo: NsdServiceInfo) {
                    Log.d(TAG, "mDNS Service registered: ${NsdServiceInfo.serviceName}")
                }
                override fun onRegistrationFailed(serviceInfo: NsdServiceInfo, errorCode: Int) {
                    Log.w(TAG, "mDNS Registration failed: $errorCode")
                }
                override fun onServiceUnregistered(arg0: NsdServiceInfo) {
                    Log.d(TAG, "mDNS Service unregistered")
                }
                override fun onUnregistrationFailed(serviceInfo: NsdServiceInfo, errorCode: Int) {
                    Log.w(TAG, "mDNS Unregistration failed: $errorCode")
                }
            }

            nsdManager.registerService(serviceInfo, NsdManager.PROTOCOL_DNS_SD, listener)
            listener
        } catch (e: Exception) {
            Log.w(TAG, "Could not register mDNS service", e)
            null
        }
    }

    fun unregisterMdnsService(context: Context, listener: NsdManager.RegistrationListener?) {
        if (listener == null) return
        try {
            val nsdManager = context.getSystemService(Context.NSD_SERVICE) as? NsdManager
            nsdManager?.unregisterService(listener)
        } catch (e: Exception) {
            Log.w(TAG, "Error unregistering mDNS service", e)
        }
    }
}
