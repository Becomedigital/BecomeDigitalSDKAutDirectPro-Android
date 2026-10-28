# SDK de Become para Android

Integra la verificación de identidad de Become en tu aplicación. La SDK presenta las pantallas de captura y devuelve el resultado mediante objetos que tu aplicación puede consultar.

El [proyecto de ejemplo con Jetpack Compose](examples/compose-demo/README.md) muestra una integración completa desde la pantalla de la aplicación hasta la configuración y las respuestas de la SDK. Para ejecutar una verificación necesitas credenciales y una licencia de captura emitidas para tu contrato y el identificador de tu aplicación.

Puedes iniciar dos flujos:

- **Onboarding:** registro y verificación de una identidad.
- **Authentication:** autenticación de un usuario existente.

Los pasos, documentos admitidos, apariencia y textos de la verificación corresponden al contrato de tu organización.

## Contenido de la guía

- [Requisitos](INSTALACION.md#requisitos)
- [Instalación](INSTALACION.md#instalación)
- [Licencia y permisos](INSTALACION.md#licencia-y-permisos)
- [Iniciar una verificación](#iniciar-una-verificación)
- [Configurar la SDK](#configurar-la-sdk)
- [Consultar el resultado](#consultar-el-resultado)
- [Apariencia e idioma](#apariencia-e-idioma)
- [Ejemplo práctico con Jetpack Compose](#ejemplo-práctico-con-jetpack-compose)
- [Guías complementarias](#guías-complementarias)

## Antes de comenzar

Necesitas una aplicación para Android 7.0 o posterior, las credenciales de tu integración, el identificador del contrato y la licencia de captura correspondiente a tu aplicación. Sigue la [guía de instalación](INSTALACION.md) para agregar la SDK, sus dependencias y permisos.

## Iniciar una verificación

Registra `BecomeInterfaseCallback` antes de iniciar la SDK y conserva `BecomeCallBackManager` mientras el flujo esté activo.

```kotlin
import androidx.appcompat.app.AppCompatActivity
import com.becomedigital.sdk.identity.becomedigitalsdk.core.callback.BecomeCallBackManager
import com.becomedigital.sdk.identity.becomedigitalsdk.core.callback.BecomeInterfaseCallback
import com.becomedigital.sdk.identity.becomedigitalsdk.core.callback.BecomeResponseManager
import com.becomedigital.sdk.identity.becomedigitalsdk.models.BDIVConfig
import com.becomedigital.sdk.identity.becomedigitalsdk.models.BDIdentityVerificationResponse
import com.becomedigital.sdk.identity.becomedigitalsdk.models.DocumetType

class VerificacionActivity : AppCompatActivity() {
    private val callbackManager = BecomeCallBackManager.createNew()

    fun iniciarOnboarding() {
        BecomeResponseManager.getInstance().registerCallback(
            callbackManager,
            object : BecomeInterfaseCallback {
                override fun onFinish(response: BDIdentityVerificationResponse) {
                    if (response.responseStatus != BDIdentityVerificationResponse.StatusType.SUCCES) {
                        // Presenta el estado recibido sin asumir una aprobación.
                        return
                    }
                    response.authentication?.let { resultado ->
                        if (resultado.result) {
                            // Continúa con la autenticación aprobada.
                        } else {
                            // Informa que la autenticación no fue aprobada.
                        }
                    }
                    response.verification?.let { resultado ->
                        val referencia = resultado.urlGetData
                        // Continúa con el onboarding confirmado.
                    }
                    response.onboarding?.let { resultado ->
                        val usuario = resultado.userId
                        // El registro fue creado; no representa una aprobación final.
                    }
                }

                override fun onCancel() {
                    // Recupera la interfaz de tu aplicación.
                }
            }
        )
        val config = BDIVConfig(
            "TU_CLIENT_ID", "TU_CLIENT_SECRET", "TU_CONTRACT_ID",
            arrayOf(DocumetType.DNI, DocumetType.PASSPORT, DocumetType.LICENSE),
            true, "TU_USER_ID"
        )
        config.flow = BDIVConfig.Flow.Onboarding
        config.themeMode = BDIVConfig.ThemeMode.system
        BecomeResponseManager.getInstance().startAuthentication(this, config)
    }
}
```

Utiliza los identificadores `clienId`, `DocumetType`, `BecomeInterfaseCallback` y `SUCCES` exactamente como aparecen en esta guía. El método `startAuthentication` inicia el flujo que hayas elegido en `config.flow`.

### Autenticar a un usuario existente

Antes de iniciar la SDK, configura `config.flow = BDIVConfig.Flow.Authentication` y asigna el `userId` del usuario que deseas autenticar. Puedes indicar `emptyArray()` como lista de documentos cuando el flujo no los requiera. El registro de notificaciones es el mismo del ejemplo anterior.

## Configurar la SDK

Define las opciones mediante el constructor y los métodos de `BDIVConfig` antes de iniciar la verificación.

| Parámetro | Valor predeterminado | Uso |
| --- | --- | --- |
| `clienId`, `clientSecret`, `contractId` | Obligatorios | Credenciales de tu integración e identificador del contrato. No deben estar vacíos. |
| `userId` | Argumento obligatorio | Identificador del usuario. En onboarding puede ser una cadena vacía; en autenticación debe identificar a un usuario existente. |
| `documentTypes` | Argumento obligatorio | Tipos `DNI`, `PASSPORT` y `LICENSE`. Un arreglo vacío utiliza los disponibles en el contrato. |
| `allowLibraryLoading` | Argumento obligatorio | Indica `true` como en el ejemplo. El modo de captura corresponde al contrato. |
| `flow` | `Flow.Onboarding` | Flujo que deseas iniciar: `Onboarding` o `Authentication`. |
| `performVerificationCheck` | `true` | Espera la confirmación del onboarding. Con `false`, devuelve el resultado de creación. |
| `pollingMaxAttempts` | `0` | Número máximo de consultas del resultado. `0` permite seguir esperando sin límite de intentos. |
| `pollingTimeoutSeconds` | `2` segundos | Tiempo máximo de espera por consulta del resultado. No es el tiempo máximo del flujo completo. |
| `debugLogsEnabled` | `false` | Activa los mensajes de diagnóstico para soporte. |
| `preventScreenCapture` | `false` | Activa la protección de las pantallas de la SDK frente a capturas y grabación. |
| `country` | `null` | Código de país de dos letras, como `CO`, o varios códigos separados por comas. |
| `state` | `null` | Código de estado de Estados Unidos, cuando corresponda. |
| `nationalIdType` | `null` | Subtipo de identificación precargado. |
| `nationalIdTypeChoices` | Arreglo vacío | Opciones de subtipo de identificación. |
| `documentNumber` | `null` | Número de documento precargado. |
| `themeMode` | `ThemeMode.system` | Apariencia `light`, `dark` o la preferencia del dispositivo con `system`. |

En Kotlin puedes utilizar las propiedades, por ejemplo `config.themeMode = BDIVConfig.ThemeMode.dark`. En Java, utiliza los métodos, por ejemplo `config.setThemeMode(BDIVConfig.ThemeMode.dark)`.

### Espera del resultado

Con `performVerificationCheck = true`, la SDK mantiene la espera mientras el resultado siga pendiente. Si necesitas limitarla, indica un valor positivo en `pollingMaxAttempts` y atiende el estado de error recibido. Puedes aumentar `pollingTimeoutSeconds` cuando la conexión requiera más tiempo por consulta.

Con `performVerificationCheck = false`, recibirás el resultado de creación sin esperar la confirmación final.

El recurso opcional [`timeOut`](examples/network-config/res/values/become_config.xml), expresado en segundos, configura los tiempos generales de conexión, lectura y escritura; su valor predeterminado es `180`. La espera de cada consulta del resultado se configura por separado con `pollingTimeoutSeconds`.

### Selección de documentos

La SDK combina los tipos solicitados con los admitidos por el contrato. Si no hay coincidencias, utiliza los del contrato. Cuando solo existe un tipo, también lo muestra para que el usuario confirme qué documento va a capturar.

El pasaporte requiere la cara frontal. Los demás documentos solicitan los lados definidos para el contrato. La vista previa puede mostrar un recorte; la verificación utiliza la captura completa. Si el contrato solo requiere documentos, no se exige una captura facial.

## Consultar el resultado

`onFinish` recibe un `BDIdentityVerificationResponse` con `responseStatus`, `message` y objetos opcionales según la operación:

| Propiedad | Tipo | Contenido |
| --- | --- | --- |
| `onboarding` | `BDIVOnboardingResult?` | `code`, `message`, `urlResource`, `userId`. Disponible al devolver la creación sin esperar la confirmación final. |
| `verification` | `BDIVVerificationResult?` | `urlGetData`. Disponible con el resultado confirmado del onboarding. |
| `authentication` | `BDIVAuthenticationResult?` | `company`, `confidence`, `executionId`, `liveness`, `result`, `userId`. Consulta `result` para decidir si la autenticación fue aprobada. |

Consulta cada propiedad de forma opcional. El resultado de creación no implica una aprobación final. En autenticación, recibir `SUCCES` indica que la operación devolvió un resultado; la decisión está en `authentication.result`.

Los estados declarados son `SUCCES`, `ERROR`, `PENDING`, `NOFOUND` y `CANCEL`. El objeto también ofrece `toJson()` si necesitas una representación en texto. La cancelación del usuario se notifica normalmente mediante `onCancel()`.

El contenido de `message` es descriptivo y puede cambiar con el idioma; no lo utilices como código para tomar decisiones. Consulta la [guía de resultados y errores](docs/ERRORES.md).

## Apariencia e idioma

La SDK utiliza el logo, colores, tipografía y textos asociados al contrato. En la aplicación puedes elegir el modo claro, oscuro o del sistema con `themeMode`.

Las indicaciones de captura y algunos mensajes de carga y conexión admiten traducciones locales. Consulta las claves y los ejemplos en la [guía de localización](docs/PERSONALIZACION_TEXTOS.md).

## Ejemplo práctico con Jetpack Compose

El [proyecto de ejemplo](examples/compose-demo/README.md) incluye el permiso de cámara, el administrador de respuestas de la SDK y recursos de localización. Puedes compilarlo sin credenciales para revisar la integración; sigue su guía para agregar tus datos y tu licencia de forma local antes de probar el flujo en un dispositivo físico.

## Guías complementarias

- [Instalación, dependencias, licencia y permisos](INSTALACION.md)
- [Resultados, errores y cancelación](docs/ERRORES.md)
- [Localización y claves disponibles](docs/PERSONALIZACION_TEXTOS.md)
- [Diagnóstico para soporte](docs/LOGGING.md)
- [Protección de pantalla](SCREEN_CAPTURE_CONFIGURATION.md)
- [Preparar la publicación con R8](docs/R8.md)
- [Revisión al actualizar la integración](docs/CAMBIOS.md)

Antes de publicar tu aplicación, comprueba en un dispositivo físico los permisos, la licencia, los documentos solicitados, la cancelación y el manejo del resultado de cada flujo que utilices.
