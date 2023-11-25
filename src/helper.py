from pathlib import Path
from typing import List


def load_data(file_path: Path) -> List[str]:
    with file_path.open() as f:
        data = f.read().splitlines()
    return data
