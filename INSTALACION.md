# Instalación de la SDK de Become

## Requisitos

| Requisito | Versión o condición |
| --- | --- |
| Versión de Become | `3.5.1-rc.1` |
| Sistema operativo | Android 7.0, nivel de API 24, o posterior |
| Arquitecturas de captura | ARMv7 (`armeabi-v7a`) y ARM64 (`arm64-v8a`) |
| `compileSdk` y `targetSdk` de la integración de referencia | 36 |
| JDK para Gradle | 21 |
| Compatibilidad de Java y Kotlin | 11 |
| Gradle | 9.2.1 |
| Complemento de Android para Gradle | 9.0.1 |
| Kotlin y complemento de Compose | 2.2.10 |
| Licencia de captura | Emitida para el `applicationId` de tu aplicación |

Necesitas un JWT válido obtenido mediante tu backend y el identificador de contrato de tu integración. Esta entrega está preparada para producción; utiliza un token correspondiente a ese ambiente. Consulta la [guía de autenticación de la integración](docs/AUTENTICACION.md). Realiza las pruebas de cámara, documentos y rostro en un dispositivo físico.

## Instalación

La candidata `3.5.1-rc.1` está disponible en [Releases](https://github.com/Becomedigital/BecomeDigitalSDKAutDirectPro-Android/releases/tag/3.5.1-rc.1). Utiliza Maven Central y una versión exacta para integrar esta entrega.

En los repositorios de dependencias de tu proyecto, conserva `google()` y `mavenCentral()`:

```groovy
dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
    }
}
```

Habilita el desazucarado en el módulo de tu aplicación y agrega la versión exacta:

```groovy
android {
    compileOptions {
        coreLibraryDesugaringEnabled true
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
    }
    kotlinOptions { jvmTarget = '11' }
}

dependencies {
    coreLibraryDesugaring 'com.android.tools:desugar_jdk_libs:2.1.5'
    implementation 'ai.becomedigital:identity-verification-legacy:3.5.1-rc.1'
}
```

El POM descarga automáticamente las dependencias requeridas. El desazucarado se habilita en la aplicación porque es una opción de compilación de Android.

Consulta las versiones de las bibliotecas generales con las que se compiló esta entrega en [Dependencias y compatibilidad](DEPENDENCIAS.md). Conserva la configuración pública, los permisos y las credenciales de tu integración.

Si actualizas una integración por archivo, sigue primero la [guía de migración](MIGRACION.md) para retirar las copias locales anteriores.

## Configuración de referencia de Gradle

Si utilizas Android Gradle Plugin 9.0.1 con los complementos externos de Kotlin 2.2.10 del ejemplo, conserva estas opciones en `gradle.properties`:

```properties
android.useAndroidX=true
android.enableJetifier=true
android.builtInKotlin=false
android.newDsl=false
android.uniquePackageNames=false
```

Selecciona JDK 21 para Gradle. Si tu aplicación utiliza Compose, conserva su complemento de compilación compatible con la versión de Kotlin. El [proyecto de ejemplo](examples/compose-demo/README.md) muestra la configuración completa de referencia.

## Licencia y permisos

Agrega la licencia de captura como **`app/src/main/assets/com.become.mb.key`**. El `applicationId` debe coincidir con el autorizado en la licencia.

La SDK incluye las declaraciones de permisos de internet, cámara y ubicación aproximada. Solicita el permiso de cámara antes de iniciar un flujo que la requiera. Si tu contrato utiliza ubicación, su permiso es opcional: rechazarlo no bloquea la verificación.

Continúa con el [ejemplo de inicialización](README.md#iniciar-una-verificación).

## Arquitecturas y emuladores

La dependencia Capture Core 1.4.1 incluye el motor de captura para ARMv7 y ARM64; no incluye una biblioteca nativa `x86_64`. Consulta los [requisitos de arquitectura del proveedor](https://github.com/BlinkID/capture-android#processor-architecture). Una app puede compilar y contener otras bibliotecas para `x86_64` sin que esto habilite la captura documental en esa arquitectura.

Para revisar la integración en un emulador, utiliza una arquitectura ARM compatible con las dependencias de captura. Las pruebas funcionales de cámara, documento y rostro se realizan en un dispositivo físico con la licencia correspondiente a la app.

Si prefieres utilizar los binarios descargables, consulta la [integración manual](INSTALACION_MANUAL.md), que requiere configurar sus dependencias por separado.
