# Jetpack Compose integration example

This app shows how a Compose screen starts the distributed Android SDK through an `AppCompatActivity`. `BecomeComposeScreen` collects a user ID and requests camera permission. `BecomeComposeLauncher` retains the callback manager, configures `BDIVConfig`, and reports SDK completion or cancellation to Compose state.

This repository includes no client credentials or capture license for the example. A contract with Become, credentials for that contract, and a license issued for your app ID are required to complete a verification. The example builds without them and displays a missing configuration message before requesting camera permission.

## Prepare your local app

1. Follow the [installation guide](../../README.md#installation-and-dependencies). Use JDK 21 and Android 7.0 or later.
2. Copy `credentials.example.properties` to `credentials.properties`. Fill in `applicationId`, `clientId`, `clientSecret`, and `contractId` with the values issued for your integration. The real file is ignored by Git. The application ID must match the capture license; an empty `applicationId` uses a nonfunctional example ID.
3. Place the license issued for that app ID at `app/src/main/assets/com.become.mb.key`. The license file is ignored by Git.
4. Open this folder in Android Studio, select JDK 21 for Gradle, and build the `app` module. On a physical Android device, enter a user ID and tap **Start onboarding**.

The app references `becomedigitalsdk.aar` and the two Capture AARs directly from the repository root. No SDK binary is copied into the example. The Gradle wrapper, plugin versions, and dependencies match the [distribution guide](../../README.md#installation-and-dependencies). Debug and Release both use the production SDK; a different build variant does not change its environment.

`BDIVConfig.debugLogsEnabled` is enabled for support diagnostics. Logs can contain personal information from a test session. English and Spanish resources show how to translate the host screen and supported native text; [localization guidance](../../docs/PERSONALIZACION_TEXTOS.md) explains which flow text comes from the contract. See the [logging guide](../../docs/LOGGING.md) for diagnostics.

Document capture and facial verification require a physical device and valid integration details. A successful build confirms compilation and resource packaging only. Do not commit `credentials.properties`, the license, or a built APK or AAB.
