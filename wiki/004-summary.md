# Signal Processing for Telecommunications and Economics Lab

**Prof. Ing. F. Benedetto**  
*University of Roma Tre*  
*Chair of “Machine Learning and Data Processing”*  
*Chair of the "Definitions and Concepts for Dynamic Spectrum Access“ - IEEE 1900.1*  
*Contact: francesco.benedetto@uniroma3.it | fbenedetto@ieee.org*  

## Overview of Supervised Learning for Classification Problems

### Logistic Regression
- **Definition**: A supervised learning algorithm that builds a probabilistic linear model for data classification.
- **Objective**: Establish the probability of an observation belonging to one of two classes.
- **Training Phase**: The algorithm processes training examples to derive a weight distribution for accurate classification.

### Performance Metrics for Classification
1. **Accuracy**: Measures the proportion of correct predictions. 
   - Formula: `accuracy = correct_predictions / total_predictions`
   - Caution: Misleading in imbalanced datasets.
  
2. **Confusion Matrix**: A table to visualize the performance of a classification model.
   - Contains true positives (TP), true negatives (TN), false positives (FP), and false negatives (FN).
   - Accuracy can be derived from it: `accuracy = (TP + TN) / (TP + TN + FP + FN)`

3. **Precision and Recall**:
   - **Precision**: `precision = TP / (TP + FP)` - Measures the correctness of positive predictions.
   - **Recall**: `recall = TP / (TP + FN)` - Measures the ability to identify all positive instances.
   - **F1 Score**: Harmonic mean of precision and recall: `F1 = 2 * (precision * recall) / (precision + recall)`

4. **ROC and AUC**:
   - **ROC Curve**: Graphical representation of true positive rate vs. false positive rate.
   - **AUC**: Area under the ROC curve; a higher AUC indicates better model performance.

### Algorithms for Supervised Learning
- **Support Vector Machines (SVM)**: Used for classification tasks, especially with non-linearly separable data through kernel tricks.
  
- **Decision Trees**: A flowchart-like structure for decision-making based on input attributes. 
  - **Advantages**: Easy to interpret and implement.
  - **Disadvantages**: Prone to overfitting and complexity in deep trees.

### Ensemble Learning
- **Definition**: Combines multiple models to improve prediction accuracy.
- **Methods**:
  - **Bagging**: Creates multiple models from random subsets of data.
  - **Random Forest**: An extension of bagging using decision trees, reducing overfitting.
  - **Boosting**: Sequentially builds models that focus on the errors of previous models.

### Conclusion
The lab focuses on applying machine learning techniques, particularly supervised learning, to solve classification problems in telecommunications and economics. Understanding various algorithms and their performance metrics is crucial for developing effective predictive models.