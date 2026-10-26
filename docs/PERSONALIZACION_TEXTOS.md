# Native component text — Android

## Become flow text

Become titles, instructions, consent, country/document selection, introductions, review and results are managed by the contract configuration. Local translation files are not required to receive those texts. Missing entries retain the SDK defaults.

This guide and its examples intentionally list native component and technical SDK keys only. Remove old flow entries from app resources when those phrases should follow contract updates. A supported local override can pin a phrase and hide later updates; do not copy the whole template.

## Native technical SDK labels

These labels still read local resources rather than contract text. The examples retain verified startup `text_loader_init`; network errors `timeout_error`, `no_internet_error` and `connection_lost_error`; progress `text_info_upload`, `text_progress_result`, `text_progress_delay_result` and `text_progress_delay_finish_result` (the SDK appends the upload percentage).

These are not flow title/action configuration keys.

## Supported components

| Component | Verified version | Local keys |
| --- | --- | --- |
| Microblink Capture UX | 1.2.0 | `mbic_*` |
| Amplify Face Liveness | 1.10.0 | `amplify_ui_liveness_*` |

This distribution retains Capture Legacy. BlinkID `mb_*` / `mb_blinkid_*` resources do not apply to its capture interface. Names differ across platforms; use this distribution’s keys.

## Optional customization

Add only the entries you intend to customize to `app/src/main/res/values/become_strings.xml`:

```xml
<resources>
    <string name="mbic_flip_document">Turn the document over</string>
    <string name="amplify_ui_liveness_challenge_connecting">Connecting…</string>
</resources>
```

The 16 Capture examples are the native resource IDs wired by this SDK’s Capture settings, not a generic catalog for other Capture versions. App resources replace the same merged resource names. Equivalent Amplify instructions may receive contract text; the native resource is the fallback when that instruction has no configured text. Contract-managed phrases should be updated through that configuration.

Use `values-es` / `values-en` language variants; avoid duplicating `values-b+en`. See the optional [Spanish](../examples/custom-texts/res/values/strings.xml) and [English](../examples/custom-texts/res/values-b+en/strings.xml) examples.

## Validation

Preserve exact key names, capitalization, format placeholders, and the meaning of camera safety and photosensitivity instructions. Edit only required values. Rebuild the app after resource changes; rebuilding the SDK is unnecessary. Validate customized languages on physical devices. `BDIVConfig` does not select a localization table or configure Become flow text.
