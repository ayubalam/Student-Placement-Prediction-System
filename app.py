from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        cgpa = request.form["cgpa"]

        marks = request.form["marks"]

        internship = request.form["internship"]

        tier = request.form["tier"]

        print("CGPA:", cgpa)
        print("Marks:", marks)
        print("Internship:", internship)
        print("College Tier:", tier)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)