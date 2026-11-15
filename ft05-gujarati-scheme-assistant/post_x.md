Asked a {model_size} open AI model {n_q} questions about Indian government schemes, in English and in Gujarati, from official documents. English: {en_correct}/{n_q} right. Gujarati: {gu_correct}/{n_q}. 23N Field Test #05. Notebook below.

---
Thread (optional):
1/ Corpus: {n_docs} official documents (PIB, PFRDA, Finance Ministry, Gujarat WCD) on {n_schemes} schemes. Retrieval with {embed_name}, answers from {model_name} on a free GPU.
2/ Given the right document directly: English {en_oracle}/{n_q}, Gujarati {gu_oracle}/{n_q}. Right document retrieved: English {en_retrieval}/{n_q}, Gujarati {gu_retrieval}/{n_q}.
3/ Limits: {n_q} questions per language, our translations, number-matching scorer. Independent study on public data.
