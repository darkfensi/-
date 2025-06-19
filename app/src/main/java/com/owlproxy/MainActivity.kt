
package com.owlproxy

import android.content.Context
import android.content.Intent
import android.net.VpnService
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.owlproxy.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private var isConnected = false
    private lateinit var prefs: Prefs

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        prefs = Prefs(this)

        // Восстановить последние данные
        binding.editIp.setText(prefs.ip)
        binding.editPort.setText(prefs.port)
        binding.editUser.setText(prefs.user)
        binding.editPass.setText(prefs.pass)
        binding.switchTls.isChecked = prefs.tls

        updateStatus("Отключено", false)

        binding.buttonConnect.setOnClickListener {
            if (!isConnected) {
                connect()
            } else {
                disconnect()
            }
        }
    }

    private fun connect() {
        val ip = binding.editIp.text.toString()
        val port = binding.editPort.text.toString()
        val user = binding.editUser.text.toString()
        val pass = binding.editPass.text.toString()
        val tls = binding.switchTls.isChecked

        if (ip.isBlank() || port.isBlank()) {
            Toast.makeText(this, "IP и порт обязательны", Toast.LENGTH_SHORT).show()
            return
        }

        // Сохраняем данные
        prefs.save(ip, port, user, pass, tls)

        val intent = VpnService.prepare(this)
        if (intent != null) {
            startActivityForResult(intent, 0)
        } else {
            startVpn()
        }
    }

    private fun startVpn() {
        val intent = Intent(this, OwlVpnService::class.java)
        startService(intent)
        isConnected = true
        updateStatus("Подключение...", true)
    }

    private fun disconnect() {
        val intent = Intent(this, OwlVpnService::class.java)
        stopService(intent)
        isConnected = false
        updateStatus("Отключено", false)
    }

    private fun updateStatus(text: String, connected: Boolean) {
        binding.statusText.text = text
        binding.statusText.setTextColor(if (connected) getColor(R.color.green) else getColor(R.color.red))
        binding.buttonConnect.text = if (connected) "Отключиться" else "Подключиться"
    }
}
