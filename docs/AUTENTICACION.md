# JWT y compatibilidad con credenciales

La firma recomendada de `BDIVConfig` recibe un JWT. Las firmas anteriores con `clienId` y `clientSecret` siguen disponibles y funcionales, marcadas como deprecadas para facilitar una migración gradual. No se anuncia una versión de retiro en esta entrega.

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

## Cuidado del token

No incluyas tokens reales en el código, los archivos de configuración compartidos, los mensajes de diagnóstico ni los reportes de soporte. No guardes un token en recursos o constantes de compilación de una aplicación de producción. El [ejemplo Compose](../examples/compose-demo/README.md) permite ingresarlo en pantalla para una prueba de integración y no lo conserva al recrear la aplicación.

Las notificaciones de resultado y cancelación no cambian. Atiende los errores mediante el callback existente y consulta la [guía de resultados y errores](ERRORES.md).
