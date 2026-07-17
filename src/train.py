import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

df = pd.read_csv("data/raw/Student_Placement_Record.csv")

df = df.drop_duplicates()

df = pd.get_dummies(df, columns=["college_tier"], dtype=int)

X = df.drop("placement", axis=1)

y = df["placement"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

model = LogisticRegression()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print()

print("Model Trained Successfully")

print()

print("Accuracy:", accuracy)

joblib.dump(model, "models/placement_model.pkl")

joblib.dump(scaler, "models/scaler.pkl")

print()

print("Model Saved Successfully")

print("Scaler Saved Successfully")