# Manejo de errores — Android

## Qué recibe la aplicación

Registre `BecomeInterfaseCallback` antes de iniciar la SDK y conserve la referencia al `BecomeCallBackManager`.

| Salida | Cómo se entrega | Qué debe hacer la app |
| --- | --- | --- |
| Éxito | `onFinish(response)` con `responseStatus == SUCCES` | Continuar según el flujo configurado. |
| Error terminal | `onFinish(response)` con `responseStatus == ERROR` | Restaurar su pantalla y ofrecer una acción; no relanzar automáticamente la SDK. |
| Cancelación del proceso | `onCancel()` | Permitir continuar en la app sin considerar la identidad aprobada. |
| Error recuperable | Pantalla de reintento o recaptura dentro de la SDK | Dejar que la SDK gestione el flujo; no se emite un callback por cada fallo. |

`SUCCES` conserva esa escritura por compatibilidad. El enum también define `PENDING`, `NOFOUND` y `CANCEL`: no trate ninguno como éxito. El gestor convierte `CANCEL` en `onCancel()`; no debe esperar ese estado por el `onFinish` habitual. Un resultado de polling pendiente se gestiona dentro de la SDK.

`message` contiene el texto descriptivo. `responseDictionary` es nullable y no es un catálogo de errores; los errores terminales generados por la SDK lo entregan como `null`. Con `performVerificationCheck=false`, un éxito significa que `newIdentity` aceptó la creación, **no que terminó o aprobó la validación biométrica**. Su diccionario puede incluir `code`, `message`, `url_resource` y `user_id`.

### Límite del mapeo

El callback expone un estado general y un mensaje, **no un `errorCode`, código HTTP ni clave de recursos por causa**. Las claves de esta guía sirven para personalizar textos; no son valores devueltos en `message`. El idioma, los recursos de la app y algunos mensajes del servicio cambian el texto.

Mapee el resultado por `responseStatus` y la cancelación por `onCancel()`. No base decisiones de aprobación, bloqueo o reintento automático en comparaciones de mensajes. Distinguir de manera fiable cada causa requiere ampliar el contrato público de la SDK, no solo esta documentación. Mantenga una salida segura para mensajes vacíos o desconocidos.

## Errores de inicio y otros flujos

Los siguientes casos pueden finalizar con `onFinish` y `StatusType.ERROR`.

| Clave o mensaje identificable | Cuándo ocurre | Acción recomendada |
| --- | --- | --- |
| `Configuration is null` | No se recibió configuración | Entregar una instancia válida de `BDIVConfig`. |
| `Invalid configuration parameters` | Credenciales, contrato o usuario vacíos; lista documental vacía en Onboarding | Corregir los parámetros antes de iniciar. Authentication admite documentos vacíos. |
| `No camera on this device` | No se encuentra cámara compatible en la comprobación inicial | Usar un dispositivo con cámara. |
| `denied permits for the camera` | Permiso de cámara denegado | Explicar el permiso y habilitarlo antes de volver a iniciar. |
| `Error obtaining sessionid` | No se obtuvo la sesión facial | Revisar conectividad y configuración; iniciar una nueva ejecución. |
| Mensaje de Face Liveness o `Error desconocido` | Fallo de captura facial o de su resultado | Ofrecer un proceso nuevo; no reutilizar la sesión facial. El detalle puede variar. |
| `timeout_error` | Tiempo de espera agotado en servicios fuera del catálogo ampliado | Revisar conexión y permitir reintento iniciado por el usuario. |
| `no_internet_error` | No se pudo resolver el servidor / no hay conexión | Revisar Internet. |
| `connection_lost_error` | No se pudo conectar con el servicio | Revisar la red y volver a intentar. |
| Mensaje del servicio, sin clave fija | Autenticación inicial, contrato, `/matches` u otro servicio | No asumir un catálogo cerrado; mostrar una alternativa segura y contactar con soporte si persiste. |
| `Unable to create temporary SDK storage`, `Unable to compress captured image`, `Unable to finalize captured image`, `Unable to save captured image` o detalle del sistema | No se pudo guardar la captura localmente | Revisar espacio disponible; iniciar una nueva captura después de resolverlo. |
| `general_error`, `unknown_error` o detalle de inicialización | Configuración de captura, dependencias o fallo no clasificado | Revisar integración y diagnóstico para soporte. |
| `text_license` | Microblink devuelve `ERROR_LICENCE_CHECK` | Revisar licencia y `applicationId`. Actualmente se reutiliza esta clave de texto de documento; no es un código de error ni un mensaje inequívoco. |
| `text_error_compliance_not_allowed` | Cierre desde una pantalla de validación fallida de versiones anteriores | No considerar la verificación aprobada. |

