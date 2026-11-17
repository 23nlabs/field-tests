# 23N Field Tests #07 · Ships at anchor, seen by radar

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23nlabs/field-tests/blob/ft07-ships-at-anchor-radar/ft07-ships-at-anchor-radar/ft07_ships_at_anchor_radar.ipynb)

> **Status: built, not yet run on real data.** The notebook has run end to end only in smoke-test mode
> (synthetic radar scenes, no internet), and the GCP-based scene reader was tested offline on a synthetic
> radar-geometry GeoTIFF. There are no results yet. The badge and raw-file links point at the
> `ft07-ships-at-anchor-radar` branch until it is merged.

**Question.** How many ships wait at anchor off Mundra and Kandla in the Gulf of Kutch each week, counted from radar
satellites that see through cloud and the monsoon? And how does the count change in the monsoon months?

**Headline (computed at runtime, never hard-coded):**
"Sentinel-1 radar counted N ships on an average pass in the anchorage waters off Mundra and Kandla in 2025
(estimate); in the monsoon months (Jun–Sep) there were X% more/fewer than in the rest of the year."

**Documented fact the post leads with.** In FY 2024-25 the average pre-berthing detention at Deendayal Port
(Kandla) was 68.78 hours, against 23.38 hours across India's major ports (Ministry of Ports, Shipping and
Waterways, [*Update on Indian Ports Sector up to 31.03.2025*](https://shipmin.gov.in/sites/default/files/Update%20on%20Indian%20Ports%20Sector%20upto%2031.03.2025_0.pdf), Table 23).

Independent study on public data by 23N AI Labs. Mundra and Kandla are used only as locations: this says nothing
about any port operator, shipping line or government body, and implies no affiliation with any of them. All counts
are estimates from a stated detector.

## What the notebook does

1. **Zones.** Mundra: the five anchorage areas (SPM/STS, General A, General B, LNG, VLCC) whose corner coordinates
   are printed in the Mundra *Port Information Booklet*, Section 3.6, reviewed 30 Jun 2025, each as the convex hull
   of its corners plus a 500 m buffer. Kandla: a study box, 69.95–70.15° E × 22.70–22.88° N, that **we** drew over
   open water off Tuna and the Kandla creek mouth. We found no published Kandla anchorage coordinates, so the box is
   an assumption.
2. **Scenes.** Searches the Planetary Computer STAC API for every Sentinel-1 IW GRD scene over the zones in
   2024–2025 and groups slices into passes.
3. **Read only what's needed.** For each pass, reads two small VH windows from the Cloud-Optimised GeoTIFFs at
   ~20 m (via the overview), using the scene's ground control points to resample them onto a 20 m UTM 42N grid.
   Values are uncalibrated DN²; only ratios within one image are used, so calibration differences between
   Sentinel-1A, 1C and 1D do not shift the counts directly.
4. **Mask.** The median of all passes marks land, jetties and fixed structures (anything 6 dB above the typical
   sea); anything touching the mask is not counted.
5. **Detect.** Cell-averaging CFAR: a pixel is a candidate if it is 5× brighter than the mean sea in a 1.2 km window
   (leaving out a 420 m guard window and already-bright pixels). Clusters of 3–600 pixels are ships.
6. **Count.** Ships per pass per zone (passes covering < 90 % of a zone are skipped, never counted as zero), a weekly
   index (mean per pass, summed over both zones), the year mean, and monsoon (Jun–Sep) vs the rest of the year.
7. **Robustness.** 2024 vs 2025; a stricter 8× threshold; ascending vs descending passes; Sentinel-1A vs 1C over the
   same months.
8. **Sanity checks.** Before the headline the notebook prints `!! SANITY CHECK FAILED … Do NOT post` if: fewer
   than 30 usable passes a year per zone; two or more months without any pass; Mundra's mean is outside 0.5–60
   ships per pass; more than 15 % of Mundra's anchorages are masked as land (geolocation error); the Kandla box is
   more than 60 % land; the median detected length is outside 40–400 m; more than half the detections are the
   minimum size (speckle); Sentinel-1A and 1C counts differ by more than ×1.5 (sensor/version break); ascending and
   descending counts differ by more than ×2; the monsoon change is beyond ±80 %; the monsoon change flips sign under
   the stricter threshold; or smoke-test mode is on. It notes (does not block) a sign change between 2024 and 2025
   and any month-to-month jump of more than 3 dB in the sea background.
9. **Outputs.** `ft07_weekly.png`, `ft07_mundra_density.png`, a Gradio demo (pick a pass, see both zones with each
   ship circled), `ft07_video.mp4` (1080×1080, 30 fps, 58 s, H.264), `ft07_cover.png` (1080×1350), and the filled
   LinkedIn and X posts with character counts.

## Data and licences

| What | Source | Licence / login |
|---|---|---|
| Sentinel-1 GRD (IW, VH), 2024–2025 | Microsoft Planetary Computer STAC, collection `sentinel-1-grd`, `https://planetarycomputer.microsoft.com/api/stac/v1` | Copernicus Sentinel data terms: free, full and open, commercial use allowed; attribution "Contains modified Copernicus Sentinel data 2024–2025". **No account, no key**: `planetary-computer` gets a free anonymous SAS token |
| Mundra anchorage corners | Mundra Port Information Booklet, Sec. 3.6, rev. 02, reviewed 30 Jun 2025 (port website) | Public document, coordinates used as facts |
| Kandla–Tuna box | Our assumption (Tuna Port is at 22.91° N, 70.10° E per Wikipedia) | — |
| Pre-berthing detention | Ministry of Ports, Shipping and Waterways, *Update on Indian Ports Sector up to 31.03.2025*, Table 23 | Public government statistics |
| Model | none: a classical CFAR detector written in the notebook | — |

The Planetary Computer could not be reached from the build environment (its network is restricted), so the search
and download are untested against the live service. The code follows the STAC collection's published asset keys
(`vh`, `vv`, Cloud-Optimised GeoTIFF) as of 17 Nov 2026. If the Planetary Computer stops serving
`sentinel-1-grd`, the same scenes are on the Copernicus Data Space Ecosystem (free account needed).

## How to run

1. Click the Colab badge, then Runtime → **Run all**. CPU is fine.
2. Expect roughly 10–25 minutes: install (~1 min), the scene search, reading two small windows from a few hundred
   passes (8 in parallel), the detector (~1 min) and the video (~1–2 min). If it is slow, set `MAX_PASSES = 120`
   in the config cell. The radar stack is cached in `ft07_cache.npz`, so a re-run skips the download.
3. Read the **Results** cell. If it prints `!! SANITY CHECK FAILED`, don't post. Fix the cause first.
4. Before posting, open the Gradio demo and look at a few passes: the circles should sit on ships, not on land
   edges, wakes or wind streaks.
5. On Kaggle, turn on Internet in the notebook settings.

`FT07_SMOKE_TEST=1` (environment variable, off by default) runs the notebook without internet on synthetic sea
clutter and synthetic ships on the same grids. It exists only to check that the notebook runs; its output is
labelled as not real and must never be posted.

## Limitations

- **"Present", not "waiting".** One radar image can't tell a ship at anchor from one moving slowly through the zone.
- **Snapshots every few days**, at fixed times (about 01:00 and 13:00 UTC). The number of satellites changed during
  the period (Sentinel-1C from 2025), which changes how many snapshots a week has, not what each one counts.
- **No ground truth.** AIS isn't open; detections are checked only for plausibility.
- **Detector limits.** Small craft are often missed; ships moored side by side count as one; monsoon winds brighten
  the sea; bright targets on land can leave faint ghost echoes over water.
- **Zones are choices.** Ships told to wait outside the Gulf of Kutch are in neither zone. The Kandla box is ours.

## Files

- `ft07_ships_at_anchor_radar.ipynb`: the notebook (no outputs)
- `post_linkedin.md`, `post_x.md`: post templates with `{placeholders}`, filled in by the notebook
