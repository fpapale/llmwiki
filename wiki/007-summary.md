**Summary – Natural Language Processing (NLP) Overview**  

| Section | Key Points |
|---------|------------|
| **1. What is NLP?** | AI discipline that processes, understands, and generates human language. Bridges the gap between unstructured human text and structured machine input. |
| **2. Applications** | • NLU – meaning, sentiment, intent extraction  <br>• NLG – human‑like text generation  <br>• Search engines, translators, virtual assistants, sentiment monitoring |
| **3. Historical Milestones** | • **1950s** – Turing test, rule‑based MT (Georgetown‑IBM)  <br>• **1960‑70s** – Formal grammars (Chomsky)  <br>• **1980s** – Statistical models (HMM)  <br>• **1990‑2000s** – Large corpora, statistical algorithms  <br>• **2010s** – Deep learning, word embeddings (Word2Vec, GloVe)  <br>• **2020s** – Transformers (BERT, GPT, T5) |
| **4. Main Approaches** | 1. **Rule‑based** – hand‑crafted grammars (rigid, low scalability) <br>2. **Statistical** – N‑grams, HMM (needs big data, limited context) <br>3. **Machine Learning** – SVM, decision trees, neural nets (requires labeled data) <br>4. **Deep Learning** – RNN/LSTM/GRU, Transformers (state‑of‑the‑art, high compute) |
| **5. Pre‑processing Pipeline** | • Text cleaning (remove symbols, numbers)  <br>• Lower‑casing  <br>• Stop‑word removal  <br>• **Tokenization** – word, sentence, sub‑word (BPE, WordPiece, SentencePiece)  <br>• Normalization  <br>• **Stemming** vs. **Lemmatization** (context‑aware)  <br>• Punctuation removal |
| **6. Word Embeddings** | Fixed‑size vectors representing semantics (Word2Vec, GloVe). Limitations: OOV words, static context. |
| **7. Transformers** | Architecture based on **self‑attention** (Q‑K‑V). Components: Encoder, Decoder, Multi‑Head Attention, Positional Encoding. Major models: **BERT** (bidirectional), **GPT** (causal), **T5**, **RoBERTa**, **XLNet**. |
| **8. Neural Networks for NLP** | • **Feed‑forward** – simple classification  <br>• **RNN** – sequential data, suffers vanishing gradient  <br>• **LSTM / GRU** – gates to capture long‑range dependencies  <br>• **Transformers** – parallel processing, superior long‑range modeling |
| **9. Sentiment Analysis** | Goal: classify text as positive/negative/neutral. <br>• Rule‑based (sentiment lexicons) – easy but limited. <br>• ML (Naïve Bayes, SVM, Logistic Regression). <br>• DL (CNN, LSTM/GRU, Transformers) – handles sarcasm, context but needs large data. |
| **10. Ethical Issues & Bias** | • Data/model bias (gender, cultural, linguistic). <br>• Privacy concerns. <br>• Misuse (deepfakes, disinformation). |
| **11. Mitigation Strategies** | • Balanced, diverse datasets. <br>• Annotator training. <br>• Debiasing embeddings (e.g., gender‑axis projection). <br>• Fairness regularization, bias metrics, open‑source audits. |
| **12. Current Challenges & Future Directions** | • Ambiguity, sarcasm, low‑resource languages. <br>• High computational cost of large models. <br>• Privacy & security risks. <br>• **Future**: multimodal models (e.g., CLIP, GPT‑4 Vision), efficient lightweight models (DistilBERT), multilingual equity, Explainable AI, advanced debiasing. |

---

### Take‑away
NLP has evolved from rule‑based systems to powerful transformer models that can understand and generate language at near‑human levels. While the technology enables automation, accessibility, and deep insight from text, responsible development—addressing bias, privacy, and computational sustainability—is essential for its future impact.