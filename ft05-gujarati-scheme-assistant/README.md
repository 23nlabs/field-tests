# 23N Field Tests #05 · Ask about a government scheme, in Gujarati

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23nlabs/field-tests/blob/ft05-gujarati-scheme-assistant/ft05-gujarati-scheme-assistant/ft05_gujarati_scheme_assistant.ipynb)

> **Status: built, not yet run on real data.** The notebook has been executed end to end only in smoke-test mode
> (excerpt snapshot and stand-in models, no internet, no GPU). There are no results yet. The badge and raw-file
> links point at the `ft05-gujarati-scheme-assistant` branch until it is merged.

**Question.** Can a small open model, running for free, answer a citizen's question about a government scheme
accurately from the official documents, in Gujarati as well as in English?

**Headline (computed at runtime, never hard-coded):**
"A 3B open model answered N/15 government-scheme questions correctly in English [and | but only] M/15 in Gujarati,
reading the same official documents on a free GPU."

Independent study on public data by 23N AI Labs. It is not affiliated with or endorsed by any government department
or scheme mentioned here, and nothing in it is advice on eligibility.

## What the notebook does

1. **Documents.** Downloads 8 official documents on 7 schemes (table below). PDFs become text with `pypdf`, web
   pages with BeautifulSoup. Any download that fails or returns under 400 characters falls back to a short excerpt
   from `data/scheme_excerpts.json`, and the notebook prints which source each document came from.
2. **Index.** Splits the text into ~120-word passages (30-word overlap) and embeds them with
   `intfloat/multilingual-e5-small`, so a Gujarati question can find an English passage.
3. **Answer.** For each question, the top 4 passages go to `Qwen/Qwen2.5-3B-Instruct` (fp16, free T4). It must
   answer only from them, in the language of the question, with the exact amount or age and a citation. Without a
   GPU the notebook switches to `Qwen/Qwen2.5-1.5B-Instruct`.
4. **Evaluate.** 15 questions, each asked in English and in Gujarati. Every question has one gold source document
   and gold number(s), such as 6000 for PM-KISAN's annual amount. An answer is correct if it contains every gold
   number, contains no stale number (the 2015 premiums of ₹12 and ₹330), and lists no more than 3 other numbers.
   The scorer reads Gujarati digits, digit-group commas, lakh/crore/thousand in English and Gujarati, English number
   words and Gujarati number words from one to ten.
5. **Oracle variant (robustness).** Every question is asked again with passages from the correct document only.
   This separates search failures from reading or writing failures.
6. **Sanity checks.** Before the headline, the notebook prints `!! SANITY CHECK FAILED … Do NOT post` if any of
   these hold: a gold value is missing from its downloaded source document (the document changed), more than 2
   documents fell back to excerpts, English accuracy is under 40 % or English retrieval under 60 % (the pipeline is
   probably broken), oracle accuracy is clearly below retrieval accuracy (a bug), or smoke-test mode is on.
7. **Outputs.** `ft05_eval_results.csv`, `ft05_results.png`, a Gradio demo (`share=True`, non-blocking),
   `ft05_video.mp4` (1080×1080, 30 fps, 58 s, H.264), `ft05_cover.png` (1080×1350), and the filled LinkedIn and X
   posts with character counts.

## Documents, provenance and licences

