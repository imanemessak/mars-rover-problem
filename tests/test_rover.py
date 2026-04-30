"""Tests for the Rover class — construction, turning, moving, and instructions.

Covers:
- Valid construction and initial state
- Invalid heading and out-of-bounds construction errors
- Left and right turns, including full 360° rotation
- Single and multi-step movement in all four directions
- Out-of-bounds movement errors
- Instruction case-insensitivity, empty instructions, unknown commands
- ``position`` property format
- Acceptance tests from the original NASA specification
"""

import pytest

from mars_rover.plateau import Plateau
from mars_rover.rover import Rover


@pytest.fixture
def plateau():
    """Return a standard 5×5 plateau shared across all rover tests."""
    return Plateau(5, 5)


# ── Construction ──────────────────────────────────────────────────────────────


def test_initial_state(plateau):
    """Rover stores x, y, and heading correctly after construction."""
    r = Rover(1, 2, "N", plateau)
    assert r.x == 1
    assert r.y == 2
    assert r.heading == "N"


def test_invalid_heading_raises(plateau):
    """An unrecognised heading character raises ValueError."""
    with pytest.raises(ValueError, match="heading"):
        Rover(0, 0, "X", plateau)


def test_position_out_of_bounds_raises(plateau):
    """A starting position outside the plateau raises ValueError."""
    with pytest.raises(ValueError, match="out of bounds"):
        Rover(6, 0, "N", plateau)


# ── Turning ───────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "start, cmd, expected",
    [
        ("N", "L", "W"),
        ("W", "L", "S"),
        ("S", "L", "E"),
        ("E", "L", "N"),
    ],
)
def test_turn_left(plateau, start, cmd, expected):
    """Turning left rotates the heading 90° counter-clockwise."""
    r = Rover(0, 0, start, plateau)
    r.execute(cmd)
    assert r.heading == expected


@pytest.mark.parametrize(
    "start, cmd, expected",
    [
        ("N", "R", "E"),
        ("E", "R", "S"),
        ("S", "R", "W"),
        ("W", "R", "N"),
    ],
)
def test_turn_right(plateau, start, cmd, expected):
    """Turning right rotates the heading 90° clockwise."""
    r = Rover(0, 0, start, plateau)
    r.execute(cmd)
    assert r.heading == expected


def test_turn_left_full_circle(plateau):
    """Four left turns cycle through all headings and return to North."""
    r = Rover(0, 0, "N", plateau)
    for expected in ["W", "S", "E", "N"]:
        r.execute("L")
        assert r.heading == expected


def test_turn_right_full_circle(plateau):
    """Four right turns cycle through all headings and return to North."""
    r = Rover(0, 0, "N", plateau)
    for expected in ["E", "S", "W", "N"]:
        r.execute("R")
        assert r.heading == expected


# ── Moving ────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "x, y, heading, ex, ey",
    [
        (0, 0, "N", 0, 1),
        (0, 0, "E", 1, 0),
        (0, 1, "S", 0, 0),
        (1, 0, "W", 0, 0),
    ],
)
def test_move_one_step(plateau, x, y, heading, ex, ey):
    """A single 'M' moves the rover exactly one grid point in its heading."""
    r = Rover(x, y, heading, plateau)
    r.execute("M")
    assert r.x == ex and r.y == ey


def test_move_multiple_steps(plateau):
    """Three 'M' instructions move the rover three grid points forward."""
    r = Rover(0, 0, "N", plateau)
    r.execute("MMM")
    assert r.x == 0 and r.y == 3


def test_move_out_of_bounds_raises(plateau):
    """Moving off the plateau edge raises ValueError."""
    r = Rover(0, 0, "S", plateau)
    with pytest.raises(ValueError, match="out of bounds"):
        r.execute("M")


def test_move_stops_at_boundary(plateau):
    """Moving north from the top edge raises ValueError."""
    r = Rover(5, 5, "N", plateau)
    with pytest.raises(ValueError):
        r.execute("M")


# ── Instructions ──────────────────────────────────────────────────────────────


def test_instructions_case_insensitive(plateau):
    """Lowercase instructions are treated identically to uppercase."""
    r = Rover(1, 2, "N", plateau)
    r.execute("lmlmlmlmm")
    assert r.position == "1 3 N"


def test_empty_instructions_no_op(plateau):
    """An empty instruction string leaves the rover unchanged."""
    r = Rover(2, 2, "N", plateau)
    r.execute("")
    assert r.position == "2 2 N"


def test_unknown_instruction_raises(plateau):
    """An unrecognised instruction character raises ValueError."""
    r = Rover(0, 0, "N", plateau)
    with pytest.raises(ValueError, match="Unknown instruction"):
        r.execute("Z")


# ── Position property ─────────────────────────────────────────────────────────


def test_position_string(plateau):
    """position returns a correctly formatted 'x y HEADING' string."""
    r = Rover(3, 4, "W", plateau)
    assert r.position == "3 4 W"


# ── Acceptance tests (spec) ───────────────────────────────────────────────────


def test_acceptance_rover_1(plateau):
    """Rover 1 from the NASA spec reaches '1 3 N' after 'LMLMLMLMM'."""
    r = Rover(1, 2, "N", plateau)
    r.execute("LMLMLMLMM")
    assert r.position == "1 3 N"


def test_acceptance_rover_2(plateau):
    """Rover 2 from the NASA spec reaches '5 1 E' after 'MMRMMRMRRM'."""
    r = Rover(3, 3, "E", plateau)
    r.execute("MMRMMRMRRM")
    assert r.position == "5 1 E"
