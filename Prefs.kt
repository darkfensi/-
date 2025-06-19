
package com.owlproxy

import android.content.Context

class Prefs(context: Context) {
    private val prefs = context.getSharedPreferences("owlproxy", Context.MODE_PRIVATE)

    var ip: String
        get() = prefs.getString("ip", "") ?: ""
        set(value) = prefs.edit().putString("ip", value).apply()

    var port: String
        get() = prefs.getString("port", "") ?: ""
        set(value) = prefs.edit().putString("port", value).apply()

    var user: String
        get() = prefs.getString("user", "") ?: ""
        set(value) = prefs.edit().putString("user", value).apply()

    var pass: String
        get() = prefs.getString("pass", "") ?: ""
        set(value) = prefs.edit().putString("pass", value).apply()

    var tls: Boolean
        get() = prefs.getBoolean("tls", false)
        set(value) = prefs.edit().putBoolean("tls", value).apply()

    fun save(ip: String, port: String, user: String, pass: String, tls: Boolean) {
        this.ip = ip
        this.port = port
        this.user = user
        this.pass = pass
        this.tls = tls
    }
}