Una captura documental incompleta puede mostrar `text_error_capture_document` y permitir reintentar dentro de la SDK, sin callback terminal. Cancelar una captura concreta tampoco implica siempre cancelar todo el proceso.

## Catálogo ampliado de creación y resultados

Este catálogo está incluido en el AAR de este repositorio e incorpora el mapeo del repositorio fuente `31872df`. Si utiliza una copia anterior, reemplace el AAR; agregar recursos XML en la app no actualiza el comportamiento del binario.

Aplica a `POST /api/v1/newIdentity`, con o sin polling, y a GET de resultados cuando está habilitado. No sustituye el manejo independiente de `/matches`, autenticación inicial ni los errores de las dependencias.

- **Cerrar:** termina la Activity de la SDK y entrega `onFinish` con `ERROR` y el mensaje. La aplicación anfitriona permanece abierta.
- **Recapturar:** abre el error documental y permite volver a capturar; no entrega todavía un error terminal.
- **Reintentar:** muestra el mensaje y detiene las consultas hasta la acción del usuario; tampoco entrega un error terminal automáticamente.

| Clave de recurso | Causa reconocida / significado del mensaje | Acción de la SDK y manejo recomendado |
| --- | --- | --- |
| `identity_error_liveness` | Prueba de vida no confirmada, incluido `liveness=false` | Cerrar. Iniciar un proceso nuevo si el usuario desea reintentar. |
| `identity_error_face` | Rostro no validado, incluido `face_match=false` | Cerrar. Nueva verificación con el rostro descubierto. |
| `identity_error_documentfront` | Frente ilegible o `documentError=1` | Recapturar el frente completo, enfocado y sin reflejos. |
| `identity_error_documentback` | Reverso ilegible o `documentError=2` | Recapturar el lado correcto. |
| `identity_error_documentfiles` | Archivos documentales no recibidos correctamente o lados incorrectos | Recapturar los lados solicitados. |
| `identity_error_documentquality` | Calidad insuficiente o datos documentales no legibles | Recapturar con buena luz y enfoque. |
| `identity_error_documentunsupported` | Tipo documental no reconocido/admitido | Recapturar con un tipo admitido. |
| `identity_error_documentvalidation` | Documento no validado; por ejemplo `alteration=false` o `template=false` | Recapturar. Revisar original, vigencia y tipo; no interpretar el mensaje como prueba de fraude. |
| `identity_error_session` | Sesión vencida/no válida; token o HTTP 401 | Reintentar disponible. Se recomienda cerrar e iniciar una nueva sesión. |
| `identity_error_permission` | Operación no habilitada; HTTP 403 | Reintentar disponible. Revisar permisos con soporte. |
| `identity_error_configuration` | Parámetros requeridos ausentes o inválidos | Reintentar disponible. Corregir la integración antes de iniciar otra ejecución. |
| `identity_error_contract` | No se pudo validar el contrato | Reintentar disponible. Revisar el contrato con soporte. |
| `identity_error_quota` | Saldo/cupo de verificaciones no disponible | Reintentar disponible. Contactar con soporte. |
| `identity_error_notfound` | Usuario/verificación no encontrado; HTTP 404 | Reintentar disponible. Comprobar el proceso con soporte. |
| `identity_error_conflict` | Ya existe un proceso asociado; HTTP 409 | Reintentar disponible. Resolver el conflicto; evitar nuevas altas automáticas. |
| `identity_error_uploadsize` | Archivos demasiado grandes; HTTP 413 | Reintentar disponible. El mensaje recomienda cerrar y hacer una nueva captura. |
| `identity_error_fileformat` | Formato no compatible; HTTP 415 | Reintentar disponible. Nueva captura o soporte. |
| `identity_error_ratelimit` | Demasiadas solicitudes; HTTP 429 | Reintentar después de esperar. |
| `identity_error_unavailable` | Servicio no disponible; HTTP 5xx salvo 504 u otro fallo no clasificado | Reintentar más tarde. |
| `identity_error_processing` | No se completó el procesamiento; HTTP 400/422 sin causa más específica | Reintentar; contactar con soporte si persiste. |
| `identity_error_invalidresponse` | Respuesta vacía, inválida, desconocida o evidencia requerida incompleta | Reintentar; nunca asumir aprobación. |
| `identity_error_timeout` | Tiempo de espera agotado, HTTP 408/504 o límite de intentos de polling alcanzado | Reintentar tras revisar la conexión. El límite no cierra la SDK automáticamente. |
| `identity_error_offline` | Sin conexión / no se puede resolver el servidor | Reconectar y reintentar. |
| `identity_error_connection` | Conexión interrumpida u otro fallo de entrada/salida de red | Revisar la red y reintentar. |

