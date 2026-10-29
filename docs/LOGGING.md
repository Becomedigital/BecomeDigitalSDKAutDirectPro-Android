# Diagnóstico para soporte en Android

Activa `debugLogsEnabled` cuando necesites recopilar información para revisar una incidencia de integración. Su valor predeterminado es `false`.

```kotlin
config.setDebugLogsEnabled(true)
BecomeResponseManager.getInstance().startAuthentication(activity, config)
```

En Java, utiliza también `config.setDebugLogsEnabled(true)` antes de iniciar la SDK.

En Logcat de Android Studio, filtra por la etiqueta `BecomeSDK` y habilita el nivel **Debug**. Para soporte, indica la versión de la SDK, el dispositivo, la versión de Android y el paso donde ocurrió el problema.

Comparte solo los mensajes relevantes y revisa su contenido antes de enviarlos. No incluyas JWT, credenciales, licencias, imágenes ni datos personales.

Al terminar, desactiva la opción con `config.setDebugLogsEnabled(false)` antes de iniciar una nueva verificación.
