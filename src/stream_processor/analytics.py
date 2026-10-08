from collections import Counter
from collections.abc import Iterable
from .models import StudentRecord

def calculate_statistics(students: Iterable[StudentRecord]) -> dict:
    count = 0
    total = 0.0
    minimum = None
    maximum = None
    groups = Counter()
    
    for student in students:
        grade = student.grade
        count += 1
        total += grade
        groups[student.group] += 1
        
        if minimum is None or grade < minimum:
            minimum = grade
        if maximum is None or grade > maximum:
            maximum = grade
            
    average = total / count if count else 0.0
    
    return {
        "count": count,
        "average": average,
        "minimum": minimum,
        "maximum": maximum,
        "groups": dict(groups),
    }