# Ejemplo de integración con Compose

Este proyecto muestra cómo iniciar la SDK de Become desde una pantalla Compose: solicita el permiso de cámara, configura la verificación y presenta su resultado o cancelación.

## Preparar la aplicación

1. Sigue los requisitos y dependencias de la [guía de instalación](../../INSTALACION.md). Utiliza JDK 21 para esta configuración.
2. Copia `credentials.example.properties` como `credentials.properties` y completa `applicationId` y `contractId` con los datos de tu integración. El archivo local está excluido de Git.
3. Agrega la licencia emitida para ese identificador como `app/src/main/assets/com.become.mb.key`. Cada identificador de aplicación requiere su propia licencia.
4. Abre esta carpeta en Android Studio y genera la aplicación. En un dispositivo físico, ingresa un JWT válido obtenido mediante tu backend y el identificador del usuario; luego inicia el onboarding. Entrega el JWT sin el prefijo `Bearer `. Consulta la [guía de autenticación](../../docs/AUTENTICACION.md).

El ejemplo utiliza el archivo `becomedigitalsdk.aar` y los dos AAR de Capture Core/UX **1.4.1** incluidos en este repositorio. Mantén estos archivos actualizados en conjunto. Incluye los ajustes de AppCompat **1.7.1** necesarios para esta entrega.

El proyecto puede compilar sin configuración local ni licencia; para completar una verificación necesita los valores válidos de tu integración. Si falta alguno, muestra un mensaje antes de solicitar la cámara. No incluyas tokens ni archivos de licencia al compartir el proyecto.

El JWT se ingresa en un campo oculto y su valor se mantiene en la memoria de la pantalla. No se guarda al recrear esa pantalla, no se incorpora en `BuildConfig` y no se registra en mensajes. Este ejemplo no obtiene ni renueva el token; tu integración debe suministrarlo mediante su backend. Para probar un token diferente, inicia de nuevo con el valor vigente.

## Idioma y diagnóstico

La pantalla de ejemplo y las instrucciones de captura incluyen recursos en español e inglés. Consulta las [claves de localización](../../docs/PERSONALIZACION_TEXTOS.md) para personalizar solo los textos que necesites.

El ejemplo activa `debugLogsEnabled` para facilitar el soporte. Revisa los mensajes antes de compartirlos y desactiva la opción al terminar tus pruebas, según la [guía de diagnóstico](../../docs/LOGGING.md).

## Prueba de integración

Comprueba en un dispositivo físico el permiso de cámara, los lados del documento, la alternativa manual, la revisión de las imágenes, la cancelación y la recepción del resultado. Utiliza también la versión de publicación de tu aplicación al realizar esta comprobación.
