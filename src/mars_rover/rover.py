from __future__ import annotations
from .plateau import Plateau

DIRECTIONS = ["N", "E", "S", "W"]

MOVES = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
}


class Rover:
    """A robotic rover navigating a Mars plateau."""

    def __init__(self, x: int, y: int, heading: str, plateau: Plateau) -> None:
        if heading not in DIRECTIONS:
            raise ValueError(f"Invalid heading '{heading}'. Must be one of {DIRECTIONS}.")
        if not plateau.is_within_bounds(x, y):
            raise ValueError(f"Initial position ({x}, {y}) is out of bounds.")
        self.x = x
        self.y = y
        self.heading = heading
        self.plateau = plateau

    # ── Private helpers ──────────────────────────────────────────────────────

    def _turn_left(self) -> None:
        idx = DIRECTIONS.index(self.heading)
        self.heading = DIRECTIONS[(idx - 1) % 4]

    def _turn_right(self) -> None:
        idx = DIRECTIONS.index(self.heading)
        self.heading = DIRECTIONS[(idx + 1) % 4]

    def _move_forward(self) -> None:
        dx, dy = MOVES[self.heading]
        new_x, new_y = self.x + dx, self.y + dy
        if not self.plateau.is_within_bounds(new_x, new_y):
            raise ValueError(
                f"Move would take rover out of bounds: ({new_x}, {new_y})."
            )
        self.x, self.y = new_x, new_y

    # ── Public API ───────────────────────────────────────────────────────────

    def execute(self, instructions: str) -> None:
        """Execute a string of instructions ('L', 'R', 'M')."""
        for cmd in instructions.upper():
            if cmd == "L":
                self._turn_left()
            elif cmd == "R":
                self._turn_right()
            elif cmd == "M":
                self._move_forward()
            else:
                raise ValueError(f"Unknown instruction '{cmd}'.")

    @property
    def position(self) -> str:
        """Return position as 'x y HEADING' string."""
        return f"{self.x} {self.y} {self.heading}"

    def __repr__(self) -> str:
        return f"Rover(x={self.x}, y={self.y}, heading='{self.heading}')"
