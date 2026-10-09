# Diagnóstico — Android

Para una prueba, active el parámetro antes de iniciar la SDK:

```kotlin
config.setDebugLogsEnabled(true)
BecomeResponseManager.getInstance().startAuthentication(activity, config)
```

En Java, use también `config.setDebugLogsEnabled(true)`. El valor predeterminado es `false`; vuelva a desactivarlo al terminar.

En Logcat, filtre por `tag:BecomeSDK level:DEBUG`. Por terminal:

```sh
adb logcat -v threadtime 'BecomeSDK:D' '*:S'
```

Para solicitar soporte, indique la versión de la SDK, el dispositivo, el paso visible y las líneas relevantes de `BecomeSDK`. Revise cualquier registro antes de compartirlo para excluir información personal.
