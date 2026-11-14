# 23N Field Tests #04 — Ask India's Payments Data, in Hindi or English

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23nlabs/field-tests/blob/main/ft04-ask-upi-data/ft04_ask_upi_data.ipynb)

**Question.** Can a small open model, running for free, answer plain-language questions about India's UPI payments
data accurately, in both Hindi (Devanagari) and English?

**Headline (computed at runtime, never hard-coded):**
"A 3B-parameter open model answers N/25 questions about India's UPI data correctly — in Hindi and English — on a free GPU."

An independent study on public data by 23N AI Labs. It is not affiliated with or endorsed by NPCI, RBI, or any bank.

## What the notebook does

1. **Data.** Loads UPI monthly statistics into SQLite as the table `upi_monthly`. Columns: month, year, fiscal
   year, banks live, volume in millions, value in ₹ crore.
2. **Model.** Loads `Qwen/Qwen2.5-Coder-3B-Instruct` (3.09B params) in fp16 on a free Colab T4. Without a GPU it
   falls back to `Qwen/Qwen2.5-Coder-1.5B-Instruct`.
3. **Text-to-SQL.** The prompt contains the schema, units, a short Hindi→column glossary, 3 sample rows and 2 worked
   examples (1 English, 1 Hindi), none of them in the eval set. The model writes SQL. The notebook accepts only one
   `SELECT`/`WITH` statement and runs it on a read-only connection with an authorizer that blocks writes, plus a
   5-second limit. If the SQL errors, the model gets one self-correction attempt. Deterministic code, not the LLM,
   turns the result into a chart and a one-line answer.
4. **Evaluation.** 25 questions, 12 in English and 13 in Hindi, each with hand-written gold SQL. The score is
   execution accuracy: the model's result must have the same row count as gold, and every gold column must match a
   result column as a multiset of values, within a 0.1 % numeric tolerance. Extra columns and row order are
   ignored. Latency is recorded per question. Results are saved to `ft04_eval_results.csv`.
5. **Optional.** The same 25 questions can be sent to Claude (`claude-sonnet-5-5`) through the `anthropic` SDK.
   This only runs if `ANTHROPIC_API_KEY` is set as an environment variable or Colab secret. Those calls are paid.
6. **Gradio demo.** Type a question to see the SQL, the answer, a chart and the result rows. The demo uses
   `launch(share=True, prevent_thread_lock=True)`, so it doesn't block "Run all".
7. **Outputs.** Renders `ft04_video.mp4` (1080×1080, 30 fps, 58 s, H.264) and `ft04_cover.png` (1080×1350), and
   fills in the LinkedIn and X post templates.

## Dataset, provenance and licence

| | |
|---|---|
| What | UPI monthly product statistics: banks live on UPI, volume (million transactions), value (₹ crore) |
| Publisher | National Payments Corporation of India (NPCI), <https://www.npci.org.in/what-we-do/upi/product-statistics> |
| Coverage in snapshot | Jan 2024 → Oct 2026, 34 months. `banks_live` is blank for Apr–Dec 2025 because we could not verify it |
| Snapshot file | `data/upi_monthly.csv`, retrieved 2026-11-09 |
| Licence | NPCI publishes these figures publicly but states no open-data licence. We redistribute a small factual snapshot with attribution for research and education. Check NPCI's website terms before any commercial use. |

**Snapshot construction.** NPCI's statistics page is rendered by JavaScript and could not be fetched by machine from
our build environment. The numbers were therefore transcribed from NPCI's monthly table as republished in the
sources below. The `transcribed_from` column records which source each row came from.

- `HB-2503`: Jan 2024–Mar 2025, from hellobanker.in's reproduction of NPCI's table, "UPI data March 2025"
  (<https://hellobanker.in/upi-data-march-2025-check-how-many-transactions-were-done-via-upi-in-march-2025>).
  These rows were cross-checked against the same site's October 2024 table. That table lists Apr 2024 banks as 581
  instead of 583, and has differences of 0.01–0.04 crore in a few value cells. We kept the later publication's
  figures.
- `HB-2601`: Apr–Dec 2025, from hellobanker.in's January 2026 table, which has no banks column
  (<https://hellobanker.in/rs-28-33-trillion-upi-transactions-in-january-2026-check-day-wise-data>).
- `DF-432`: Jan–Oct 2026, from Dataful/Factly dataset 432, "Year and Month wise number of banks live on UPI…"
  (<https://dataful.in/datasets/432>), which cites NPCI.
- Spot checks against press reports of NPCI releases all agreed, for example: Mar 2025 18.30 bn / ₹24.77 lakh
  crore, Aug 2025 above 20 bn for the first time, Oct 2025 20.70 bn, Dec 2025 21.63 bn, Jan 2026 21.70 bn /
  ₹28.33 lakh crore, Sep 2026 24.07 bn, Oct 2026 25.47 bn.

**At runtime** the notebook first tries a live scrape of NPCI's page with `pandas.read_html`. If that returns a
plausible table, those rows override the snapshot and any newer months are added. Otherwise it loads the snapshot,
trying the local file, then GitHub raw, then an identical copy embedded in the notebook. The data source actually
used is printed.

**Model licence.** `Qwen2.5-Coder-3B-Instruct` is released under the *Qwen Research* licence, which is
non-commercial. Read the model card before any production use.

**Fonts.** Noto Sans Devanagari, SIL Open Font License, downloaded from the Google Fonts GitHub repo.

## How to run

1. Click the Colab badge, then go to Runtime → Change runtime type → **T4 GPU**, then Runtime → **Run all**.
2. Expect about 8–12 minutes in total: ~1 min of installs, ~2 min to download the 6 GB model, ~2–4 min for the
   25 questions, and ~1–2 min for the video.
3. No logins or keys are needed. The model is public on Hugging Face. A Hugging Face token is optional; without one
   you may see an "unauthenticated" warning, which you can ignore.
4. On Kaggle, turn on GPU T4 and Internet in the notebook settings. The Colab-only download step is skipped
   automatically.

## Hindi text rendering

DejaVu Sans has no Devanagari glyphs. matplotlib versions before 3.11 also don't shape complex scripts, so matras and
conjuncts render wrong (for example, किस comes out as कसि). The notebook installs `libraqm0`/`libfribidi0`,
downloads Noto Sans Devanagari, and renders every Devanagari string with Pillow + libraqm (HarfBuzz shaping). The
rendered text is pasted into the matplotlib figures as an image. It writes `hindi_render_check.png` so you can
check the result. If libraqm is missing, it prints a warning with the fix: apt-install, restart the session, Run
all. The Gradio demo shows Hindi as browser text, so the browser handles shaping there.

## Limitations

- 25 questions on a single 34-row table is a capability probe, not a benchmark. We wrote the questions and gold
  SQL, and some of them follow the same patterns as the prompt's glossary and worked examples.
- The scorer ignores column names and row order and allows 0.1 % tolerance. A right answer in the wrong unit or
  format, such as "October 2026" instead of `2026-10`, is marked wrong.
- The data is transcribed from republications of NPCI's table (see above). NPCI sometimes revises recent months.
  `banks_live` is missing for Apr–Dec 2025.
- Only standard Devanagari Hindi was tested. Hinglish, romanised Hindi and other Indian languages were not.
- Latency is for single greedy-decoded queries on the printed hardware. It is not a served or batched deployment.

## Files

- `ft04_ask_upi_data.ipynb`: the notebook
- `data/upi_monthly.csv`: the data snapshot (see provenance above)
- `post_linkedin.md`, `post_x.md`: post templates with `{placeholders}`, filled in by the notebook
