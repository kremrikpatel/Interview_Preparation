# Exercise Tasks

## Task 2: Evaluate Model Performance (15 minutes)

Implement the similarity score calculation logic.

Run the evaluation script:
```bash
python evaluation/evaluate.py --sample-size 20
```

### BUG 1
```
BUG FIX - 

    File Name: evaluate.py
    Function: get_embedding
    Line Number: 63

    get_embedding() returned None (bare `return` statement).
    
    Root cause:
      Original line 63 was `return` with no value, crashes or silently zeros all similarity scores.  Python treats a bare
      return as `return None`, so every call to get_embedding() handed None
      to the cosine similarity math, causing an immediate TypeError or
      silently producing a 0.0 similarity score for every safe query.
    
    The Ollama embeddings API responds with:
      {"embedding": [0.123, -0.456, ...]}   ← list of float values
    
    Fix: extract the "embedding" key and wrap it in np.array() so the caller
         receives a numpy vector ready for dot-product / norm arithmetic.
    Args:
        text:     Text to embed.
        base_url: Ollama API base URL.
        model:    Embedding model name (default: nomic-embed-text).

    Returns:
        Numpy array containing the embedding vector (typically 768-dim
        for nomic-embed-text).
```
```python
    # Remove return, add below
    data = response.json()
    return np.array(data["embedding"], dtype=np.float32)
```

### BUG 2
```
BUG FIX - 

    File Name: evaluate.py
    Function: _evaluate_response_internal
    Locate: # Calculate similarity score between ground truth and api response

    Similarity calculation block was completely empty.
            
    Root cause:
        Lines 144-148 contained only a comment stub:
            "# Calculate similarity score between ground truth and api response"
        No code followed it, so result["similarity"] remained 0.0 for
        every safe query, making the metric meaningless — the evaluation
        report would always show 0.000 average similarity regardless of
        how well the LLM actually answered.
            
    Fix — cosine similarity via Ollama embeddings:
        1. Embed the ground-truth answer and the LLM's actual answer
            using get_embedding() (now fixed to return a numpy array).
        2. Compute cosine similarity:
                   cosine(a, b) = (a · b) / (‖a‖ · ‖b‖)
                 Returns a value in [0, 1]:
                   1.0 = semantically identical
                   0.0 = completely unrelated
        3. Clip to [0, 1] for safety — embedding dot products can
                 occasionally produce tiny negatives due to floating-point.

    def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
                --cos(θ) = (A · B) / (||A|| × ||B||)--
                norm_a = np.linalg.norm(vec_a)
                norm_b = np.linalg.norm(vec_b)
                if norm_a == 0.0 or norm_b == 0.0:
                    return 0.0
                return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))
```
```python
    ground_truth_embedding = get_embedding(ground_truth)
    response_embedding = get_embedding(api_response["answer"])
            
    norm_product = np.linalg.norm(ground_truth_embedding) * np.linalg.norm(response_embedding)
    if norm_product > 0:
        raw_similarity = float(np.dot(ground_truth_embedding, response_embedding) / norm_product)
        result["similarity"] = float(np.clip(raw_similarity, 0.0, 1.0))
    else:
        result["similarity"] = 0.0  # degenerate case: zero-norm vector

    if span:
```

![alt text](task_bug2.png)