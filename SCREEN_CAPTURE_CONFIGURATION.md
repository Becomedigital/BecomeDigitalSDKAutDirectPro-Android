# Screen capture configuration for the Android SDK

This guide applies to the `becomedigitalsdk.aar` included in this repository. The AAR was built from source commit `7b2414c0232a315354179fbb9da1be696fb35032` using the Android library's Release variant. The source uses the production Become API endpoint.

## Behavior change

`BDIVConfig.preventScreenCapture` now defaults to `false` in every constructor that omits it. Earlier distributed builds defaulted to `true`. An application that omits the setting now permits screenshots and screen recording while the SDK activity is visible. The default is the same in Debug and Release builds. An explicit value continues to take precedence.

| Value | SDK behavior |
| --- | --- |
| `false` (default) | The SDK clears `WindowManager.LayoutParams.FLAG_SECURE` on its activity. |
| `true` | The SDK sets `FLAG_SECURE` on its activity to prevent screenshots and screen recording of that window. |

The option controls the Become SDK activity. It does not change flags on unrelated host application activities or override capture policies applied independently by Android or another component.

## Enable protection explicitly

Set the value on `BDIVConfig` before calling `startAuthentication`:

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

In Kotlin, set `config.isPreventScreenCapture = true` before starting the flow. The longest `BDIVConfig` constructor also accepts `preventScreenCapture` as its final Boolean argument, after `debugLogsEnabled`. Omit the flag or pass `false` to use the new default. The setting applies to both `Flow.Onboarding` and `Flow.Authentication`.

## Migration from an earlier AAR

1. Review every `BDIVConfig` creation in the host application. Constructors that omit the setting change from protected to unprotected when this AAR is integrated.
2. Call `setPreventScreenCapture(true)` wherever the previous protected behavior must continue. Explicit `true` and `false` values need no change.
3. Replace the old `becomedigitalsdk.aar` in the host application and rebuild it with the dependencies described in the main README.
4. On a physical device, check screenshots and screen recording during document capture, face liveness, cancellation, and return to the host application. Run this check once with the default and once with `true` if your application supports both modes.

Screen capture policy should be chosen by the integrator based on the application's privacy requirements. This flag controls the SDK window; it is not a substitute for application-wide data handling or device policy.

## Artifact verification

The AAR contains `BDIVConfig.isPreventScreenCapture()` and `setPreventScreenCapture(boolean)`. Its constructors initialize the value to `false` unless the caller explicitly supplies `true`. The AAR includes the SDK's native production endpoint library. Functional document capture and face liveness require the integrator's licensed application and a physical device.

The AAR retains the same distribution filename as earlier builds. Use the checksum below to identify this build after replacing a locally stored copy.

The SHA-256 checksum of `becomedigitalsdk.aar` is `3acaeb92d836d007fe5a5d1cbab8b2075b2e91ec36baf2ab344354328ed3bb73`.