Las causas del cuerpo de la respuesta tienen prioridad sobre el mapeo HTTP genérico: **HTTP 400 no significa necesariamente error documental**. Las categorías son del procesamiento interno; no equivalen a códigos públicos del backend ni llegan separadas al callback. Android usa las claves en minúscula; iOS conserva sufijos camelCase.

### Cómo se reintenta

Con polling habilitado, sin URL guardada se reenvían los mismos datos a `newIdentity`; con URL guardada se reinicia la consulta GET. Sin polling, el reintento vuelve al POST y nunca inicia GET. Un error documental descarta las capturas documentales y la URL anteriores para recapturar. Un rechazo facial cierra la SDK y exige un proceso nuevo.

Un resultado pendiente no es un error: sigue consultándose. `pollingMaxAttempts=0` no limita intentos; un límite positivo detiene el polling y muestra reintento al agotarse. Si el usuario decide salir desde un error recuperable, recibe `onCancel()`, no un error con la causa del servicio anterior.

## Ejemplo de manejo seguro

Dentro del callback registrado, separe los estados sin depender del texto:

```kotlin
override fun onFinish(response: BDIdentityVerificationResponse) {
    runOnUiThread {
        when (response.responseStatus) {
            BDIdentityVerificationResponse.StatusType.SUCCES -> {
                // Continúe según el flujo configurado.
                // Sin polling significa creación aceptada, no aprobación final.
            }
            BDIdentityVerificationResponse.StatusType.ERROR -> {
                // No relance automáticamente ni registre response.message.
                androidx.appcompat.app.AlertDialog.Builder(this@MainActivity)
                    .setTitle("Verificación no completada")
                    .setMessage("El proceso terminó sin completar la verificación. Puedes volver a iniciarlo.")
                    .setPositiveButton("Aceptar", null)
                    .show()
            }
            BDIdentityVerificationResponse.StatusType.PENDING,
            BDIdentityVerificationResponse.StatusType.NOFOUND,
            BDIdentityVerificationResponse.StatusType.CANCEL -> {
                // No son aprobación. Restaure la pantalla de su app.
            }
        }
    }
}

override fun onCancel() {
    runOnUiThread {
        // Restaure la pantalla. No es una validación aprobada ni un fallo técnico.
    }
}
```

El ejemplo supone que el callback se registra en una `MainActivity`; sustituya ese nombre por su Activity. Use textos localizados en su implementación. El ejemplo no muestra mensajes técnicos variables directamente al usuario.

Para adaptar mensajes, consulte [Personalización de textos](PERSONALIZACION_TEXTOS.md) y las claves `identity_error_*` de los ejemplos. No registre mensajes completos, respuestas JSON, imágenes ni credenciales. Para soporte use los [logs de diagnóstico](LOGGING.md), la versión de la SDK y el paso donde falló.
