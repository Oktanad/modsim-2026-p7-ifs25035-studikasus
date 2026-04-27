import json
from app.extensions import SessionLocal
from app.models.question_set import QuestionSet
from app.models.question import Question
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_llm_response


def create_question_set(subject: str, topic: str, difficulty: str, total: int):
    session = SessionLocal()
    try:
        prompt = f"""
        Dalam format JSON, buat {total} soal pilihan ganda untuk mata pelajaran "{subject}"
        dengan topik "{topic}" dan tingkat kesulitan "{difficulty}".

        Format:
        {{
            "questions": [
                {{
                    "question_text": "...",
                    "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
                    "answer": "A"
                }}
            ]
        }}

        Pastikan:
        - Setiap soal memiliki tepat 4 pilihan (A, B, C, D)
        - Field "answer" berisi huruf kapital pilihan yang benar (A/B/C/D)
        - Soal sesuai dengan tingkat kesulitan "{difficulty}"
        """

        result = generate_from_llm(prompt)
        questions_data = parse_llm_response(result)

        # Simpan QuestionSet
        qs = QuestionSet(subject=subject, topic=topic, difficulty=difficulty)
        session.add(qs)
        session.commit()

        # Simpan setiap Question
        saved = []
        for item in questions_data:
            q = Question(
                question_text=item.get("question_text"),
                options=json.dumps(item.get("options", []), ensure_ascii=False),
                answer=item.get("answer"),
                set_id=qs.id
            )
            session.add(q)
            saved.append({
                "question_text": item.get("question_text"),
                "options": item.get("options", []),
                "answer": item.get("answer")
            })

        session.commit()

        return {
            "set_id": qs.id,
            "subject": subject,
            "topic": topic,
            "difficulty": difficulty,
            "total": len(saved),
            "data": saved
        }

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_all_questions(subject: str = None, page: int = 1, per_page: int = 100):
    session = SessionLocal()
    try:
        query = session.query(Question).join(QuestionSet, Question.set_id == QuestionSet.id)

        if subject:
            query = query.filter(QuestionSet.subject.ilike(f"%{subject}%"))

        total = query.count()
        data = (
            query
            .order_by(Question.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        result = []
        for q in data:
            result.append({
                "id": q.id,
                "question_text": q.question_text,
                "options": json.loads(q.options) if q.options else [],
                "answer": q.answer,
                "set_id": q.set_id,
                "created_at": q.created_at.isoformat()
            })

        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
            "data": result
        }
    finally:
        session.close()
