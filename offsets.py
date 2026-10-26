"""The camera chosen for each unit type, kept in the plugin's store between sessions."""

ORIGIN = (0.0, 0.0, 0.0)

# Third person: (distance, pitch) the camera starts at for a type nobody has turned yet.
ORBIT = (6.0, 25.0)


class Cameras:
    """One camera value per unit type, in a table of the plugin's store: first person
    `(right, up, forward)` from the anchor, or third person `(distance, pitch)`. A type with no
    value, or one of the wrong shape, starts from `default`."""

    def __init__(self, table, default):
        self.table = table
        self.default = tuple(default)

    def get(self, unit_type):
        """The value saved for `unit_type`, or the default."""
        value = self.table.get(unit_type)
        if (isinstance(value, list) and len(value) == len(self.default)
                and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in value)):
            return tuple(float(v) for v in value)
        return self.default

    def set(self, unit_type, value):
        """Save `value` as the one to use for `unit_type` from now on."""
        self.table.set(unit_type, [float(v) for v in value])

    def reset(self, unit_type):
        """Forget the value of `unit_type`: it starts from the default again."""
        self.table.delete(unit_type)
