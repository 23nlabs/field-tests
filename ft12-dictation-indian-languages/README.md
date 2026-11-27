# 23N Field Tests #12 · Indian-language dictation: a paid API against free open models

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23nlabs/field-tests/blob/ft12-dictation-indian-languages/ft12-dictation-indian-languages/ft12_dictation_indian_languages.ipynb)

> **Status: built, not yet run on real data.** The notebook has been executed end to end only in smoke-test mode
> (synthetic clips, stand-in models and a stand-in API, no internet, no GPU, no key). There are no results yet. The
> badge and raw-file links point at the `ft12-dictation-indian-languages` branch until it is merged.

**Question.** Apps that let people type by voice in Gujarati, Hindi or Tamil can run a free open speech model on
their own GPU or pay a dictation API per minute. On the same public test clips, how often does each get the words
wrong, and what does it cost?

**Why now.** On 23 Nov 2026 Sarvam AI released Sarvam Dictate, a dictation API for English and 22 Indian languages
at ₹0.50 per audio minute. Its announcement reports fewer character edits than other commercial systems on real
dictations from its own app, a set that is not public. This notebook runs the API on a public test set, next to
free open models, so anyone can repeat it.

**Headline (computed at runtime, never hard-coded):**
"Sarvam Dictate's raw transcript got X% of Gujarati words wrong on N public test clips; the best free open model
({model}) got Y%. Lower error in W of 4 languages, clearly lower in S."
("Clearly" = the paired 95% bootstrap interval of the gap is entirely below zero.)

Independent study on public data by 23N AI Labs. Not affiliated with or endorsed by Sarvam AI, Google, OpenAI, Meta
or any model author mentioned here. The API is used as any paying developer would use it.

## What the notebook does

1. **Data.** FLEURS test transcripts and audio for `gu_in`, `hi_in`, `ta_in` and `en_us` from the Hugging Face
   repo `google/fleurs`. Recordings over 29.5 s are dropped (the API takes at most 30 s per clip), then up to 100
   sentence IDs present in all four languages are sampled (seed 23): the same sentences in every language.
2. **Systems.**
   - **Sarvam Dictate**, `POST https://api.sarvam.ai/v2/dictate`, `model=dictate-v1` (documented alias; the served
     snapshot is printed), `language_code` stated (`gu-IN`, `hi-IN`, `ta-IN`, `en-IN`), `mode=transcribe`,
     `style={"preset":"clean"}`. One call returns the raw `transcript` and the edited `text`; both are scored.
     Responses are cached in `ft12_api_cache.json` (re-runs never bill a clip twice), calls stay under 50/min, retry
     on 429/5xx, and stop at a 150-minute budget.
   - **Open models** on the free Colab T4, greedy decoding, language forced: `openai/whisper-large-v3-turbo` and
     `facebook/mms-1b-all` (language adapters).
3. **Scoring.** One script-safe normaliser for all systems (NFC, lower case, Indic digits to 0–9, punctuation
   removed, vowel signs kept), pooled WER and CER with `jiwer`, 95% bootstrap intervals, and a paired bootstrap on
   the API-minus-best-open gap per language.
4. **Where it fails.** Gujarati error rate on numbers, Latin-script words and other words; examples of what the
   editing step changed (raw → edited → reference).
5. **Sanity checks.** Before the headline, the notebook prints `!! SANITY CHECK FAILED … Do NOT post` if: any
   language has fewer than 80 clips; references aren't in the expected script; an open model failed to load; a WER
   is outside 0–500%; whisper-large-v3-turbo English WER is above 15%; the best open model beats English in Gujarati;
   **the API arm didn't run** (no key); more than 5% of API calls failed, came back `degraded`, or report another
   language; the API's English WER is above 15%; the API's WER in any language is over 2× the best open model's
   (implausible, so check the request first); the budget ran out; or smoke-test mode is on. Robustness variants:
   mean per-clip WER, CER, and the paired gap intervals.
6. **Outputs.** `ft12_transcripts.csv`, `ft12_summary.csv`, `ft12_results.png`, `ft12_failures.png`, a Gradio demo
   (record a clip, compare the API and the best open model), `ft12_video.mp4` (1080×1080, 30 fps, 58 s timeline
   saved at 1.5×, H.264), `ft12_cover.png` (1080×1350), and the filled LinkedIn and X posts with character counts.

## Data, models, API and licences

