# Instalación de la SDK de Become

## Requisitos

| Requisito | Versión o condición |
| --- | --- |
| Sistema operativo | Android 7.0, nivel de API 24, o posterior |
| `compileSdk` y `targetSdk` de la integración de referencia | 36 |
| JDK para Gradle | 21 |
| Compatibilidad de Java y Kotlin | 11 |
| Gradle | 9.2.1 |
| Complemento de Android para Gradle | 9.0.1 |
| Kotlin y complemento de Compose | 2.2.10 |
| Capture Core y Capture UX incluidos | 1.2.0 |
| Licencia de captura | Emitida para el `applicationId` de tu aplicación |

Necesitas las credenciales y el identificador de contrato entregados por Become. Esta entrega está preparada para producción. Realiza las pruebas de cámara, documentos y rostro en un dispositivo físico.

## Instalación

### Agregar los archivos

Copia los siguientes archivos a `app/libs`:

- [`becomedigitalsdk.aar`](becomedigitalsdk.aar)
- [`capture-core-1.2.0.aar`](libs/capture-core-1.2.0.aar)
- [`capture-ux-1.2.0.aar`](libs/capture-ux-1.2.0.aar)

Incluye también las dependencias de los ejemplos siguientes, aunque tu contrato no solicite captura facial. Si ya utilizas alguna en tu aplicación, mantén una única versión compatible con esta entrega.

### Configuración del proyecto

En el archivo `build.gradle` del proyecto:

```groovy
buildscript {
    ext.kotlin_version = "2.2.10"
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
    dependencies {
        classpath "com.android.tools.build:gradle:9.0.1"
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
        classpath "org.jetbrains.kotlin:compose-compiler-gradle-plugin:$kotlin_version"
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
```

En `gradle.properties`, utiliza esta configuración para el ejemplo de integración:

```properties
android.useAndroidX=true
android.enableJetifier=true
android.builtInKotlin=false
android.newDsl=false
android.uniquePackageNames=false
```

### Configuración de la aplicación

En `app/build.gradle`, reemplaza `TU_APPLICATION_ID` por el identificador autorizado en tu licencia:

```groovy
plugins {
    id "com.android.application"
    id "org.jetbrains.kotlin.android"
    id "org.jetbrains.kotlin.plugin.compose"
}

android {
    namespace "com.ejemplo.verificacion"
    compileSdk 36
    defaultConfig {
        applicationId "TU_APPLICATION_ID"
        minSdk 24
        targetSdk 36
    }
    compileOptions {
        coreLibraryDesugaringEnabled true
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
    }
    kotlinOptions { jvmTarget = "11" }
    buildFeatures {
        compose true
        viewBinding true
    }
    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'),
                'proguard-rules.pro'
        }
    }
}

dependencies {
    implementation files("libs/becomedigitalsdk.aar")
    implementation files("libs/capture-core-1.2.0.aar")
    implementation files("libs/capture-ux-1.2.0.aar")
    implementation platform("androidx.compose:compose-bom:2026.06.00")
    coreLibraryDesugaring "com.android.tools:desugar_jdk_libs:2.1.5"

    implementation "androidx.appcompat:appcompat:1.6.1"
    implementation "androidx.constraintlayout:constraintlayout:2.1.4"
    implementation "androidx.core:core-ktx:1.15.0"
    implementation "androidx.activity:activity-ktx:1.12.4"
    implementation "androidx.activity:activity-compose:1.12.4"
    implementation "androidx.fragment:fragment-ktx:1.6.2"
    implementation "androidx.navigation:navigation-fragment:2.5.3"
    implementation "androidx.navigation:navigation-ui:2.5.3"
    implementation "androidx.compose.material3:material3"

    implementation "androidx.camera:camera-core:1.5.3"
    implementation "androidx.camera:camera-camera2:1.5.3"
    implementation "androidx.camera:camera-view:1.5.3"
    implementation "androidx.camera:camera-lifecycle:1.5.3"
    implementation "com.google.guava:guava:33.3.1-android"

    implementation "com.amplifyframework.ui:liveness:1.10.0"
    implementation "com.amplifyframework:aws-auth-cognito:2.33.0"
    implementation "com.google.code.gson:gson:2.10.1"
    implementation "com.squareup.okhttp3:okhttp:4.9.3"
    implementation "com.android.volley:volley:1.2.1"
    implementation "com.github.bumptech.glide:glide:4.10.0"
    implementation "androidx.room:room-runtime:2.6.1"
    implementation "androidx.lifecycle:lifecycle-livedata:2.8.7"
    implementation "androidx.lifecycle:lifecycle-viewmodel:2.8.7"
}
```

Selecciona JDK 21 en la configuración de Gradle de Android Studio. Mantén las opciones `compose`, `viewBinding` y las versiones indicadas al incorporar este paquete a tu aplicación. Consulta la [guía de publicación](docs/R8.md) si utilizas optimización de código y recursos.

## Licencia y permisos

Agrega la licencia de captura como **`app/src/main/assets/com.become.mb.key`**. El `applicationId` debe coincidir con el autorizado en la licencia.

La SDK incluye las declaraciones de permisos de internet, cámara y ubicación aproximada. Solicita el permiso de cámara antes de iniciar un flujo que la requiera. Si tu contrato utiliza ubicación, su permiso es opcional: rechazarlo no bloquea la verificación.

Continúa con el [ejemplo de inicialización](README.md#iniciar-una-verificación).
