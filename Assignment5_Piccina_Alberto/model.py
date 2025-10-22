import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, confusion_matrix, 
                            roc_curve, auc, accuracy_score, precision_recall_curve)

# Load dataset
df = pd.read_csv("battles_dataframe.csv")

print("="*80)
print("POKEMON BATTLE WIN PROBABILITY PREDICTOR")
print("="*80)
print(f"\nDataset shape: {df.shape}")
print(f"Total battles: {len(df)}")
print(f"\nOutcome distribution:\n{df['outcome'].value_counts()}")

# Preprocessing
le_type = LabelEncoder()
all_types = pd.concat([
    df['player_type1'], 
    df['player_type2'].dropna(),
    df['opponent_type1'],
    df['opponent_type2'].dropna()
]).unique()

le_type.fit(all_types)

# Types Encoding
df['player_type1_encoded'] = le_type.transform(df['player_type1'])
df['player_type2_encoded'] = df['player_type2'].apply(
    lambda x: le_type.transform([x])[0] if pd.notna(x) else -1
)
df['opponent_type1_encoded'] = le_type.transform(df['opponent_type1'])
df['opponent_type2_encoded'] = df['opponent_type2'].apply(
    lambda x: le_type.transform([x])[0] if pd.notna(x) else -1
)

# Target: 1 = victory, 0 = loss
df['win'] = (df['outcome'] == 'victory').astype(int)

# Features selection
feature_cols = [
    'player_type1_encoded', 'player_type2_encoded',
    'player_hp', 'player_attack', 'player_defense',
    'player_special', 'player_speed',
    'opponent_type1_encoded', 'opponent_type2_encoded',
    'opponent_hp', 'opponent_attack', 'opponent_defense',
    'opponent_special', 'opponent_speed'
]

X = df[feature_cols]
y = df['win']

print(f"\nFeatures shape: {X.shape}")
print(f"Target distribution: {y.value_counts().to_dict()}")

# Split train/test (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTrain set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")

# Training
print("\n" + "="*80)
print("TRAINING RANDOM FOREST CLASSIFIER")
print("="*80)

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Metrics
accuracy = accuracy_score(y_test, y_pred)
print(f"\nTest Accuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Loss', 'Victory']))

# Feature Importance
feature_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 10 Most Important Features:")
print(feature_importance.head(10).to_string(index=False))


# 1. Confusion Matrix
plt.figure(figsize=(6, 5))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix', fontsize=14, fontweight='bold')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.xticks(ticks=[0.5, 1.5], labels=['Loss', 'Victory'])
plt.yticks(ticks=[0.5, 1.5], labels=['Loss', 'Victory'], rotation=0)
plt.tight_layout()
plt.savefig('plot_confusion_matrix.png', dpi=300)
print("✓ Saved: plot_confusion_matrix.png")
plt.show()

# 2. ROC Curve
plt.figure(figsize=(6, 5))
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve', fontsize=14, fontweight='bold')
plt.legend(loc="lower right")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('plot_roc_curve.png', dpi=300)
print("✓ Saved: plot_roc_curve.png")
plt.show()

# 3. Feature Importance (Top 10)
plt.figure(figsize=(7, 6))
top_features = feature_importance.head(10)
plt.barh(top_features['feature'], top_features['importance'], color='steelblue')
plt.xlabel('Importance')
plt.title('Top 10 Feature Importance', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('plot_feature_importance.png', dpi=300)
print("✓ Saved: plot_feature_importance.png")
plt.show()

# 4. Precision-Recall Curve
plt.figure(figsize=(6, 5))
precision, recall, _ = precision_recall_curve(y_test, y_pred_proba)
plt.plot(recall, precision, color='green', lw=2)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve', fontsize=14, fontweight='bold')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('plot_precision_recall.png', dpi=300)
print("✓ Saved: plot_precision_recall.png")
plt.show()


# Analisi aggiuntiva: Probabilità di vittoria per diversi range
print("\n" + "="*80)
print("PREDICTION PROBABILITY ANALYSIS")
print("="*80)

df_test = X_test.copy()
df_test['actual_win'] = y_test.values
df_test['predicted_win'] = y_pred
df_test['win_probability'] = y_pred_proba

# Histogram delle probabilità predette
plt.figure(figsize=(7, 5))
plt.hist(df_test[df_test['actual_win']==1]['win_probability'], 
         bins=20, alpha=0.6, label='Actual Wins', color='green')
plt.hist(df_test[df_test['actual_win']==0]['win_probability'], 
         bins=20, alpha=0.6, label='Actual Losses', color='red')
plt.xlabel('Predicted Win Probability')
plt.ylabel('Frequency')
plt.title('Distribution of Predicted Win Probabilities', fontsize=12, fontweight='bold')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('plot_probability_distribution.png', dpi=300)
print("✓ Saved: plot_probability_distribution.png")
plt.show()

# Calibration plot
plt.figure(figsize=(7, 5))
prob_bins = np.linspace(0, 1, 11)
bin_centers = (prob_bins[:-1] + prob_bins[1:]) / 2
true_probs = []

for i in range(len(prob_bins)-1):
    mask = (df_test['win_probability'] >= prob_bins[i]) & \
           (df_test['win_probability'] < prob_bins[i+1])
    if mask.sum() > 0:
        true_probs.append(df_test[mask]['actual_win'].mean())
    else:
        true_probs.append(np.nan)

plt.plot([0, 1], [0, 1], 'k--', label='Perfect Calibration')
plt.plot(bin_centers, true_probs, 'o-', label='Model', color='blue', markersize=8)
plt.xlabel('Predicted Probability')
plt.ylabel('Actual Probability')
plt.title('Calibration Plot', fontsize=12, fontweight='bold')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('plot_calibration.png', dpi=300)
print("✓ Saved: plot_calibration.png")
plt.show()


# Save results to CSV
results_df = df_test[['win_probability', 'predicted_win', 'actual_win']]
results_df.to_csv('predictions_results.csv', index=False)
print("\n✓ Predictions saved to 'predictions_results.csv'")

print("\n" + "="*80)
print("MODEL TRAINING AND EVALUATION COMPLETED!")
print("="*80)