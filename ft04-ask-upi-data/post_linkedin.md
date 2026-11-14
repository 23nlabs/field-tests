Can a free AI model correctly answer a question about India's payments data asked in Hindi?

23N Field Test #04: {headline}

How we tested it:
• Data: {n_months} months of official NPCI UPI statistics ({data_range})
• Model: {model_name}, open weights, on a free Colab GPU
• Method: the model writes SQL, we validate it and run it on the real table, and the result becomes a chart plus a one-line answer
• Score: 25 questions with hand-written reference SQL. English {en_correct}/{en_total}, Hindi {hi_correct}/{hi_total}. Median {median_latency}s per question

Example: "{example_q_hi}"
→ {example_answer}

Why it matters: departments, PSUs and banks sit on tabular data. A small model on cheap hardware that answers in the user's own language could open that data to far more people, as long as every answer shows its SQL so someone can check it.

Limits: one table, 25 questions, our own test set. Read it as a capability probe, not a benchmark.

Notebook in the comments. Try your own questions.

Independent study on public data. Not affiliated with NPCI or RBI.
#23NFieldTests #UPI #AI #Hindi
