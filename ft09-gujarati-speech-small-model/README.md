# 23N Field Tests #09 · Can small open models understand spoken Gujarati?

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23nlabs/field-tests/blob/ft09-gujarati-speech-small-model/ft09-gujarati-speech-small-model/ft09_gujarati_speech_small_model.ipynb)

> **Status: built, not yet run on real data.** The notebook has been executed end to end only in smoke-test mode
> (synthetic clips and stand-in models, no internet, no GPU). There are no results yet. The badge and raw-file
> links point at the `ft09-gujarati-speech-small-model` branch until it is merged.

**Question.** Phone lines, shops and citizen helpdesks that want to take voice in Gujarati need a model that hears
it. How well do small open speech-recognition models, on a free GPU, transcribe spoken Gujarati, and where do they
fail?

**Headline (computed at runtime, never hard-coded):**
"The best small open model we tested ({model}) got X% of spoken Gujarati words wrong, against Y% in English for the
same sentences ({model})."

Independent study on public data by 23N AI Labs. It is not affiliated with or endorsed by Google, OpenAI, Meta or
any model author mentioned here.

## What the notebook does

1. **Data.** Downloads the FLEURS test transcripts and test audio for `gu_in`, `hi_in` and `en_us` from the
   Hugging Face dataset repo `google/fleurs` (`data/<lang>/test.tsv`, `data/<lang>/audio/test.tar.gz`; if that
   layout has moved, it searches the repo's file list). It keeps one recording per sentence and samples up to 150
   sentence IDs present in all three languages (seed 23). FLEURS sentences are translations of the same FLoRes-101
   sentences, so the content is the same in every language.
2. **Models.** Runs four open models with greedy decoding, one at a time so they fit a T4:
   `openai/whisper-small`, `openai/whisper-large-v3-turbo`, `facebook/mms-1b-all` (Gujarati, Hindi and English
   adapters) and `vasista22/whisper-gujarati-small` (Gujarati only). Whisper gets the language forced.
3. **Scoring.** One script-safe normaliser for all languages (NFC, lower case, Indic digits to 0–9, punctuation
   removed, vowel signs kept), then pooled word error rate (WER) and character error rate (CER) with `jiwer`, and a
   95% bootstrap interval over clips.
4. **Where it fails.** Error rate on numbers, Latin-script words and other words; WER by sentence length; runaway
   outputs; the most common word swaps; speed (seconds of audio per second of compute).
5. **Sanity checks.** Before the headline, the notebook prints `!! SANITY CHECK FAILED … Do NOT post` if: any
   language has fewer than 100 usable clips; references aren't in the expected script (wrong config or TSV parse);
   more than 5% of clips have implausible durations; a model failed to load; a WER is outside 0–500%;
   `whisper-large-v3-turbo` English WER is above 15% on read speech (pipeline broken); Gujarati beats English
   (contradicts published FLEURS results); the Gujarati fine-tune scores worse than 2× the 18.98% WER its authors
   report for the base variant; the run used the CPU fallback; or smoke-test mode is on. Robustness variants:
   mean per-clip WER and a split by speaker gender.
6. **Outputs.** `ft09_transcripts.csv`, `ft09_summary.csv`, `ft09_results.png`, `ft09_speed.png`,
   `ft09_failures.png`, a Gradio demo (record or upload a clip; `share=True`, non-blocking), `ft09_video.mp4`
   (1080×1080, 30 fps, 58 s timeline saved at 1.5×, H.264), `ft09_cover.png` (1080×1350), and the filled LinkedIn
   and X posts with character counts.

## Data, models and licences

| Item | Source | Licence | Login |
|---|---|---|---|
| FLEURS test split, `gu_in` / `hi_in` / `en_us` | <https://huggingface.co/datasets/google/fleurs> (Google) | CC BY 4.0 | No (not gated, checked 19 Nov 2026) |
| `openai/whisper-small` (~0.24B) | Hugging Face | MIT | No |
| `openai/whisper-large-v3-turbo` (~0.81B) | Hugging Face | MIT | No |
| `facebook/mms-1b-all` (~1B) | Hugging Face | **CC-BY-NC 4.0, non-commercial** | No |
| `vasista22/whisper-gujarati-small` (~0.24B) | Hugging Face | Apache 2.0 | No |
| Noto Sans Gujarati, Noto Sans Devanagari, Bricolage Grotesque, IBM Plex | Google Fonts / brand kit | SIL OFL 1.1 | No |

- The FLEURS audio (about 0.5 GB per language) is downloaded at run time and is not redistributed here.
- `vasista22/whisper-gujarati-small` was fine-tuned on FLEURS **train + dev** (per the model family's card), so the
  test clips are held out but match its training domain. Treat its number as a best case; the notebook also
  reports the best general multilingual model separately.
- **Context fact used in the post.** Census 2011 recorded 5,54,92,554 people in India with Gujarati as their mother
  tongue (Census of India 2011, language data).

## How to run

1. Click the Colab badge, then Runtime → Change runtime type → **T4 GPU**, then Runtime → **Run all**.
2. Expect about 15–20 minutes: installs (~1 min), FLEURS audio (~1.6 GB) and models (~6 GB), about 1,050
   transcriptions, and the video (~1–2 min).
3. Read the **Results** cell. If it prints `!! SANITY CHECK FAILED`, don't post. Fix the cause first.
4. On Kaggle, turn on GPU T4 and Internet in the notebook settings.

`FT09_SMOKE_TEST=1` (environment variable, off by default) runs the notebook without internet or a GPU: a few
synthetic noise clips with sentences we wrote, and stand-in "models" that corrupt the reference at made-up rates. It
exists only to check that the notebook runs; its output is labelled as not real and must never be posted.

## Limitations

- FLEURS is read speech from adult volunteers on a good microphone. Phone audio, noise, spontaneous speech,
  code-mixing and dialects (Kathiawadi, Surti and others) will be harder. The result is a ceiling, not what a call
  centre would see.
- Up to 150 clips per language: differences of a few points between models sit inside the bootstrap interval.
- WER depends on the normaliser. Numbers spoken as words and written as digits count as errors; CER is printed too.
- Whisper is told the language. Detecting Gujarati first is a separate source of error not measured here.
- `facebook/mms-1b-all` is non-commercial. Check every model card before commercial use.

## Files

- `ft09_gujarati_speech_small_model.ipynb`: the notebook (no outputs)
- `post_linkedin.md`, `post_x.md`: post templates with `{placeholders}`, filled in by the notebook
