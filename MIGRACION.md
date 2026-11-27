# Migrar la integración Legacy de Android a Maven Central

Integra Become con el número exacto de la [última versión estable](https://github.com/Becomedigital/BecomeDigitalSDKAutDirectPro-Android/releases/latest). Conserva los JWT, el contrato, la licencia de tu aplicación, los permisos y los recursos de localización.

Si ya integrabas una versión candidata mediante Maven, reemplaza la declaración anterior por `ai.becomedigital:identity-verification-aut-direct-pro:<latest-version>` y sustituye `<latest-version>` por el número exacto que consultaste. Conserva una sola dependencia de Become en el módulo para evitar clases duplicadas.

## Retirar las copias locales

1. Retira las declaraciones `implementation files(...)` y las copias locales que agregaste para `becomedigitalsdk.aar`, `capture-core-1.4.1.aar` y `capture-ux-1.4.1.aar`.
2. Retira las dependencias que declaraste exclusivamente para la integración anterior. Conserva las que tu aplicación use directamente y compara sus versiones con la [guía de dependencias](DEPENDENCIAS.md).
3. Conserva `app/src/main/assets/com.become.mb.key`, los permisos y las personalizaciones de tu aplicación.

## Agregar la coordenada exacta

Conserva `google()` y `mavenCentral()` en los repositorios de dependencias. En el módulo de la aplicación, utiliza:

```groovy
dependencies {
    coreLibraryDesugaring 'com.android.tools:desugar_jdk_libs:2.1.5'
    implementation "ai.becomedigital:identity-verification-aut-direct-pro:<latest-version>"
}
```

El POM resuelve las dependencias transitivas. Habilita también `coreLibraryDesugaringEnabled true` en `compileOptions`, como se indica en la [instalación](INSTALACION.md). Las opciones de compilación de tu aplicación se configuran en su módulo.

La [inicialización y los callbacks](README.md#iniciar-una-verificación) conservan sus identificadores públicos. Las reglas de consumidor de R8 se incluyen en el AAR; revisa también las [reglas propias de tu aplicación](docs/R8.md).

## Comprobar la integración

Revisa la versión resuelta y compila las variantes de desarrollo y publicación de tu app. La captura documental está disponible para ARMv7 y ARM64. En un dispositivo físico, prueba la licencia, los permisos, la captura, la validación facial, la cancelación y los resultados.
