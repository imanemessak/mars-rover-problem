import sys

from .mission import Mission


def main() -> None:
    """Entry point for the ``mars-rover`` CLI command.

    Reads a mission input file, runs all rovers sequentially, and prints
    each rover's final position to stdout on its own line.

    Expected usage::

        mars-rover examples/input.txt

    Args (via sys.argv):
        sys.argv[1]: Path to a UTF-8 encoded mission input file.

    Exits:
        1 — if the wrong number of arguments is provided.

    Example output::

        1 3 N
        5 1 E
    """
    if len(sys.argv) != 2:
        print("Usage: python -m mars_rover <input_file>")
        sys.exit(1)

    mission = Mission.from_file(sys.argv[1])
    for result in mission.run():
        print(result)


if __name__ == "__main__":
    main()
