package com.becomedigital.legacyintegration

import android.Manifest
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat

@Composable
fun BecomeComposeScreen(sdkLauncher: BecomeComposeLauncher) {
    val context = LocalContext.current
    var userId by rememberSaveable { mutableStateOf("") }
    var pendingUserId by rememberSaveable { mutableStateOf("") }
    val permissionRequest = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
        if (granted) sdkLauncher.startOnboarding(pendingUserId)
        else sdkLauncher.report(context.getString(R.string.camera_permission_required))
    }

    Column(modifier = Modifier.fillMaxSize().padding(24.dp)) {
        Text(stringResource(R.string.host_app_name))
        Spacer(Modifier.height(20.dp))
        OutlinedTextField(
            value = userId,
            onValueChange = { userId = it },
            label = { Text(stringResource(R.string.user_id_label)) },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true
        )
        Spacer(Modifier.height(20.dp))
        Button(onClick = {
            val id = userId.trim()
            if (id.isEmpty()) {
                sdkLauncher.report(context.getString(R.string.user_id_required))
            } else if (sdkLauncher.checkConfiguration()) {
                if (ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
                    sdkLauncher.startOnboarding(id)
                } else {
                    pendingUserId = id
                    permissionRequest.launch(Manifest.permission.CAMERA)
                }
            }
        }) {
            Text(stringResource(R.string.start_onboarding))
        }
        Spacer(Modifier.height(20.dp))
        Text(sdkLauncher.status)
    }
}
