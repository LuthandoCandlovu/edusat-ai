"""
🚀 EDUSAT AI - Professional ML Pipeline (NO DATA LEAKAGE)
"""
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# ML imports
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    f1_score, precision_score, recall_score, roc_auc_score
)
import warnings
warnings.filterwarnings('ignore')

# Create directories
os.makedirs('models', exist_ok=True)
os.makedirs('reports', exist_ok=True)

# ============================================================================
# CONFIGURATION
# ============================================================================
DATA_PATH = "data/Eastern_Cape_Education_Factors_Dataset.xlsx"
TARGET = "DropoutRisk"
MODEL_VERSION = "v1.1.0"
MODEL_OUT = f"models/edusat_rf_{MODEL_VERSION}_{datetime.now().strftime('%Y%m%d')}.joblib"
REPORT_OUT = f"reports/model_report_{MODEL_VERSION}_{datetime.now().strftime('%Y%m%d')}.txt"

print("="*60)
print("🚀 EDUSAT AI - PROFESSIONAL MODEL TRAINING (NO LEAKAGE)")
print("="*60)

# ============================================================================
# LOAD AND PREPARE DATA
# ============================================================================
print("\n📂 Loading Eastern Cape dataset...")
df = pd.read_excel(DATA_PATH, sheet_name="data")
print(f"✅ Loaded {len(df)} learners, {len(df.columns)} features")

# Create binary target
df['risk_binary'] = (df[TARGET] == 'At Risk').astype(int)

# REMOVE target and ID from features
drop_cols = ['LearnerID', TARGET, 'risk_binary']
available_cols = [c for c in df.columns if c not in drop_cols]
X = df[available_cols].copy()
y = df[TARGET].astype(str)
y_binary = df['risk_binary']

print(f"\n✅ Features used: {len(available_cols)}")
print(f"✅ Target: {TARGET}")
print("✅ No data leakage - removed risk_binary from features")

# ============================================================================
# FEATURE ENGINEERING
# ============================================================================
print("\n🔧 Engineering features...")

# Identify column types
cat_cols = X.select_dtypes(include=['object']).columns.tolist()
num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

print(f"📊 Numerical features: {len(num_cols)}")
print(f"🏷️ Categorical features: {len(cat_cols)}")

# ============================================================================
# PREPROCESSING PIPELINE
# ============================================================================
# Numerical pipeline
num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Categorical pipeline
cat_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Combined preprocessor
preprocessor = ColumnTransformer([
    ('num', num_pipeline, num_cols),
    ('cat', cat_pipeline, cat_cols)
])

# ============================================================================
# MODEL
# ============================================================================
print("\n🧠 Training Random Forest model...")

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=3,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)

clf = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', model)
])

# Split data
X_train, X_test, y_train, y_test, y_binary_train, y_binary_test = train_test_split(
    X, y, y_binary, test_size=0.2, random_state=42, stratify=y
)

print(f"📊 Training set: {len(X_train)} samples")
print(f"📊 Test set: {len(X_test)} samples")

# Train
print("🔄 Training model...")
clf.fit(X_train, y_train)

# ============================================================================
# CROSS-VALIDATION
# ============================================================================
print("\n🔄 Performing 5-fold cross-validation...")
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(clf, X, y, cv=cv, scoring='f1_weighted')
print(f"📊 Cross-validation F1 scores: {[f'{s:.3f}' for s in cv_scores]}")
print(f"📈 Mean F1: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")

# ============================================================================
# PREDICTIONS AND METRICS
# ============================================================================
print("\n📊 Evaluating on test set...")
y_pred = clf.predict(X_test)
y_proba = clf.predict_proba(X_test)

# Get probabilities for ROC-AUC
at_risk_idx = list(clf.classes_).index('At Risk') if 'At Risk' in clf.classes_ else 1
risk_proba = y_proba[:, at_risk_idx]

# Metrics
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='weighted')
precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
roc_auc = roc_auc_score(y_binary_test, risk_proba)

print(f"\n✅ Model Performance:")
print(f"   Accuracy:  {accuracy:.3f}")
print(f"   F1 Score:  {f1:.3f}")
print(f"   Precision: {precision:.3f}")
print(f"   Recall:    {recall:.3f}")
print(f"   ROC-AUC:   {roc_auc:.3f}")

# ============================================================================
# CONFUSION MATRIX
# ============================================================================
print("\n📉 Generating confusion matrix...")
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=clf.classes_, yticklabels=clf.classes_)
plt.title('Confusion Matrix - EduSat AI Risk Prediction')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.tight_layout()
plt.savefig('reports/confusion_matrix_fixed.png', dpi=300)
plt.close()
print("✅ Confusion matrix saved to reports/confusion_matrix_fixed.png")

# ============================================================================
# FEATURE IMPORTANCE
# ============================================================================
print("\n🔍 Extracting feature importance...")

