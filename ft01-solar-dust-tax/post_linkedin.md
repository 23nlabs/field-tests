# LinkedIn post template — Field Test #01 (filled automatically in notebook section 7)

Placeholders are filled from the run. Keep the filled post <= 1,300 characters.

---

What does dust cost India's solar parks?

23N Field Tests #01 - The Solar Dust Tax

Left uncleaned, dust would cost a 1 GW solar park in Kutch, Gujarat ~₹{loss_uncleaned_cr} crore a year. Cleaning every {headline_interval} days wins back ~₹{recovered_cr} crore of that.

How we got there (independent study, public data only):
- Vision: a ResNet18 fine-tuned on {n_train} open DeepSolarEye panel images predicts % power loss from a photo. Error: {mae_pts} percentage points (MAE) on days it never saw.
- Sunlight: NASA POWER daily irradiance and rain at Khavda, Kutch for {year} (avg {ghi_avg} kWh/m2/day).
- Dust: {soiling_rate}%/day build-up (a field rate measured in Gandhinagar), reset by heavy rain or a wash.
- Money: 1 GW x PR {pr} x ₹{tariff}/kWh.

Still lost per year when cleaning every {interval_list} days: ₹{interval_losses} crore.
Going from every {slow_interval} to every {headline_interval} days pays off if a wash costs under ~₹{breakeven_rs_per_mw} per MW.

These are estimates. Every assumption is a named variable in the notebook - change the tariff, dust rate or site and re-run.

Notebook + live demo (upload a panel photo, get ₹ lost per MW) in the comments.

#SolarEnergy #AI #Gujarat #RenewableEnergy #23NFieldTests
