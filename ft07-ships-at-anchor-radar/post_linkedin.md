How many ships wait at anchor off Mundra and Kandla? We counted them from radar satellites that see through cloud and the monsoon.

23N Field Test #07: {headline}

In 2024-25 the average pre-berthing detention at Deendayal Port (Kandla) was {pbdt_kandla} hours, against {pbdt_major} hours across India's major ports (Ministry of Ports, Shipping and Waterways).

How we tested it:
• {n_passes} Sentinel-1 radar passes, {period}, over Mundra's five published anchorage areas and a Kandla–Tuna study box
• A classic adaptive-threshold (CFAR) ship detector: no training data, runs on a free Colab CPU
• Weekly index = mean ships per pass; monsoon = Jun–Sep

Result: {mean_t} ships per pass in {test_year} ({mean_r} in {robust_year}). Monsoon {mon_t} vs {rest_t} the rest of the year. Busiest week: {peak_week}.

Limits: one image can't tell anchored from slow-moving ships; small craft are missed; no AIS to check against. An estimate.

Notebook in the comments.

{signature}
