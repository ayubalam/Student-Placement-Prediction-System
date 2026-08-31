from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_file,
    flash
)

import os
import joblib
import pandas as pd

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database import (
    create_table,
    register_student,
    get_student_by_email,
    save_prediction,
    get_student_predictions
)

from src.career_recommendation import get_career_recommendation
from src.pdf_generator import generate_pdf


app = Flask(__name__)

app.secret_key = "student_placement_prediction_secret"

create_table()


model = joblib.load("models/placement_model.pkl")

scaler = joblib.load("models/scaler.pkl")


@app.route("/")
def home():

    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":

        return render_template("login.html")

    email = request.form["email"]

    password = request.form["password"]

    student = get_student_by_email(email)

    if student is None:

        flash("Email is not registered.")

        return redirect(url_for("login"))

    if not check_password_hash(student["password"], password):

        flash("Incorrect Password.")

        return redirect(url_for("login"))

    session["student_id"] = student["id"]

    session["student_name"] = student["full_name"]

    return redirect(url_for("prediction"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":

        return render_template("register.html")

    full_name = request.form["name"]

    email = request.form["email"]

    password = request.form["password"]

    confirm_password = request.form["confirm_password"]

    if password != confirm_password:

        flash("Passwords do not match.")

        return redirect(url_for("register"))

    hashed_password = generate_password_hash(password)

    success = register_student(
        full_name,
        email,
        hashed_password
    )

    if not success:

        flash("Email already exists.")

        return redirect(url_for("register"))

    flash("Registration Successful. Please Login.")

    return redirect(url_for("login"))


@app.route("/prediction")
def prediction():

    if "student_id" not in session:

        return redirect(url_for("login"))

    return render_template(
        "index.html",
        student_name=session.get("student_name")
    )


@app.route("/predict", methods=["POST"])
def predict():

    if "student_id" not in session:

        return redirect(url_for("login"))


    cgpa = float(request.form["cgpa"])

    marks = float(request.form["marks"])

    internship = int(request.form["internship"])

    tier = request.form["tier"]


    fullstack_projects = int(
        request.form["fullstack_projects"]
    )

    aiml_projects = int(
        request.form["aiml_projects"]
    )

    android_projects = int(
        request.form["android_projects"]
    )

    uiux_projects = int(
        request.form["uiux_projects"]
    )

    dsa_rating = int(
        request.form["dsa_rating"]
    )

    certifications = int(
        request.form["certifications"]
    )

    communication = request.form["communication"]


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


    result = model.predict(
        student_scaled
    )


    probability = round(

        model.predict_proba(
            student_scaled
        )[0][1] * 100,

        2

    )


    if result[0] == 1:

        prediction = (
            "🎉 Congratulations! "
            "You are likely to be Placed."
        )

        prediction_class = "success"

    else:

        prediction = (
            "😔 Better Luck Next Time! "
            "You are currently predicted as Not Placed."
        )

        prediction_class = "danger"


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


    student_data = {

        "cgpa": cgpa,

        "marks": marks,

        "internship":
            "Yes" if internship else "No",

        "tier": tier,

        "fullstack_projects":
            fullstack_projects,

        "aiml_projects":
            aiml_projects,

        "android_projects":
            android_projects,

        "uiux_projects":
            uiux_projects,

        "dsa_rating":
            dsa_rating,

        "certifications":
            certifications,

        "communication":
            communication

    }


    save_prediction(

        session["student_id"],

        cgpa,

        marks,

        internship,

        tier,

        fullstack_projects,

        aiml_projects,

        android_projects,

        uiux_projects,

        dsa_rating,

        certifications,

        communication,

        prediction,

        probability,

        career_result

    )


    session["prediction"] = prediction

    session["prediction_class"] = prediction_class

    session["probability"] = probability

    session["student_data"] = student_data

    session["career_result"] = career_result


    return render_template(

        "dashboard.html",

        student_name=session.get(
            "student_name"
        ),

        prediction=prediction,

        prediction_class=prediction_class,

        probability=probability,

        student_data=student_data,

        career_result=career_result

    )


@app.route("/history")
def history():

    if "student_id" not in session:

        return redirect(url_for("login"))

    predictions = get_student_predictions(
        session["student_id"]
    )

    return render_template(
        "history.html",
        student_name=session.get("student_name"),
        predictions=predictions
    )


@app.route("/download-report")
def download_report():

    if "student_id" not in session:

        return redirect(url_for("login"))


    prediction = session.get("prediction")

    probability = session.get("probability")

    student_data = session.get("student_data")

    career_result = session.get("career_result")


    if student_data is None:

        flash("Please predict first.")

        return redirect(
            url_for("prediction")
        )


    os.makedirs(
        "reports",
        exist_ok=True
    )


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


@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.")

    return redirect(
        url_for("login")
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )