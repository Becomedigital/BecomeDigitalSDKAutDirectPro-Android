# Personalizar textos — Android

## Implementación

1. Copie las claves que necesite del ejemplo [español](../examples/custom-texts/res/values/strings.xml) o [inglés](../examples/custom-texts/res/values-b+en/strings.xml) a los recursos de su app.
2. Use `app/src/main/res/values/become_strings.xml` para los textos predeterminados y `values-b+en/become_strings.xml` para inglés. Si ya tiene `values-en`, use esa carpeta sin duplicarla.
3. Cambie los valores, mantenga exactamente cada `name` y recompile la app. No necesita configurar `BDIVConfig` ni regenerar el AAR.

También puede agregar las entradas al `strings.xml` que ya tiene, dentro de su único bloque `<resources>`. La clave y el idioma determinan la sobrescritura, no el nombre del archivo.

## Ejemplo

```xml
<resources>
    <string name="text_start_btn">Comenzar</string>
    <string name="text_title_button_retry">Volver a intentar</string>
    <string name="text_title_document_error">Revisa las fotos de tu documento</string>
    <string name="mbic_scan_the_front_side">Escanea el frente del documento</string>
    <string name="amplify_ui_liveness_get_ready_begin_check">Iniciar prueba de vida</string>
</resources>
```

Las claves que no cambie conservan su texto original. Personalice cada idioma utilizado por la app para evitar que una traducción de la SDK tenga prioridad.

## Claves por pantalla

Los ejemplos contienen 115 claves. Una clave compartida cambia en todos los lugares donde se utiliza; algunas solo aparecen según el flujo y la versión del componente.
| Pantalla / uso | Claves |
| --- | --- |
| Inicio | `text_tittle_general_intro`, `text_sub_tittle_general_intro`, `text_start_btn`, `and_intro_general`, `text_video_intro_general`, `text_document_intr_general` |
| Introducción y análisis facial | `text_video_intro`, `text_tittle_selfie`, `btn_text_recording_video`, `text_loader_selfie`, `text_progress_inteligence` |
| Selección de país y documento | `text_tittle_selec_document`, `text_dni_selec_document`, `text_license`, `text_passport`, `select_text`, `text_body_country`, `text_msn_selec_document` |
| Captura y galería | `text_tittle_intro_doc_front`, `text_tittle_intro_doc`, `text_btn_introduction_doc`, `text_btn_intro_doc_galery`, `text_error_path_image_pick` |
| Vista previa | `text_info_preview`, `text_confirm_preview`, `text_retry_previe` |
| Carga y envío | `text_loader_init`, `text_loader`, `text_varification_title`, `text_varification_body`, `text_finish_upload`, `text_info_upload`, `text_document_validation` |
| Consulta de resultados | `text_progress_result`, `text_progress_delay_result`, `text_progress_delay_finish_result` |
| Error documental y reintento | `text_title_document_error`, `text_sub_title_document_error`, `text_error_capture_document`, `text_title_button_retry` |
| Creación de identidad y resultados: cierre facial, recaptura y reintento | Las 24 claves `identity_error_*` de los ejemplos. [Listado y acción por clave](ERRORES.md#catálogo-ampliado-de-creación-y-resultados). |
| Error general o validación fallida | `text_varification_title_error`, `text_varification_body_error`, `text_varification_title_compliance_error`, `text_varification_body_compliance_error`, `text_error_compliance_not_allowed`, `unknown_error`, `general_error`, `text_empty_balance` |
| Error de conexión | `timeout_error`, `no_internet_error`, `connection_lost_error` |
| Resultado final | `text_finish`, `text_sub_tittle_finish` |
| Confirmar salida | `text_undo`, `text_sub_tittle_undo`, `text_tittle_undo`, `terminate_text`, `text_cancel` |
| Microblink: frente/reverso | `mbic_scan_the_front_side`, `mbic_scan_the_back_side`, `mbic_flip_document` |
| Microblink: encuadre y luz | `mbic_move_closer`, `mbic_move_farther`, `mbic_lightning_too_bright`, `mbic_lightning_too_dark`, `mbic_occluded`, `mbic_torch_glare_tooltip_message` |
| Microblink: ayuda | `mbic_need_help_tooltip`, `mbic_onboarding_field_visible_title`, `mbic_tutorial_fields_visible_title`, `mbic_tutorial_harsh_light_title` |
| Microblink: conexión y disponibilidad | `mbic_check_internet_connection`, `mbic_network_error`, `mbic_scanning_not_available` |
| Face Liveness: preparación y fotosensibilidad | `amplify_ui_liveness_get_ready_a11y_photosensitivity_icon_content_description`, `amplify_ui_liveness_get_ready_begin_check`, `amplify_ui_liveness_get_ready_center_face_label`, `amplify_ui_liveness_get_ready_photosensitivity_description`, `amplify_ui_liveness_get_ready_photosensitivity_dialog_description`, `amplify_ui_liveness_get_ready_photosensitivity_dialog_dismiss`, `amplify_ui_liveness_get_ready_photosensitivity_dialog_title`, `amplify_ui_liveness_get_ready_photosensitivity_title` |
| Face Liveness: instrucciones y captura | `amplify_ui_liveness_challenge_a11y_cancel_content_description`, `amplify_ui_liveness_challenge_connecting`, `amplify_ui_liveness_challenge_instruction_hold_face_during_freshness`, `amplify_ui_liveness_challenge_instruction_move_face`, `amplify_ui_liveness_challenge_instruction_move_face_closer`, `amplify_ui_liveness_challenge_instruction_move_face_further`, `amplify_ui_liveness_challenge_instruction_multiple_faces_detected`, `amplify_ui_liveness_challenge_recording_indicator_label`, `amplify_ui_liveness_challenge_verifying` |

## Antes de entregar

- No duplique claves para el mismo idioma ni corrija sus nombres, aunque tengan erratas.
- Mantenga el significado de las instrucciones de cámara, accesibilidad y fotosensibilidad.
- Conserve los marcadores de formato y saltos de línea. Escape `&` como `&amp;` y los apóstrofos como `\'`.
- Los mensajes enviados por el servicio y los permisos del sistema no se sustituyen con estos archivos.
- No sobrescriba `there_already_a_record`, `_07` ni `sdk_version`; no son textos de personalización. Conserve el `app_name` de su aplicación.
- Pruebe introducción, captura, error/reintento y resultado en cada idioma después de recompilar.
