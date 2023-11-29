from typing import Iterable
from typing import List


def append(hub, c1: List[str], c2) -> List[str]:
    """
    Append two comments, no matter their type
    """
    if not c2:
        return
    if not isinstance(c1, list):
        raise TypeError(f"First comment must be a list")

    if isinstance(c2, str) or not isinstance(c2, Iterable):
        c2 = [c2]

    c1.extend(c2)
