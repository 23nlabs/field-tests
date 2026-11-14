# 23N Field Tests #01 — The Solar Dust Tax

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23nlabs/field-tests/blob/main/ft01-solar-dust-tax/ft01_solar_dust_tax.ipynb)

**Question:** How much revenue does dust (soiling) cost a large solar park in Kutch, Gujarat — and how much does
washing more often win back?

**Headline (computed at runtime, estimate):** *"Dust costs a 1 GW solar park in Kutch ~₹X crore a year if left
uncleaned; cleaning every 7 days recovers ~₹Y crore."*

An independent study on public data by 23N AI Labs. Not affiliated with, or endorsed by, any park developer,
operator, utility or government body. Khavda is used only as a location.

## What the notebook does
1. **Computer vision** — fine-tunes an ImageNet ResNet18 (torchvision) to predict % power loss from a photo of a
   panel, on the DeepSolarEye dataset. Train/test split is by capture *day* (every 5th of the 15 days is held out) to avoid
   leakage between frames taken 5 s apart. Reports MAE in percentage points and a median-predictor baseline.
2. **Time series** — pulls daily `ALLSKY_SFC_SW_DWN` (kWh/m²/day) and `PRECTOTCORR` (mm/day) for 23.90°N, 69.70°E
   (Khavda, Kutch) for the last full calendar year from the NASA POWER API (no key).
3. **Money** — 1 GW × daily irradiance × performance ratio → daily energy; a Kimber-style soiling model (linear
   build-up, reset by heavy rain or a scheduled wash) → energy and ₹ lost for no washing and washing every 7 / 14 /
   30 days; break-even wash cost; sensitivity to dust rate and tariff.
4. **Gradio demo** — upload a panel photo → predicted % loss → ₹ lakh per MW per year.
5. **Video + cover** — `ft01_video.mp4` (1080×1080, 30 fps, 58 s, H.264, burned-in captions) and
   `ft01_cover.png` (1080×1350); **post text** filled with the run's numbers.

## Data and licences
| Data | Source | Licence / terms |
|---|---|---|
| DeepSolarEye, 45,754 images (192×192) with power-loss and irradiance labels in file names | Mehta et al., *DeepSolarEye*, WACV 2018 ([arXiv 1710.03811](https://arxiv.org/abs/1710.03811), [project page](https://deep-solar-eye.github.io)). Original: Google Drive folder linked from the project page. The notebook fetches the identical `PanelImages/` folder from the public GitHub mirror [ThomasGust/SoilingNet](https://github.com/ThomasGust/SoilingNet) at pinned commit `87c4ed6b15` via sparse checkout (~30–60 s, no login). | CC BY-NC-SA 2.0 per the project page (non-commercial, share-alike, attribution). The mirror has no licence file of its own; the original terms apply. |
| Daily irradiance and precipitation | [NASA POWER](https://power.larc.nasa.gov/) daily point API, community `RE` | Free, no key; NASA requests acknowledgement. |

## Assumptions (all are named variables in the first code cell)
| Variable | Default | Basis |
|---|---|---|
| `PARK_MW` | 1000 | 1 GW (DC) reference park |
| `PERFORMANCE_RATIO` | 0.80 | Typical utility-scale PR excluding soiling (assumption) |
| `TARIFF_RS_PER_KWH` | 2.60 | GUVNL solar auctions: ₹2.60/kWh (250 MW, Mar 2025); ₹2.34–2.60/kWh (Phase XXVIII, Mar 2026) |
| `SOILING_RATE_PCT_PER_DAY` | 0.37 | Valerino et al., *Solar Energy* 204 (2020) 307–315, field measurement in Gandhinagar: 0.37 ± 0.09 %/day |
| `RAIN_CLEAN_MM`, `GRACE_DAYS`, `MAX_SOILING_PCT` | 6 mm, 14 d, 30 % | Defaults of `pvlib.soiling.kimber` |
| `CLEANING_INTERVALS` | 7, 14, 30 days | Scenarios compared |

## How to run
* **Colab (recommended):** click the badge → Runtime → Change runtime type → **T4 GPU** → Runtime → Run all.
  ~10–14 min. The video and cover download automatically at the end.
* **Kaggle:** New notebook → File → Import notebook → this `.ipynb`. In the right panel turn **Internet on** (needs a
  phone-verified Kaggle account) and pick a GPU accelerator. Outputs land in `/kaggle/working`.
* **CPU only:** works; the notebook automatically trains on a 6,000-image subsample (~20 min total).

## Outputs
`ft01_video.mp4`, `ft01_cover.png`, `ft01_posts_filled.txt`, `ft01_examples/*.jpg`, and a public Gradio link.

## Limitations
See section 8 of the notebook. In short: the ₹ headline comes from a literature soiling rate (Gandhinagar) plus
NASA sunlight, not from CNN inference on Kutch imagery; DeepSolarEye is a single rooftop rig with patchy,
mostly artificial soiling; "never washed" is a counterfactual; the yield model is deliberately simple; the trained
weights inherit a non-commercial licence.

## Citations
* S. Mehta, A. P. Azad, S. A. Chemmengath, V. Raykar, S. Kalyanaraman. *DeepSolarEye: Power Loss Prediction and
  Weakly Supervised Soiling Localization via Fully Convolutional Networks for Solar Panels.* WACV 2018.
* M. Valerino et al. *Seasonal photovoltaic soiling: Analysis of size and composition of deposited particulate
  matter.* Solar Energy 204 (2020) 307–315.
* NASA POWER Project, NASA Langley Research Center. https://power.larc.nasa.gov/
* M. Kimber et al., soiling model as implemented in `pvlib.soiling.kimber`.
