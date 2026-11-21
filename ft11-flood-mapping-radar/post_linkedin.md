How fast can open radar data map a city flood? We tested it on Vadodara, August 2024.

23N Field Test #11: {headline}

On 26 Aug 2024 the Vishwamitri crossed its {danger_ft} ft danger mark in Vadodara after {rain_in} inches of rain in 24 hours. Cloud hides a flood from optical satellites; radar sees through it.

How we tested it:
• Free Copernicus Sentinel-1 radar, no login: the first pass after the danger mark, against a dry-season baseline from the same orbit
• Open water = dark in radar and {change_db} dB darker than the baseline; permanent water left out
• Overlaid on OpenStreetMap buildings and roads

Result: {area} km² from a pass {hours} h after the danger mark. Same test on a pass before the rain: {area_pre} km². Next pass: {area_after} km².

Limits: radar misses water between tall buildings, so dense streets are undercounted; OSM is incomplete; no ground survey. An estimate.

Notebook in the comments.

{signature}
