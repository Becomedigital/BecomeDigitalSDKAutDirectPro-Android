# Activar logs — Android

Establezca el parámetro en su `BDIVConfig` antes de iniciar la SDK.

Kotlin:

```kotlin
config.isDebugLogsEnabled = true
BecomeResponseManager.getInstance().startAuthentication(activity, config)
```

Java:

```java
config.setDebugLogsEnabled(true);
BecomeResponseManager.getInstance().startAuthentication(activity, config);
```

Para desactivarlos, cambie `true` por `false` o no establezca el parámetro. No necesita modificar `BuildConfig.LOG_ENABLED`.

En Logcat, seleccione su dispositivo y filtre por `tag:BecomeSDK level:DEBUG`. Por terminal:

```sh
adb logcat -v threadtime 'BecomeSDK:D' '*:S'
```
## Uso

El valor predeterminado es `false`, también en Release/PROD. Active los logs solo para una prueba y vuelva a desactivarlos al terminar. No cambian el flujo, los tiempos de espera ni los resultados.

## Qué permiten revisar

Muestran el paso del proceso, el estado HTTP, los tiempos y la categoría del error, incluidos captura, prueba de vida, `newIdentity`, consulta de resultados y cierre.

No imprimen credenciales, datos personales, imágenes ni respuestas JSON completas. El parámetro solo controla los logs de Become, no los de la app, el sistema operativo, Microblink o Amplify.

Para soporte, comparta las líneas `BecomeSDK` de la prueba junto con la versión de la SDK y los pasos para reproducir el problema.
