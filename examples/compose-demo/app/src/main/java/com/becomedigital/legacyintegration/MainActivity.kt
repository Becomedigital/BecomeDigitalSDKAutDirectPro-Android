package com.becomedigital.legacyintegration

import android.os.Bundle
import androidx.activity.compose.setContent
import androidx.appcompat.app.AppCompatActivity
import androidx.compose.material3.MaterialTheme

class MainActivity : AppCompatActivity() {
    private val sdkLauncher by lazy { BecomeComposeLauncher(this) }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                BecomeComposeScreen(sdkLauncher)
            }
        }
    }
}
