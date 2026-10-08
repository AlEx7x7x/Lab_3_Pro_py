from collections.abc import Iterable, Iterator
from .models import StudentRecord

def validate_students(rows: Iterable[dict[str, str]]) -> Iterator[StudentRecord]:
    for row in rows:
        try:
            student_id = int(row["student_id"])
            name = row["name"].strip()
            group = row["group"].strip()
            grade = float(row["grade"])
        except (ValueError, TypeError, KeyError):
            continue
            
        if not name or not group or not (0 <= grade <= 100):
            continue
            
        yield StudentRecord(student_id=student_id, name=name, group=group, grade=grade)

def filter_by_grade(students: Iterable[StudentRecord], minimum: float) -> Iterator[StudentRecord]:
    for student in students:
        if student.grade >= minimum:
            yield student