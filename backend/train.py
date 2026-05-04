import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# ==============================
# PATH
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "16P.csv")

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv(DATA_PATH, encoding="latin1")

print("Dataset shape:", df.shape)

# ==============================
# LABEL COLUMN (LAST COLUMN)
# ==============================
label_col = df.columns[-1]

# ==============================
# FEATURES (ALL QUESTIONS)
# ==============================
X = df.drop(columns=[label_col])

# convert to numeric (VERY IMPORTANT)
X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

y = df[label_col]

# ==============================
# SPLIT
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==============================
# MODEL (BETTER FOR TABULAR DATA)
# ==============================
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ==============================
# EVALUATION
# ==============================
acc = model.score(X_test, y_test)
print("✅ Accuracy:", acc)

# ==============================
# SAVE MODEL
# ==============================
joblib.dump(model, os.path.join(BASE_DIR, "backend", "model.pkl"))

print("🎉 TRAINING COMPLETED SUCCESSFULLY")