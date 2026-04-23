**Signal Processing for Telecommunications and Economics Lab – Unsupervised Learning Summary (2024‑2025)**  

---  

### 1. Clustering  
- **Purpose:** Partition unlabeled data into *clusters* of similar observations.  
- **Key idea:** Points in the same cluster share common features; different clusters are distinct.  

### 2. K‑Means  
| Step | Description |
|------|-------------|
| 1️⃣ | Choose the number of clusters **K** (hyper‑parameter). |
| 2️⃣ | Initialise **K** random, well‑separated centroids. |
| 3️⃣ | Compute distances from each point to every centroid. |
| 4️⃣ | Assign each point to the nearest centroid (forming clusters). |
| 5️⃣ | Re‑compute each centroid as the mean of its assigned points. |
| 🔁 | Repeat steps 3‑5 until assignments stop changing. |

- **Centroid:** geometric centre of a cluster (not necessarily a data point).  
- **Choosing K:** use the *elbow (gomito) method* – run K‑Means for several K, plot total squared distance vs. K, and pick the K at the “elbow” where the decrease slows down.  

### 3. DBSCAN (Density‑Based Spatial Clustering of Applications with Noise)  
| Parameter | Role |
|-----------|------|
| **ε (eps)** | Maximum radius to consider points as neighbours. |
| **minSamples** | Minimum number of points within ε to form a dense region (≥ dim + 1). |

- **Core point:** ≥ minSamples neighbours within ε → defines a cluster.  
- **Border point:** Fewer neighbours but reachable from a core point → joins that cluster.  
- **Noise point:** Not reachable from any core point → treated as outlier.  

*Advantages:* discovers arbitrarily shaped clusters, no need to pre‑specify the number of clusters, robust to noise.  

### 4. PCA – Principal Component Analysis  
Goal: **Reduce dimensionality** while preserving as much variance (information) as possible.  

**Five steps**  

1. **Standardise** continuous variables.  
2. Compute the **covariance matrix** → reveals pairwise correlations.  
3. Obtain **eigenvectors** (principal directions) and **eigenvalues** (explained variance).  
4. Build a **feature‑vector** by selecting the top‑p eigenvectors (largest eigenvalues).  
5. **Project** the original data onto the new axes (multiply by the transpose of the feature‑vector).  

Result: a lower‑dimensional representation where the first component captures the greatest variance, the second the next greatest, etc.  

### 5. Model Selection & Bias‑Variance Trade‑off  
- **Bias:** error from overly simplistic assumptions → *under‑fitting*.  
- **Variance:** error from sensitivity to training‑set fluctuations → *over‑fitting*.  
- **Goal:** Choose a model (and its hyper‑parameters) that balances bias and variance, minimizing the expected test MSE (bias² + variance + irreducible error).  

---  

#### Quick Takeaways
- **Clustering** (K‑Means, DBSCAN) uncovers hidden structure without labels.  
- **K‑Means** needs K (use elbow); **DBSCAN** needs ε and minSamples (no K).  
- **PCA** is the go‑to technique for dimensionality reduction before clustering or other analyses.  
- Always evaluate the **bias‑variance trade‑off** to avoid under‑ or over‑fitting when selecting algorithms and tuning parameters.  