# Get feature names
feature_names = num_cols.copy()

if cat_cols:
    cat_encoder = clf.named_steps['preprocessor'].named_transformers_['cat'].named_steps['onehot']
    if hasattr(cat_encoder, 'get_feature_names_out'):
        cat_feature_names = cat_encoder.get_feature_names_out(cat_cols)
        feature_names.extend(cat_feature_names)

# Get importances
importances = clf.named_steps['classifier'].feature_importances_

# Create dataframe
feat_imp = pd.DataFrame({
    'feature': feature_names[:len(importances)],
    'importance': importances
}).sort_values('importance', ascending=False)

print("\n🔥 TOP 10 RISK FACTORS IN EASTERN CAPE:")
print(feat_imp.head(10).to_string(index=False))

# Plot
plt.figure(figsize=(12, 6))
top_features = feat_imp.head(15)
plt.barh(range(len(top_features)), top_features['importance'].values)
plt.yticks(range(len(top_features)), top_features['feature'].values)
plt.xlabel('Importance')
plt.title('Top 15 Risk Factors for Dropout in Eastern Cape')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('reports/feature_importance_fixed.png', dpi=300)
plt.close()
print("✅ Feature importance plot saved to reports/feature_importance_fixed.png")

# ============================================================================
# BIAS CHECK
# ============================================================================
print("\n⚖️ Running bias checks...")

X_test_with_pred = X_test.copy()
X_test_with_pred['Actual'] = y_test.values
X_test_with_pred['Predicted'] = y_pred
X_test_with_pred['Risk_Probability'] = risk_proba

if 'Gender' in X_test_with_pred.columns:
    print("\n📊 Gender-based analysis:")
    gender_results = X_test_with_pred.groupby('Gender').agg({
        'Risk_Probability': 'mean',
        'Predicted': lambda x: (x == 'At Risk').mean()
    })
    print(gender_results)
    
    if len(gender_results) > 1:
        gender_diff = abs(gender_results['Risk_Probability'].max() - gender_results['Risk_Probability'].min())
        print(f"   Gender risk difference: {gender_diff:.3f}")
        if gender_diff < 0.1:
            print("   ✅ No significant gender bias detected")
        else:
            print("   ⚠️ Potential gender bias detected")

# ============================================================================
# SAVE MODEL
# ============================================================================
print(f"\n💾 Saving model to {MODEL_OUT}...")

model_package = {
    'model': clf,
    'features': {
        'numerical': num_cols,
        'categorical': cat_cols,
        'all': available_cols
    },
    'metrics': {
        'accuracy': accuracy,
        'f1': f1,
        'precision': precision,
        'recall': recall,
        'roc_auc': roc_auc,
        'cv_scores': cv_scores.tolist()
    },
    'classes': clf.classes_.tolist(),
    'version': MODEL_VERSION,
    'date': datetime.now().isoformat(),
    'data_shape': X.shape
}

joblib.dump(model_package, MODEL_OUT)
print(f"✅ Model saved successfully!")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*60)
print("🚀 EDUSAT AI - TRAINING COMPLETE")
print("="*60)
print(f"✅ Model: {MODEL_OUT}")
print(f"✅ Report: {REPORT_OUT}")
print(f"✅ Confusion Matrix: reports/confusion_matrix_fixed.png")
print(f"✅ Feature Importance: reports/feature_importance_fixed.png")
print("\n🔑 Key Insights:")
print(f"   • Model F1 Score: {f1:.3f}")
print(f"   • Cross-val stability: ±{cv_scores.std():.3f}")
print(f"   • Top risk factor: {feat_imp.iloc[0]['feature']}")
print("="*60)

# Save report
with open(REPORT_OUT, 'w') as f:
    f.write("="*60 + "\n")
    f.write("EDUSAT AI - MODEL TRAINING REPORT (NO LEAKAGE)\n")
    f.write("="*60 + "\n\n")
    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"Model Version: {MODEL_VERSION}\n")
    f.write(f"Features used: {len(available_cols)}\n")
    f.write(f"Training Samples: {len(X_train)}\n")
    f.write(f"Test Samples: {len(X_test)}\n\n")
    
    f.write("CROSS-VALIDATION:\n")
    f.write(f"Mean F1: {cv_scores.mean():.3f} (+/- {cv_scores.std()*2:.3f})\n\n")
    
    f.write("TEST METRICS:\n")
    f.write(f"Accuracy:  {accuracy:.3f}\n")
    f.write(f"F1 Score:  {f1:.3f}\n")
    f.write(f"Precision: {precision:.3f}\n")
    f.write(f"Recall:    {recall:.3f}\n")
    f.write(f"ROC-AUC:   {roc_auc:.3f}\n\n")
    
    f.write("TOP 10 RISK FACTORS:\n")
    f.write(feat_imp.head(10).to_string())

print(f"\n📄 Report saved to {REPORT_OUT}")
