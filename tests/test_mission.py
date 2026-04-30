"""Tests for the Mission class — parsing, orchestration, and file I/O.

Covers:
- Acceptance test against the original NASA specification
- Single and multi-rover execution
- Whitespace tolerance (blank lines, leading/trailing spaces)
- Minimal plateau edge cases
- Input validation error paths
- ``Mission.from_file()`` factory method
"""

import pytest

from mars_rover.mission import Mission

# ── Fixtures ──────────────────────────────────────────────────────────────────

SPEC_INPUT = """\
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
"""

# ── Acceptance test ───────────────────────────────────────────────────────────


def test_full_mission_matches_spec():
    """Both rovers reach the positions specified in the NASA kata."""
    results = Mission(SPEC_INPUT).run()
    assert results == ["1 3 N", "5 1 E"]


# ── Single rover ──────────────────────────────────────────────────────────────


def test_single_rover():
    """A mission with one rover returns a single-element list."""
    assert Mission("5 5\n1 2 N\nLMLMLMLMM").run() == ["1 3 N"]


def test_single_rover_no_move():
    """Four right-turns leave the rover at its starting position."""
    assert Mission("5 5\n2 3 E\nRRRR").run() == ["2 3 E"]


# ── Multiple rovers run sequentially ─────────────────────────────────────────


def test_three_rovers():
    """Three rovers are deployed and executed one after the other."""
    raw = "5 5\n0 0 N\nM\n0 1 E\nM\n1 1 S\nM"
    results = Mission(raw).run()
    assert results == ["0 1 N", "1 1 E", "1 0 S"]


# ── Whitespace tolerance ──────────────────────────────────────────────────────


def test_extra_blank_lines_ignored():
    """Blank lines anywhere in the input are silently ignored."""
    raw = "\n5 5\n\n1 2 N\nLMLMLMLMM\n\n3 3 E\nMMRMMRMRRM\n"
    assert Mission(raw).run() == ["1 3 N", "5 1 E"]


def test_leading_trailing_spaces_in_lines():
    """Leading and trailing spaces on each line are stripped before parsing."""
    raw = "  5 5  \n  1 2 N  \n  LMLMLMLMM  "
    assert Mission(raw).run() == ["1 3 N"]


# ── Minimal plateau ───────────────────────────────────────────────────────────


def test_single_cell_plateau():
    """A 1×1 plateau (0 0) allows turning but not moving."""
    assert Mission("0 0\n0 0 N\nLLLL").run() == ["0 0 N"]


# ── Input validation ──────────────────────────────────────────────────────────


def test_missing_instructions_raises():
    """An odd number of rover lines (position without instructions) is invalid."""
    with pytest.raises(ValueError):
        Mission("5 5\n1 2 N")


def test_empty_input_raises():
    """Empty input raises ValueError or IndexError during parsing."""
    with pytest.raises((ValueError, IndexError)):
        Mission("")


# ── from_file ─────────────────────────────────────────────────────────────────


def test_from_file(tmp_path):
    """Mission.from_file() reads a file and produces the correct results."""
    f = tmp_path / "input.txt"
    f.write_text(SPEC_INPUT)
    results = Mission.from_file(str(f)).run()
    assert results == ["1 3 N", "5 1 E"]


def test_from_file_not_found():
    """Mission.from_file() raises FileNotFoundError for a missing path."""
    with pytest.raises(FileNotFoundError):
        Mission.from_file("/nonexistent/path.txt")
