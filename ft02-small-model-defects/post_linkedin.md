<!-- LinkedIn template (<= 1,300 chars once filled). The notebook's "Post text" cell fills these placeholders with the
numbers from the run and prints the result. {claude_line} is empty when the optional API cell was skipped. Keep this file in
sync with POST_LINKEDIN in the notebook. -->
Do factories need giant AI models to spot a defect?

23N Field Test #02. We trained a small open model on photos of GOOD parts only: metal nuts, screws, glass bottles and power cables from the public MVTec AD dataset. No defect labels.

Result: {headline}

How it works: a {small_name} ({small_params_m:.0f}M params) turns each photo into patch features; anything unlike every good patch lights up on a heatmap. Mean AUROC {small_auroc:.3f} vs {large_auroc:.3f} for a {large_name} ~{size_ratio:.0f}x its size. {small_ms_cpu:.0f} ms per part on a plain CPU, false alarms on {far_pct:.0f}% of good parts.
{claude_line}
Why it matters: MSME lines in India can run inspection on a ₹{box_inr:,} box on the shop floor, with no cloud bill and no data leaving the plant.

Limits: lab photos, 4 product lines, a fixed camera; costs are estimates (assumptions in the notebook). MVTec AD is CC BY-NC-SA 4.0, research use only. Independent study on public data.

Open notebook + video in comments. Runs free on Colab.

#ManufacturingAI #EdgeAI #MakeInIndia #ComputerVision #23NFieldTests
