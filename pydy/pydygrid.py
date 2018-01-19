"""Module for reading and writing data."""
import pytoml as toml


class PydyGrid:
    """Class for reading and writing grids."""

    def __init__(self):
        """Constructor."""
        self.description = []
        self.static_data = []
        self.static_components = []

    def read_configuration(self, fname):
        """Read configuration file.
        Args:
           fname: Name of configuration file
        """
        with open(fname, "rb") as fin:
            conf = toml.load(fin)

        self.description = conf["description"]
        self.static_data = conf["static_data"]
