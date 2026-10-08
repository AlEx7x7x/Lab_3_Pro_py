from pathlib import Path
from readers import read_lines
from parsers import parse_csv_rows
from filters import validate_products

def build_pipeline(path: Path):
    lines = read_lines(path)
    rows = parse_csv_rows(lines)
    valid = validate_products(rows)
    return valid