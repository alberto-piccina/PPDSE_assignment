import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, confusion_matrix, 
                            roc_curve, auc, accuracy_score, precision_recall_curve)
import warnings
warnings.filterwarnings('ignore')

# Carica il dataset
df = pd.read_csv("battles_dataframe.csv")

print("="*80)
print("POKEMON BATTLE WIN PROBABILITY PREDICTOR")
print("="*80)
print(f"\nDataset shape: {df.shape}")
print(f"Total battles: {len(df)}")
print(f"\nOutcome distribution:\n{df['outcome'].value_counts()}")

# Preprocessing
# Converti i tipi in categorici (encoding)
le_type = LabelEncoder()

# Combina tutti i tipi per un encoding consistente
all_types = pd.concat([
    df['player_type1'], 
    df['player_type2'].dropna(),
    df['opponent_type1'],
    df['opponent_type2'].dropna()
]).unique()

le_type.fit(all_types)

# Encoding dei tipi
df['player_type1_encoded'] = le_type.transform(df['player_type1'])
df['player_type2_encoded'] = df['player_type2'].apply(
    lambda x: le_type.transform([x])[0] if pd.notna(x) else -1
)
df['opponent_type1_encoded'] = le_type.transform(df['opponent_type1'])
df['opponent_type2_encoded'] = df['opponent_type2'].apply(
    lambda x: le_type.transform([x])[0] if pd.notna(x) else -1
)

# Target: 1 se victory, 0 se loss
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

# Training del modello
print("\n" + "="*80)
print("TRAINING RANDOM FOREST CLASSIFIER")
print("="*80)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Predizioni
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Metriche
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

# Visualizzazioni
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0, 0])
axes[0, 0].set_title('Confusion Matrix', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Predicted')
axes[0, 0].set_ylabel('Actual')
axes[0, 0].set_xticklabels(['Loss', 'Victory'])
axes[0, 0].set_yticklabels(['Loss', 'Victory'])

# 2. ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

axes[0, 1].plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'ROC curve (AUC = {roc_auc:.3f})')
axes[0, 1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
axes[0, 1].set_xlim([0.0, 1.0])
axes[0, 1].set_ylim([0.0, 1.05])
axes[0, 1].set_xlabel('False Positive Rate')
axes[0, 1].set_ylabel('True Positive Rate')
axes[0, 1].set_title('ROC Curve', fontsize=14, fontweight='bold')
axes[0, 1].legend(loc="lower right")
axes[0, 1].grid(alpha=0.3)

# 3. Feature Importance (Top 10)
top_features = feature_importance.head(10)
axes[1, 0].barh(top_features['feature'], top_features['importance'], color='steelblue')
axes[1, 0].set_xlabel('Importance')
axes[1, 0].set_title('Top 10 Feature Importance', fontsize=14, fontweight='bold')
axes[1, 0].invert_yaxis()
axes[1, 0].grid(axis='x', alpha=0.3)

# 4. Precision-Recall Curve
precision, recall, _ = precision_recall_curve(y_test, y_pred_proba)
axes[1, 1].plot(recall, precision, color='green', lw=2)
axes[1, 1].set_xlabel('Recall')
axes[1, 1].set_ylabel('Precision')
axes[1, 1].set_title('Precision-Recall Curve', fontsize=14, fontweight='bold')
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('battle_prediction_results.png', dpi=300, bbox_inches='tight')
print("\n✓ Plots saved as 'battle_prediction_results.png'")
plt.show()

# Analisi aggiuntiva: Probabilità di vittoria per diversi range
print("\n" + "="*80)
print("PREDICTION PROBABILITY ANALYSIS")
print("="*80)

df_test = X_test.copy()
df_test['actual_win'] = y_test.values
df_test['predicted_win'] = y_pred
df_test['win_probability'] = y_pred_proba

# Distribuzione delle probabilità
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram delle probabilità predette
axes[0].hist(df_test[df_test['actual_win']==1]['win_probability'], 
             bins=20, alpha=0.6, label='Actual Wins', color='green')
axes[0].hist(df_test[df_test['actual_win']==0]['win_probability'], 
             bins=20, alpha=0.6, label='Actual Losses', color='red')
axes[0].set_xlabel('Predicted Win Probability')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of Predicted Win Probabilities', 
                  fontsize=12, fontweight='bold')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Calibration plot
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

axes[1].plot([0, 1], [0, 1], 'k--', label='Perfect Calibration')
axes[1].plot(bin_centers, true_probs, 'o-', label='Model', color='blue', markersize=8)
axes[1].set_xlabel('Predicted Probability')
axes[1].set_ylabel('Actual Probability')
axes[1].set_title('Calibration Plot', fontsize=12, fontweight='bold')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('probability_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Plots saved as 'probability_analysis.png'")
plt.show()

# Salva il modello e alcuni esempi di predizione
print("\n" + "="*80)
print("SAMPLE PREDICTIONS")
print("="*80)

sample_predictions = df_test.head(10)[['win_probability', 'predicted_win', 'actual_win']]
sample_predictions.columns = ['Win Probability', 'Predicted', 'Actual']
print(sample_predictions.to_string())

# Salva risultati in CSV
results_df = df_test[['win_probability', 'predicted_win', 'actual_win']]
results_df.to_csv('predictions_results.csv', index=False)
print("\n✓ Predictions saved to 'predictions_results.csv'")

print("\n" + "="*80)
print("MODEL TRAINING AND EVALUATION COMPLETED!")
print("="*80)