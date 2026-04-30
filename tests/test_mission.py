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
    results = Mission(SPEC_INPUT).run()
    assert results == ["1 3 N", "5 1 E"]


# ── Single rover ──────────────────────────────────────────────────────────────

def test_single_rover():
    assert Mission("5 5\n1 2 N\nLMLMLMLMM").run() == ["1 3 N"]


def test_single_rover_no_move():
    assert Mission("5 5\n2 3 E\nRRRR").run() == ["2 3 E"]


# ── Multiple rovers run sequentially ─────────────────────────────────────────

def test_three_rovers():
    raw = "5 5\n0 0 N\nM\n0 1 E\nM\n1 1 S\nM"
    results = Mission(raw).run()
    assert results == ["0 1 N", "1 1 E", "1 0 S"]


# ── Whitespace tolerance ──────────────────────────────────────────────────────

def test_extra_blank_lines_ignored():
    raw = "\n5 5\n\n1 2 N\nLMLMLMLMM\n\n3 3 E\nMMRMMRMRRM\n"
    assert Mission(raw).run() == ["1 3 N", "5 1 E"]


def test_leading_trailing_spaces_in_lines():
    raw = "  5 5  \n  1 2 N  \n  LMLMLMLMM  "
    assert Mission(raw).run() == ["1 3 N"]


# ── Minimal plateau ───────────────────────────────────────────────────────────

def test_single_cell_plateau():
    assert Mission("0 0\n0 0 N\nLLLL").run() == ["0 0 N"]


# ── Input validation ──────────────────────────────────────────────────────────

def test_missing_instructions_raises():
    with pytest.raises(ValueError):
        Mission("5 5\n1 2 N")


def test_empty_input_raises():
    with pytest.raises((ValueError, IndexError)):
        Mission("")


# ── from_file ─────────────────────────────────────────────────────────────────

def test_from_file(tmp_path):
    f = tmp_path / "input.txt"
    f.write_text(SPEC_INPUT)
    results = Mission.from_file(str(f)).run()
    assert results == ["1 3 N", "5 1 E"]


def test_from_file_not_found():
    with pytest.raises(FileNotFoundError):
        Mission.from_file("/nonexistent/path.txt")
