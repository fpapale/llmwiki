# Signal Processing for Telecommunications and Economics Lab

**Prof. Ing. F. Benedetto**  
Email: [francesco.benedetto@uniroma3.it](mailto:francesco.benedetto@uniroma3.it) | [fbenedetto@ieee.org](mailto:fbenedetto@ieee.org)  
Chair of “Machine Learning and Data Processing” – University of Roma Tre  
Chair of the "Definitions and Concepts for Dynamic Spectrum Access“ - IEEE 1900.1  

## Apprendimento non supervisionato

### Clustering
- Tecnica di machine learning non supervisionata per analisi statistiche.
- Obiettivo: suddividere osservazioni in cluster basati su caratteristiche simili.
- Esempio: analisi di dati con caratteristiche x1, x2, x3 per identificare schemi.

### K-Means
- Algoritmo di clustering partizionale efficace.
- Si basa su centroidi per minimizzare l'errore quadratico totale.
- Processo in 5 step:
  1. Decidere il numero di cluster (K).
  2. Scegliere K centroidi casualmente.
  3. Calcolare distanze dai punti ai centroidi.
  4. Assegnare punti ai cluster più vicini.
  5. Ricalcolare le posizioni dei centroidi e ripetere.

### DBSCAN
- Algoritmo di clustering basato sulla densità.
- Non richiede il numero di cluster a priori.
- Utilizza due parametri: epsilon (distanza minima) e minSamples (numero minimo di punti per formare un cluster).
- Classifica i punti come core, border o noise.

### PCA (Analisi delle Componenti Principali)
- Riduzione della dimensionalità mantenendo la massima informazione.
- Fasi:
  1. Standardizzare le variabili.
  2. Calcolare la matrice di covarianza.
  3. Calcolare autovettori e autovalori.
  4. Creare un vettore di funzionalità per le componenti principali.
  5. Riformulare i dati lungo gli assi delle componenti principali.

### Compromesso Bias-Varianza
- Analizza l'errore di generalizzazione di un modello.
- Bias: errore dovuto a presupposti errati (underfitting).
- Varianza: errore dovuto alla sensibilità ai dati di addestramento (overfitting).
- Obiettivo: minimizzare l'errore totale mantenendo bassa sia la varianza che il bias.

## Conclusione
La scelta dell'algoritmo giusto è cruciale e dipende dai dati e dal contesto. Non esiste un "metodo migliore", ma un "modello più adeguato".