def get_career_recommendation(
    fullstack_projects,
    aiml_projects,
    android_projects,
    uiux_projects,
    dsa_rating,
    certifications,
    communication,
    internship
):

    communication_score = {
        "Excellent": 20,
        "Good": 15,
        "Average": 10,
        "Poor": 5
    }

    communication_marks = communication_score.get(
        communication,
        10
    )

    internship_bonus = 15 if internship else 0

    dsa_score = dsa_rating / 100

    # ================================
    # Career Scores
    # ================================

    scores = {

        "Full Stack Developer":

            (fullstack_projects * 10) +
            dsa_score +
            (certifications * 5) +
            communication_marks +
            internship_bonus,

        "AI / ML Engineer":

            (aiml_projects * 10) +
            dsa_score +
            (certifications * 5) +
            communication_marks +
            internship_bonus,

        "Android Developer":

            (android_projects * 10) +
            dsa_score +
            (certifications * 5) +
            communication_marks +
            internship_bonus,

        "UI / UX Designer":

            (uiux_projects * 10) +
            (communication_marks * 1.5) +
            (certifications * 5)

    }

    career = max(scores, key=scores.get)

    career_score = round(scores[career], 2)

    # =====================================
    # Companies
    # =====================================

    companies = {

        "Full Stack Developer": [

            "Google",
            "Microsoft",
            "Amazon",
            "Infosys",
            "Accenture"

        ],

        "AI / ML Engineer": [

            "OpenAI",
            "Google DeepMind",
            "Microsoft",
            "NVIDIA",
            "Fractal Analytics"

        ],

        "Android Developer": [

            "Google",
            "Samsung",
            "PhonePe",
            "Paytm",
            "Flipkart"

        ],

        "UI / UX Designer": [

            "Adobe",
            "Figma",
            "Zomato",
            "Swiggy",
            "CRED"

        ]

    }

    # =====================================
    # Skills
    # =====================================

    skills = {

        "Full Stack Developer": [

            "React",
            "Node.js",
            "MongoDB",
            "Docker",
            "AWS"

        ],

        "AI / ML Engineer": [

            "Python",
            "TensorFlow",
            "PyTorch",
            "Scikit-learn",
            "Deep Learning"

        ],

        "Android Developer": [

            "Kotlin",
            "Jetpack Compose",
            "Firebase",
            "REST API",
            "MVVM"

        ],

        "UI / UX Designer": [

            "Figma",
            "Adobe XD",
            "Design Systems",
            "Prototyping",
            "User Research"

        ]

    }

    # =====================================
    # Roadmap
    # =====================================

    roadmap = {

        "Month 1":

            "Strengthen Core Concepts",

        "Month 2":

            "Build Advanced Projects",

        "Month 3":

            "Practice Interview Questions",

        "Month 4":

            "Apply to Companies"

    }

    return {

        "career": career,

        "career_score": career_score,

        "companies": companies[career],

        "skills": skills[career],

        "roadmap": roadmap

    }