Can a {model_params}-parameter open AI model forecast tomorrow's Khavda solar output better than "same as yesterday"? Est. deviation charges per GW, {test_year}: ₹{pen_persist} cr → ₹{pen_model} cr ({change}). 23N Field Test #06. Notebook below.

---
Thread (optional):
1/ Data: {n_years} years of hourly ERA5 sunlight (Open-Meteo, CC BY 4.0) for the Khavda RE park, turned into a notional 1 GW plant's output.
2/ Rule: CERC DSM 2024 Reg 8(4) for solar, ±{band1}% free band, then 10% and 100% of the contract rate. Daytime error {mae_persist}% → {mae_model}% of capacity.
3/ Limits: reanalysis, not meter data; hourly, not 15-min; no intraday revisions. Independent study on public data.
