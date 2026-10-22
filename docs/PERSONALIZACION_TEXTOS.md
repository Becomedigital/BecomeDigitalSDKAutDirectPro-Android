# Language and optional local text overrides — Android

## Standard integration

Become Compose screen text is applied automatically from the contract. **Copying the `strings.xml` examples is not required to integrate the SDK or receive contract text updates.**

This guide remains useful for intentional app overrides and text that still reads native resources. The [Spanish](../examples/custom-texts/res/values/strings.xml) and [English](../examples/custom-texts/res/values-b+en/strings.xml) templates are compatibility references. Historical entries are not a catalog of every phrase on the current screens.

## Override scope

| Text | Current behavior |
| --- | --- |
| Become Compose screens | Resolve contract text for the current locale, base language, Spanish, then the SDK screen default. |
| Introduction | First check supported native `intro_*` keys, such as `intro_title`, `intro_body`, and `intro_cta`. |
| Data processing notice | First check supported `atdp_*` keys, such as `atdp_title`, `atdp_markdown`, `atdp_checkbox_label`, and `atdp_accept`. |
| Loading and errors that read Android resources | Accept an override for the resource actually read by that label, such as `text_loader_init`, `identity_error_documentfront`, or `timeout_error`. |
| Internal capture and facial detector instructions | Use the native component's supported resources. |

Introduction key dots become underscores: `header.reminder` maps to `intro_header_reminder`. ATDP camel-case keys become snake case: `checkboxLabel` maps to `atdp_checkbox_label`.

Other Compose labels do not have a general mapping from every contract namespace to `strings.xml`. Historical introduction/document keys such as `text_tittle_general_intro` and `text_dni_selec_document` do not replace those current Compose labels. `BDIVConfig` has no locale selector or localization-table parameter; contract text uses the Android environment's locale.

## Optional example

Add **only intentional overrides** to `app/src/main/res/values/become_strings.xml`:

```xml
<resources>
    <string name="intro_cta">Start verification</string>
    <string name="atdp_accept">Accept and continue</string>
    <string name="text_loader_init">Loading…</string>
    <string name="identity_error_documentfront">Capture the front again, fully visible and in focus.</string>
</resources>
```

An override takes priority in the path that reads that resource and can hide later contract updates. If the whole template was copied into the app, remove entries that should no longer be fixed locally. Use contract text for normal flow copy changes.

## Native components

This distribution uses legacy Capture UX. Its instructions support compatible `mbic_*` native resource keys for the integrated version; the Become introduction copy has its own resolution path.

Amplify Face Liveness uses supported native `amplify_ui_liveness_*` keys. Become facial introduction copy and internal detector instructions have separate localization paths; contract copy is not automatically mapped to every internal component phrase.

## Installing and checking overrides

1. Add only selected keys, preserving their exact names and one `<resources>` root per file.
2. Use language variants such as `values-en` for languages you customize. `values-b+en` is also valid; avoid duplicate definitions in equivalent qualifiers for one language.
3. Preserve format placeholders and line breaks. Escape `&` as `&amp;` and apostrophes as required by Android.
4. Rebuild the host app; rebuilding the AAR is unnecessary.
5. Validate affected resources on a physical device and check that phrases without overrides still follow the contract or their defaults.

Resource names differ between platforms: Android uses `identity_error_documentfront`; iOS uses `identity_error_documentFront`.
