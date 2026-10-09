import os

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def serve_file(filename):
    return send_from_directory(BASE_DIR, filename)


CAREER_MAP = {
    "Software Engineer": "High logic and coding marks steered the profile down the software engineering branch.",
    "Data Scientist": "Strong analytical mathematics mixed with logical programming pointed the profile toward Data Science.",
    "Graphic Designer": "High creative traits paired with lower technical coding nodes prioritized the design career path.",
    "Product Manager": "Excellent communication profiles combined with balanced technical traits routed here."
}


def predict_career(math_score, coding_score, creativity_score, communication_score):
    math_score = int(math_score)
    coding_score = int(coding_score)
    creativity_score = int(creativity_score)
    communication_score = int(communication_score)

    technical_score = math_score + coding_score
    creative_score = creativity_score + communication_score

    if coding_score >= 7 and math_score >= 6 and creativity_score <= 5:
        return "Software Engineer"
    if math_score >= 7 and coding_score >= 4 and creativity_score <= 6:
        return "Data Scientist"
    if creativity_score >= 7 and coding_score <= 6 and math_score <= 7:
        return "Graphic Designer"
    if communication_score >= 7 and (math_score >= 5 or coding_score >= 5):
        return "Product Manager"

    if technical_score >= creative_score + 2:
        return "Software Engineer"
    if math_score >= creativity_score and coding_score >= communication_score:
        return "Data Scientist"
    if creativity_score >= math_score and creativity_score >= communication_score:
        return "Graphic Designer"
    return "Product Manager"


# 2. SERVE MULTI-PAGE STATIC FILES
@app.route('/')
def home():
    return serve_file('index.html')


@app.route('/index.html')
@app.route('/index')
def index_page():
    return serve_file('index.html')


@app.route('/quiz.html')
@app.route('/quiz')
@app.route('/Quiz.html')
@app.route('/Quiz')
def quiz():
    return serve_file('Quiz.html')


@app.route('/result.html')
@app.route('/result')
@app.route('/Result.html')
@app.route('/Result')
def result():
    return serve_file('Result.html')


@app.route('/style.css')
@app.route('/Style.css')
def css():
    return serve_file('Style.css')


@app.route('/script.js')
@app.route('/Script.js')
def js():
    return serve_file('Script.js')


# 3. MACHINE LEARNING PREDICTION API ENDPOINT
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "No JSON body provided."}), 400

        required_fields = [
            'math_score',
            'coding_score',
            'creativity_score',
            'communication_score'
        ]

        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        prediction = predict_career(
            data['math_score'],
            data['coding_score'],
            data['creativity_score'],
            data['communication_score']
        )

        explanation = CAREER_MAP.get(prediction, "Profile successfully calculated across branches.")

        return jsonify({
            "career": prediction,
            "explanation": explanation
        })

    except ValueError as exc:
        return jsonify({"error": f"Invalid score value: {exc}"}), 400
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == '__main__':
    print("Career prediction app is ready!")
    print("Multi-page app running at http://127.0.0.1:5000")
    app.run(port=5000, debug=True)