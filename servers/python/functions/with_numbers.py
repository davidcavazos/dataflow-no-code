# User defined function.


from typing import List


def with_numbers(name: str, numbers: List[float]) -> List[str]:
    return [f"{name} {num}" for num in numbers]
