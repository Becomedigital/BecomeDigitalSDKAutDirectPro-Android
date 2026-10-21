# SDK de Become para Android

## Descripción general

The SDK provides native onboarding and identity authentication. Integrate `becomedigitalsdk.aar` with the AWS Amplify Face Liveness, Microblink BlinkID Core/UX, and AndroidX dependencies listed below.

## Funciones públicas

- Flujos de onboarding y autenticación con navegación y presentación adaptadas al contrato.
- Selección de país con búsqueda, captura documental y verificación facial según el flujo disponible.
- Respuestas tipadas mediante `BDIdentityVerificationResponse`.
- Selección del modo visual con `themeMode` y personalización de textos mediante recursos Android.

## Requisitos

| Componente | Versión o valor |
| --- | --- |
| `minSdk` | 24 |
| `compileSdk` | 36 |
| `targetSdk` | 36 recomendado |
| Java | 11 |
| Android Gradle Plugin | 9.0.1 recomendado |
| Kotlin | 2.2.10 recomendado |
| BlinkID Core | 8002.0.0 |
| BlinkID UX | 8002.0.0 |
| Compose BOM | 2026.06.00 |
| Amplify UI Face Liveness | 1.10.0 |
| Amplify AWS Cognito | 2.33.0 |
| CameraX | 1.5.3 |

El proyecto consumidor debe habilitar Compose porque AWS Amplify Face Liveness lo utiliza.

Si utiliza Kotlin 2.x, aplique también el plugin de Compose con la misma versión de Kotlin. Por ejemplo, en la configuración raíz:

```groovy
buildscript {
    ext.kotlin_version = "2.2.10"

    dependencies {
        classpath "com.android.tools.build:gradle:9.0.1"
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
        classpath "org.jetbrains.kotlin:compose-compiler-gradle-plugin:$kotlin_version"
    }
}
```

## Integración del AAR

1. Copie `becomedigitalsdk.aar` en el directorio `app/libs` de la aplicación.
2. Agregue el AAR y sus dependencias externas en el `build.gradle` del módulo de la aplicación.

```groovy
plugins {
    id "com.android.application"
    id "org.jetbrains.kotlin.android"
    id "org.jetbrains.kotlin.plugin.compose"
}

android {
    compileSdk 36

    defaultConfig {
        minSdk 24
        targetSdk 36
    }

    compileOptions {
        coreLibraryDesugaringEnabled true
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
    }

    kotlinOptions {
        jvmTarget = "11"
    }

    buildFeatures {
        compose true
    }
}

dependencies {
    implementation files("libs/becomedigitalsdk.aar")
    implementation platform("androidx.compose:compose-bom:2026.06.00")

    coreLibraryDesugaring "com.android.tools:desugar_jdk_libs:2.1.5"

    implementation "androidx.appcompat:appcompat:1.6.1"
    implementation "androidx.constraintlayout:constraintlayout:2.1.4"
    implementation "androidx.core:core-ktx:1.10.1"
    implementation "androidx.activity:activity-ktx:1.8.2"
    implementation "androidx.fragment:fragment-ktx:1.6.2"
    implementation "androidx.navigation:navigation-fragment:2.5.3"
    implementation "androidx.navigation:navigation-ui:2.5.3"

    implementation "androidx.camera:camera-core:1.5.3"
    implementation "androidx.camera:camera-camera2:1.5.3"
    implementation "androidx.camera:camera-view:1.5.3"
    implementation "androidx.camera:camera-lifecycle:1.5.3"
    implementation "com.google.guava:guava:33.3.1-android"

    implementation "com.google.code.gson:gson:2.10.1"
    implementation "com.squareup.okhttp3:okhttp:4.9.3"
    implementation "com.android.volley:volley:1.2.1"
    implementation "com.github.bumptech.glide:glide:4.10.0"

    implementation "com.amplifyframework.ui:liveness:1.10.0"
    implementation "com.amplifyframework:aws-auth-cognito:2.33.0"
    implementation "androidx.compose.material3:material3"
    implementation "androidx.activity:activity-compose:1.7.2"

    implementation "com.microblink:blinkid-core:8002.0.0"
    implementation "com.microblink:blinkid-ux:8002.0.0"

    implementation "androidx.room:room-runtime:2.6.1"
    implementation "androidx.lifecycle:lifecycle-livedata:2.8.7"
    implementation "androidx.lifecycle:lifecycle-viewmodel:2.8.7"
}
```

> Evite declarar una segunda versión de estas dependencias. Si la aplicación ya las utiliza, resuelva la versión de forma explícita y valide el flujo completo.

Resolve dependencies from `google()` and `mavenCentral()`. A local AAR does not carry Gradle dependency metadata, so the application must declare the dependencies above. Keep Compose UI, runtime, and Material 3 aligned with the indicated BOM. When upgrading, remove the previous `capture-core` and `capture-ux` dependencies.

### Document capture

Automatic document capture includes framing, image quality guidance, and instructions for scanning the other side when required. If automatic capture does not finish, a manual capture button becomes available after 30 seconds by default. Manual photographs retain document recognition, and the user can retry an invalid capture.

## Licencia y permisos

Add the BlinkID Core license as `app/src/main/assets/com.become.blinkid.key`. The application's `applicationId` must match the license. Keep the license contents out of source control. A development app with a different `applicationId` requires its own valid license.

