from flask import Blueprint, request, jsonify
from app.services.question_service import create_question_set, get_all_questions

question_bp = Blueprint("question", __name__)


@question_bp.route("/questions/generate", methods=["POST"])
def generate():
    data = request.get_json()
    subject = data.get("subject")
    topic = data.get("topic")
    difficulty = data.get("difficulty")
    total = data.get("total")

    if not subject:
        return jsonify({"error": "Subject (mata pelajaran) is required"}), 400
    if not topic:
        return jsonify({"error": "Topic (topik) is required"}), 400
    if not difficulty:
        return jsonify({"error": "Difficulty (tingkat kesulitan) is required"}), 400
    if difficulty not in ["mudah", "sedang", "sulit"]:
        return jsonify({"error": "Difficulty harus salah satu dari: mudah, sedang, sulit"}), 400
    if not total:
        return jsonify({"error": "Total (jumlah soal) is required"}), 400
    if total <= 0:
        return jsonify({"error": "Total harus lebih besar dari 0"}), 400
    if total > 10:
        return jsonify({"error": "Total maksimal 10 soal"}), 400

    try:
        result = create_question_set(subject, topic, difficulty, total)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@question_bp.route("/questions", methods=["GET"])
def get_all():
    subject = request.args.get("subject", default=None)
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=100, type=int)
    data = get_all_questions(subject=subject, page=page, per_page=per_page)
    return jsonify(data)
