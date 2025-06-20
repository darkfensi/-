package com.owlproxy.app

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.widget.Toast
import com.owlproxy.app.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.statusText.text = "Статус: отключено"

        binding.connectButton.setOnClickListener {
            startService(Intent(this, OwlVpnService::class.java))
            binding.statusText.text = "Статус: подключено"
        }

        binding.disconnectButton.setOnClickListener {
            stopService(Intent(this, OwlVpnService::class.java))
            binding.statusText.text = "Статус: отключено"
        }
    }
}