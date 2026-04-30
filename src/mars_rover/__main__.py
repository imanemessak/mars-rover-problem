import sys
from .mission import Mission


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m mars_rover <input_file>")
        sys.exit(1)

    mission = Mission.from_file(sys.argv[1])
    for result in mission.run():
        print(result)


if __name__ == "__main__":
    main()
