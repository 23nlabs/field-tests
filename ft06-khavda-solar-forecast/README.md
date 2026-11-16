# 23N Field Tests #06 · Tomorrow's sun at Khavda

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23nlabs/field-tests/blob/ft06-khavda-solar-forecast/ft06-khavda-solar-forecast/ft06_khavda_solar_forecast.ipynb)

> **Status: built, not yet run on real data.** The notebook has been executed end to end only in smoke-test mode
> (synthetic weather and a stand-in forecaster, no internet). There are no results yet. The badge and raw-file
> links point at the `ft06-khavda-solar-forecast` branch until it is merged.

**Question.** Can a small open time-series model forecast tomorrow's solar output at the Khavda renewable energy park
in Kutch better than "same as yesterday", and what does the difference save in grid deviation charges for 1 GW?

**Headline (computed at runtime, never hard-coded):**
"A 48M-parameter open model cut estimated deviation charges for a notional 1 GW plant at Khavda from ₹A crore to
₹B crore a year, against "same as yesterday" (2025)." If the model loses, the notebook says so instead.

**Documented fact the post leads with.** Under the CERC (Deviation Settlement Mechanism and Related Matters)
Regulations 2024, Reg 8(4), the free deviation band for solar sellers narrowed from ±10 % to ±5 % from
1 April 2026 (CERC Statement of Reasons, para 7.65; CERC order on the value of X, 2026).

Independent study on public data by 23N AI Labs. "Khavda" is used only as a location: the notebook models a notional
plant, not any real one, and implies no affiliation with any developer, operator, utility, regulator or government
body. All money figures are estimates.

## What the notebook does

1. **Weather.** Downloads hourly ERA5 reanalysis for 24.117° N, 69.350° E (the park's coordinates in its
   Wikipedia infobox), 2021–2025: `shortwave_radiation` (GHI, W/m², preceding-hour mean) and `temperature_2m`,
   from the Open-Meteo Historical Weather API with `models=era5` and `timezone=Asia/Kolkata`.
2. **Cross-check.** Downloads NASA POWER daily `ALLSKY_SFC_SW_DWN` for the same point and compares the mean.
3. **Plant.** Converts weather to the AC output of a notional 1 GW plant with a stated PV model (DC/AC 1.25,
   performance ratio 0.80, −0.35 %/°C, NOCT 45 °C, clipped at 1,000 MW).
4. **Forecasts.** For every day of 2025, from data up to midnight, three next-day schedules: persistence ("same as
   yesterday"), a 7-day average profile, and `amazon/chronos-bolt-small` (median of its quantile forecast,
   28 days of context, zero-shot).
5. **Charges.** Applies CERC DSM 2024 Reg 8(4) for solar sellers: deviation as % of available capacity (X = 100 %
   in FY 2026-27); up to 5 % no loss; 5–10 % a loss of 10 % of the contract rate; beyond 10 % a loss of 100 %
   (under-injection paid at 200 %, over-injection received at 0 %). Contract rate ₹2.60/kWh (assumption).
6. **Robustness.** The same test on 2024; the old ±10/15 % bands; X = 90 % (FY 2027-28); monsoon vs the rest of
   the year.
7. **Sanity checks.** Before the headline the notebook prints `!! SANITY CHECK FAILED … Do NOT post` if: an
   hour count is wrong or many hours are missing; mean GHI is outside 4.8–6.8 kWh/m²/day; GHI exceeds
   1,250 W/m²; the sunniest hour is not 12:00–14:00 IST (time-zone bug); capacity factor is outside 15–30 %; any
   year's GHI differs from the median year by more than 8 % (data-version break); Open-Meteo and NASA POWER
   disagree by more than 15 %; persistence error is outside 2–30 % of capacity; a charge exceeds revenue; the model
   cuts charges by more than 70 % (leakage?); the model is far worse than the 7-day average (misuse?); or
   smoke-test mode is on. A change of sign between 2024 and 2025 is printed as a robustness warning.
