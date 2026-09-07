# SDK de Become para Android

## Descripción general

El SDK permite ejecutar procesos de onboarding y autenticación de identidad desde una aplicación Android. El archivo `becomedigitalsdk.aar` debe integrarse junto con las dependencias de AWS Amplify Face Liveness, Microblink Capture y AndroidX indicadas en esta guía.

## Cambios incluidos en esta versión

- Selección de flujo mediante `flow`: `BDIVConfig.Flow.Onboarding` o `BDIVConfig.Flow.Authentication`.
- Control opcional de la consulta del resultado final con `performVerificationCheck`.
- Configuración del número máximo de consultas mediante `pollingMaxAttempts`.
- Configuración del timeout de cada consulta mediante `pollingTimeoutSeconds`.
- Envío al servicio de las capturas completas del documento; la imagen recortada por Microblink se conserva únicamente para la vista previa.
- Aislamiento y limpieza de los archivos de cada captura para evitar que un reintento reutilice imágenes de un intento anterior.
- `responseDictionary` ahora es nullable en `BDIdentityVerificationResponse`.
- Cuando `newIdentity` informa que no se superó la prueba de vida, el botón de reintento cierra el SDK y retorna un resultado con estado `ERROR`. La aplicación debe iniciar un proceso nuevo.
- Los logs internos están deshabilitados en el AAR de tipo `release`.

## Requisitos

| Componente | Versión o valor |
| --- | --- |
| `minSdk` | 24 |
| `compileSdk` | 36 |
| `targetSdk` | 36 recomendado |
| Java | 11 |
| Android Gradle Plugin | 9.0.1 recomendado |
| Kotlin | 2.2.10 recomendado |
| Microblink Capture Core | 1.4.2 |
| Microblink Capture UX | 1.4.2 |
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

    implementation "com.google.code.gson:gson:2.10.1"
    implementation "com.squareup.okhttp3:okhttp:4.9.3"
    implementation "com.android.volley:volley:1.2.1"
    implementation "com.github.bumptech.glide:glide:4.10.0"

    implementation "com.amplifyframework.ui:liveness:1.10.0"
    implementation "com.amplifyframework:aws-auth-cognito:2.33.0"
    implementation "androidx.compose.material3:material3:1.4.0"
    implementation "androidx.activity:activity-compose:1.7.2"

    implementation "com.microblink:capture-core:1.4.2"
    implementation "com.microblink:capture-ux:1.4.2"

    implementation "androidx.room:room-runtime:2.6.1"
    implementation "androidx.lifecycle:lifecycle-livedata:2.8.7"
    implementation "androidx.lifecycle:lifecycle-viewmodel:2.8.7"
}
```

> Evite declarar una segunda versión de estas dependencias. Si la aplicación ya las utiliza, resuelva la versión de forma explícita y valide el flujo completo.

## Licencia y permisos

Incluya el archivo de licencia `com.become.mb.key` en `app/src/main/assets`. El `applicationId` debe coincidir con el autorizado en la licencia.

El AAR declara los permisos de Internet y cámara. La aplicación debe solicitar el permiso de cámara en tiempo de ejecución antes de iniciar un flujo que la necesite.

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.CAMERA" />
```

## Inicialización

El API conserva los nombres públicos `clienId` y `DocumetType` por compatibilidad. Los tipos de documento disponibles son `DNI`, `PASSPORT` y `LICENSE`.

