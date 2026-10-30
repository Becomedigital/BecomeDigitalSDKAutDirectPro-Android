# JWT y compatibilidad con credenciales

La firma recomendada de `BDIVConfig` recibe un JWT. Las firmas anteriores con `clienId` y `clientSecret` siguen disponibles y funcionales, marcadas como deprecadas para facilitar una migración gradual. No se anuncia una versión de retiro en esta entrega.

## Tokens de creación y consulta

Para onboarding con consulta del resultado final, recibe dos JWT vigentes desde el backend de tu aplicación, sin el prefijo `Bearer` y para el mismo ambiente y contrato:

| Operación | Permiso solicitado (`grant_type`) | Configuración pública |
| --- | --- | --- |
| Crear la verificación | `verification:create` | Argumento `jwt` del constructor. |
| Consultar el resultado | `verification:get` | `verificationResultsJwt` en Kotlin o `setVerificationResultsJwt(...)` en Java. |

Consulta la [guía de autenticación](https://becomedigital.gitbook.io/kyc_api_es/authentication), la [obtención de tokens](https://becomedigital.gitbook.io/kyc_api_es/endpoints/auth) y los [permisos de consulta de resultados](https://becomedigital.gitbook.io/kyc_api_es/endpoints/verification-results). Mantén las credenciales en tu backend. Cambiar únicamente el permiso del JWT principal a `verification:get` deja sin cubrir la creación.

En Kotlin, asigna el token de consulta antes de iniciar:

```kotlin
val config = BDIVConfig(
    creationJwt, contractId,
    arrayOf(DocumetType.DNI, DocumetType.PASSPORT),
    true, userId
)
config.verificationResultsJwt = resultsJwt
config.flow = BDIVConfig.Flow.Onboarding
BecomeResponseManager.getInstance().startAuthentication(activity, config)
```

En Java:

```java
BDIVConfig config = new BDIVConfig(
    creationJwt, contractId,
    new DocumetType[] { DocumetType.DNI, DocumetType.PASSPORT },
    true, userId
);
config.setVerificationResultsJwt(resultsJwt);
config.setFlow(BDIVConfig.Flow.Onboarding);
BecomeResponseManager.getInstance().startAuthentication(activity, config);
```

Registra el callback antes de iniciar, como en el ejemplo de la primera verificación. `verificationResultsJwt` se usa únicamente al consultar el resultado final de onboarding con `performVerificationCheck=true`. No reemplaza el token principal en la creación ni modifica `Flow.Authentication`. Con `performVerificationCheck=false`, se entrega la creación sin esperar el resultado final. En autenticación de un usuario existente, el token principal debe autorizar ese flujo.

El valor predeterminado de `verificationResultsJwt` es `null`: si lo omites, se conserva el uso del token principal para consultar. Ese token debe tener el permiso requerido; uno limitado a `verification:create` no autoriza la consulta de resultados. Un valor explícito vacío o compuesto por espacios se rechaza al intentar consultar, sin utilizar otro token como reemplazo.

Si utilizas `setJwt(...)`, asigna `verificationResultsJwt` **después**: reemplazar el JWT principal elimina el token de consulta anterior. Obtén tokens vigentes y configura ambos antes de iniciar un nuevo intento. La firma JWT no obtiene ni renueva tokens automáticamente ni cambia a credenciales si un token falla.

La firma deprecada con credenciales conserva su comportamiento y no utiliza `verificationResultsJwt`. Para migrar esa configuración, selecciona primero el constructor JWT o llama a `setJwt(...)` y después asigna el token de consulta.

## Creación correcta y consulta con HTTP 403

Una creación confirmada con HTTP 201 seguida de HTTP 403 al consultar puede indicar que el token de consulta no está autorizado para esa operación. El estado 403 no demuestra por sí solo que el token haya vencido.

Comprueba que `jwt` corresponda a creación (`verification:create`) y que hayas asignado un token de consulta (`verification:get`) a `verificationResultsJwt`. Revisa también vigencia, ambiente, contrato y permisos de tu integración. Si el problema continúa, comparte con soporte el estado HTTP y el paso afectado, sin incluir tokens, credenciales ni datos personales.

## Comparación de las firmas

| Aspecto | JWT, recomendada | Credenciales, deprecada y compatible |
| --- | --- | --- |
| Argumentos de acceso | `jwt` | `clienId`, `clientSecret` |
| Firma básica, en orden | `BDIVConfig(jwt, contractId, documentTypes, allowLibraryLoading, userId)` | `BDIVConfig(clienId, clientSecret, contractId, documentTypes, allowLibraryLoading, userId)` |
| Uso recomendado | Integraciones nuevas y aplicaciones que ya obtienen el token mediante su backend. | Aplicaciones existentes mientras preparan su migración. |
| Advertencias | Los constructores JWT no están deprecados. | Java y Kotlin muestran una advertencia con la firma JWT equivalente. |
| Compatibilidad | Conserva las opciones públicas y los resultados de la SDK. | Conserva el orden de argumentos, las opciones y los valores predeterminados anteriores. |

La deprecación es una recomendación de migración: no elimina ni deshabilita la firma anterior. No reemplaces una credencial por un token dentro de la firma deprecada; selecciona el constructor que recibe `jwt`.

## Iniciar con JWT

1. Obtén un JWT mediante el backend de tu integración antes de abrir la SDK. Mantén las credenciales de una integración nueva en tu backend.
2. Entrega el token como `jwt`, sin el prefijo `Bearer ` y sin espacios adicionales. Debe autorizar el contrato y el flujo que utilizarás, y corresponder al ambiente de esta entrega: producción.
3. Administra su vigencia, almacenamiento y renovación desde tu integración. Si pierde vigencia o es rechazado, obtén un nuevo token antes de volver a iniciar la SDK.

En Kotlin, utiliza argumentos posicionales:

```kotlin
val config = BDIVConfig(
    jwt,
    contractId,
    arrayOf(DocumetType.DNI, DocumetType.PASSPORT, DocumetType.LICENSE),
    true,
    userId
)
config.verificationResultsJwt = resultsJwt
config.flow = BDIVConfig.Flow.Onboarding
BecomeResponseManager.getInstance().startAuthentication(activity, config)
```

En Java:

```java
BDIVConfig config = new BDIVConfig(
    jwt,
    contractId,
    new DocumetType[] { DocumetType.DNI, DocumetType.PASSPORT, DocumetType.LICENSE },
    true,
    userId
);
config.setVerificationResultsJwt(resultsJwt);
config.setFlow(BDIVConfig.Flow.Onboarding);
BecomeResponseManager.getInstance().startAuthentication(activity, config);
```

Registra el callback antes de iniciar, como se muestra en la [primera verificación](../README.md#iniciar-una-verificación). El JWT no se obtiene ni se renueva automáticamente al usar esta firma. Un JWT vacío produce un error de configuración; no activa la firma con credenciales como alternativa.

El acceso mediante JWT es independiente de `Flow.Authentication`, que sirve para autenticar la identidad de un usuario existente. Puedes utilizar JWT con `Onboarding` o `Authentication`.

## Integraciones existentes

Si ya utilizas credenciales, tu código continúa siendo compatible:

```kotlin
// Firma deprecada, disponible durante la migración.
val config = BDIVConfig(
    clientId, clientSecret, contractId,
    arrayOf(DocumetType.DNI), true, userId
)
```

```java
// Firma deprecada, disponible durante la migración.
BDIVConfig config = new BDIVConfig(
    clientId, clientSecret, contractId,
    new DocumetType[] { DocumetType.DNI }, true, userId
);
```

Estas firmas conservan el orden de sus argumentos, las opciones adicionales y sus valores predeterminados. Las propiedades `clienId` y `clientSecret` también permanecen disponibles y deprecadas. Las advertencias de Java y Kotlin indican la firma JWT equivalente.

Para migrar, prepara primero la obtención del JWT en tu backend y sustituye los dos argumentos `clientId, clientSecret` por `jwt`. Conserva los demás argumentos de tu constructor: contrato, documentos, usuario y opciones de flujo, espera, diagnóstico y protección de pantalla.

También puedes asignar `config.jwt = jwt` en Kotlin o `config.setJwt(jwt)` en Java antes de iniciar la SDK. Esto selecciona el acceso mediante JWT y borra las credenciales almacenadas en esa configuración. Asignar credenciales a una configuración creada con JWT no selecciona la firma deprecada.

## Opciones adicionales del constructor

Las dos familias ofrecen ocho variantes. Empiezan con los argumentos de su firma básica y aceptan las siguientes combinaciones **después de `userId`**, en este orden:

| Variante | Argumentos adicionales |
| --- | --- |
| Básica | Ninguno. |
| Espera | `performVerificationCheck` |
| Flujo | `flow` |
| Espera y flujo | `performVerificationCheck, flow` |
| Flujo y límites de espera | `flow, pollingMaxAttempts, pollingTimeoutSeconds` |
| Espera, flujo y límites | `performVerificationCheck, flow, pollingMaxAttempts, pollingTimeoutSeconds` |
| Con diagnóstico | `performVerificationCheck, flow, pollingMaxAttempts, pollingTimeoutSeconds, debugLogsEnabled` |
| Con protección de pantalla | `performVerificationCheck, flow, pollingMaxAttempts, pollingTimeoutSeconds, debugLogsEnabled, preventScreenCapture` |

Si omites estas opciones, se mantienen `Flow.Onboarding`, `performVerificationCheck=true`, `pollingMaxAttempts=0`, `pollingTimeoutSeconds=2`, `debugLogsEnabled=false` y `preventScreenCapture=false`. El valor `0` permite esperar sin límite de intentos; el tiempo corresponde a cada consulta del resultado. También puedes configurar estas opciones mediante sus métodos `set…` antes de iniciar.

Por ejemplo, esta migración conserva todas las opciones en Kotlin:

```kotlin
// Antes: firma deprecada, todavía compatible.
val anterior = BDIVConfig(
    clientId, clientSecret, contractId, documentTypes, true, userId,
    false, BDIVConfig.Flow.Onboarding, 4, 30, false, true
)

// Después: JWT obtenido mediante el backend de tu integración.
val actual = BDIVConfig(
    jwt, contractId, documentTypes, true, userId,
    false, BDIVConfig.Flow.Onboarding, 4, 30, false, true
)
```

En Java:

```java
// Antes: firma deprecada, todavía compatible.
BDIVConfig anterior = new BDIVConfig(
    clientId, clientSecret, contractId, documentTypes, true, userId,
    false, BDIVConfig.Flow.Onboarding, 4, 30, false, true
);

// Después: JWT obtenido mediante el backend de tu integración.
BDIVConfig actual = new BDIVConfig(
    jwt, contractId, documentTypes, true, userId,
    false, BDIVConfig.Flow.Onboarding, 4, 30, false, true
);
```

Los nombres de los parámetros y sus valores se describen en la [configuración pública](../README.md#configurar-la-sdk). El cambio de firma no modifica las notificaciones de resultado y cancelación.

## Cuidado del token

No incluyas tokens reales en el código, los archivos de configuración compartidos, los mensajes de diagnóstico ni los reportes de soporte. No guardes un token en recursos o constantes de compilación de una aplicación de producción. El [ejemplo Compose](../examples/compose-demo/README.md) permite ingresarlo en pantalla para una prueba de integración y no lo conserva al recrear la aplicación.

Las notificaciones de resultado y cancelación no cambian. Atiende los errores mediante el callback existente y consulta la [guía de resultados y errores](ERRORES.md).