| Item | Source | Licence / price | Login |
|---|---|---|---|
| FLEURS test split, `gu_in` / `hi_in` / `ta_in` / `en_us` | <https://huggingface.co/datasets/google/fleurs> (Google) | CC BY 4.0 | No |
| Sarvam Dictate (`dictate-v1`) | <https://docs.sarvam.ai> | ₹0.50 per audio minute, pay-as-you-go, excl. GST (checked 24 Nov 2026). Sarvam's pricing page says verified sign-ups get ₹100 of free credit | **Yes: API key** |
| `openai/whisper-large-v3-turbo` (~0.81B) | Hugging Face | MIT | No |
| `facebook/mms-1b-all` (~1B) | Hugging Face | **CC-BY-NC 4.0, non-commercial** | No |
| Noto Sans Gujarati / Devanagari / Tamil, Bricolage Grotesque, IBM Plex | Google Fonts / brand kit | SIL OFL 1.1 | No |

- The FLEURS audio is downloaded at run time and is not redistributed here.
- A full run sends about 400 clips, typically 60–90 minutes of audio: about ₹30–45 at list price, within the
  free credit. The notebook stops at 150 minutes.
- **Context fact used in the post** (from Sarvam's launch announcement, 23 Nov 2026): Dictate is priced at ₹0.50 per
  minute of audio and covers English and 22 Indian languages; Sarvam reports fewer character edits than Gemini 3.5
  Transcribe and AssemblyAI Dictation on dictations from its own Kivi app, a set that is not public.

## How to run

1. Get a key at dashboard.sarvam.ai. In Colab open the 🔑 **Secrets** panel, add `SARVAM_API_KEY`, and allow
   notebook access. (On Kaggle: Add-ons → Secrets, same name. Locally: the environment variable.)
2. Click the Colab badge, then Runtime → Change runtime type → **T4 GPU**, then Runtime → **Run all**.
3. Expect about 15–20 minutes: installs, FLEURS audio (~2 GB) and models (~5 GB), ~800 open-model transcriptions,
   ~400 API calls (rate-limited to 50/min, about 8 minutes), and the video.
4. Read the **Results** cell. If it prints `!! SANITY CHECK FAILED`, don't post. Fix the cause first.
5. **Outputs go to Google Drive automatically.** Near the start, Colab asks once for Drive access; at the end, the
   video, cover, charts, CSVs, both post texts, the API cache and `RUN_STATUS.txt` (headline plus every sanity-check
   result) are copied to `My Drive/23N Field Tests/FT12/<date_time>`. Failed runs get `_CHECKS-FAILED` in the folder
   name. Set `SAVE_TO_DRIVE = False` in the drive cell to skip.
6. To rerun without paying again, upload the saved `ft12_api_cache.json` to the Colab session first: cached clips
   are not sent (or billed) again.

`FT12_SMOKE_TEST=1` (environment variable, off by default) runs the notebook without internet, GPU or key:
synthetic noise clips with sentences we wrote, stand-in "models" and a stand-in "API" that corrupt the reference at
made-up rates. It exists only to check that the notebook runs; its output is labelled as not real and must never be
posted. `FT12_SMOKE_API=0` additionally tests the no-key path.

## What was tested in this build

- `nbformat.validate` passes; every code cell compiles with `%`/`!` lines removed.
- Smoke-test run end to end twice (with and without the stand-in API): results, charts, failure analysis, video
  (38.7 s at 1.5×, 1080×1080, H.264, 30 fps), cover and post text. Frames from every video section and the cover were
  inspected; the post text is within limits (LinkedIn ~1,160 chars, X ~185).
- **Not tested:** the FLEURS download, the two open models on a GPU, and every real call to the Sarvam API (this
  build environment can't reach Hugging Face or api.sarvam.ai). The request format follows Sarvam's API reference
  (multipart `file`, `model`, `language_code`, `mode`, `style` as JSON text; response fields `transcript`, `text`,
  `language_code`, `degraded`, `usage`). If the first real run returns HTTP 4xx, the error text is printed; check
  the field names against the current reference.

## Limitations

- **Read speech, not dictation.** FLEURS is adult volunteers reading Wikipedia-style sentences. Real dictation is
  spontaneous, with names, code-mixing and self-corrections, which is what the API's editing step is built for. This
  test measures recognition on clean read speech; it does not reproduce Sarvam's own benchmark, which used a
  different test set and metric.
- **Raw transcript in the headline.** The edited `text` is what an app's users would see, but WER against a
  verbatim reference penalises fair edits (number formats, dropped fillers, rewrites), so its WER is reported
  separately with how often the editor changed the text.
- **US-English speakers** with the API set to `en-IN`.
- **Small sample** (≤100 clips per language): rely on the paired intervals.
- **Prices and model snapshots change.** Both are printed with the result.
- **Terms.** The API is used under Sarvam's terms of service with your own key. Read them before publishing a
  comparison.
- `facebook/mms-1b-all` is **non-commercial** (CC-BY-NC 4.0).
