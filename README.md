# 23N Field Tests

**Small, repeatable, real-world AI studies on open data, from [23N AI Labs](https://23nlabs.com), Gandhinagar.**

Each Field Test takes one industry and one open dataset and asks one question. The notebook runs end-to-end on a free Colab or Kaggle GPU, computes a headline number, launches a live demo, and renders its own 60-second video.

| # | Field Test | Industry | Techniques | Notebook |
|---|---|---|---|---|
| 01 | The Solar Dust Tax | Renewable energy | Computer vision + time series | [ft01-solar-dust-tax](ft01-solar-dust-tax/) |
| 02 | Small Model, Big Factory | Manufacturing | Anomaly detection, edge inference | [ft02-small-model-defects](ft02-small-model-defects/) |
| 03 | Gujarat from Space | Government / economy | Satellite imagery + natural-language Q&A | [ft03-night-lights-gujarat](ft03-night-lights-gujarat/) |
| 04 | Ask India's Payments Data | Finance | Text-to-SQL in Hindi and English with a small open model | [ft04-ask-upi-data](ft04-ask-upi-data/) |

## Latest results (free Colab, 15 Nov 2026)

| # | Headline | Full results |
|---|---|---|
| 01 | *Results to be added from the first Colab run* | [notebook](ft01-solar-dust-tax/) |
| 02 | A ResNet-18 on a ₹45,000 CPU box flags **88% of defects** at **₹0.16 per 1,000 parts** (mean AUROC 0.985, against 0.993 for a 6× larger model) | [results](ft02-small-model-defects/#results-free-colab-t4-15-nov-2026) · [HTML](https://23nlabs.github.io/field-tests/ft02_small_model_defects_executed.html) |
| 03 | From space, **Morbi** grew its night lights **156%** from 2014 to 2021, the fastest in Gujarat (state +57%) | [results](ft03-night-lights-gujarat/#results-free-colab-cpu-15-nov-2026) · [HTML](https://23nlabs.github.io/field-tests/ft03_night_lights_gujarat_executed.html) |
| 04 | A 3B open model answers **16/25** UPI questions: **English 11/12, Hindi 5/13** | [results](ft04-ask-upi-data/#results-free-colab-t4-15-nov-2026) · [HTML](https://23nlabs.github.io/field-tests/ft04_ask_upi_data_executed.html) |

Each folder holds a clean notebook to run (`ftNN_*.ipynb`) and a copy saved with its outputs from the run above (`ftNN_*_executed.ipynb`).

## How to run
1. Open a notebook with its **Open in Colab** badge.
2. Set *Runtime → Change runtime type → T4 GPU* (most notebooks also run on CPU, just more slowly).
3. Click **Runtime → Run all**.
4. You get the headline result, a public Gradio demo link, `ftNN_video.mp4`, a cover image, and ready-to-paste LinkedIn and X post text.

## Principles
- **Open data only.** Each folder's README lists the sources and licences.
- **Computed, not claimed.** Every headline number is calculated at runtime, and its assumptions are named variables you can change.
- **Independent.** These are independent studies on public data. They imply no affiliation with any company or government body mentioned.
- **Honest limits.** Every notebook ends with a section on its limitations.

## Licence
Code: MIT. Datasets keep their own licences. Some (e.g. MVTec AD) are non-commercial.
