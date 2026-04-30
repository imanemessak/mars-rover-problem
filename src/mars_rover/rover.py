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
    """A robotic rover navigating a Mars plateau.

    The rover maintains its position (x, y) and heading (N/E/S/W) on a
    bounded plateau. It delegates boundary validation to the injected
    Plateau instance.

    Attributes:
        x: Current column position on the plateau grid.
        y: Current row position on the plateau grid.
        heading: Current cardinal direction ('N', 'E', 'S', 'W').
        plateau: The plateau used for boundary validation.
    """

    def __init__(self, x: int, y: int, heading: str, plateau: Plateau) -> None:
        """Initialise a Rover at the given position and heading.

        Args:
            x: Initial column position (must be within plateau bounds).
            y: Initial row position (must be within plateau bounds).
            heading: Initial direction; one of 'N', 'E', 'S', 'W'.
            plateau: Plateau instance used to validate movement bounds.

        Raises:
            ValueError: If heading is not a valid cardinal direction.
            ValueError: If (x, y) is outside the plateau bounds.
        """
        if heading not in DIRECTIONS:
            raise ValueError(
                f"Invalid heading '{heading}'. Must be one of {DIRECTIONS}."
            )
        if not plateau.is_within_bounds(x, y):
            raise ValueError(f"Initial position ({x}, {y}) is out of bounds.")
        self.x = x
        self.y = y
        self.heading = heading
        self.plateau = plateau

    # ── Private helpers ──────────────────────────────────────────────────────

    def _turn_left(self) -> None:
        """Rotate 90° counter-clockwise without moving."""
        idx = DIRECTIONS.index(self.heading)
        self.heading = DIRECTIONS[(idx - 1) % 4]

    def _turn_right(self) -> None:
        """Rotate 90° clockwise without moving."""
        idx = DIRECTIONS.index(self.heading)
        self.heading = DIRECTIONS[(idx + 1) % 4]

    def _move_forward(self) -> None:
        """Move one grid point in the current heading direction.

        Raises:
            ValueError: If the resulting position is outside the plateau.
        """
        dx, dy = MOVES[self.heading]
        new_x, new_y = self.x + dx, self.y + dy
        if not self.plateau.is_within_bounds(new_x, new_y):
            raise ValueError(
                f"Move would take rover out of bounds: ({new_x}, {new_y})."
            )
        self.x, self.y = new_x, new_y

    # ── Public API ───────────────────────────────────────────────────────────

    def execute(self, instructions: str) -> None:
        """Execute a string of instructions ('L', 'R', 'M').

        Instructions are case-insensitive and processed sequentially.

        Args:
            instructions: A string of commands where each character is
                'L' (turn left), 'R' (turn right), or 'M' (move forward).

        Raises:
            ValueError: If an unrecognised instruction character is found.
        """
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
        """Return position as 'x y HEADING' string.

        Returns:
            A space-separated string of the form ``'x y HEADING'``,
            e.g. ``'1 3 N'``.
        """
        return f"{self.x} {self.y} {self.heading}"

    def __repr__(self) -> str:
        """Return unambiguous string representation for debugging.

        Returns:
            A string of the form ``Rover(x=1, y=3, heading='N')``.
        """
        return f"Rover(x={self.x}, y={self.y}, heading='{self.heading}')"
