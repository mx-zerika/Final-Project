import json
from pathlib import Path

#Subject system configuration

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SUBJECT_PROGRESS_FILE = DATA_DIR / "subject_progress.json"

EXP_PER_LEVEL = 100
EXP_PER_LESSON = 20

DEFAULT_PROGRESS = {
    "version": 1,
    "subjects": {
        "english": {
            "exp": 0,
            "level": 1,
            "completed_lessons": {}
        },
        "python": {
            "level": 0,
            "level": 1,
            "completed_lessons": {}
        }
    }
}

#Default Data

def create_default_progress():
    return {
        "version": 1,
        "subjects": {
            subject: {
                "exp": 0,
                "level": 1,
                "completed_lessons": {}
            }
            for subject in ("english", "python")
        }
    }

def load_subject_progress():

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not SUBJECT_PROGRESS_FILE.exists():
        progress = create_default_progress()
        save_subject_progress(progress)
        return progress

    try:
        with open(
            SUBJECT_PROGRESS_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            saved_data = json.load(file)

    except (json.JSONDecodeError, OSError):
        return create_default_progress()

    defaults = create_default_progress()

    if not isinstance(saved_data, dict):
        return defaults

    saved_subjects = saved_data.get("subjects", {})

    if not isinstance(saved_subjects, dict):
        return defaults

    for subject in ("english", "python"):
        subject_data = saved_subjects.get(subject, dict)
        if not isinstance(subject_data, dict):
            subject_data = {}

        defaults["subjects"][subject]["exp"] = max(
            0,
            int(subject_data.get("exp", 0))
        )
        defaults["subjects"][subject]["level"] = max(
            1,
            int(subject_data.get("exp", 1))
        )

        completed = subject_data.get(
            "completed_lessons", []
        )

        if isinstance(completed, list):
            defaults["subjects"][subject]["completed_lessons"] = completed

    return defaults

def save_subject_progress(progress):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(
        SUBJECT_PROGRESS_FILE,
        "w",
            encoding="utf-8"
    ) as file:
        json.dump(
            progress,
            file,
            indent=4
        )

def get_subject_data(progress, subject):

    subject = subject.lower()

    if subject not in ("english", "python"):
        raise ValueError(
            f"Unknown subject: {subject}"
        )

    return progress["subjects"][subject]

def award_subject_exp(progress, subject, amount=20):

    subject_data = get_subject_data(
        progress,
        subject
    )

    old_level = subject_data["level"]
    subject_data["exp"] += amount

    while subject_data["exp"] >= EXP_PER_LEVEL:

        subject_data["exp"] -= EXP_PER_LEVEL
        subject_data["level"] += 1
        save_subject_progress(progress)

    return old_level, subject_data["level"]

def complete_subject_lesson(progress, subject, lesson_id):

    subject_data = get_subject_data(progress, subject)

    completed = subject_data["completed_lesosns"]

    if lesson_id in completed:
        return False, subject_data["level"], subject_data["level"]

    old_level = subject_data["level"]

    subject_data["exp"] += EXP_PER_LESSON

    while subject_data["exp"] >= EXP_PER_LEVEL:
        subject_data["exp"] -= EXP_PER_LEVEL
        subject_data["level"] += 1

    completed.append(lesson_id)
    save_subject_progress(progress)

    return True, old_level, subject_data["level"]

def is_lesson_completed(
        progress,
        subject,
        lesson_id
):
    subject_data = get_subject_data(
        progress, 
        subject
    )

    return lesson_id in subject_data["completed_lessons"]

def get_subject_statistics(progress, subject):

    subject_data = get_subject_data(
        progress,
        subject
    )

    return {
        "level": subject_data["level"],
        "exp": subject_data["exp"],
        "exp_required": EXP_PER_LEVEL,
        "completed_count": len(
            subject_data["completed_lessons"]
        )
    }