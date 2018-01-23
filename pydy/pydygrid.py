"""Module for reading and writing data."""
import pytoml as toml
import networkx as nx
import csv
import inspect

import pydy.components


# List of components to read. The order is important
COMPONENTS = ["Load", "Generator", "Line"]

class PydyGrid:
    """Class for reading and writing grids."""

    def __init__(self):
        """Constructor."""
        self.description = []
        self.static_data = []
        self.components = []
        self.graph = nx.Graph()

    def read_configuration(self, fname):
        """Read configuration file.
        Args:
           fname: Name of configuration file
        """
        with open(fname, "rb") as fin:
            conf = toml.load(fin)

        self.description = conf["description"]
        self.components = conf["components"]

        self.read_grid()

    def read_grid(self):
        """Read in the grid as a graph"""
        
        # Iterate through the components
        for component in COMPONENTS:
            read_component(component)

    def read_component(self, component):
        """Read in component from file
        Args:
            component: The component to read in
        """
        try:
            class_ = getattr(pydy.components, component)
        except:
            print("This should not have happened.")
            raise
        for comp in component
            w

