from collections.abc import Iterable, Iterator
from itertools import islice
from .models import StudentRecord

def batched_students(students: Iterable[StudentRecord], batch_size: int) -> Iterator[list[StudentRecord]]:
    iterator = iter(students)
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch:
            return
        yield batch