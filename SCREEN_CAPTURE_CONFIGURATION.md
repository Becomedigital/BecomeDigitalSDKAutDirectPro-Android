# Protección de pantalla en Android

`preventScreenCapture` permite elegir la protección de las pantallas presentadas por la SDK durante la verificación.

| Valor | Comportamiento |
| --- | --- |
| `false`, predeterminado | Permite capturas y grabación sin aplicar la protección de la SDK. |
| `true` | Activa la protección de la pantalla de verificación frente a capturas y grabación. |

La opción se aplica a los dos flujos de verificación y no modifica otras pantallas de tu aplicación. Las restricciones del dispositivo o de otros componentes pueden seguir aplicándose.

## Activar la protección

Define el valor antes de iniciar la verificación:

```java
BDIVConfig config = new BDIVConfig(
    jwt,
    contractId,
    documentTypes,
    true,
    userId
);
config.setPreventScreenCapture(true);
BecomeResponseManager.getInstance().startAuthentication(this, config);
```

En Kotlin puedes utilizar el mismo método `config.setPreventScreenCapture(true)`. Omite la opción o indica `false` para permitir las capturas sin aplicar esta protección.

## Al actualizar tu integración

En entregas anteriores, omitir el parámetro activaba la protección. En esta entrega, su valor predeterminado es `false`. Llama a `setPreventScreenCapture(true)` si tu aplicación necesita conservar la protección anterior.

Comprueba en un dispositivo físico las capturas, la grabación y el regreso a tu aplicación. Elige esta opción de acuerdo con los requisitos de privacidad de tu integración.
