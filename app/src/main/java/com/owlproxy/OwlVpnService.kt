
package com.owlproxy

import android.content.Intent
import android.net.VpnService
import android.os.ParcelFileDescriptor
import java.io.IOException
import java.net.InetSocketAddress
import java.net.Socket
import javax.net.ssl.SSLSocketFactory

class OwlVpnService : VpnService() {

    private var vpnInterface: ParcelFileDescriptor? = null
    private var thread: Thread? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        thread = Thread {
            try {
                runVpn()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        thread?.start()
        return START_STICKY
    }

    private fun runVpn() {
        val prefs = Prefs(this)
        val builder = Builder()

        builder.setSession("OwlProxy")
            .addAddress("10.0.0.2", 24)
            .addDnsServer("1.1.1.1")
            .addRoute("0.0.0.0", 0)

        vpnInterface = builder.establish()

        val socket = if (prefs.tls) {
            val sslFactory = SSLSocketFactory.getDefault() as SSLSocketFactory
            sslFactory.createSocket(prefs.ip, prefs.port.toInt())
        } else {
            Socket().apply {
                connect(InetSocketAddress(prefs.ip, prefs.port.toInt()), 8000)
            }
        }

        // Здесь должен быть SOCKS5 handshake и проксирование через VPN-интерфейс
        // Это упрощённая заготовка, которую нужно дополнить реализацией туннеля

        socket.close()
    }

    override fun onDestroy() {
        thread?.interrupt()
        vpnInterface?.close()
        super.onDestroy()
    }
}