```kotlin
private val callbackManager = BecomeCallBackManager.createNew()

private fun configureBecomeSdk() {
    BecomeResponseManager.getInstance().registerCallback(
        callbackManager,
        object : BecomeInterfaseCallback {
            override fun onFinish(response: BDIdentityVerificationResponse) {
                when (response.responseStatus) {
                    BDIdentityVerificationResponse.StatusType.SUCCES -> {
                        Log.d("BecomeSDK", response.toJson().orEmpty())
                    }

                    BDIdentityVerificationResponse.StatusType.ERROR -> {
                        Log.e("BecomeSDK", response.message)
                    }

                    else -> {
                        Log.d("BecomeSDK", response.toJson().orEmpty())
                    }
                }
            }

            override fun onCancel() {
                Log.d("BecomeSDK", "Proceso cancelado por el usuario")
            }
        }
    )
}

private fun startOnboarding() {
    val config = BDIVConfig(
        "TU_CLIENT_ID",
        "TU_CLIENT_SECRET",
        "TU_CONTRACT_ID",
        arrayOf(DocumetType.DNI, DocumetType.PASSPORT, DocumetType.LICENSE),
        true,
        "TU_USER_ID",
        null,
        true,
        BDIVConfig.Flow.Onboarding,
        0,
        2
    )

    BecomeResponseManager.getInstance().startAuthentication(this, config)
}
```

Registre el callback antes de llamar a `startAuthentication` y mantenga una referencia a `BecomeCallBackManager` mientras el proceso esté activo.

## Parámetros de `BDIVConfig`

| Posición | Parámetro | Tipo | Predeterminado | Descripción |
| --- | --- | --- | --- | --- |
| 1 | `clienId` | `String` | Requerido | Identificador entregado al cliente. |
| 2 | `clientSecret` | `String` | Requerido | Credencial secreta del cliente. |
| 3 | `contractId` | `String` | Requerido | Contrato asociado al proceso. |
| 4 | `documentTypes` | `DocumetType[]` | Requerido en onboarding | Documentos habilitados: `DNI`, `PASSPORT` y `LICENSE`. |
| 5 | `allowLibraryLoading` | `Boolean` | Requerido | Conserva la opción pública de carga de librerías. |
| 6 | `userId` | `String` | Requerido | Identificador único del usuario. |
| 7 | `customerLogo` | `ByteArray?` | `null` | Logo personalizado del cliente. |
| 8 | `performVerificationCheck` | `Boolean` | `true` | Si es `true`, consulta el resultado final; si es `false`, retorna la respuesta decodificada de `POST /api/v1/newIdentity`. |
| 9 | `flow` | `BDIVConfig.Flow` | `Onboarding` | Selecciona el flujo completo o solo autenticación facial. Un valor `null` se normaliza a `Onboarding`. |
| 10 | `pollingMaxAttempts` | `Int` | `0` | Máximo de consultas del resultado. `0` significa ilimitado; los valores negativos se normalizan a `0`. |
| 11 | `pollingTimeoutSeconds` | `Int` | `2` | Timeout en segundos para cada GET de resultados. Un valor menor o igual a cero se normaliza a `2`. |

Los constructores anteriores de 7 parámetros siguen disponibles y conservan el comportamiento predeterminado: onboarding, consulta del resultado, intentos ilimitados y timeout de 2 segundos por GET.

## Tipos de flujo

### Onboarding

Ejecuta la captura de documento, prueba de vida, creación de identidad y, cuando `performVerificationCheck` es `true`, la consulta del resultado.

```kotlin
val onboardingConfig = BDIVConfig(
    clientId,
    clientSecret,
    contractId,
    arrayOf(DocumetType.DNI, DocumetType.PASSPORT),
    true,
    userId,
    null,
    true,
    BDIVConfig.Flow.Onboarding,
    30,
    5
)
```

### Authentication

Omite el onboarding y la validación de verificaciones anteriores. Ejecuta únicamente la prueba de vida y la autenticación facial mediante `POST /api/v1/matches`. `documentTypes` puede enviarse vacío porque este flujo no captura documentos.

```kotlin
val authenticationConfig = BDIVConfig(
    clientId,
    clientSecret,
    contractId,
    emptyArray(),
    true,
    userId,
    null,
    BDIVConfig.Flow.Authentication
)
```

## Consulta del resultado y polling

Con `performVerificationCheck = true`, el SDK consulta la URL `url_resource` retornada por `POST /api/v1/newIdentity`. Si debe usar el fallback, consulta `GET /api/v1/identity/<user_id>`.

