import pandas as pd
import joblib

model = joblib.load("models/placement_model.pkl")

scaler = joblib.load("models/scaler.pkl")

student = pd.DataFrame({
    "cgpa": [8.5],
    "placement_exam_marks": [75],
    "internship_experience": [1],
    "college_tier_Tier 1": [1],
    "college_tier_Tier 2": [0],
    "college_tier_Tier 3": [0]
})

student_scaled = scaler.transform(student)

prediction = model.predict(student_scaled)

if prediction[0] == 1:
    print("Prediction: Placed")
else:
    print("Prediction: Not Placed")