package com.owlproxy.app

import android.content.Context

object Prefs {
    fun saveProxySettings(context: Context, host: String, port: Int) {
        val prefs = context.getSharedPreferences("proxy_prefs", Context.MODE_PRIVATE)
        prefs.edit().putString("host", host).putInt("port", port).apply()
    }
    fun getProxySettings(context: Context): Pair<String?, Int> {
        val prefs = context.getSharedPreferences("proxy_prefs", Context.MODE_PRIVATE)
        return prefs.getString("host", null) to prefs.getInt("port", 0)
    }
}