Las consultas se programan cada 4 segundos. `pollingTimeoutSeconds` controla el timeout individual de cada GET y no modifica ese intervalo. Si `pollingMaxAttempts` es mayor que cero, al agotarse los intentos el SDK retorna el error de timeout. El valor predeterminado `0` conserva el polling ilimitado.

Con `performVerificationCheck = false`, no se inicia el polling. El SDK decodifica la respuesta documentada de `newIdentity` y la retorna en `responseDictionary`.

```kotlin
val configWithoutPolling = BDIVConfig(
    clientId,
    clientSecret,
    contractId,
    arrayOf(DocumetType.DNI),
    true,
    userId,
    null,
    false
)
```

## Manejo de respuestas

`BDIdentityVerificationResponse` contiene:

| Propiedad | Tipo | Descripción |
| --- | --- | --- |
| `message` | `String` | Mensaje descriptivo del resultado. |
| `responseDictionary` | `Map<String, Any>?` | Datos adicionales cuando existen. Es nullable y debe consumirse de forma segura. |
| `responseStatus` | `StatusType` | `SUCCES`, `ERROR`, `PENDING`, `NOFOUND` o `CANCEL`. El nombre `SUCCES` se conserva por compatibilidad. |

```kotlin
override fun onFinish(response: BDIdentityVerificationResponse) {
    if (response.responseStatus == BDIdentityVerificationResponse.StatusType.ERROR) {
        showError(response.message)
        return
    }

    response.responseDictionary?.let { values ->
        // Consumir únicamente las claves requeridas por la aplicación.
        Log.d("BecomeSDK", values.keys.joinToString())
    }
}
```

Cuando `performVerificationCheck = false`, la respuesta exitosa de `newIdentity` puede incluir las claves `code`, `message`, `url_resource` y `user_id`. No use `!!` sobre `responseDictionary`, ya que otros resultados válidos pueden retornarlo como `null`.

Si el backend indica que no se superó la prueba de vida, el reintento no reutiliza la identidad actual: el SDK cierra el flujo y entrega `StatusType.ERROR` con el mensaje recibido. La aplicación debe crear una nueva ejecución con `startAuthentication`.

## Captura documental

Microblink produce dos representaciones de cada lado del documento:

- `ImageResult`: frame completo de la cámara. Es la imagen enviada por el SDK a `newIdentity`.
- `TransformedImageResult`: documento recortado y corregido en perspectiva. Se usa solamente para la vista previa.

Cada intento crea un identificador de captura independiente. Al cancelar, reintentar o finalizar el flujo, el SDK limpia las rutas anteriores para evitar mostrar o enviar una captura previa.

## Generación y reemplazo del AAR

Desde el directorio `SDK` del repositorio fuente:

```bash
GRADLE_USER_HOME=$PWD/.gradle \
JAVA_TOOL_OPTIONS='-Djava.net.useSystemProxies=false -Dhttp.proxyHost= -Dhttp.proxyPort= -Dhttps.proxyHost= -Dhttps.proxyPort=' \
./gradlew --no-daemon :becomedigitalsdk:clean :becomedigitalsdk:assembleRelease
```

El artefacto se genera en:

```text
becomedigitalsdk/build/outputs/aar/becomedigitalsdk-release.aar
```

Copie ese archivo como `becomedigitalsdk.aar` en este repositorio y en `ClientDemo/app/libs`. Antes de distribuirlo, valide que corresponda al build `release`; en esta variante `BuildConfig.LOG_ENABLED` debe ser `false`.

## Compatibilidad con Android 15 y páginas de 16 KB

El AAR contiene librerías nativas para `armeabi-v7a`, `arm64-v8a`, `x86` y `x86_64`. Antes de publicar un APK o AAB dirigido a Android 15 o superior, valide el paquete final con las herramientas de Android Studio y Google Play para confirmar la compatibilidad de todas las dependencias nativas con páginas de 16 KB.
