<!-- X template. Main post <= 280 chars once filled ({claude_short} is dropped automatically if it would exceed 280).
The notebook's "Post text" cell fills and prints these. Keep this file in sync with POST_X / POST_X_THREAD in the notebook. -->

## Main post
Do factories need giant AI models to spot a defect?

{headline}

Trained on good parts only (MVTec AD). AUROC {small_auroc:.3f} vs {large_auroc:.3f} for a {size_ratio:.0f}x bigger model.{claude_short}

Open notebook ↓ #EdgeAI

## Optional thread
1/ Method: PatchCore. ImageNet {small_name} features per image patch, a memory bank of good-part patches, nearest-neighbour distance = anomaly score. No training loop, no defect labels.

2/ Alarm threshold set from held-out GOOD parts only. On {n_test} test photos it caught {recall_pct:.0f}% of defects with {far_pct:.0f}% false alarms. {small_ms_cpu:.0f} ms/part on CPU.

3/ Caveats: lab photos, fixed camera, 4 product lines, cost = estimate. Data is CC BY-NC-SA (research only). Notebook runs free on Colab: {colab}
