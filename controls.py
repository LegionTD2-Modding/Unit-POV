"""Which key moves the camera which way, in the unit's frame: (right, up, forward)."""

KEYS = {
    "RightArrow": (1, 0, 0),
    "LeftArrow": (-1, 0, 0),
    "PageUp": (0, 1, 0),
    "PageDown": (0, -1, 0),
    "UpArrow": (0, 0, 1),
    "DownArrow": (0, 0, -1),
}

# ProLeak refuses offsets beyond this distance from the anchor, in each direction.
LIMIT = 50.0

# With Shift held, a key press moves the camera this fraction of a step.
FINE = 0.2


def nudge(offset, key, step, fine):
    """`offset` moved by one step (a fifth of one when `fine`) the way `key` points."""
    direction = KEYS.get(key)
    if direction is None:
        return tuple(offset)
    size = step * FINE if fine else step
    return tuple(round(max(-LIMIT, min(LIMIT, o + d * size)), 4) for o, d in zip(offset, direction))
