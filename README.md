# Documentación del SDK de Become Android

Esta documentación describe cómo integrar el **SDK de Become** en un proyecto Android, incluyendo **requisitos mínimos**, configuración moderna con **AGP 9 + Kotlin 2.x**, dependencias necesarias (OCR, Liveness, CameraX) y recomendaciones de build.

<p align="center">
  <img src="https://github.com/Becomedigital/become_ANDROID_SDK/blob/master/Pantalla_Android.png" width="284" height="572">
</p>

---

## 1. Requisitos mínimos del proyecto

### Android / SDK
- **minSdk:** 24  
- **compileSdk:** 36  
- **targetSdk:** 36  

> `compileSdk 36` es requerido por varias dependencias recientes (Compose/Activity/Browser, etc.).

### Gradle / Kotlin (recomendado)
- **Android Gradle Plugin (AGP):** `9.0.1`
- **Kotlin:** `2.2.10`
- **Compose Compiler Plugin:** requerido en Kotlin 2.x cuando `compose = true` (se habilita con el plugin `org.jetbrains.kotlin.plugin.compose`)

### Java
- **Java 11**
- `kotlinOptions.jvmTarget = "11"`

### Features requeridas
- `compose true` (obligatorio por Amplify Liveness)
- `viewBinding true` (si el proyecto lo usa)
- `buildConfig true` (si el proyecto usa BuildConfig)
- `coreLibraryDesugaringEnabled true`

---

## 2. Configuración Gradle recomendada

### 2.1 Root `build.gradle` (Proyecto)

1. Configuración del app/build.gradle (Cliente demo / App)

Ejemplo base compatible con el SDK:

    dependencies {
        // Soporte Java 8+ (desugaring)
        coreLibraryDesugaring "com.android.tools:desugar_jdk_libs:2.1.5"

        // === SDK (elige UNA opción) ===
        // A) Módulo:
        // implementation project(":becomedigitalsdk")
        // B) AAR local:
        // implementation fileTree(dir: "libs", include: ["*.aar"])
        // C) Remoto:
        // implementation("com.becomedigital:sdk:VERSION")

        // UI / AndroidX base
        implementation "androidx.appcompat:appcompat:1.6.1"
        implementation "androidx.constraintlayout:constraintlayout:2.1.4"
        implementation "androidx.core:core-ktx:1.15.0"
        implementation "androidx.fragment:fragment-ktx:1.6.2"
        implementation "androidx.activity:activity-ktx:1.8.2"

        // CameraX
        implementation "androidx.camera:camera-core:1.5.3"
        implementation "androidx.camera:camera-camera2:1.5.3"
        implementation "androidx.camera:camera-view:1.5.3"
        implementation "androidx.camera:camera-lifecycle:1.5.3"

        // Navegación
        implementation "androidx.navigation:navigation-fragment:2.5.3"
        implementation "androidx.navigation:navigation-ui:2.5.3"

        // JSON / HTTP / Imágenes
        implementation "com.google.code.gson:gson:2.10.1"
        implementation "com.squareup.okhttp3:okhttp:4.9.3"
        implementation "com.github.bumptech.glide:glide:4.10.0"

        // Liveness (Amplify UI) + Compose
        implementation "com.amplifyframework.ui:liveness:1.10.0"
        implementation "com.amplifyframework:aws-auth-cognito:2.33.0"
        implementation "androidx.compose.material3:material3:1.4.0"
        implementation "androidx.activity:activity-compose:1.12.4"

        // OCR / Captura (Microblink)
        implementation "com.microblink:capture-core:1.4.2"
        implementation "com.microblink:capture-ux:1.4.2"

        // SDK additional libraries required
        implementation "com.android.volley:volley:1.2.1"

        def room_version = "1.1.0"
        implementation "android.arch.persistence.room:runtime:$room_version"
        annotationProcessor "android.arch.persistence.room:compiler:$room_version"
        implementation "android.arch.lifecycle:livedata:1.1.1"
        implementation "android.arch.lifecycle:viewmodel:1.1.1"

        // Tests (opcional)
        testImplementation "junit:junit:4.13.2"
        androidTestImplementation "androidx.test.espresso:espresso-core:3.5.1"
        androidTestImplementation "androidx.test.uiautomator:uiautomator:2.3.0"
    }

✅ Importante:
    •    No dupliques androidx.core:core-ktx con versiones diferentes.
    •    Evita fijar buildToolsVersion; AGP 9 lo maneja mejor sin forzarlo.

⸻

2. Inicialización del SDK

La inicialización utiliza BecomeCallBackManager y BDIVConfig.

    private val mCallbackManager: BecomeCallBackManager = BecomeCallBackManager.createNew()

    fun startAuthentication() {
        val config = BDIVConfig(
        clientId = "yourClientId",
        clientSecret = "yourClientSecret",
        contractId = "yourContractId",
        documetTypes = arrayOf(DocumetType.PASSPORT, DocumetType.DNI),
        true,
        userId = userInput.text.toString(),
        null
    )

    BecomeResponseManager.getInstance().startAuthentication(this, config)

    BecomeResponseManager.getInstance().registerCallback(
        mCallbackManager,
        object : BecomeInterfaseCallback {
            override fun onFinish(responseIV: BDIdentityVerificationResponse) {
                // TODO: manejo de respuesta
            }

            override fun onCancel() {
                Log.d("cancel", "cancel by user")
                textError.setText(R.string.text_cancelk_by_user)
            }
        }
    )
}

ℹ️ Reemplaza credenciales por las reales.

⸻

3. Licencia

Incluye los archivos de licencia provistos por Become dentro de assets/:
    •    com.become.mb.key

⚠️ Importante: el applicationId debe coincidir con el autorizado en la licencia para que la validación funcione.

⸻

4. Manejo de errores

Validación / Respuesta

override fun onFinish(responseIV: BDIdentityVerificationResponse) {
    if (responseIV.responseStatus == ResponseIV.ResponseType.ERROR) {
        // Manejo de error
    } else {
        // Validación exitosa
    }
}

Cancelación por usuario

override fun onCancel() {
    textError.setText(R.string.text_cancelk_by_user)
}


⸻

5. Nota sobre compatibilidad Android 15+ (16 KB page size)

Si el APK/AAB marca advertencias de 16 KB page size por librerías nativas (.so), revisa especialmente dependencias que incluyen binarios nativos (OCR/Liveness y cualquier .aar con jni/).
Para publicar en Google Play apuntando a Android 15+, usa versiones de librerías que ya empacen binarios compatibles con 16 KB.

⸻
