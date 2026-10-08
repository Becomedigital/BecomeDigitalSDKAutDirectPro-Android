# SDK de Become para Android

## Descripción general

El SDK permite ejecutar procesos de onboarding y autenticación de identidad desde una aplicación Android. El archivo `becomedigitalsdk.aar` debe integrarse junto con las dependencias de AWS Amplify Face Liveness, Microblink Capture y AndroidX indicadas en esta guía.

## Cambios incluidos en esta versión

- Las pantallas de onboarding y authentication se resuelven desde `GET /api/v1/sdk-config`: orden de `flows`, políticas, país, estado de EE. UU. y tipo documental.
- La interfaz Jetpack Compose recibe colores, tipografía, densidad, radios, componentes, logo y textos de `GET /api/v1/public-config`. El host elige únicamente `themeMode` (`light`, `dark` o `system`).
- La selección de país ocupa su propia pantalla, con búsqueda y banderas. La navegación y las acciones permanecen visibles.
- `BDIdentityVerificationResponse` entrega objetos públicos `onboarding`, `authentication` o `verification` según el resultado; ya no expone `responseDictionary`.
- Se conservan el éxito HTTP 201 de `newIdentity`, el polling opcional y los diagnósticos seguros con `debugLogsEnabled`.

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

## Configuración del contrato y presentación

La SDK autentica al cliente y consulta `GET /api/v1/sdk-config` y `GET /api/v1/public-config` para el contrato. `BDIVConfig.Flow.Onboarding` corresponde a `flows.onboarding`; `BDIVConfig.Flow.Authentication`, a `flows.reverification`. El contrato determina los pasos habilitados y su orden, la captura documental y facial, los tipos de documento, la exigencia del reverso y las demás políticas. Un tipo documental único se muestra seleccionado para que el usuario sepa qué capturará. La pantalla de país presenta una lista con búsqueda; cuando corresponde, solicita el estado de EE. UU.

`public-config` define cinco bloques: `theming`, `components`, `branding`, `texts` y `ui`. La SDK aplica la paleta clara u oscura, tipografía, espaciado, radios, alineación, componentes y `branding.logo.url`. El logo se descarga para la ejecución actual sin usar caché. Los colores de texto se ajustan cuando hace falta contraste. Los textos del contrato usan `texts.{locale}.{namespace}.{clave}`; las claves faltantes recurren a `es` y luego a los recursos predeterminados. Los recursos `strings.xml` de la app tienen prioridad para las claves nativas que la app sobrescriba.

El host **no** establece colores, logo, copy del flujo, URL del servicio ni políticas de captura en `BDIVConfig`. `themeMode` es la elección visual del host: `system` es el valor predeterminado y sigue la preferencia del dispositivo. Para elegir una paleta sin cambiar el contrato:

```kotlin
config.themeMode = BDIVConfig.ThemeMode.dark // light, dark o system
```

El parámetro web `webhookUrl` no se envía desde mobile.

## Personalización de textos

Copie las claves que necesite del ejemplo [español](examples/custom-texts/res/values/strings.xml) o [inglés](examples/custom-texts/res/values-b+en/strings.xml) al `strings.xml` de su app. Mantenga sus nombres y personalice cada idioma. Estas claves nativas sobrescriben la frase equivalente del contrato; no hay parámetros de diseño ni de textos en `BDIVConfig`.

[Guía de claves y precedencia](docs/PERSONALIZACION_TEXTOS.md).

## Inicialización

Los nombres públicos `clienId` y `DocumetType` se conservan por compatibilidad. Registre el callback antes de iniciar la SDK y mantenga la referencia a `BecomeCallBackManager` mientras el proceso esté activo.

