# Resultados, errores y cancelación en Android

Registra `BecomeInterfaseCallback` antes de iniciar una verificación y conserva `BecomeCallBackManager` mientras el flujo esté activo.

## Qué recibe tu aplicación

| Notificación | Cómo atenderla |
| --- | --- |
| `onFinish(response)` con `SUCCES` | Consulta el objeto opcional correspondiente al flujo. En autenticación, evalúa también `authentication.result`. |
| `onFinish(response)` con `ERROR` | Recupera la interfaz de tu aplicación y permite un nuevo intento si corresponde. |
| Estado `PENDING` o `NOFOUND` | El resultado no representa una aprobación. |
| `onCancel()` o estado `CANCEL` | Regresa a tu aplicación sin marcar la verificación como aprobada. |

`onboarding`, `verification` y `authentication` pueden ser `null`. Los estados y los campos disponibles se describen en la [guía de integración](../README.md#consultar-el-resultado).

Si elegiste `performVerificationCheck = false`, `onboarding` confirma la creación del registro, no su aprobación final. Cuando esperas la confirmación, consulta `verification`. Para autenticación, la decisión está en el booleano `authentication.result`.

## Reintentos durante la captura

La SDK presenta las opciones de revisión y reintento disponibles para el usuario. Tu aplicación recibe la notificación al terminar o cancelar el flujo; no recibe una notificación por cada intento de captura.

## Resolver problemas de integración

| Situación | Qué revisar |
| --- | --- |
| No inicia la verificación | JWT e identificador de contrato no vacíos. Si aún utilizas la firma deprecada, revisa `clienId` y `clientSecret`. En autenticación, indica un `userId` existente. |
| El JWT fue rechazado o perdió vigencia | Obtén un nuevo token mediante tu backend antes de reiniciar la SDK. No reutilices el token rechazado. |
| Creación correcta y HTTP 403 al consultar | Comprueba `jwt` con permiso de creación y `verificationResultsJwt` con permiso de consulta. Cambiar solo el token principal a `verification:get` deja sin cubrir la creación. Revisa vigencia, ambiente y contrato; consulta la [guía de autenticación](AUTENTICACION.md#creación-correcta-y-consulta-con-http-403). |
| No se abre la cámara | Dispositivo físico y permiso de cámara concedido. |
| No se habilita la captura de documento | Archivo `app/src/main/assets/com.become.mb.key` y coincidencia del `applicationId` con la licencia. |
| Falta una clase o recurso al integrar | Los tres archivos AAR y las dependencias indicadas en [Instalación](../INSTALACION.md#instalación). |
| La conexión se interrumpe | Recuperar la conectividad y permitir que el usuario vuelva a intentarlo. |
| Se agota la espera del resultado | Revisar `pollingTimeoutSeconds` y `pollingMaxAttempts` según el comportamiento que necesita tu aplicación. |
| El problema aparece solo al publicar | Revisar la [configuración de R8](R8.md) y probar la versión de publicación en un dispositivo físico. |
| Se solicita repetir el documento o el rostro | Seguir las indicaciones de la pantalla y permitir una nueva captura. |

## Información para soporte

Comparte la versión de la SDK, el modelo del dispositivo, la versión de Android, el paso visible y una descripción del problema. Si habilitaste el [diagnóstico](LOGGING.md), agrega únicamente las líneas relevantes, después de revisar que no contengan datos personales ni credenciales.

No utilices el texto de `message` para decidir una aprobación o iniciar reintentos automáticos. Es un mensaje descriptivo y puede variar según el idioma.
