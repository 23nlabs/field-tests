# How to build a Field Test

This is the spec for anyone, person or agent, adding a new Field Test to this repo. Follow [BRAND.md](BRAND.md) for every visual and every piece of wording.

## Folder layout
```
ftNN-slug/
  ftNN_slug.ipynb     # clean notebook (no outputs); the Open-in-Colab badge points here
  README.md           # question, data and licence, how to run, assumptions, limitations, Colab badge
  post_linkedin.md    # template with {placeholders}, ≤1,300 chars when filled
  post_x.md           # ≤280 chars, plus an optional 3-post thread
  data/               # only small factual snapshots, with source, retrieval date and licence noted in the README
```
Badge URL: `https://colab.research.google.com/github/23nlabs/field-tests/blob/main/ftNN-slug/ftNN_slug.ipynb`

## Notebook rules
1. **Runtime:** Run all must work on free Colab (T4 or CPU) and on Kaggle within 25 minutes. Paid API keys are never required; optional paid comparisons sit in a cell that skips itself when the key is missing.
2. **Data:** real, open data only, downloaded inside the notebook from a URL you have verified. Prefer sources with no login. If a free key is unavoidable, document every step and offer a fallback.
3. **Sections, in this order:** title card → Setup → Data → Method → Results (headline) → Interactive demo (Gradio, `launch(share=True, prevent_thread_lock=True)` in try/except) → Video → Cover → Post text → Limitations.
4. **Brand:** load the kit in Setup with `urllib.request.urlretrieve("https://raw.githubusercontent.com/23nlabs/field-tests/main/brand/brand23n.py", "brand23n.py"); import brand23n as B; B.setup()`. Make every chart, video frame and the cover with it. Write no colours or fonts by hand.
5. **Headline numbers:** computed at runtime and never hard-coded. Every assumption (tariff, cost, threshold) is a named variable at the top of the notebook and is printed with the result. Call estimates estimates.
6. **Sanity checks (required):** before the headline is printed, assert or print a loud `!! SANITY CHECK FAILED … Do NOT post` if the result contradicts something already known. Examples: a state's economy shrinking 78%, accuracy above 100%, a negative "growth" winner. Check for breaks in data versions and units (FT03 lost a whole run to a 2021→2022 change of satellite processing). Print a robustness variant, such as 2-year averages or another split.
7. **Video:** 1080×1080 (or 1080×1350 portrait from #13 on, see BRAND.md "Video formats"), 30 fps, H.264, made with `B.Video`. Author a 45–60 s timeline: hook (`B.hook_card`, 0–5 s), then real evidence from the run with `B.header` on every frame (5–40 s), then `B.headline_card` (40–52 s), then `B.end_card` (52–58 s). `B.Video` saves the file at **1.5× speed by default** (`B.VIDEO_SPEED`), so a 58 s timeline becomes a ~39 s file; pass `speed=1.0` (or set `B23N_VIDEO_SPEED=1`) for normal speed, `keep_1x=True` to keep both. Burn in captions with `B.caption`. Download the files with `google.colab.files.download` inside try/except.
8. **Cover:** use `B.cover(...)` at 1080×1350.
9. **Post text:** fill both templates from computed values and print the character counts. The first two lines must say what was tested and what the result was. Lead with a documented fact about the problem, never an invented statistic. End with `B.post_signature("NN")`.
10. **Framing:** name the sector's problem, not a company as a target. Write "Independent study on public data." Never imply a partnership or affiliation.
11. **Licences:** state the dataset and model licences in the title card and README. Flag non-commercial licences clearly.

## Deep Field Tests (#13 on)
From #13 on, every Field Test goes as deep as a short paper. Measuring a number is not enough: the notebook must show whether the number can be trusted. It has five parts, and each one is a section of the Method and Results:

1. **Baseline:** an open, pretrained model used as it is. Freeze it and report its plain accuracy first.
2. **One added method** that makes the output trustworthy, such as post-hoc uncertainty heads, temperature scaling, conformal prediction intervals or sets, selective prediction (abstain and hand off to a human), or out-of-distribution scores. Leave the baseline's predictions untouched.
3. **Evaluation protocol**, with named metrics and a held-out calibration split. Report at least one from each group:
   - calibration: coverage at 50/80/90/95%, ECE with a reliability diagram, or a Q–Q / variance-calibration check;
   - usefulness: interval width, the share of cases handled automatically at a target accuracy (`B.selective_chart`), or task precision (AP, or AKP for keypoints).
4. **Stress test under a real Indian condition**, such as monsoon cloud, night, fog or haze, rain, a new city or district, phone-quality audio or code-mixed speech. Report the same metrics on that slice. If the method breaks, say so in the headline or the limits, because that is a finding.
5. **Cost of being wrong**, stated as a named assumption (₹ of penalty, minutes of human review, alerts missed), so the result reads in the sector's terms.

The headline is about trust, not only accuracy. For example: "95% intervals hold 94% of the time on clear days and 71% in fog", or "62% of riders can be classified automatically at 98% precision". Cite the papers the method comes from in the README, and cite related prior work that inspired the topic in your own words.

**Topics involving people on roads, rail or in public places** (helmet use, phone use, crowds, traffic):
- Measure the rate, not people. Don't identify anyone, read number plates, or build per-person or per-vehicle tracking that leaves the notebook.
- Pixelate faces and plates in every published frame with `B.blur_regions`.
- Write "a measurement study, not an enforcement tool". Never imply that a detection is a violation or an offence. Calibrated uncertainty and abstention exist so that a human makes the call.
- Lead with a documented public-safety fact (an official statistic or an inquiry report, with its source), never an invented one.

**Video:** use the formats in BRAND.md ("Video formats"), at 4:5 portrait by default.

## Testing without the real data
Build agents usually can't download the datasets. Then:
- Generate the notebook from a script kept outside the repo, and validate it with nbformat (`nbformat.validate`). Every code cell must compile once `%` and `!` lines are removed.
- Execute the notebook end to end with a small synthetic stand-in for the data-loading cell only, behind an environment flag that is off by default. Never ship synthetic data or synthetic results.
- Render the video and cover on that stand-in and look at frames from each section.
- Say plainly what was and wasn't tested.

## After a real run
Save the run notebook as `ftNN_slug_executed.ipynb` (with the Colab metadata stripped), put the key charts in `results/`, add a "Results" section to the folder README, add a row to the top README, export HTML to `docs/` and add a card to `docs/index.html`.
