from pathlib import Path


def get_latest_split():
    return sorted([*Path("split").iterdir()])[-1]
