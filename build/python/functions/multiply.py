from typing import List
import numpy as np


# Note that both inputs and outputs must be JSON-encodable.
# Since numpy arrays are not JSON-encodable, we interface through lists.
def multiply(xs: List[float], n: float) -> List[float]:
    result = np.array(xs) * n
    return result.tolist()
