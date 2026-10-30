package com.becomedigital.legacyintegration

import android.Manifest
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.text.KeyboardOptions
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
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.core.content.ContextCompat

@Composable
fun BecomeComposeScreen(sdkLauncher: BecomeComposeLauncher) {
    val context = LocalContext.current
    var jwt by remember { mutableStateOf("") }
    var resultsJwt by remember { mutableStateOf("") }
    var userId by rememberSaveable { mutableStateOf("") }
    var pendingUserId by rememberSaveable { mutableStateOf("") }
    val permissionRequest = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
        if (granted) sdkLauncher.startOnboarding(pendingUserId, jwt, resultsJwt)
        else sdkLauncher.report(context.getString(R.string.camera_permission_required))
    }

    Column(modifier = Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(24.dp)) {
        Text(stringResource(R.string.host_app_name))
        Spacer(Modifier.height(20.dp))
        OutlinedTextField(
            value = jwt,
            onValueChange = { jwt = it },
            label = { Text(stringResource(R.string.jwt_label)) },
            modifier = Modifier.fillMaxWidth(),
            visualTransformation = PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            singleLine = true
        )
        Spacer(Modifier.height(20.dp))
        OutlinedTextField(
            value = resultsJwt,
            onValueChange = { resultsJwt = it },
            label = { Text(stringResource(R.string.results_jwt_label)) },
            modifier = Modifier.fillMaxWidth(),
            visualTransformation = PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            singleLine = true
        )
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
            } else if (sdkLauncher.checkConfiguration(jwt, resultsJwt)) {
                if (ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
                    sdkLauncher.startOnboarding(id, jwt, resultsJwt)
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
