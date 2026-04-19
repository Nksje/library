import json
import os

from abstractions.protocols import LibraryPersistence


class JsonLibraryPersistence:
    """JSON file persistence (SRP: only serialization I/O, no domain rules)."""

    def __init__(self, filepath: str):
        self._filepath = filepath

    def save(self, payload: dict) -> None:
        with open(self._filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def load(self) -> dict:
        if not os.path.exists(self._filepath):
            raise FileNotFoundError(f"File not found: {self._filepath}")
        with open(self._filepath, "r", encoding="utf-8") as f:
            return json.load(f)
