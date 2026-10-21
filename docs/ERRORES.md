# Error and result handling — Android

Register `BecomeInterfaseCallback` before starting verification and retain `BecomeCallBackManager` while the flow is active.

| Callback or status | Host action |
| --- | --- |
| `onFinish(response)` with `SUCCES` | Inspect the optional object for the completed SDK operation. For authentication, evaluate `authentication.result` separately. |
| `onFinish(response)` with `ERROR` | Restore the host UI and offer a new user-initiated attempt. |
| `PENDING` or `NOFOUND` | Do not treat the result as approval. |
| `onCancel()` | Return to the host UI without marking the verification approved. |

`SUCCES` retains its historical spelling. `message` is descriptive text, not a stable error code. The `onboarding`, `authentication`, and `verification` objects can be `null`.

With `performVerificationCheck = false`, an `onboarding` object confirms creation, not final approval. With final-result checking enabled, inspect the `verification` object. Document-only flows do not require a facial result.

The SDK presents its available capture and retry actions inside its own UI. The host does not receive a callback for every capture attempt.

## Integration checks

- **Configuration:** provide nonempty client credentials and a contract ID. Authentication also requires a nonempty existing user ID. An empty document array uses the contract's available document types.
- **Camera:** check the physical device and obtain runtime camera permission before starting again.
- **Capture license:** verify `app/src/main/assets/com.become.mb.key` and the licensed `applicationId`.
- **Missing class or resource:** include all three AARs and the runtime dependencies in the [README](../README.md). Avoid mixing Capture versions or adding BlinkID migration dependencies.
- **Connection:** allow a new user-initiated attempt after connectivity returns. Result checks use `pollingTimeoutSeconds` and `pollingMaxAttempts`; the general connection/read/write timeout is a separate resource setting.
- **Incomplete capture:** allow the SDK to request the required sides again. A cropped preview is not a substitute for a missing full-frame capture.

Do not branch on localized message text to approve an identity or trigger automatic retries. When requesting support, provide the SDK version, device, visible step, and relevant [client diagnostics](LOGGING.md), excluding credentials and images.