8. **Outputs.** `ft06_results.png`, `ft06_week.png`, a Gradio demo (pick a day, see the schedules and the
   charge), `ft06_video.mp4` (1080×1080, 30 fps, 58 s, H.264), `ft06_cover.png` (1080×1350), and the filled
   LinkedIn and X posts with character counts.

## Data, rules and licences

| What | Source | Licence / login |
|---|---|---|
| Hourly GHI and temperature, 2021–2025 | ERA5 (Copernicus C3S) via Open-Meteo Historical Weather API, `https://archive-api.open-meteo.com/v1/archive` | **CC BY 4.0**, attribution "Weather data by Open-Meteo.com". No key, no login (free tier is for non-commercial use) |
| Daily GHI cross-check | NASA POWER daily point API, `https://power.larc.nasa.gov/api/temporal/daily/point` | NASA open data, no key; NASA asks for acknowledgement |
| Deviation rule | CERC DSM Regulations 2024, Reg 8(4) and Statement of Reasons (<https://www.cercind.gov.in/Regulations/SOR192.pdf>); X trajectory per CERC's 2026 order (reported by Energetica India, 1 Apr 2026) | Public regulation. The regulations are under challenge in the Delhi High Court |
| Contract rate ₹2.60/kWh | Lowest tariff in NTPC's 1.5 GW ISTS solar auction, Tranche I (Mercom, 4 Jan 2024); also FT01's tariff | Assumption, change it in the config cell |
| Site coordinates | Gujarat Hybrid Renewable Energy Park, Wikipedia infobox | — |
| Model | `amazon/chronos-bolt-small` (48M parameters), via `pip install chronos-forecasting` | **Apache 2.0**, not gated (checked 16 Nov 2026) |

The Open-Meteo, NASA POWER and Hugging Face downloads could not be tested from the build environment (its network
is restricted). The endpoints and parameter names follow the providers' documentation as of 16 Nov 2026.

## How to run

1. Click the Colab badge, then Runtime → **Run all**. CPU is fine; a T4 makes the model step faster.
2. Expect about 3–6 minutes: install (~1 min), weather download (one request, 43,824 hours), two years of
   365 forecasts with a 48M model, and the video (~1–2 min).
3. Read the **Results** cell. If it prints `!! SANITY CHECK FAILED`, don't post. Fix the cause first.
4. On Kaggle, turn on Internet in the notebook settings.

`FT06_SMOKE_TEST=1` (environment variable, off by default) runs the notebook without internet: a synthetic
clear-sky-plus-clouds weather series and a stand-in forecaster (a blend of the two baselines) replace the download
and Chronos. It exists only to check that the notebook runs; its output is labelled as not real and must never be
posted.

## Limitations

- **Reanalysis, not meter data.** Output is modelled from ERA5 at a ~25 km grid cell. ERA5 smooths clouds, so real
  plants are harder to forecast and real charges are probably higher for every method. The comparison between
  methods is the finding, not the rupee level.
- **Hourly, not 15-minute.** Each hour counts as four identical DSM blocks, which hides intra-hour swings.
- **No intraday revisions.** The schedule is fixed at midnight and never revised, so charges are an upper bound for
  this forecaster. The real day-ahead gate closes earlier than midnight, which would make forecasts harder.
- **Simple PV model.** Horizontal irradiance, no tilt, tracking, outages or curtailment; available capacity is
  1,000 MW in every block.
- **History-only model.** Chronos-Bolt-Small sees only past output. A model fed a numerical weather forecast would
  likely do better; this test asks what a small, history-only model can do.
- **Rule and price are assumptions**, and real PPAs differ. Change the named variables and re-run.

## Files

- `ft06_khavda_solar_forecast.ipynb`: the notebook (no outputs)
- `post_linkedin.md`, `post_x.md`: post templates with `{placeholders}`, filled in by the notebook
