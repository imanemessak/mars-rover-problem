import pytest
from mars_rover.plateau import Plateau


# ── Construction ─────────────────────────────────────────────────────────────

def test_valid_plateau():
    p = Plateau(5, 5)
    assert p.max_x == 5
    assert p.max_y == 5


def test_single_cell_plateau():
    p = Plateau(0, 0)
    assert p.is_within_bounds(0, 0)


def test_non_square_plateau():
    p = Plateau(10, 3)
    assert p.max_x == 10
    assert p.max_y == 3


def test_negative_x_raises():
    with pytest.raises(ValueError):
        Plateau(-1, 5)


def test_negative_y_raises():
    with pytest.raises(ValueError):
        Plateau(5, -1)


def test_both_negative_raises():
    with pytest.raises(ValueError):
        Plateau(-3, -3)


# ── Boundary checks ──────────────────────────────────────────────────────────

@pytest.mark.parametrize("x, y", [
    (0, 0),   # bottom-left corner
    (5, 0),   # bottom-right corner
    (0, 5),   # top-left corner
    (5, 5),   # top-right corner
    (2, 3),   # interior
])
def test_inside_bounds(x, y):
    assert Plateau(5, 5).is_within_bounds(x, y)


@pytest.mark.parametrize("x, y", [
    (-1,  0),  # left of plateau
    ( 0, -1),  # below plateau
    ( 6,  0),  # right of plateau
    ( 0,  6),  # above plateau
    (-1, -1),  # diagonal out
    ( 6,  6),  # diagonal out
])
def test_outside_bounds(x, y):
    assert not Plateau(5, 5).is_within_bounds(x, y)


def test_repr():
    assert repr(Plateau(5, 5)) == "Plateau(max_x=5, max_y=5)"
