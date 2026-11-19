# 23N Field Tests #08 · Industrial air, measured from space

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23nlabs/field-tests/blob/main/ft08-industrial-air-from-space/ft08_industrial_air_from_space.ipynb)

> **Status: built, not yet run on real data.** The notebook has run end to end only in smoke-test mode
> (synthetic satellite pixels and a synthetic ground series, no internet). The HDF5 slice reader was tested offline
> on a synthetic file with the Level-2 NO₂ layout. There are no results yet: run it on Colab and check the sanity
> checks before posting.

**Question.** How has nitrogen dioxide (NO₂) over the Vapi, Ankleshwar and Dahej industrial estates changed between
2019 and 2025, measured from space? And do the satellite readings move with the ground monitors near the estates?

**Headline (computed at runtime, never hard-coded):**
"From 2019 to 2025, tropospheric NO₂ measured by Sentinel-5P changed by X% over Vapi, Y% over Ankleshwar, Z% over
Dahej (matched months, estimate); the south Gujarat regional level changed R%." The video and cover lead with the
estate that changed most.

**Documented fact the post leads with.** In the Central Pollution Control Board's *Comprehensive Environmental
Assessment of Industrial Clusters* (EIAS/5/2009-10, December 2009), Ankleshwar ranked 1st and Vapi 2nd of 88
industrial clusters on the Comprehensive Environmental Pollution Index (CEPI 88.50 and 88.09; Table 8).
[Copy of the report](https://oldiwp.indiawaterportal.org/sites/default/files/iwp2/comprehensive_environmental_assessment_of_industrial_clusters.pdf).

Independent study on public data by 23N AI Labs. The estates are used only as locations: this says nothing about
any company, estate authority or regulator, and implies no affiliation with any of them. A satellite column is not
a ground concentration; all numbers are estimates.

## What the notebook does

1. **Places.** Three 10 km circles (an assumption) around published points: Vapi town (20.3667° N, 72.9000° E),
   Ankleshwar notified industrial area "Anklesvar INA" (21.6269° N, 73.0119° E) and Dahej railway station inside
   the Dahej industrial area (21.7091° N, 72.5895° E), all from Wikipedia. A regional box over south Gujarat and
   the Gulf of Khambhat, 72.2–73.5° E × 20.0–22.2° N, gives the "regional level" (median pixel).
2. **Files.** Searches the Planetary Computer STAC API for every Sentinel-5P L2 NO₂ file over the box in 2019–2025,
   keeps reprocessed (RPRO) and offline (OFFL) files, one per orbit (RPRO preferred), and records each file's
   collection and processor version from its file name.
3. **Read only what's needed.** For `DAYS_PER_MONTH` = 8 evenly spaced days per month, it opens each orbit file over
   HTTP (h5py + fsspec) and reads only the scanlines that cross the box. Days are read round-robin across months, so
   if `TIME_BUDGET_MIN` (16 min) stops the reading, every month is still covered evenly. Pixels are cached in
   `ft08_pixels.parquet`.
4. **Quality.** Keeps pixels with `qa_value ≥ 0.75` (the producer's recommendation for tropospheric NO₂); a
   robustness variant uses 0.5.
5. **Aggregate.** Per overpass, the mean of good pixels within 10 km of each estate (≥ 2 pixels); monthly means;
   the regional median per overpass; the estate's enhancement over the region.
6. **Change.** 2019 vs 2025 on **matched months** (months with data in both years), so a cloudier year can't look
   cleaner. Also: a Theil–Sen trend over 2019–2025 yearly means (fixed basket of months), 2-year averages (2019 and
   2021 vs 2024 and 2025, leaving out the lockdown year), qa ≥ 0.5, and enhancement over the region.
7. **Ground check (optional).** With a free OpenAQ key (`OPENAQ_API_KEY`, environment variable or Colab secret),
   finds NO₂ monitors within 15 km of each estate (OpenAQ API v3 `/locations`), downloads daily means
   (`/sensors/{id}/days`, days with ≥ 75 % hourly coverage), builds monthly means (≥ 10 days) and correlates them
   with the satellite at each monitor's location (within-station, standardised). Without a key it skips itself and
   the post says so.
8. **Sanity checks.** Before the headline the notebook prints `!! SANITY CHECK FAILED … Do NOT post` if: an estate
   has fewer than 40 usable overpasses in any year; fewer than 6 matched months; a yearly mean outside 0.3–40 ×10¹⁵
   molec/cm² (unit or reading error); a change beyond ±70 %; a change of 10 % or more whose sign disagrees with the
   7-year trend or with the 2-year averages; the regional level swinging by more than ±40 % (processing change);
   April–May 2020 (lockdown) above 110 % of April–May 2019 (contradicts the documented lockdown dip); winter not
   above the monsoon (contradicts the known seasonal cycle); different **processor major versions** in 2019 and 2025
   (a version break can look like a trend); any processor 01.xx file; satellite and ground moving in opposite
   directions; or smoke-test mode. It notes sign flips under qa ≥ 0.5 or enhancement, a weak ground correlation, and
   minor version changes.
9. **Outputs.** `ft08_monthly.png`, `ft08_maps.png`, `ft08_ground.png` (if the ground check ran), a Gradio demo (pick
   a year: map plus monthly series), `ft08_video.mp4` (1080×1080, 30 fps, 58 s timeline saved at 1.5×, H.264),
   `ft08_cover.png` (1080×1350), and the filled LinkedIn and X posts with character counts.

## Data and licences

| What | Source | Licence / login |
|---|---|---|
| Sentinel-5P TROPOMI L2 NO₂ (RPRO + OFFL), 2019–2025 | Microsoft Planetary Computer STAC, collection `sentinel-5p-l2-netcdf`, asset `no2`, `https://planetarycomputer.microsoft.com/api/stac/v1` | Copernicus Sentinel data terms: free, full and open, commercial use allowed; attribution "Contains modified Copernicus Sentinel data 2019–2025". **No account, no key**: `planetary-computer` gets a free anonymous token |
| Ground NO₂ monitors (optional) | OpenAQ API v3, `https://api.openaq.org/v3` | **Free OpenAQ account and API key needed** (header `X-API-Key`). Each station's licence is printed with its data; check it before quoting |
| CEPI ranking | CPCB, *Comprehensive Environmental Assessment of Industrial Clusters*, Dec 2009, Table 8 | Public government report, used as a fact |
| Estate points | Wikipedia coordinates (Vapi; Anklesvar INA; Dahej railway station) | Facts |
| Model | none: averages, a Theil–Sen slope and a correlation, written in the notebook | — |

Checked on 18 Nov 2026: the collection is live (items dated 17 Nov 2026, collection identifier `03`), its NO₂ files
are netCDF4/HDF5 with `PRODUCT/latitude`, `longitude`, `qa_value` and `nitrogendioxide_tropospheric_column`
(mol m⁻²). The TROPOMI site says the RPRO set covers 30 Apr 2018 – 25 Jul 2022 (processor 02.04.00, collection 03)
and recommends `qa_value > 0.75`. Not checked: whether the Planetary Computer holds RPRO files for all of 2019–2022,
and which processor versions its OFFL files carry in 2025 (processor 03.x exists). The notebook prints the version
table and stops the headline on a major-version break; if that happens, compare within one version or read the
release notes for the size of the change. The Planetary Computer and OpenAQ could not be reached from the build
environment (restricted network), so the search, download and API calls are untested against the live services.

## How to run

1. Optional: create a free account and API key at openaq.org and add it in Colab as a secret
   named `OPENAQ_API_KEY` (key icon in the left bar; allow notebook access). Without it the ground check is skipped.
2. Click the Colab badge, then Runtime → **Run all**. CPU is fine.
3. Expect roughly 15–25 minutes: install (~1 min), the file search (~1–2 min), reading ~670 orbit slices
   (capped by `TIME_BUDGET_MIN = 16`), and the video (~1–2 min). The first progress lines print seconds per file;
   if it is slow, lower `DAYS_PER_MONTH`. A re-run uses the cache.
4. Read the **Results** cell. If it prints `!! SANITY CHECK FAILED`, don't post. Fix the cause first. Read the
   processor-version table in the Data cell either way.
5. Look at the maps: the hotspots should sit on the circles, and the sea should be low. Check the 2020 lockdown dip
   in the monthly chart.
6. On Kaggle, turn on Internet in the notebook settings (and add the key as a Kaggle secret or environment variable).

`FT08_SMOKE_TEST=1` (environment variable, off by default) runs the notebook without internet on synthetic pixels
and a synthetic ground series. It exists only to check that the notebook runs; its output is labelled as not real
and must never be posted.

## Limitations

- **A column, not a concentration.** It can't be compared with the ambient standard in µg/m³; it is good for
  changes and comparisons.
- **One look a day, about 13:30 local time.** Night-time and morning emissions are not seen.
- **Clouds.** `qa_value ≥ 0.75` removes most monsoon days; yearly levels are mostly dry-season levels.
- **Weather and neighbours.** Wind and boundary-layer height change the column from year to year. Vapi's circle
  includes the town, Ankleshwar's reaches Bharuch city, Dahej's includes the port; Surat is in the regional box.
- **Versions and sampling.** Retrieval versions change; 8 days a month is a sample, not every day.
- **Ground check** is optional, correlational, and limited by short, gappy monitor records.

## Files

- `ft08_industrial_air_from_space.ipynb`: the notebook (no outputs)
- `post_linkedin.md`, `post_x.md`: post templates with `{placeholders}`, filled in by the notebook
