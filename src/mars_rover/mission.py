from __future__ import annotations
from .plateau import Plateau
from .rover import Rover


class Mission:
    """Parses input and orchestrates rovers sequentially."""

    def __init__(self, raw_input: str) -> None:
        self.plateau, self.rover_data = self._parse(raw_input.strip())

    # ── Parsing ──────────────────────────────────────────────────────────────

    @staticmethod
    def _parse(raw: str) -> tuple[Plateau, list[tuple[int, int, str, str]]]:
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        if len(lines) < 3 or (len(lines) - 1) % 2 != 0:
            raise ValueError("Invalid input format.")

        max_x, max_y = map(int, lines[0].split())
        plateau = Plateau(max_x, max_y)

        rover_data: list[tuple[int, int, str, str]] = []
        for i in range(1, len(lines), 2):
            parts = lines[i].split()
            x, y, heading = int(parts[0]), int(parts[1]), parts[2]
            instructions = lines[i + 1]
            rover_data.append((x, y, heading, instructions))

        return plateau, rover_data

    # ── Execution ────────────────────────────────────────────────────────────

    def run(self) -> list[str]:
        """Deploy each rover sequentially and return their final positions."""
        results: list[str] = []
        for x, y, heading, instructions in self.rover_data:
            rover = Rover(x, y, heading, self.plateau)
            rover.execute(instructions)
            results.append(rover.position)
        return results

    # ── Factory helpers ──────────────────────────────────────────────────────

    @classmethod
    def from_file(cls, path: str) -> "Mission":
        with open(path, encoding="utf-8") as fh:
            return cls(fh.read())
