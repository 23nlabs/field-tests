# 23N Field Tests #10 · Gujarat's reservoirs, measured from space

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23nlabs/field-tests/blob/ft10-reservoirs-from-space/ft10-reservoirs-from-space/ft10_reservoirs_from_space.ipynb)

> **Status: built, not yet run on real data.** The notebook has run end to end only in smoke-test mode
> (synthetic images and synthetic bulletins, no internet). The CWC PDF parser was tested offline on a PDF built
> from rows of the 10 Oct 2024 bulletin. There are no results yet: run it on Colab and check the sanity checks
> before posting. The badge points at the `ft10-reservoirs-from-space` branch; switch it (and `REPO_REF` in the
> config cell) to `main` after merging.

**Question.** How full are Sardar Sarovar, Ukai, Kadana and Dharoi each month, measured from the area of open water
in Sentinel-2 images? And does that move with the storage the Central Water Commission (CWC) publishes?

**Headline (computed at runtime, never hard-coded):**
"From the 2024 post-monsoon peak to the 2025 pre-monsoon low, the open-water area measured by Sentinel-2 changed by
A% at Sardar Sarovar, B% at Ukai, C% at Kadana, D% at Dharoi (estimate)", plus "Satellite area moves with CWC's
published storage: median rank correlation ρ over N reservoirs". The video and cover lead with the reservoir whose
area changed most.