```kotlin
private val callbackManager = BecomeCallBackManager.createNew()

private fun startOnboarding() {
    BecomeResponseManager.getInstance().registerCallback(
        callbackManager,
        object : BecomeInterfaseCallback {
            override fun onFinish(response: BDIdentityVerificationResponse) {
                when (response.responseStatus) {
                    BDIdentityVerificationResponse.StatusType.SUCCES -> {
                        response.onboarding?.let { accepted ->
                            // newIdentity aceptó la creación cuando el polling está desactivado.
                        }
                        response.verification?.let { checked ->
                            // Resultado del polling; checked.urlGetData es la URL consultada.
                        }
                    }
                    BDIdentityVerificationResponse.StatusType.ERROR -> {
                        // Mostrar una salida segura; no registrar datos personales.
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

### Parámetros que controla la app

| Parámetro | Tipo y valor predeterminado | Uso |
| --- | --- | --- |
| `clienId`, `clientSecret`, `contractId`, `userId` | `String`, requeridos | Credenciales, contrato e identificador del usuario. |
| `documentTypes` | `DocumetType[]`, requerido en onboarding | Acota los documentos del contrato; `DNI`, `PASSPORT` y `LICENSE`. En authentication puede estar vacío. |
| `allowLibraryLoading` | `Boolean`, argumento del constructor | Conserva la opción pública de carga desde galería. |
| `flow` | `Flow.Onboarding` | `Onboarding` o `Authentication`. |
| `performVerificationCheck` | `true` | Espera el resultado de la identidad después de `newIdentity` cuando corresponde. |
| `pollingMaxAttempts` | `0` | Límite de consultas; `0` significa ilimitadas. |
| `pollingTimeoutSeconds` | `2` | Timeout en segundos de cada GET de polling; no altera el intervalo. |
| `debugLogsEnabled` | `false` | Activa diagnósticos seguros antes de iniciar. |
| `preventScreenCapture` | `true` | Bloquea capturas y grabación mientras se muestra la SDK; puede cambiarse con `setPreventScreenCapture(false)`. |
| `country`, `state` | `null` | País ISO de dos letras y, para EE. UU., estado precargado. |
| `nationalIdType`, `nationalIdTypeChoices`, `documentNumber` | `null` / lista vacía | Valores documentales precargados; se aplican junto con las políticas del contrato. |
| `themeMode` | `ThemeMode.system` | Paleta `light`, `dark` o `system` elegida por la app. |

Use los setters de `BDIVConfig` para los campos opcionales. El constructor mínimo recibe seis argumentos; las sobrecargas permiten especificar `performVerificationCheck`, `flow`, intentos, timeout, logs y protección de pantalla. Ninguna sobrecarga acepta `customerLogo` ni colores. Las políticas de `sdk-config` tienen prioridad sobre restricciones incompatibles enviadas por la app.

### Authentication

`Authentication` selecciona `reverification` y, según el contrato, ejecuta liveness y `POST /api/v1/matches`. No exige tipos documentales:

```kotlin
val config = BDIVConfig(
    clientId, clientSecret, contractId,
    emptyArray(), true, userId,
    BDIVConfig.Flow.Authentication
)
```

Un HTTP exitoso de `/matches` produce `StatusType.SUCCES` incluso si `authentication.result == false`: ese booleano es el resultado de negocio y debe evaluarse por separado. Los campos opcionales de `BDIVAuthenticationResult` son `company`, `confidence`, `executionId`, `liveness` y `userId`; `result` es obligatorio.

## Ambientes

Este repositorio distribuye el AAR **release de producción**, que apunta a `https://api.svi.becomedigital.net`. El ambiente está incorporado en el AAR; la app no puede cambiarlo con `BDIVConfig` ni con su propio `BuildConfig`. El repositorio fuente genera `becomedigitalsdk-develop.aar` para pruebas internas contra `https://api.dev.svi.becomedigital.net`; es un artefacto separado y no reemplaza al release de este repositorio.

## Consulta del resultado y objetos de respuesta

En onboarding, `POST /api/v1/newIdentity` se considera exitoso con HTTP 201. Con `performVerificationCheck = false`, `onFinish` entrega `response.onboarding` (`BDIVOnboardingResult`) con `code`, `message`, `urlResource` y `userId`, todos opcionales. Esto indica creación aceptada, no aprobación biométrica final. Con `performVerificationCheck = true`, la SDK conserva el polling existente y al completarlo entrega `response.verification?.urlGetData`.

Las consultas se programan cada 4 segundos. `pollingTimeoutSeconds` controla cada GET y `pollingMaxAttempts` limita el total; `0` conserva intentos ilimitados. Al agotar un límite positivo se muestra un reintento dentro de la SDK. Las respuestas de autenticación llegan en `response.authentication`. Solo se llena el objeto que corresponde al flujo y al modo de respuesta; los otros quedan `null`. `responseStatus` admite `SUCCES`, `ERROR`, `PENDING`, `NOFOUND` y `CANCEL`; `onCancel()` recibe la cancelación habitual.

Para omitir el polling:

```kotlin
val config = BDIVConfig(
    clientId, clientSecret, contractId,
    arrayOf(DocumetType.DNI), true, userId,
    false
)
```

[Catálogo y manejo de errores](docs/ERRORES.md).

## Timeout de carga y servicios

La app puede definir `timeOut` en `app/src/main/res/values/become_config.xml` para el timeout de servicios generales. Ese recurso es distinto de `pollingTimeoutSeconds`. [Archivo de ejemplo](examples/network-config/res/values/become_config.xml):

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <integer name="timeOut">180</integer>
</resources>
```

## Captura documental y permisos

Microblink produce `ImageResult` (imagen completa enviada a `newIdentity`) y `TransformedImageResult` (vista previa recortada). Cada intento usa capturas aisladas y limpia sus archivos al cancelar, reintentar o finalizar. El contrato decide el modo de captura, el reverso y los pasos de liveness. La app debe conceder cámara en tiempo de ejecución cuando el flujo la requiera.

## Logs de diagnóstico

`config.setDebugLogsEnabled(true)` habilita temporalmente los eventos `BecomeSDK` sin registrar credenciales, imágenes ni respuestas JSON completas. El valor predeterminado es `false`. [Guía de diagnóstico](docs/LOGGING.md).

## Generación y reemplazo del AAR

Desde `SDK` del repositorio fuente, genere `:becomedigitalsdk:assembleRelease`. El archivo resultante `becomedigitalsdk/build/outputs/aar/becomedigitalsdk-release.aar` se copia como `becomedigitalsdk.aar` en este repositorio. El release distribuido conserva el ambiente productivo.

## Compatibilidad con Android 15 y páginas de 16 KB

Antes de publicar un APK o AAB dirigido a Android 15 o superior, valide el paquete final y todas sus dependencias nativas con las herramientas de Android Studio y Google Play.

## Procedencia del artefacto

El `becomedigitalsdk.aar` de este repositorio se generó desde `Android_become_sdk` en `feature/mobile-contract-parity` (commit `45d660b`), variante `release` productiva. SHA-256 del AAR: `2749b828c93d279dbd36d464955357e7c46f37901195f32e7db04041e905b8e8`.
