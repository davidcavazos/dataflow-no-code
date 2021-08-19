# User defined function.


from typing import Iterable, List


# Side inputs must be Iterable.
# Since the output must be JSON-encodable, we must return a List, not Iterable.
def with_numbers(name: str, numbers: Iterable[float]) -> List[str]:
    return [f"{name} {num}" for num in numbers]
