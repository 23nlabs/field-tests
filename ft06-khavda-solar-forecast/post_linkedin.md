Can a small open AI model forecast tomorrow's solar output at Khavda better than "same as yesterday"? And what is that worth?

23N Field Test #06: {headline}

Since 1 April 2026, CERC's deviation rules for solar sellers charge for any miss beyond ±5% of capacity in a 15-minute block, down from ±10%.

How we tested it:
• {n_years} years of hourly ERA5 sunlight for the Khavda RE park, Kutch (via Open-Meteo), as output of a notional 1 GW plant
• {n_days} next-day forecasts for {test_year}: "same as yesterday", a 7-day average, and {model_name} ({model_params} parameters, zero-shot, free Colab)
• Charges under CERC DSM Regulations 2024, Reg 8(4), at an assumed ₹{rate}/kWh contract rate

Result: estimated deviation charges ₹{pen_persist} cr → ₹{pen_model} cr a year per GW ({change}). Daytime error {mae_persist}% → {mae_model}% of capacity.

Limits: reanalysis weather, not meter data; hourly, not 15-minute; no intraday revisions. An estimate, not a plant's bill.

Notebook in the comments.

{signature}
