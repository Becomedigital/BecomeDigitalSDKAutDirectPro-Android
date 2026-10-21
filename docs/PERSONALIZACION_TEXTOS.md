# Text customization — Android

## Scope of this distributed AAR

The current Compose screens read their visible copy from the contract. If a key is missing, the SDK checks the requested locale, its base language, Spanish, and the bundled screen default.

App `strings.xml` overrides apply where the SDK or a native component reads Android string resources. They do **not** replace the contract-rendered Compose labels in this artifact. In particular, defining legacy introduction or document-button resource names in the app does not override the corresponding Compose screen copy. `BDIVConfig` does not provide custom text, logo, color, or localization-table setters.

The [Spanish template](../examples/custom-texts/res/values/strings.xml) and [English template](../examples/custom-texts/res/values-b+en/strings.xml) include resource keys retained across SDK versions. Some are compatibility entries that the current flow does not display. Copy only keys used by the component or error label you want to customize.

## Resource-backed labels

Use the exact Android resource name. For example:

```xml
<resources>
    <string name="identity_error_documentfront">Capture the front again with all edges visible.</string>
    <string name="identity_error_documentback">Capture the back again with all edges visible.</string>
    <string name="timeout_error">The operation is taking too long. Try again.</string>
    <string name="mbic_scan_the_front_side">Scan the front of your document</string>
    <string name="amplify_ui_liveness_get_ready_begin_check">Start the liveness check</string>
</resources>
```

| Component or label | Resource names |
| --- | --- |
| Identity and document errors | The applicable `identity_error_*` entries in the template |
| Connection errors | `timeout_error`, `no_internet_error`, `connection_lost_error` |
| Capture UX instructions | Supported `mbic_*` entries |
| Amplify preparation and photosensitivity | Supported `amplify_ui_liveness_get_ready_*` entries |
| Amplify capture instructions | Supported `amplify_ui_liveness_challenge_*` entries |

Resource keys vary between Android and iOS. For example, Android uses `identity_error_documentfront`; the iOS resource uses `identity_error_documentFront`.

## Installation

1. Add selected entries under the app's `app/src/main/res/values/become_strings.xml`, or its existing `strings.xml`.
2. Add language variants under the corresponding Android resource qualifier, such as `values-en`. The supplied `values-b+en` example is also a valid English qualifier; use one location per language rather than duplicating it.
3. Keep one `<resources>` root, preserve each `name`, and retain the app's own `app_name`.
4. Preserve format placeholders and intended line breaks. Escape `&` as `&amp;` and Android apostrophes as needed.
5. Rebuild the host app. App resource changes do not require rebuilding the AAR.
6. Validate the affected native component or error message in each supported language on a physical device.

Changing a resource does not enable a step, change the document type, or change the configured capture mode.