**Documented fact the post leads with.** CWC's weekly bulletin of 10 Oct 2024 lists 17 Gujarat reservoirs with
17.964 BCM of live capacity at full reservoir level (Table 01,
[fb10102024.pdf](https://cwc.gov.in/sites/default/files/fb10102024.pdf)).

Independent study on public data by 23N AI Labs. The reservoirs are used only as places: this says nothing about any
dam authority, water board or ministry, and implies no affiliation with any of them. Water area is not storage
volume; all numbers are estimates.

## What the notebook does

1. **Windows and points.** One lon/lat window per reservoir, drawn generously around it, and one published point:
   Sardar Sarovar dam 21.8303° N, 73.7472° E (Wikipedia); Ukai reservoir 21.3235° N, 73.7073° E
   ([DAHITI id 238](https://dahiti.dgfi.tum.de/en/238/)); Kadana dam 23.3073° N, 73.8273° E (Wikipedia); Dharoi dam
   24.0044° N, 72.8536° E (Wikipedia).
2. **Images.** Searches the Planetary Computer STAC API (`sentinel-2-l2a`) for 2022–2025, tiles with ≤ 60 % cloud;
   for each reservoir and month, tries the two clearest dates whose tiles cover the window, and reads B03, B11 and
   SCL at 60 m in UTM 43N (`odc-stac`, overviews only). Reading is round-robin across months, capped by
   `TIME_BUDGET_MIN` (15 min). Scenes are cached in `ft10_scenes.pkl`.
3. **Baseline 04.00.** From 25 Jan 2022 ESA adds +1000 to L2A reflectances; the notebook removes it (by the item's
   `s2:processing_baseline` if present, else by date, as in the Planetary Computer's own example) and prints the
   baselines by year.
4. **Water.** MNDWI = (B03 − B11)/(B03 + B11) > 0, with SCL cloud, shadow and cirrus masked.
5. **Zone.** Pixels that are water in ≥ 5 % of their clear looks, widened 2 pixels, split into connected bodies;
   the reservoir is every body within 5 km of its point. A month counts only if ≤ 5 % of the zone is cloud or missing.
6. **Measures.** Area (km²) per month; fill index = % of the largest area in the run; dry-season drawdown = smallest
   area in Mar–Jun 2025 vs the largest in Sep–Dec 2024 (earlier cycles printed too).
7. **CWC check.** Downloads 38 weekly bulletins whose URLs were found on cwc.gov.in (2022–2025), and, with
   `CWC_PROBE`, tries CWC's file-name patterns for one Thursday in each month without one (3 min cap). Each
   reservoir's row is read from the PDF text and kept only if its live capacity matches the CWC value (±10 %).
   Bulletin and image are paired if ≤ 12 days apart; Spearman rank correlation per reservoir.
8. **Sanity checks.** Before the headline the notebook prints `!! SANITY CHECK FAILED … Do NOT post` if: a
   reservoir has < 18 clear months; the largest area is outside 50–120 % of the documented surface area (Sardar
   Sarovar 375 km², Ukai ~520 km², Dharoi 107 km²); the fill index is < 85 % near a documented full date (Sardar
   Sarovar full on 17 Sep 2023 and 1 Oct 2025; Ukai 100 % on 10 Oct 2024); Apr–Jun area is not below Oct–Dec; the
   area grows through the dry season or shrinks > 90 %; MNDWI and SCL water areas differ by a median > 35 % (offset
   problem); a scene after 25 Jan 2022 kept its +1000 offset; satellite and CWC move in opposite directions; or
   smoke-test mode. It notes: a zone touching its window edge (area underestimated), threshold variants (MNDWI > −0.1
   and > 0.1) or the SCL water class moving the drawdown by > 15 points, a weak CWC correlation (ρ < 0.5), and thin
   CWC matching.
9. **Outputs.** `ft10_monthly.png`, `ft10_cwc.png`, `ft10_maps.png`, a Gradio demo (reservoir + month → water map
   and series), `ft10_video.mp4` (1080×1080, 30 fps, 58 s timeline saved at 1.5×, H.264), `ft10_cover.png`
   (1080×1350), and the filled LinkedIn and X posts with character counts.

## Data and licences

| What | Source | Licence / login |
|---|---|---|
| Sentinel-2 L2A (B03, B11, SCL), 2022–2025 | Microsoft Planetary Computer STAC, collection `sentinel-2-l2a`, `https://planetarycomputer.microsoft.com/api/stac/v1` | Copernicus Sentinel data terms: free, full and open, commercial use allowed; attribution "Contains modified Copernicus Sentinel data 2022–2025". **No account, no key**: `planetary-computer` gets a free anonymous token |
| Reservoir storage | CWC weekly bulletins (PDF), `https://cwc.gov.in/sites/default/files/…` and one from `rsms.cwc.gov.in` | Public Government of India documents, cited as the source; no login |
| Documented facts | Sardar Sarovar: 375.33 km² surface area ([Wikipedia](https://en.wikipedia.org/wiki/Sardar_Sarovar_Dam)), 37,000 ha ([sardarsarovardam.org](https://sardarsarovardam.org/dam-reservoir.aspx)), full at 138.68 m on 17 Sep 2023 and 1 Oct 2025 ([DeshGujarat 2023](https://deshgujarat.com/2023/09/17/sardar-sarovar-narmada-dam-achieves-full-storage), [2025](https://deshgujarat.com/2025/10/01/sardar-sarovar-narmada-dam-achieves-100-percent-storage-138-68-m-full-level/)); Ukai water spread about 52,000 ha (Wikipedia via Wikiwand); Dharoi 107 km² ([Wikipedia](https://en.wikipedia.org/wiki/Dharoi_dam)); live capacities from the CWC bulletin of 10 Oct 2024 | Facts |
| Model | none: a spectral index, a threshold and connected components, written in the notebook | — |

Checked on 21 Nov 2026 (from web pages; the build environment could not reach the Planetary Computer or cwc.gov.in):
the `sentinel-2-l2a` collection lists assets B03 (10 m), B11 (20 m) and SCL (20 m); the 10 Oct 2024 bulletin is a
text PDF with columns FRL, current level, live capacity at FRL, current live storage, date, % of capacity; the
Gujarat rows read UKAI, SABARMATI(DHAROI), KADANA, SARDAR SAROVAR. Not checked: that every listed bulletin still
downloads, that older (2022) and newer (`rsms.cwc.gov.in`) bulletins use the same column order (the parser finds
the capacity by value, then takes the next number as storage, so a different order is rejected rather than
misread), whether items carry `s2:processing_baseline`, and the real read time per scene.

## How to run

1. Click the Colab badge, then Runtime → **Run all**. CPU is fine; no keys.
2. Expect roughly 15–25 minutes: install (~1 min), the searches (~1–2 min), the scene reads (capped at 15 min), the
   CWC bulletins (~1–4 min) and the video (~1 min). Progress lines print seconds per scene; a re-run uses the cache.
3. Read the **Results** cell. If it prints `!! SANITY CHECK FAILED`, don't post. Fix the cause first.
4. Look at the peak/low maps: the amber zone should follow the reservoir's shore, without rivers or other lakes, and
   clouds should be grey, not water. If a zone touches its window edge, widen the window in `RESERVOIRS`.
5. On Kaggle, turn on Internet in the notebook settings.

`FT10_SMOKE_TEST=1` (environment variable, off by default) runs the notebook without internet on synthetic images
and bulletins. It exists only to check that the notebook runs; its output is labelled as not real and must never be
posted.

## Limitations

- **Area, not volume.** A gorge reservoir can lose storage with little change in area; a shallow one the reverse.
  The fill index is a % of the largest area seen, not of live capacity.
- **Clouds.** Most monsoon months are dropped; the rise is seen late and the peak can be missed by weeks.
- **One image a month at 60 m.** Narrow arms and shallow edges are missed or mixed; floating weeds and shadow can
  hide water; wet soil can look like water.
- **Windows.** Sardar Sarovar's backwater runs 214 km upstream; if its zone touches the window edge the area is an
  underestimate, and the notebook says so.
- **Zone from the run.** A record-high shoreline would be partly outside it.
- **CWC parsing.** File names vary, so some weeks are missing; rows are kept only when the capacity matches.

## Files

- `ft10_reservoirs_from_space.ipynb`: the notebook (no outputs)
- `post_linkedin.md`, `post_x.md`: post templates with `{placeholders}`, filled in by the notebook
