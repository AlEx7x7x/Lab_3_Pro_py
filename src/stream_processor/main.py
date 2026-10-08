import csv
import random
import tracemalloc
import time
from pathlib import Path
from itertools import islice

from stream_processor.pipeline import build_pipeline
from stream_processor.analytics import calculate_statistics

def generate_test_file(path: Path, count: int) -> None:
    # Створення великого test file на 100 000 records[cite: 1]
    groups = ("PI-21", "PI-22", "PI-23", "PI-24")
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["student_id", "name", "group", "grade"])
        for index in range(1, count + 1):
            writer.writerow([
                index,
                f"Student {index}",
                random.choice(groups),
                round(random.uniform(40, 100), 2),
            ])

def read_all_students_eager(path: Path) -> list[dict]:
    # Eager implementation, де весь dataset матеріалізується[cite: 1]
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)

def measure_execution(function, *args):
    # Оцінка memory consumption[cite: 1]
    tracemalloc.start()
    start_time = time.time()
    
    result = function(*args)
    
    elapsed_time = time.time() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return result, peak / 1024 / 1024, elapsed_time # Пам'ять у МБ

def consume_lazy(path: Path):
    pipeline = build_pipeline(path, 0)
    # Generator expression[cite: 1]
    grades = (student.grade for student in pipeline)
    return sum(grades)

def main() -> None:
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    path = data_dir / "students_large.csv"
    
    print("Генерація тестового файлу (100,000 записів)...")
    generate_test_file(path, 100_000)
    
    # Демонстрація роботи пайплайну
    pipeline = build_pipeline(path, 85.0)
    print("\nПерші 3 студенти з балом >= 85 (itertools.islice):")
    for student in list(islice(pipeline, 3)):
        print(student.student_id, student.name, student.group, student.grade)

    # Отримання повної статистики
    pipeline_for_stats = build_pipeline(path, 85.0)
    stats = calculate_statistics(pipeline_for_stats)
    print(f"\nСтатистика (streaming processing):")
    print(f"Кількість: {stats['count']}, Середній бал: {stats['average']:.2f}")

    # Порівняння Eager та Lazy
    print("\n--- Порівняння Eager та Lazy варіантів ---")
    
    eager_result, eager_mem, eager_time = measure_execution(read_all_students_eager, path)
    print(f"Eager Evaluation: Читання {len(eager_result)} записів")
    print(f"Eager Time: {eager_time:.4f} секунд | Eager Peak Memory: {eager_mem:.2f} MB")
    
    lazy_result, lazy_mem, lazy_time = measure_execution(consume_lazy, path)
    print(f"\nLazy Evaluation: Сума балів {lazy_result:.2f}")
    print(f"Lazy Time: {lazy_time:.4f} секунд | Lazy Peak Memory: {lazy_mem:.2f} MB")

if __name__ == "__main__":
    main()