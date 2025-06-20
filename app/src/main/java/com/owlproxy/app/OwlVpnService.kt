package com.owlproxy.app

import android.net.VpnService
import android.os.ParcelFileDescriptor

class OwlVpnService : VpnService() {
    private var vpnInterface: ParcelFileDescriptor? = null

    override fun onCreate() {
        super.onCreate()
        val builder = Builder()
        builder.setSession("OwlProxy")
            .addAddress("10.0.0.2", 24)
            .addDnsServer("8.8.8.8")
            .addRoute("0.0.0.0", 0)
        vpnInterface = builder.establish()
    }

    override fun onDestroy() {
        vpnInterface?.close()
        vpnInterface = null
        super.onDestroy()
    }
}