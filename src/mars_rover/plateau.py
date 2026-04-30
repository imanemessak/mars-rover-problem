class Plateau:
    """Represents the rectangular Mars plateau."""

    def __init__(self, max_x: int, max_y: int) -> None:
        if max_x < 0 or max_y < 0:
            raise ValueError("Plateau dimensions must be non-negative integers.")
        self.max_x = max_x
        self.max_y = max_y

    def is_within_bounds(self, x: int, y: int) -> bool:
        """Return True if (x, y) is inside the plateau."""
        return 0 <= x <= self.max_x and 0 <= y <= self.max_y

    def __repr__(self) -> str:
        return f"Plateau(max_x={self.max_x}, max_y={self.max_y})"
