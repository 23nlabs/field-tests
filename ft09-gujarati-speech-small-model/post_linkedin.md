Can a small open speech model understand spoken Gujarati?

23N Field Test #09: {headline}

Census 2011 counted about 5.5 crore people whose mother tongue is Gujarati. Phone lines, shops and helpdesks that want to take voice need a model that hears them.

How we tested it:
• {n_utt} clips per language from Google's FLEURS test set: the same sentences read in Gujarati, Hindi and English
• {n_models} open models on a free Colab GPU: {model_list}
• Word error rate, Gujarati: {gu_wer} for {best_gu} (95% CI {gu_lo}–{gu_hi}); best general multilingual model {gu_wer_gen} ({best_gu_gen}). Hindi best {hi_wer}, English best {en_wer}
• Where it fails: numbers wrong {num_err} of the time against {other_err} for other words

Limits: read speech by adult volunteers, not phone calls or dialects; {finetuned} was fine-tuned on FLEURS train data, so it is a best case. Some model licences are non-commercial.

Notebook in the comments.

{signature}
