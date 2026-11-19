Tested {n_models} small open speech models on the same sentences read in Gujarati, Hindi and English (FLEURS). Best Gujarati word error rate: {gu_wer} ({best_gu}). English: {en_wer}. 23N Field Test #09. Notebook below.

---
Thread (optional):
1/ {n_utt} test clips per language, forced language, greedy decoding, one script-safe normaliser. Best general multilingual model on Gujarati: {gu_wer_gen} ({best_gu_gen}).
2/ Where it fails: numbers {num_err} wrong vs {other_err} for other words. Runaway outputs: {runaway}.
3/ Limits: read speech, not calls or dialects; one model fine-tuned on FLEURS train. Independent study on public data.
