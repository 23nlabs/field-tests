Can a small open AI model answer a Gujarati question about a government scheme, using only the official documents?

23N Field Test #05: {headline}

Census 2011 counted about 5.5 crore people whose mother tongue is Gujarati. All {n_docs} official documents we used are in English.

How we tested it:
• {n_docs} documents from PIB, PFRDA, the Finance Ministry and Gujarat WCD, on {n_schemes} schemes
• {model_name} with {embed_name} retrieval, on a free Colab GPU
• The same {n_q} questions in English and Gujarati, checked against the source: English {en_correct}/{n_q}, Gujarati {gu_correct}/{n_q}
• Given the right document directly: English {en_oracle}/{n_q}, Gujarati {gu_oracle}/{n_q}

Example: "{example_q_gu}"
→ {example_answer_gu} {example_mark}

Limits: {n_q} questions per language, our translations, a number-matching scorer. A capability probe, not a benchmark, and not eligibility advice.

Notebook in the comments.

{signature}
