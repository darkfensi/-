package com.owlproxy.app

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.owlproxy.app.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // TODO: здесь будет логика подключения к прокси
        binding.statusText.text = "OwlProxy готов 🦉"
    }
}
