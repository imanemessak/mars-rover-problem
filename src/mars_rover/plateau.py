from __future__ import annotations


class Plateau:
    """Represents the rectangular Mars plateau.

    The plateau is a zero-indexed grid whose lower-left corner is always
    (0, 0) and whose upper-right corner is (max_x, max_y). It is the
    single source of truth for boundary validation — Rover delegates all
    bounds checks here.

    Attributes:
        max_x: Maximum valid column index (inclusive).
        max_y: Maximum valid row index (inclusive).
    """

    def __init__(self, max_x: int, max_y: int) -> None:
        """Initialise a Plateau with the given upper-right corner.

        Args:
            max_x: Width of the plateau (maximum x coordinate, inclusive).
            max_y: Height of the plateau (maximum y coordinate, inclusive).

        Raises:
            ValueError: If either dimension is negative.
        """
        if max_x < 0 or max_y < 0:
            raise ValueError("Plateau dimensions must be non-negative integers.")
        self.max_x = max_x
        self.max_y = max_y

    def is_within_bounds(self, x: int, y: int) -> bool:
        """Return True if (x, y) lies within the plateau boundaries.

        Both axes are inclusive, so (0, 0) and (max_x, max_y) are valid.

        Args:
            x: Column coordinate to check.
            y: Row coordinate to check.

        Returns:
            True if ``0 <= x <= max_x`` and ``0 <= y <= max_y``,
            False otherwise.
        """
        return 0 <= x <= self.max_x and 0 <= y <= self.max_y

    def __repr__(self) -> str:
        """Return unambiguous string representation for debugging.

        Returns:
            A string of the form ``Plateau(max_x=5, max_y=5)``.
        """
        return f"Plateau(max_x={self.max_x}, max_y={self.max_y})"
