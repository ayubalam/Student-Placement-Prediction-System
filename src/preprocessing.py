import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

df = pd.read_csv("data/raw/Student_Placement_Record.csv")

print(df.head())

print()

print(df.tail())

print()

print(df.shape)

print()

print(df.columns)

print()

df.info()

print()

print(df.describe())

print()

print(df.isnull().sum())

print()

print(df.duplicated().sum())

df = df.drop_duplicates()

print()

print(df.duplicated().sum())

print()

print(df.shape)

print()

print(df["college_tier"].unique())

print()

print(df["college_tier"].nunique())

plt.figure(figsize=(6, 4))

sns.countplot(x="placement", data=df)

plt.title("Student Placement Distribution")

plt.xlabel("Placement")

plt.ylabel("Number of Students")

plt.show()

plt.figure(figsize=(8, 5))

sns.histplot(df["cgpa"], bins=20, kde=True)

plt.title("CGPA Distribution")

plt.xlabel("CGPA")

plt.ylabel("Number of Students")

plt.show()

plt.figure(figsize=(8, 5))

sns.boxplot(x=df["cgpa"])

plt.title("CGPA Box Plot")

plt.xlabel("CGPA")

plt.show()

plt.figure(figsize=(8, 5))

sns.scatterplot(
    x="cgpa",
    y="placement_exam_marks",
    hue="placement",
    data=df
)

plt.title("CGPA vs Placement Exam Marks")

plt.xlabel("CGPA")

plt.ylabel("Placement Exam Marks")

plt.show()

correlation = df.select_dtypes(include=["number"]).corr()

plt.figure(figsize=(8, 6))

sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f")

plt.title("Correlation Heatmap")

plt.show()

df = pd.get_dummies(df, columns=["college_tier"], dtype=int)

print()

print(df.head())

print()

print(df.columns)

print()

print(df.shape)

X = df.drop("placement", axis=1)

y = df["placement"]

print()

print(X.head())

print()

print(y.head())

print()

print(X.shape)

print()

print(y.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print()

print(X_train.shape)

print(X_test.shape)

print(y_train.shape)

print(y_test.shape)

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)

model = LogisticRegression()

model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)

print()

print("========== Logistic Regression ==========")

print()

print("Accuracy:", accuracy)

print()

print("Confusion Matrix")

print(confusion_matrix(y_test, y_pred))

print()

print("Classification Report")

print(classification_report(y_test, y_pred))

decision_tree = DecisionTreeClassifier(random_state=42)

decision_tree.fit(X_train, y_train)

dt_predictions = decision_tree.predict(X_test)

dt_accuracy = accuracy_score(y_test, dt_predictions)

print()

print("========== Decision Tree ==========")

print()

print("Accuracy:", dt_accuracy)

print()

print("Confusion Matrix")

print(confusion_matrix(y_test, dt_predictions))

print()

print("Classification Report")

print(classification_report(y_test, dt_predictions))

random_forest = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

random_forest.fit(X_train, y_train)

rf_predictions = random_forest.predict(X_test)

rf_accuracy = accuracy_score(y_test, rf_predictions)

print()

print("========== Random Forest ==========")

print()

print("Accuracy:", rf_accuracy)

print()

print("Confusion Matrix")

print(confusion_matrix(y_test, rf_predictions))

print()

print("Classification Report")

print(classification_report(y_test, rf_predictions))

knn = KNeighborsClassifier(n_neighbors=5)

knn.fit(X_train_scaled, y_train)

knn_predictions = knn.predict(X_test_scaled)

knn_accuracy = accuracy_score(y_test, knn_predictions)

print()

print("========== K-Nearest Neighbors ==========")

print()

print("Accuracy:", knn_accuracy)

print()

print("Confusion Matrix")

print(confusion_matrix(y_test, knn_predictions))

print()

print("Classification Report")

print(classification_report(y_test, knn_predictions))

svm = SVC(kernel="linear", random_state=42)

svm.fit(X_train_scaled, y_train)

svm_predictions = svm.predict(X_test_scaled)

svm_accuracy = accuracy_score(y_test, svm_predictions)

print()

print("========== Support Vector Machine ==========")

print()

print("Accuracy:", svm_accuracy)

print()

print("Confusion Matrix")

print(confusion_matrix(y_test, svm_predictions))

print()

print("Classification Report")

print(classification_report(y_test, svm_predictions))