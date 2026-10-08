from collections.abc import Iterable, Iterator
from .models import StudentRecord

def normalize_names(students: Iterable[StudentRecord]) -> Iterator[StudentRecord]:
    for student in students:
        yield student._replace(name=student.name.title())