# 23N Field Tests #11 · Mapping a city flood from radar

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23nlabs/field-tests/blob/ft11-flood-mapping-radar/ft11-flood-mapping-radar/ft11_flood_mapping_radar.ipynb)

> **Status: built, not yet run on real data.** The notebook has run end to end only in smoke-test mode
> (a synthetic radar scene, synthetic buildings and roads, no internet). There are no results yet: run it on Colab and
> check the sanity checks before posting. The Colab badge points at the `ft11-flood-mapping-radar` branch until it is
> merged.

**Question.** How fast can open radar data map a city flood? A case study of Vadodara in August 2024: how much open
floodwater could the first free satellite pass show, and how many buildings and roads were in it?

**Headline (computed at runtime, never hard-coded):**
"Free Sentinel-1 radar mapped X km² of open floodwater in and around Vadodara on <date>, N hours after the Vishwamitri
crossed its danger mark; B OpenStreetMap buildings and R km of road were in or beside it (estimates)."

**Documented facts the post leads with.** On 26 Aug 2024 the Vishwamitri crossed its 26 ft danger mark at about 4 pm,
after 12.44 inches of rain fell on Vadodara between 6 am on 26 Aug and 6 am on 27 Aug; the official gauge then read
35.25 ft for more than 24 hours (DeshGujarat, [*Vishwamitri river flood in Vadodara in August 2024*](https://deshgujarat.com/2024/10/01/vishwamitri-river-flood-in-vadodara-in-august-2024-what-caused-it-how-it-started-progressed-and-ended),
1 Oct 2024, a timeline compiled from Vadodara Municipal Corporation updates). NRSC/ISRO issued a rapid flood map of
Vadodara district "as on 28.08.2024" from a Sentinel-1A pass of 28 Aug 2024 ([map PDF](https://bhuvan-app1.nrsc.gov.in/disaster/usrtasks/flood/doc/GJ_2024_28_08_VAP.pdf)),
so the open satellite data for this question exist.

Independent study on public data by 23N AI Labs. Vadodara is used only as a case study of a city flood: this says
nothing about any municipal body, dam authority or agency, and implies no affiliation with any of them. All areas and
counts are estimates from a stated method.

## What the notebook does

1. **Box and grid.** A box over Vadodara city and its edges, 73.10–73.28° E × 22.22–22.40° N (our choice, not the
   municipal boundary), on a 10 m UTM 43N grid (about 380 km²).
2. **Passes.** Searches the Planetary Computer STAC API for Sentinel-1 IW GRD scenes over the box, Jan–Sep 2024.
   The **flood pass** is the first pass that covers ≥ 90 % of the box within 6 days after the danger mark
   (26 Aug, 16:00 IST). Every other pass used is from the **same orbit**: all dry-season passes (Jan–May 2024) for
   the baseline median, the last pass before the rain began (24 Aug) and the next pass after the flood.
3. **Read only what's needed.** For each pass, reads the VV and VH windows over the box at full resolution from the
   Cloud-Optimised GeoTIFFs, resampled onto the grid with the scene's ground control points. Values are uncalibrated
   DN²; only dB differences between passes of the same orbit are used, and the notebook checks that unflooded land
   doesn't shift.
4. **Detect.** 5×5 boxcar against speckle. A pixel is open floodwater if it is below the Otsu water threshold of the
   flood pass **and** ≥ 3 dB darker than its dry-season median. Water already there in the dry season is left out;
   patches under 0.5 ha are dropped.
5. **Exposure.** OpenStreetMap buildings (centre within 20 m of floodwater) and roads (length through water, all and
   major), from the Overpass API. Optional: Microsoft Global ML Building Footprints for the same box, to measure how
   complete OSM is.
6. **Robustness.** 2 and 4 dB change thresholds; the water threshold ±1 dB; VH instead of VV; the pre-rain pass as the
   baseline instead of the dry-season median.
7. **Sanity checks.** Before the headline the notebook prints `!! SANITY CHECK FAILED … Do NOT post` if: fewer than
   4 dry-season passes; the flood pass falls outside the window; less than 0.5 km² or more than half the box is
   "flooded"; unflooded land shifts more than 1.5 dB between baseline and flood pass (calibration or processing
   break); the Otsu threshold sits less than 4 dB below typical land; the pre-rain pass shows more than 30 % of the
   flood area (placebo); less than 40 % of the floodwater lies within 2 km of the Vishwamitri; the area changes by
   more than ×2 between the 2 and 4 dB thresholds; more than 60 % of mapped buildings are "in water"; or smoke-test
   mode is on. It notes (doesn't block): no pre/after pass, more water on the next pass than on the flood pass, VV vs
   VH outside ×2, fewer than 20,000 OSM buildings, or OSM below half of Microsoft's count.
8. **Outputs.** `ft11_flood_map.png`, `ft11_areas.png`, a Gradio demo (move the thresholds, switch VV/VH, see the
   map and counts change), `ft11_video.mp4` (1080×1080, 30 fps, H.264, 58 s timeline saved at 1.5×, about 39 s),
   `ft11_cover.png` (1080×1350), and the filled LinkedIn and X posts with character counts.

## Data and licences

| What | Source | Licence / login |
|---|---|---|
| Sentinel-1 GRD (IW, VV + VH), Jan–Sep 2024 | Microsoft Planetary Computer STAC, collection `sentinel-1-grd`, `https://planetarycomputer.microsoft.com/api/stac/v1` | Copernicus Sentinel data terms: free, full and open, commercial use allowed; attribution "Contains modified Copernicus Sentinel data 2024". **No account, no key**: `planetary-computer` gets a free anonymous SAS token |
| Buildings, roads, Vishwamitri river line | OpenStreetMap via the Overpass API (`overpass-api.de`, fallback `overpass.kumi.systems`) | © OpenStreetMap contributors, ODbL 1.0. No key. Cached to JSON after the first run |
| Building footprints (optional cross-check) | Microsoft Global ML Building Footprints, `dataset-links.csv` index (hosting moved to `bfppub.blob.core.windows.net` in July 2026; the old URL is a fallback) | CDLA Permissive 2.0. No key. Skipped automatically if the download fails |
| Danger mark, crossing time, rainfall, gauge peak | DeshGujarat timeline, 1 Oct 2024 (link above) | News report; used as documented facts and for choosing the passes, not as data |
| Official flood map | NRSC/ISRO, Vadodara district, as on 28.08.2024 (link above) | "For official use"; a visual cross-check only, not used as data |
| Model | none: a classical change-detection rule written in the notebook | — |

The Planetary Computer and Overpass could not be reached from the build environment (its network is restricted), so
the search and downloads are untested against the live services. The code follows the STAC collection's published
asset keys (`vv`, `vh`, Cloud-Optimised GeoTIFF) and `platform` / `sat:orbit_state` properties as of 22 Nov 2026.
The collection summary does not list `sat:relative_orbit`; if items lack it, passes are matched by orbit direction and
time of day instead. If the Planetary Computer stops serving `sentinel-1-grd`, the same scenes are on the Copernicus
Data Space Ecosystem (free account needed).

## How to run

1. Click the Colab badge, then Runtime → **Run all**. CPU is fine.
2. Expect roughly 5–15 minutes: install (~1 min), the scene search, reading about 15 windows of ~2,000 × 2,000
   pixels, three Overpass queries (the building query is the slowest; if both Overpass servers time out, run the cell
   again later), and the video (~1–2 min). Radar and OSM are cached locally, so a re-run skips the downloads.
3. Read the **Results** cell. If it prints `!! SANITY CHECK FAILED`, don't post. Fix the cause first.
4. Before posting, look at `ft11_flood_map.png` next to the NRSC map for 28 Aug 2024: the moss areas should follow the
   Vishwamitri and the low ground beside it. Then try the Gradio demo: the map should not change shape wildly with
   the thresholds.
5. On Kaggle, turn on Internet in the notebook settings.

`FT11_SMOKE_TEST=1` (environment variable, off by default) runs the notebook without internet on a synthetic radar
scene, synthetic buildings and roads on the same grid. It exists only to check that the notebook runs; its output is
labelled as not real and must never be posted.

## Limitations

- **Open water, not every wet street.** Flooded lanes between buildings often look bright to radar (double bounce),
  so dense urban flooding is undercounted. The number is "open floodwater", not "flooded area".
- **One snapshot.** The pass may not catch the peak; the next pass shows recession, not the whole event.
- **"Within hours" means the acquisition time.** Data-delivery latency to the Planetary Computer is not measured.
- **No ground truth.** Checked only by a placebo pass, a later pass, distance to the river and threshold variants.
- **Dark is not always water** (tarmac, sand, radar shadow); wind or rain during the pass can hide water.
- **OSM is incomplete** in Indian cities, so the building count is a lower bound; "beside the water" isn't "water
  inside".
- **The box is ours**, not the municipal boundary.

## Files

- `ft11_flood_mapping_radar.ipynb`: the notebook (no outputs)
- `post_linkedin.md`, `post_x.md`: post templates with `{placeholders}`, filled in by the notebook
