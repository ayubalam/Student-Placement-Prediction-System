from flask import Flask, render_template, request
import pandas as pd
import joblib

from src.career_recommendation import get_career_recommendation

app = Flask(__name__)

# Load ML Model
model = joblib.load("models/placement_model.pkl")
scaler = joblib.load("models/scaler.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # ==========================
    # Academic Details
    # ==========================

    cgpa = float(request.form["cgpa"])
    marks = float(request.form["marks"])
    internship = int(request.form["internship"])
    tier = request.form["tier"]

    # ==========================
    # Technical Profile
    # ==========================

    fullstack_projects = int(request.form["fullstack_projects"])
    aiml_projects = int(request.form["aiml_projects"])
    android_projects = int(request.form["android_projects"])
    uiux_projects = int(request.form["uiux_projects"])
    dsa_rating = int(request.form["dsa_rating"])
    certifications = int(request.form["certifications"])
    communication = request.form["communication"]

    # ==========================
    # One Hot Encoding
    # ==========================

    tier1 = 0
    tier2 = 0
    tier3 = 0

    if tier == "Tier 1":
        tier1 = 1
    elif tier == "Tier 2":
        tier2 = 1
    else:
        tier3 = 1

    # ==========================
    # ML Prediction
    # ==========================

    student = pd.DataFrame({
        "cgpa": [cgpa],
        "placement_exam_marks": [marks],
        "internship_experience": [internship],
        "college_tier_Tier 1": [tier1],
        "college_tier_Tier 2": [tier2],
        "college_tier_Tier 3": [tier3]
    })

    student_scaled = scaler.transform(student)

    result = model.predict(student_scaled)

    probability = round(
        model.predict_proba(student_scaled)[0][1] * 100,
        2
    )

    # ==========================
    # Placement Result
    # ==========================

    if result[0] == 1:
        prediction = "🎉 Congratulations! You are likely to be Placed."
        prediction_class = "success"
    else:
        prediction = "😔 Better Luck Next Time! You are currently predicted as Not Placed."
        prediction_class = "danger"

    # ==========================
    # AI Career Recommendation
    # ==========================

    career_result = get_career_recommendation(
        fullstack_projects,
        aiml_projects,
        android_projects,
        uiux_projects,
        dsa_rating,
        certifications,
        communication,
        internship
    )

    # ==========================
    # Student Summary
    # ==========================

    student_data = {

        "cgpa": cgpa,
        "marks": marks,
        "internship": "Yes" if internship else "No",
        "tier": tier,

        "fullstack_projects": fullstack_projects,
        "aiml_projects": aiml_projects,
        "android_projects": android_projects,
        "uiux_projects": uiux_projects,
        "dsa_rating": dsa_rating,
        "certifications": certifications,
        "communication": communication

    }

    # ==========================
    # Open Dashboard Page
    # ==========================

    return render_template(
        "dashboard.html",
        prediction=prediction,
        prediction_class=prediction_class,
        probability=probability,
        student_data=student_data,
        career_result=career_result
    )


if __name__ == "__main__":
    app.run(debug=True)