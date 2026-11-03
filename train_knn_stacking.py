import pandas as pd
import numpy as np
import pickle
import os

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

print("="*70)
print("DEMOGRAPHIC & SEASONAL TOURISM RECOMMENDER SYSTEM")
print("Implementation of Marzuki et al. (2025) KNN-Stacking Architecture")
print("="*70)

# 1. Load the unified dataset
df = pd.read_csv("data/unified_tourism_dataset.csv")
print(f"\n1. Loaded Dataset: {df.shape[0]} samples, {df.shape[1]} columns")

# 2. Define Features and Target
feature_cols = ['Age', 'Gender', 'Income_Level', 'Spending_Amount', 'Avg_Trip_Duration', 'Travel_Group_Type', 'Travel_Season']
target_col = 'Target_Category'

X = df[feature_cols]
y = df[target_col]

print(f"Features: {feature_cols}")
print(f"Target: {target_col} -> {y.unique().tolist()}")

# 3. Preprocessing Pipeline
numeric_features = ['Age', 'Spending_Amount', 'Avg_Trip_Duration']
categorical_features = ['Gender', 'Travel_Group_Type', 'Travel_Season']
ordinal_features = ['Income_Level']

income_categories = [['Low', 'Medium', 'High']]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_features),
        ('ord', OrdinalEncoder(categories=income_categories), ordinal_features)
    ]
)

# 4. Train-Test Split (80% Train, 20% Test with Stratification)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train set: {X_train.shape[0]} samples | Test set: {X_test.shape[0]} samples")

# Transform features
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

# 5. Define Base Learners & Meta Learner as per Marzuki et al. (2025)
base_learners = [
    ('knn_k3', KNeighborsClassifier(n_neighbors=3, metric='euclidean', weights='distance')),
    ('knn_k5', KNeighborsClassifier(n_neighbors=5, metric='euclidean', weights='distance')),
    ('knn_k7', KNeighborsClassifier(n_neighbors=7, metric='euclidean', weights='distance')),
    ('knn_k9', KNeighborsClassifier(n_neighbors=9, metric='euclidean', weights='distance')),
    ('rf_base', RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42))
]

meta_learner = LogisticRegression(max_iter=1000, random_state=42)

stacking_clf = StackingClassifier(
    estimators=base_learners,
    final_estimator=meta_learner,
    cv=5,
    passthrough=False
)

# 6. Benchmark Models for Literature Comparison
models = {
    "Baseline KNN (k=5)": KNeighborsClassifier(n_neighbors=5),
    "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42),
    "KNN Stacking Ensemble (Proposed)": stacking_clf
}

# 7. Model Training & Evaluation
results = []
print("\n2. Training & Evaluating Models...")
print("-" * 70)

for name, model in models.items():
    model.fit(X_train_processed, y_train)
    y_pred = model.predict(X_test_processed)
    
    acc = accuracy_score(y_test, y_pred) * 100
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0) * 100
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0) * 100
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0) * 100
    
    results.append({
        "Model": name,
        "Accuracy (%)": round(acc, 2),
        "Precision (%)": round(prec, 2),
        "Recall (%)": round(rec, 2),
        "F1-Score (%)": round(f1, 2)
    })
    print(f"[*] {name:35s} | Acc: {acc:.2f}% | F1: {f1:.2f}%")

# Save results table
results_df = pd.DataFrame(results)
print("\n" + "="*70)
print("FINAL PERFORMANCE EVALUATION TABLE")
print("="*70)
print(results_df.to_string(index=False))

# 8. Classification Report for Proposed Model
y_pred_stack = stacking_clf.predict(X_test_processed)
print("\nClassification Report (KNN Stacking Ensemble):")
print(classification_report(y_test, y_pred_stack))

# 9. Save Models & Preprocessor to disk
os.makedirs("models", exist_ok=True)
with open("models/preprocessor.pkl", "wb") as f:
    pickle.dump(preprocessor, f)

with open("models/stacking_model.pkl", "wb") as f:
    pickle.dump(stacking_clf, f)

results_df.to_csv("models/evaluation_results.csv", index=False)
print("[OK] Saved preprocessor, model pipeline, and evaluation results to 'models/'")
