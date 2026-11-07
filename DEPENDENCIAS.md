# Dependencias y compatibilidad Android

El POM declara las dependencias transitivas de la entrega `3.5.1-rc.1`. La tabla presenta las versiones seleccionadas al compilar el AAR de producción; sirve para comparar con las que ya tiene tu aplicación. No establece rangos mínimos o máximos de compatibilidad que no se hayan probado.

| Biblioteca | Versión utilizada |
| --- | --- |
| `androidx.activity:activity-compose` | `1.12.4` |
| `androidx.activity:activity-ktx` | `1.12.4` |
| `androidx.appcompat:appcompat` | `1.7.1` |
| `androidx.camera:camera-camera2` | `1.5.3` |
| `androidx.camera:camera-core` | `1.5.3` |
| `androidx.camera:camera-lifecycle` | `1.5.3` |
| `androidx.camera:camera-view` | `1.5.3` |
| `androidx.compose.material3:material3` | `1.4.0` |
| `androidx.compose:compose-bom` | `2026.06.00` |
| `androidx.core:core-ktx` | `1.16.0` |
| `androidx.fragment:fragment-ktx` | `1.6.2` |
| `androidx.lifecycle:lifecycle-livedata` | `2.9.4` |
| `androidx.lifecycle:lifecycle-viewmodel` | `2.9.4` |
| `androidx.room:room-runtime` | `2.6.1` |
| `androidx.test.uiautomator:uiautomator` | `2.3.0` |
| `com.android.volley:volley` | `1.2.1` |
| `com.google.code.gson:gson` | `2.10.1` |
| `com.google.guava:guava` | `33.3.1-android` |
| `com.squareup.okhttp3:okhttp` | `5.1.0` |
| `org.jetbrains.kotlin:kotlin-stdlib` | `2.2.10` |
| `androidx.compose.foundation:foundation` | `1.11.3` |
| `androidx.compose.foundation:foundation-layout` | `1.11.3` |
| `androidx.compose.animation:animation` | `1.11.3` |
| `androidx.compose.animation:animation-core` | `1.11.3` |
| `androidx.compose.material:material-ripple` | `1.11.3` |
| `androidx.compose.ui:ui` | `1.11.3` |
| `androidx.compose.runtime:runtime` | `1.11.3` |
| `com.android.tools:desugar_jdk_libs` | `2.1.5` |

La aplicación consumidora de referencia compiló en debug y release con R8, JDK 21, Gradle 9.2.1, Android Gradle Plugin 9.0.1, Kotlin 2.2.10 y `compileSdk 36`. Se verificaron ARMv7/ARM64 y alineación de memoria de 16 KB. Las pruebas funcionales requieren un dispositivo físico.

Para revisar una diferencia de resolución en tu aplicación:

```bash
./gradlew :app:dependencyInsight --configuration releaseRuntimeClasspath --dependency androidx.core:core-ktx
```

Gradle puede seleccionar otra versión cuando confluyen dependencias de tu aplicación. Usa el reporte para revisar esas diferencias y verifica tu compilación y el flujo funcional con la combinación seleccionada.
