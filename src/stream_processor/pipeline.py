from .readers import read_lines
from .parsers import parse_csv_rows
from .filters import validate_students, filter_by_grade
from .transformations import normalize_names

def build_pipeline(path: Path, minimum_grade: float = 0.0):
    lines = read_lines(path)
    rows = parse_csv_rows(lines)
    valid = validate_students(rows)
    normalized = normalize_names(valid)
    filtered = filter_by_grade(normalized, minimum_grade)
    return filtered