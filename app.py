from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_file
)

import pandas as pd
import joblib
import os

from src.career_recommendation import get_career_recommendation
from src.pdf_generator import generate_pdf

app = Flask(__name__)

app.secret_key = "student_placement_prediction_secret"

# ==========================
# Load ML Model
# ==========================

model = joblib.load("models/placement_model.pkl")
scaler = joblib.load("models/scaler.pkl")


# ==========================
# Home Page
# ==========================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================
# Predict Placement
# ==========================

@app.route("/predict", methods=["POST"])
def predict():

    # Academic Details

    cgpa = float(request.form["cgpa"])
    marks = float(request.form["marks"])
    internship = int(request.form["internship"])
    tier = request.form["tier"]

    # Technical Profile

    fullstack_projects = int(request.form["fullstack_projects"])
    aiml_projects = int(request.form["aiml_projects"])
    android_projects = int(request.form["android_projects"])
    uiux_projects = int(request.form["uiux_projects"])
    dsa_rating = int(request.form["dsa_rating"])
    certifications = int(request.form["certifications"])
    communication = request.form["communication"]

    # One Hot Encoding

    tier1 = 0
    tier2 = 0
    tier3 = 0

    if tier == "Tier 1":
        tier1 = 1
    elif tier == "Tier 2":
        tier2 = 1
    else:
        tier3 = 1

    # ML Prediction

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

    if result[0] == 1:

        prediction = "🎉 Congratulations! You are likely to be Placed."

        prediction_class = "success"

    else:

        prediction = "😔 Better Luck Next Time! You are currently predicted as Not Placed."

        prediction_class = "danger"

    # Career Recommendation

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

    # Student Summary

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

    # Store in Session

    session["prediction"] = prediction
    session["prediction_class"] = prediction_class
    session["probability"] = probability
    session["student_data"] = student_data
    session["career_result"] = career_result

    # Open Dashboard

    return render_template(

        "dashboard.html",

        prediction=prediction,
        prediction_class=prediction_class,
        probability=probability,
        student_data=student_data,
        career_result=career_result

    )


# ==========================
# Download PDF Report
# ==========================

@app.route("/download-report")
def download_report():

    prediction = session.get("prediction")
    probability = session.get("probability")
    student_data = session.get("student_data")
    career_result = session.get("career_result")

    if student_data is None:

        return redirect(url_for("home"))

    os.makedirs("reports", exist_ok=True)

    pdf_path = os.path.join(

        "reports",

        "placement_report.pdf"

    )

    generate_pdf(

        pdf_path,

        student_data,
        prediction,
        probability,
        career_result

    )

    return send_file(

        pdf_path,

        as_attachment=True

    )


# ==========================
# Run App
# ==========================

if __name__ == "__main__":

    app.run(debug=True)