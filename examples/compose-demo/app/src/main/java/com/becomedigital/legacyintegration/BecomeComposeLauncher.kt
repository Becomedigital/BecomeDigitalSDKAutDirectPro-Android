package com.becomedigital.legacyintegration

import androidx.appcompat.app.AppCompatActivity
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import com.becomedigital.sdk.identity.becomedigitalsdk.core.callback.BecomeCallBackManager
import com.becomedigital.sdk.identity.becomedigitalsdk.core.callback.BecomeInterfaseCallback
import com.becomedigital.sdk.identity.becomedigitalsdk.core.callback.BecomeResponseManager
import com.becomedigital.sdk.identity.becomedigitalsdk.models.BDIVConfig
import com.becomedigital.sdk.identity.becomedigitalsdk.models.BDIdentityVerificationResponse
import com.becomedigital.sdk.identity.becomedigitalsdk.models.DocumetType
import java.io.IOException

class BecomeComposeLauncher(private val activity: AppCompatActivity) {
    private val callbackManager = BecomeCallBackManager.createNew()

    var status by mutableStateOf(activity.getString(R.string.status_ready))
        private set

    init {
        BecomeResponseManager.getInstance().registerCallback(callbackManager, object : BecomeInterfaseCallback {
            override fun onFinish(response: BDIdentityVerificationResponse) {
                activity.runOnUiThread {
                    status = activity.getString(R.string.sdk_status, response.responseStatus)
                }
            }

            override fun onCancel() {
                activity.runOnUiThread { status = activity.getString(R.string.status_cancelled) }
            }
        })
    }

    fun report(message: String) {
        status = message
    }

    fun checkConfiguration(jwt: String): Boolean {
        if (jwt.isBlank()) {
            status = activity.getString(R.string.jwt_missing)
            return false
        }
        if (BuildConfig.BECOME_CONTRACT_ID.isBlank()) {
            status = activity.getString(R.string.configuration_missing)
            return false
        }
        try {
            activity.assets.open("com.become.mb.key").use { }
        } catch (_: IOException) {
            status = activity.getString(R.string.license_missing)
            return false
        }
        return true
    }

    fun startOnboarding(userId: String, jwt: String) {
        if (!checkConfiguration(jwt)) return
        val config = BDIVConfig(
            jwt.trim(),
            BuildConfig.BECOME_CONTRACT_ID,
            arrayOf(DocumetType.DNI, DocumetType.PASSPORT),
            true,
            userId
        )
        config.flow = BDIVConfig.Flow.Onboarding
        config.setDebugLogsEnabled(true)
        status = activity.getString(R.string.status_starting)
        BecomeResponseManager.getInstance().startAuthentication(activity, config)
    }
}
