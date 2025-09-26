# Paul Sachse - Retrieval Augmented Generation System Reflection Report

## Selected Document: Wikipedia page of the iPhone
I downloaded the iPhone Wikipedia page as a pdf and processed it as a document rather than a webpage. This was due to an error I received while attempting to use the automated system to access Wikipedia's site. This Wikipedia page contains general information about the iPhone and its many releases over the years. The page contains details about the device's hardware including models, internal components, and physical design. The source also goes on to talk about the iPhone's software and services including iOS and the App Store. This resource also includes company information about Apple and the iPhone such as retail data, marketing information, and the history of the device. 


## 4.1 Chunk‑Size & Overlap Experiments
### 3 RAG System Responses

Your question: What was the second iPhone?
Answer: iPhone 3G

Your question: What year did iPhone screens start getting larger?
Answer: 2012

Your question: What percent of young people in the United States use iPhone?
Answer: 88%

### Adjusting chunk_size and chunk_overlap

By adjusting the chunk sizes to a lesser value, it seems the RAG system is able to more precisely find information and was noticeably able to answer questions more reliably. With chunk sizes set at 150 rather than 500, answers were found that were missed entirely prior to the change. When adjusting the chunk_overlap, I was able to improve results from queries that required slightly more context, such as asking what the second iPhone model was. Adjusting the overlap value too low did also cause the document split count to be large resulting in a significantly slowed system. 


## 4.2 Deep‑Dive Questions

1. How does the embedding dimensionality of the model affect FAISS search speed and accuracy?
Answer: Embedding dimensionality directly controls both memory usage and query speed in FAISS. Higher-dimensional embeddings (e.g., 768 vs. 384) typically capture more semantic nuance, which can improve recall and answer quality. However, they also require more memory and make nearest-neighbor search slower. For small-to-medium corpora, the performance hit is negligible, but at scale, dimensionality reduction (like PCA) or smaller models can significantly improve efficiency without a huge loss in accuracy.

2. What role does the distance metric (L2 vs. cosine) play in FAISS retrieval?
Answer: Sentence-Transformers embeddings are generally trained with cosine similarity in mind, but FAISS IndexFlatL2 can still perform well because cosine similarity and L2 distance are monotonically related when vectors are normalized. If embeddings are not normalized, cosine and L2 may diverge in ranking results. For best practice, normalize embeddings before adding them to FAISS if cosine similarity is intended, or configure FAISS with an inner product index (IndexFlatIP).

3. Why is chunk overlap important, and how does it affect retrieval quality?
Answer: Chunk overlap helps preserve context that spans chunk boundaries. Without overlap, information at the edge of a chunk may be split, reducing the chance of retrieving relevant evidence. A small overlap (e.g., 50 tokens) ensures continuity while keeping the number of chunks manageable. Too much overlap (e.g., >200) increases redundancy, index size, and retrieval time without proportional benefits.

4. How does prompt design influence the final answer quality in a RAG system?
Answer: Prompt design is critical because the LLM combines retrieved context with instructions to form its answer. A clear system prompt that explicitly tells the model to rely only on the provided context reduces hallucinations. The structure of the user prompt (showing “Context” followed by “Question” and then “Answer:”) encourages the model to ground its response in evidence. Poorly designed prompts can cause the model to ignore the retrieved chunks or invent information.

5. What is the trade-off between top_k retrieval and top_m re-ranking?
Answer: Increasing top_k improves recall — the chance that the correct information is among the retrieved candidates. However, this comes with more computation during re-ranking, since each candidate must be scored by the cross-encoder. The top_m parameter controls how many chunks survive to the final context. If top_k is too low, you risk missing relevant evidence; if it’s too high, re-ranking becomes slow. Balancing top_k (broad recall) and top_m (focused precision) is essential for efficient, accurate answers.