El AAR declara los permisos de Internet y cámara. La aplicación debe solicitar el permiso de cámara en tiempo de ejecución antes de iniciar un flujo que la necesite.

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.CAMERA" />
```

## Configuración y personalización

La app selecciona `Flow.Onboarding` o `Flow.Authentication`. La SDK presenta los pasos y la identidad visual asignados al contrato. `themeMode` permite escoger `light`, `dark` o `system`; el valor predeterminado sigue el modo del dispositivo. Colores, logo, contenido y diseño no se configuran en `BDIVConfig`.

Para sobrescribir frases visibles en su app, copie las claves necesarias a `strings.xml`. Consulte la [guía de personalización](docs/PERSONALIZACION_TEXTOS.md).

## Inicialización

Los nombres públicos `clienId` y `DocumetType` se conservan por compatibilidad. Registre el callback antes de iniciar la SDK y conserve `BecomeCallBackManager` durante el proceso.

```kotlin
private val callbackManager = BecomeCallBackManager.createNew()

private fun startOnboarding() {
    BecomeResponseManager.getInstance().registerCallback(
        callbackManager,
        object : BecomeInterfaseCallback {
            override fun onFinish(response: BDIdentityVerificationResponse) {
                when (response.responseStatus) {
                    BDIdentityVerificationResponse.StatusType.SUCCES -> {
                        response.onboarding?.let { /* Inicio registrado. */ }
                        response.verification?.let { /* Resultado final disponible. */ }
                        response.authentication?.let { /* Revisar it.result. */ }
                    }
                    BDIdentityVerificationResponse.StatusType.ERROR -> {
                        // Restaurar la app y ofrecer una nueva acción.
                    }
                    else -> Unit
                }
            }

            override fun onCancel() {
                // Restaurar la pantalla de la app.
            }
        }
    )

    val config = BDIVConfig(
        "TU_CLIENT_ID", "TU_CLIENT_SECRET", "TU_CONTRACT_ID",
        arrayOf(DocumetType.DNI, DocumetType.PASSPORT),
        true, "TU_USER_ID"
    )
    config.themeMode = BDIVConfig.ThemeMode.system
    BecomeResponseManager.getInstance().startAuthentication(this, config)
}
```

### Parámetros públicos

| Parámetro | Predeterminado | Uso |
| --- | --- | --- |
| `clienId`, `clientSecret`, `contractId`, `userId` | Requeridos | Identifican al cliente, contrato y usuario. |
| `documentTypes` | Requerido en onboarding | `DocumetType[]`; admite `DNI`, `PASSPORT` y `LICENSE`. En autenticación puede estar vacío. |
| `allowLibraryLoading` | Argumento del constructor | Habilita la opción pública de selección desde galería. |
| `flow` | `Flow.Onboarding` | `Onboarding` o `Authentication`. |
| `performVerificationCheck` | `true` | Espera el resultado final de onboarding antes de devolverlo. |
| `pollingMaxAttempts` | `0` | Límite de intentos de espera; `0` no establece límite. |
| `pollingTimeoutSeconds` | `2` | Tiempo máximo en segundos para cada intento de espera. |
| `debugLogsEnabled` | `false` | Activa diagnósticos durante una prueba. |
| `preventScreenCapture` | `false` | Protege el contenido mostrado por la SDK cuando es `true`. |
| `country`, `state` | `null` | País de dos letras y estado precargado para EE. UU. |
| `nationalIdType`, `nationalIdTypeChoices`, `documentNumber` | Vacíos | Datos documentales precargados, si corresponden. |
| `themeMode` | `ThemeMode.system` | Modo visual de la app. |

Los campos opcionales se establecen con los setters de `BDIVConfig`. Para autenticación use `Flow.Authentication` y, si no corresponde capturar documentos, `emptyArray()`.

Para habilitar la protección de capturas de pantalla y grabaciones, consulte la [guía de capturas](SCREEN_CAPTURE_CONFIGURATION.md).

## Respuestas

`onFinish` entrega `BDIdentityVerificationResponse`, con `responseStatus`, `message` y estos objetos opcionales:

| Objeto | Campos públicos | Cuándo consultarlo |
| --- | --- | --- |
| `onboarding` | `code`, `message`, `urlResource`, `userId` | Onboarding con `performVerificationCheck=false`; indica que se inició el proceso, no que haya sido aprobado. |
| `verification` | `urlGetData` | Onboarding con espera del resultado final. |
| `authentication` | `company`, `confidence`, `executionId`, `liveness`, `result`, `userId` | Autenticación. Evalúe `result` por separado de `responseStatus`. |

`responseStatus` puede ser `SUCCES`, `ERROR`, `PENDING`, `NOFOUND` o `CANCEL`. La cancelación habitual se recibe en `onCancel()`. Consulte [manejo de errores](docs/ERRORES.md). Cuando el contrato solo solicita captura documental, el resultado final se confirma con la aprobación del documento; no se exige un resultado facial.

## Diagnóstico y compatibilidad

`config.setDebugLogsEnabled(true)` habilita diagnósticos para una prueba; desactívelos al terminar. [Guía de logs](docs/LOGGING.md).

Si necesita ajustar el tiempo de espera general desde la app, consulte el [recurso de ejemplo](examples/network-config/res/values/become_config.xml).

Antes de publicar en Android 15 o posterior, valide el paquete final y sus dependencias nativas con Android Studio y Google Play.
