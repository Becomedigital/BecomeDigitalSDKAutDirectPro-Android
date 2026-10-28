# Ejemplo de integración con Jetpack Compose

Este proyecto muestra cómo una pantalla de Compose inicia la SDK de Android distribuida mediante una `AppCompatActivity`. `BecomeComposeScreen` recibe el identificador de usuario y solicita el permiso de cámara. `BecomeComposeLauncher` conserva el administrador de respuestas, configura `BDIVConfig` y comunica la finalización o cancelación a la pantalla de Compose.

El repositorio no incluye credenciales de cliente ni licencia de captura para este ejemplo. Para completar una verificación necesitas un contrato con Become, las credenciales de ese contrato y una licencia emitida para el identificador de tu aplicación. Sin estos datos, el ejemplo compila y muestra un aviso de configuración faltante antes de solicitar el permiso de cámara.

## Preparar la aplicación local

1. Lee la [guía de instalación](../../INSTALACION.md). Utiliza JDK 21 y Android 7.0 o posterior.
2. Copia `credentials.example.properties` como `credentials.properties`. Completa `applicationId`, `clientId`, `clientSecret` y `contractId` con los valores entregados para tu integración. El archivo real está excluido de Git. El identificador de la aplicación debe coincidir con la licencia de captura; si dejas `applicationId` vacío, el proyecto utiliza un identificador de ejemplo que no está autorizado para verificar identidades.
3. Coloca la licencia emitida para ese identificador en `app/src/main/assets/com.become.mb.key`. El archivo de licencia está excluido de Git.
4. Abre esta carpeta en Android Studio, selecciona JDK 21 para Gradle y compila el módulo `app`. En un dispositivo Android físico, ingresa un identificador de usuario y toca **Iniciar verificación**.

La aplicación referencia directamente `becomedigitalsdk.aar` y los dos AAR de Capture de este repositorio. El ejemplo no contiene copias de esos binarios. Las versiones de Gradle, los complementos y las dependencias corresponden a la [guía de instalación](../../INSTALACION.md). Las variantes Debug y Release utilizan la SDK de producción; cambiar la variante no cambia su ambiente.

`BDIVConfig.debugLogsEnabled` está activado para generar mensajes de diagnóstico. Los registros de una prueba pueden contener información personal. Los recursos en inglés y español muestran cómo traducir la pantalla de la aplicación y los textos nativos compatibles. La [guía de localización](../../docs/PERSONALIZACION_TEXTOS.md) explica cuáles textos del flujo provienen del contrato. Consulta también la [guía de registros](../../docs/LOGGING.md).

La captura de documentos y la validación facial requieren un dispositivo físico y datos válidos de integración. Una compilación correcta solo confirma que el código y los recursos se empaquetan. No agregues a Git `credentials.properties`, la licencia ni un APK o AAB compilado.
