from __future__ import annotations

from .plateau import Plateau
from .rover import Rover


class Mission:
    """Parses raw input and orchestrates rovers sequentially.

    Mission is the facade of the system — it is the only class that knows
    about both Plateau and Rover. All input parsing is isolated here so
    that Plateau and Rover remain pure domain objects.

    Attributes:
        plateau: The plateau created from the first line of the input.
        rover_data: Ordered list of (x, y, heading, instructions) tuples,
            one per rover, ready for deployment.
    """

    def __init__(self, raw_input: str) -> None:
        """Initialise a Mission by parsing raw text input.

        Args:
            raw_input: Multi-line string following the NASA format:
                first line is the plateau upper-right corner,
                then alternating rover position and instruction lines.

        Raises:
            ValueError: If the input format is invalid or unparseable.
        """
        self.plateau, self.rover_data = self._parse(raw_input.strip())

    # ── Parsing ──────────────────────────────────────────────────────────────

    @staticmethod
    def _parse(raw: str) -> tuple[Plateau, list[tuple[int, int, str, str]]]:
        """Parse raw input into a Plateau and an ordered list of rover data.

        Expected format (blank lines and leading/trailing whitespace ignored)::

            5 5
            1 2 N
            LMLMLMLMM
            3 3 E
            MMRMMRMRRM

        Args:
            raw: Stripped multi-line input string.

        Returns:
            A tuple of:
                - A ``Plateau`` built from the first line.
                - A list of ``(x, y, heading, instructions)`` tuples,
                  one per rover, in order of appearance.

        Raises:
            ValueError: If fewer than 3 non-empty lines are found, or if
                the number of rover lines is not a multiple of 2.
        """
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
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
        """Deploy each rover sequentially and return their final positions.

        Rovers are executed in the order they appear in the input. Each
        rover completes all its instructions before the next one starts.

        Returns:
            A list of position strings of the form ``'x y HEADING'``,
            one per rover, in deployment order.
        """
        results: list[str] = []
        for x, y, heading, instructions in self.rover_data:
            rover = Rover(x, y, heading, self.plateau)
            rover.execute(instructions)
            results.append(rover.position)
        return results

    # ── Factory helpers ──────────────────────────────────────────────────────

    @classmethod
    def from_file(cls, path: str) -> Mission:
        """Create a Mission by reading input from a file.

        Args:
            path: Path to a UTF-8 encoded text file in NASA input format.

        Returns:
            A fully initialized ``Mission`` instance.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file contents are not valid mission input.
        """
        with open(path, encoding="utf-8") as fh:
            return cls(fh.read())
