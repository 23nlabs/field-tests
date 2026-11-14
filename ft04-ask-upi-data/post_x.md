Asked India's UPI data 25 questions in Hindi and English. A {model_size} open model on a free GPU wrote the SQL and got {n_correct}/{n_total} right (Hindi {hi_correct}/{hi_total}, English {en_correct}/{en_total}). 23N Field Test #04. Notebook below.

---
Thread (optional):
1/ Data: {n_months} months of NPCI UPI stats ({data_range}). Model: {model_name}. Every answer shows its SQL, and the SQL runs read-only on SQLite.
2/ Scored on execution accuracy against hand-written gold SQL. Median {median_latency}s per question on a free Colab GPU.
3/ Limits: 1 table, 25 questions, our own test set. Independent study on public data, not affiliated with NPCI or RBI.
