from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load("models/placement_model.pkl")
scaler = joblib.load("models/scaler.pkl")


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    prediction_class = ""

    if request.method == "POST":

        cgpa = float(request.form["cgpa"])
        marks = float(request.form["marks"])
        internship = int(request.form["internship"])
        tier = request.form["tier"]

        tier1 = 0
        tier2 = 0
        tier3 = 0

        if tier == "Tier 1":
            tier1 = 1
        elif tier == "Tier 2":
            tier2 = 1
        else:
            tier3 = 1

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

        if result[0] == 1:
            prediction = "Placed"
            prediction_class = "success"
        else:
            prediction = "Not Placed"
            prediction_class = "danger"

    return render_template(
        "index.html",
        prediction=prediction,
        prediction_class=prediction_class
    )


if __name__ == "__main__":
    app.run(debug=True)