| ID | Scheme | Document | Publisher | URL |
|---|---|---|---|---|
| D1 | PM-KISAN | Backgrounder on the 21st instalment (Nov 2025) | PIB | <https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251120700401.pdf> |
| D2 | Sukanya Samriddhi | Backgrounder (Jan 2026) | PIB | <https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/jan/doc2026121762801.pdf> |
| D3 | PMJJBY | "PMJJBY: 10 Years of Empowering Indian Families" (May 2025) | PIB | <https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/may/doc202558551501.pdf> |
| D4 | PM-JAY | "Transforming Healthcare: Six Years of Ayushman Bharat PM-JAY" (Sep 2024) | PIB / MoHFW | <https://static.pib.gov.in/WriteReadData/specificdocs/documents/2024/sep/doc2024923400001.pdf> |
| D5 | Atal Pension Yojana | Scheme page | PFRDA | <https://pfrda.org.in/web/pfrda/schemes/atal-pension-yojana-apy> |
| D6 | PMSBY / PMJJBY / APY | 2015 launch press note (original premiums) | Dept of Financial Services | <https://financialservices.gov.in/sites/default/files/press-release/Press-note-PMSBY-PMJJBY-APY.pdf> |
| D7 | PMSBY / PMJJBY | Premium revision w.e.f. 1 June 2022 | PIB (Ministry of Finance) | <https://pib.gov.in/PressReleasePage.aspx?PRID=1829772> |
| D8 | Vahli Dikri Yojana (Gujarat) | Scheme page | Women and Child Development Dept, Gujarat | <https://wcd.gujarat.gov.in/posts?id=328> |

D6 and D7 are included on purpose. The 2015 note gives the original premiums and the 2022 release the revised ones,
so a question about the *current* premium tests whether the model prefers the newer document.

- **Licence.** These are Government of India and Government of Gujarat publications. They are downloaded at run
  time from the publishers and are not redistributed here. No login is needed. All 8 URLs were readable on 15 Nov 2026. Some government portals
  may refuse requests from outside India, which can affect Colab's servers; the excerpt fallback covers that.
- **`data/scheme_excerpts.json`** holds short excerpts from each document, transcribed on 2026-11-15 with the source
  URL, for use only when a download fails. Quoted phrases are as published; connecting text is ours. A run with
  more than 2 documents from excerpts is flagged as not representative.
- **Models.** `Qwen/Qwen2.5-3B-Instruct`: *Qwen Research* licence, **non-commercial**. `Qwen/Qwen2.5-1.5B-Instruct`
  (CPU fallback): Apache 2.0. `intfloat/multilingual-e5-small`: MIT. The 3B model page showed no gating on 15 Nov 2026; if a download asks for a login, add a free Hugging Face token.
- **Fonts.** Bricolage Grotesque, IBM Plex and Noto Sans Gujarati, all SIL OFL 1.1.
- **Context fact used in the post.** Census 2011 recorded 5,54,92,554 people in India with Gujarati as their mother
  tongue (Census of India 2011, language data).

## How to run

1. Click the Colab badge, then Runtime → Change runtime type → **T4 GPU**, then Runtime → **Run all**.
2. Expect about 10–15 minutes: installs (~1 min), model downloads (~6.5 GB, ~2–3 min), 60 generations (15 questions
   × 2 languages × retrieval and oracle; Gujarati answers are slower because each word costs more tokens), and the
   video (~1–2 min).
3. Read the **Results** cell. If it prints `!! SANITY CHECK FAILED`, don't post. Fix the cause first, for example a
   document that failed to download or changed.
4. On Kaggle, turn on GPU T4 and Internet in the notebook settings.

`FT05_SMOKE_TEST=1` (environment variable, off by default) runs the notebook without internet or a GPU: excerpt
snapshot, TF-IDF retrieval and an extractive stub in place of the models. It exists only to check that the
notebook runs; its output is labelled as not real and must never be posted.

## Limitations

- 15 questions per language over 8 documents is a capability probe, not a benchmark. Every question has a single
  numeric answer, while real citizen questions are vaguer ("am I eligible?") and often mix languages.
- 23N AI Labs wrote the questions and the Gujarati translations. A native speaker's phrasing, dialect or Gujlish
  could give different results. Please report awkward Gujarati.
- The scorer checks numbers, not the words around them. A right number in a wrong sentence still scores.
- The source documents are in English, so the Gujarati condition tests cross-lingual retrieval plus answering in
  Gujarati. It doesn't test Gujarati-language source documents.
- Scheme rules and premiums change. Re-run before quoting a number.

## Files

- `ft05_gujarati_scheme_assistant.ipynb`: the notebook (no outputs)
- `data/scheme_excerpts.json`: fallback excerpts (see provenance above)
- `post_linkedin.md`, `post_x.md`: post templates with `{placeholders}`, filled in by the notebook
