from skill_db import skills_db

from skill_db import skills_db

negative_words = [
    "don't know",
    "do not know",
    "not familiar with",
    "no experience in",
    "cannot use",
    "can't use",
    "never used"
]

def extract_skills(text):

    found = []

    sentences = text.lower().split(".")

    for sentence in sentences:

        for role, skills in skills_db.items():

            for skill in skills:

                if skill in sentence:

                    negative = False

                    for neg in negative_words:

                        if neg in sentence:
                            negative = True
                            break

                    if not negative:
                        found.append(skill)

    return list(set(found))


def match_jobs(found_skills):
    results = {}

    for role, skills in skills_db.items():
        match = len(set(found_skills) & set(skills))
        score = int((match / len(skills)) * 100)
        results[role] = score

    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))


def resume_score(found_skills):
    return min(100, len(found_skills) * 10)


def missing_skills(top_role, found_skills):
    return list(set(skills_db[top_role]) - set(found_skills))


def interview_questions():
    return [
        "What is Python?",
        "Explain OOP concepts.",
        "What is SQL?",
        "Difference between list and tuple?",
        "What is API?",
        "What is machine learning?",
        "Explain Django/Flask.",
        "What is normalization?",
        "What is React?",
        "What is debugging?",
        "what is pyspark?",
        "what is diff between join vs group by?"
    ]

def fake_resume_score(text, skills):
    warnings = []

    # Too many repeated words
    words = text.split()
    if len(words) > 0:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.4:
            warnings.append("Too many repeated words (possible keyword stuffing)")

    # Too many skills
    if len(skills) > 15:
        warnings.append("Too many skills listed (may be unrealistic)")

    # Same skill repeated many times
    for skill in skills:
        if text.count(skill) > 10:
            warnings.append(f"'{skill}' repeated too many times")

    if not warnings:
        return "✅ Resume looks genuine"
    
    return "⚠️ Issues found:\n" + "\n".join(warnings)


