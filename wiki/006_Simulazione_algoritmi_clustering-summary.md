**Summary – K‑means clustering on a supervised dataset**

1. **Goal** – Determine the optimal number of clusters \(K\) (the *K‑means* “means”) for a labelled dataset (e.g., for a classifier or a query case).  

2. **Assumption** – The true clusters are well‑separated in feature space; otherwise the algorithm may fail to converge.

3. **Step 3** – Compute the distance of every data point to its nearest cluster centre.

4. **Step 4** – Assign each point to the *closest* cluster centre (the one with the smallest distance).

5. **Step 5** – For each cluster compute the **position of its centre** (the mean of all points belonging to that cluster).  
   *Only the centre coordinates are needed for the next steps.*

6. **Step 6** – Stop the iteration when the centres no longer move (i.e., the change in any centre is below a small threshold).

---

### Pseudocode fragment (Python‑like)

```python
def kmeans(data, K, eps=1e-4, max_iter=100):
    # 1. initialise K centres (randomly or with a smarter init)
    centres = initialise_centres(data, K)

    for it in range(max_iter):
        # 2. assign each point to the nearest centre
        assignments = np.argmin(
            pairwise_distances(data, centres), axis=1
        )                     # shape (n_samples,)

        # 3. recompute centres as the mean of assigned points
        new_centres = np.array([
            data[assignments == k].mean(axis=0) if np.any(assignments == k)
            else centres[k]                     # keep old centre if empty
            for k in range(K)
        ])

        # 4. check convergence
        if np.linalg.norm(new_centres - centres) < eps:
            break
        centres = new_centres

    return centres, assignments
```

*Key functions referenced in the original text*  

- `get_numero_punti_vicini(p, eps)`: count points within distance `eps` of point `p`.  
- `core_point_cluster(p)`: find the cluster centre that is the nearest *core* point.  
- `cerca_core_point_vicino(p, eps)`: locate the nearest core point to `p` within `eps`.  
- `bordere_point(p)`: handle points that lie on the border between clusters.  

These utilities are used inside the assignment and centre‑updating steps.