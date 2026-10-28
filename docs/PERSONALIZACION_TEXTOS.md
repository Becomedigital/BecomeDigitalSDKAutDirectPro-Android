# Localización de la SDK de Android

La SDK utiliza los textos de verificación asociados a tu contrato. No necesitas agregar archivos locales para los títulos, consentimiento, selección de país y documento, introducciones, revisión o resultado. Si falta un texto del contrato, se conserva el valor disponible en la SDK.

Puedes personalizar las indicaciones de captura y los mensajes de carga y conexión que se enumeran en esta guía.

## Agregar traducciones a tu aplicación

1. Crea o edita `app/src/main/res/values/become_strings.xml`.
2. Agrega únicamente las claves que deseas personalizar.
3. Utiliza variantes como `values-es` y `values-en` para los idiomas que necesites.

Ejemplo:

```xml
<resources>
    <string name="mbic_flip_document">Voltea el documento</string>
    <string name="amplify_ui_liveness_challenge_connecting">Conectando…</string>
    <string name="text_loader_init">Iniciando…</string>
</resources>
```

Las claves no incluidas conservan sus traducciones disponibles. Para la captura facial, los textos configurados en el contrato tienen prioridad sobre la traducción local de la misma indicación; si no hay un texto configurado, se utiliza el recurso local disponible.

Encontrarás ejemplos en [español](../examples/custom-texts/res/values/strings.xml) e [inglés](../examples/custom-texts/res/values-b+en/strings.xml). Si tu aplicación ya contiene `values-en`, incorpora allí las entradas del ejemplo en inglés sin duplicarlas en `values-b+en`.

## Claves disponibles

Estas claves corresponden a Capture UX 1.4.1 y Face Liveness 1.10.0, las dependencias de esta entrega. Utiliza los nombres exactos de esta plataforma.

### Carga, progreso y conexión

| Clave | Ejemplo de texto |
| --- | --- |
| `text_loader_init` | Iniciando… |
| `timeout_error` | La conexión ha tardado demasiado. Inténtalo otra vez. |
| `no_internet_error` | No tienes conexión a Internet. Verifica tu red. |
| `connection_lost_error` | Se perdió la conexión a Internet. Inténtalo nuevamente. |
| `text_info_upload` | Estamos subiendo tu información... |
| `text_progress_result` | Verificando el resultado... |
| `text_progress_delay_result` | Estamos por finalizar |
| `text_progress_delay_finish_result` | Estamos tardando un poco más de lo normal |

La SDK agrega el porcentaje al mensaje de carga; no agregues un marcador de porcentaje a estas claves.

### Captura de documento

| Clave | Ejemplo de texto |
| --- | --- |
| `mbic_check_internet_connection` | Verifica la conexión a internet |
| `mbic_flip_document` | Voltea el documento |
| `mbic_lightning_too_bright` | Muévete a un lugar con menos iluminación |
| `mbic_lightning_too_dark` | Muévete a un lugar más brillante |
| `mbic_move_closer` | Acércate |
| `mbic_move_farther` | Aleja |
| `mbic_need_help_tooltip` | ¿Necesitas ayuda? |
| `mbic_network_error` | Error de red |
| `mbic_occluded` | Mantén el documento completamente visible |
| `mbic_onboarding_field_visible_title` | Mantén todos los detalles visibles |
| `mbic_scan_the_back_side` | Escanea el lado posterior del documento |
| `mbic_scan_the_front_side` | Escanea el lado frontal del documento |
| `mbic_scanning_not_available` | Escaneo no disponible |
| `mbic_torch_glare_tooltip_message` | Cuidado con el reflejo de la linterna.<br>Mueve suavemente tu ID para evitarlo. |
| `mbic_tutorial_fields_visible_title` | Mantén todos los campos visibles |
| `mbic_tutorial_harsh_light_title` | Cuidado con la luz intensa |

### Captura facial

| Clave | Ejemplo de texto |
| --- | --- |
| `amplify_ui_liveness_challenge_a11y_cancel_content_description` | Cancelar desafío |
| `amplify_ui_liveness_challenge_connecting` | Conectando |
| `amplify_ui_liveness_challenge_instruction_hold_face_during_freshness` | No te muevas |
| `amplify_ui_liveness_challenge_instruction_move_face` | Mueve tu rostro frente a la cámara |
| `amplify_ui_liveness_challenge_instruction_move_face_closer` | Acércate |
| `amplify_ui_liveness_challenge_instruction_move_face_further` | Aléjate |
| `amplify_ui_liveness_challenge_instruction_multiple_faces_detected` | Solo un rostro por verificación |
| `amplify_ui_liveness_challenge_recording_indicator_label` | REC |
| `amplify_ui_liveness_challenge_verifying` | Verificando |
| `amplify_ui_liveness_get_ready_a11y_photosensitivity_icon_content_description` | Información sobre fotosensibilidad |
| `amplify_ui_liveness_get_ready_begin_check` | Iniciar verificación de video |
| `amplify_ui_liveness_get_ready_center_face_label` | Centra tu rostro |
| `amplify_ui_liveness_get_ready_photosensitivity_description` | Esta verificación parpadea con diferentes colores. Usa precaución si eres fotosensible. |
| `amplify_ui_liveness_get_ready_photosensitivity_dialog_description` | Algunas personas pueden experimentar convulsiones epilépticas al exponerse a luces de colores. Usa precaución si tú o alguien de tu familia tiene una condición epiléptica. |
| `amplify_ui_liveness_get_ready_photosensitivity_dialog_dismiss` | Entendido |
| `amplify_ui_liveness_get_ready_photosensitivity_dialog_title` | Advertencia de fotosensibilidad |
| `amplify_ui_liveness_get_ready_photosensitivity_title` | Advertencia de fotosensibilidad |

## Recomendaciones

- Mantén los nombres, mayúsculas, saltos de línea y marcadores de formato de cada clave.
- Conserva el significado de los avisos de permisos, seguridad de captura y fotosensibilidad.
- Verifica las traducciones en un dispositivo físico con el idioma que utilizará tu usuario.
- Actualiza los textos generales de verificación en la configuración del contrato. `BDIVConfig` permite elegir `themeMode`, pero no establece una tabla de traducciones ni textos del flujo.

Volver a la [guía de integración](../README.md).
