# Configuración de la protección contra capturas de pantalla en Android

Esta guía corresponde al `becomedigitalsdk.aar` incluido en este repositorio. El AAR se compiló a partir del commit `7b2414c0232a315354179fbb9da1be696fb35032` con la variante Release de la biblioteca Android. El código fuente utiliza el servicio de producción de Become.

## Cambio de comportamiento

`BDIVConfig.preventScreenCapture` ahora tiene el valor predeterminado `false` en todos los constructores que omiten este parámetro. En versiones distribuidas anteriores, el valor predeterminado era `true`. Si la aplicación omite la configuración, se permiten las capturas de pantalla y la grabación mientras está visible la actividad de la SDK. El valor predeterminado es el mismo en Debug y Release. Los valores indicados explícitamente conservan el comportamiento solicitado.

| Valor | Comportamiento de la SDK |
| --- | --- |
| `false` (predeterminado) | La SDK quita `WindowManager.LayoutParams.FLAG_SECURE` de su actividad. |
| `true` | La SDK aplica `FLAG_SECURE` a su actividad para impedir capturas de pantalla y grabaciones de esa ventana. |

La opción controla la actividad de la SDK de Become. No modifica las banderas de otras actividades de la aplicación anfitriona ni anula protecciones aplicadas de forma independiente por Android u otros componentes.

## Activar la protección explícitamente

Configure `BDIVConfig` antes de llamar a `startAuthentication`:

```java
BDIVConfig config = new BDIVConfig(
    clientId,
    clientSecret,
    contractId,
    documentTypes,
    true,     // allowLibraryLoading
    userId,
    null      // customerLogo
);
config.setPreventScreenCapture(true);

BecomeResponseManager.getInstance().startAuthentication(this, config);
```

En Kotlin, configure `config.isPreventScreenCapture = true` antes de iniciar el flujo. El constructor más completo de `BDIVConfig` también acepta `preventScreenCapture` como último argumento booleano, después de `debugLogsEnabled`. Omita el parámetro o indique `false` para usar el nuevo valor predeterminado. La opción aplica a `Flow.Onboarding` y `Flow.Authentication`.

## Migración desde un AAR anterior

1. Revise cada creación de `BDIVConfig` en la aplicación. Los constructores que omiten la opción pasan de tener protección a permitir capturas al integrar este AAR.
2. Llame a `setPreventScreenCapture(true)` donde deba mantenerse la protección anterior. Los valores explícitos `true` y `false` no requieren cambios.
3. Reemplace el archivo `becomedigitalsdk.aar` de la aplicación y recompílela con las dependencias indicadas en el [README](README.md).
4. En un dispositivo físico, compruebe las capturas de pantalla y la grabación durante la captura del documento, la prueba de vida, la cancelación y el regreso a la aplicación. Si la aplicación admite ambos modos, pruebe el valor predeterminado y el valor `true`.

La aplicación integradora debe elegir esta configuración según sus requisitos de privacidad. El parámetro controla la ventana de la SDK; no reemplaza las políticas de tratamiento de datos ni la protección general de la aplicación.

## Verificación del artefacto

El AAR contiene `BDIVConfig.isPreventScreenCapture()` y `setPreventScreenCapture(boolean)`. Sus constructores inicializan el valor en `false` salvo que la aplicación indique explícitamente `true`. El AAR incluye la biblioteca nativa del servicio de producción. Las pruebas funcionales de captura de documentos y validación facial requieren una aplicación con licencia y un dispositivo físico.

El nombre del archivo de distribución no cambió respecto a versiones anteriores. Después de reemplazar una copia local, identifique este artefacto mediante su SHA-256:

`3acaeb92d836d007fe5a5d1cbab8b2075b2e91ec36baf2ab344354328ed3bb73`
