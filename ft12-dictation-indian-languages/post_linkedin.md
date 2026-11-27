Dictation in Indian languages: does a paid API beat free open models?

23N Field Test #12: {headline}

On 23 Nov a dictation API for English and 22 Indian languages launched at ₹0.50 per audio minute. Its maker reports fewer edits than rival systems on its own, non-public test set. We ran it on a public one.

How we tested it:
• {n_utt} FLEURS test clips per language (Gujarati, Hindi, Tamil, English), the same sentences in each
• Sarvam Dictate's raw transcript vs {open_list} on a free Colab GPU
• Word error rate, API vs best open: Gujarati {api_gu} vs {open_gu}, Hindi {api_hi} vs {open_hi}, Tamil {api_ta} vs {open_ta}, English {api_en} vs {open_en}
• Cost: ₹{inr_hr} per audio hour; median {lat}s per clip

Limits: read speech, not real dictation; the API's edited text is scored separately. Not affiliated with Sarvam AI.

Notebook in the comments.

{signature}
