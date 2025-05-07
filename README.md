# Documentación del SDK de Become Android

Esta documentación proporciona información actualizada sobre el SDK de Become para Android, incluyendo la integración de nuevas dependencias y autenticación mediante JFrog Artifactory.

<p align="center">
  <img src="https://github.com/Becomedigital/become_ANDROID_SDK/blob/master/Pantalla_Android.png" width="284" height="572">
</p>

## 1. Configuración de Gradle

### Configuración del Repositorio JFrog

Para utilizar la nueva librería `finger`, agregue el siguiente repositorio privado de JFrog en el archivo `build.gradle` a nivel de proyecto o módulo:

```gradle
maven {
    url "https://identy.jfrog.io/identy/identy-finger-release"
    credentials {
        username = "your_username"
        password = "your_password"
    }
}
```

> 🔐 **Nota:** asegúrese de reemplazar `your_username` y `your_password` con las credenciales proporcionadas.

### Implementación de Dependencias Requeridas

Agregue las siguientes dependencias en el bloque `dependencies` de su `build.gradle`:

```gradle
// Librería principal del SDK
implementation(group: 'com.identy.app', name: 'finger', version: '6.1.1-develop', ext: 'aar')

// Dependencias adicionales necesarias
implementation 'com.android.volley:volley:1.2.1'

def room_version = "1.1.0"
implementation "android.arch.persistence.room:runtime:$room_version"
annotationProcessor "android.arch.persistence.room:compiler:$room_version"

implementation 'android.arch.lifecycle:livedata:1.1.1'
implementation 'android.arch.lifecycle:viewmodel:1.1.1'
```

Además, conserve las dependencias previamente configuradas:

```gradle
implementation 'com.mikhaellopez:circularimageview:4.3.1'
implementation 'com.google.android.material:material:1.3.0'
implementation 'com.amplifyframework.ui:liveness:1.3.0'
implementation 'com.amplifyframework:aws-auth-cognito:2.26.0'
implementation 'androidx.compose.material3:material3:1.1.2'
implementation 'androidx.activity:activity-compose:1.7.2'

implementation("androidx.camera:camera-core:1.3.0")
implementation("androidx.camera:camera-camera2:1.3.0")
implementation("androidx.camera:camera-view:1.3.0")
implementation("androidx.camera:camera-lifecycle:1.3.0")

implementation 'androidx.navigation:navigation-fragment:2.5.3'
implementation 'androidx.navigation:navigation-ui:2.5.3'

implementation 'com.google.code.gson:gson:2.10.1'
implementation 'com.github.bumptech.glide:glide:4.10.0'
```

## 2. Inicialización del SDK

La inicialización de la SDK ahora utiliza un `BecomeCallBackManager` y una nueva instancia de `BDIVConfig`.

Ejemplo actualizado en Kotlin:

```kotlin
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

    BecomeResponseManager.getInstance().registerCallback(mCallbackManager, object : BecomeInterfaseCallback {
        override fun onFinish(responseIV: BDIdentityVerificationResponse) {
            // TODO: manejo de respuesta exitosa
        }

        override fun onCancel() {
            Log.d("cancel", "cancel by user")
            textError.setText(R.string.text_cancelk_by_user)
        }
    })
}
```

> ℹ️ **Nota:** Reemplace `yourClientId`, `yourClientSecret`, `yourContractId` y otros valores por las credenciales reales.

## 3. Recomendaciones y Requisitos

### Requisitos del Proyecto Android

De acuerdo con la configuración actual de `build.gradle`, los requisitos mínimos son:

* **Plugins:**

  * `com.android.application`
  * `kotlin-android`

* **SDK:**

  * `compileSdk` 35
  * `targetSdkVersion` 34
  * `minSdkVersion` 24
  * `buildToolsVersion` 30.0.3

* **Compatibilidad Java y Kotlin:**

  * `JavaVersion.VERSION_11`
  * `kotlinOptions.jvmTarget = "11"`

* **Funciones habilitadas:**

  * `viewBinding true`
  * `compose true`
  * `coreLibraryDesugaringEnabled true`

* **Namespace:** `com.example.demosdk`

* **Versiones:**

  * `versionCode 1`
  * `versionName "2.0.0"`

* **Testing configurado:**

  * `testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"`
  * Dependencias para `junit` y `espresso`

* **Otros:**

  * `multiDexEnabled true`
  * `minifyEnabled false` en build type release
  * Uso de `proguard-android-optimize.txt` y `proguard-rules.pro` para release

## 4. Licencia

Asegúrese de incluir los archivos de licencia provistos por **Become** dentro de la carpeta `assets` de su proyecto. Deben existir exactamente los siguientes archivos con estos nombres específicos:

* `com.become.finger.lic`
* `com.become.mb.key`

⚠️ **Importante:** el `applicationId` debe coincidir con el valor autorizado en la licencia para su correcto funcionamiento.

## 5. Manejo de Errores

### Validación Exitosa

```kotlin
override fun onFinish(responseIV: BDIdentityVerificationResponse) {
    if (responseIV.responseStatus == ResponseIV.ResponseType.ERROR) {
        // Manejo de error
    } else {
        // Validación exitosa
    }
}
```

### Cancelación por Usuario

```kotlin
override fun onCancel() {
    textError.setText(R.string.text_cancelk_by_user)
}
```
