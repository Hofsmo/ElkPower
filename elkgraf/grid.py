"""Module for reading and writing data."""
import pytoml as toml
import networkx as nx
import csv
import inspect
import os

import elkgraf.components


# List of components to read. The order is important
COMPONENTS = {"loads": "Load", "buses": "Node",
              "generators": "Generator", "lines": "Line"}


class Grid:
    """Class for reading and writing grids."""

    def __init__(self):
        """Constructor."""
        self.description = []
        self.static_data = []
        self.components = []
        self.conf_dir = []
        self.graph = nx.Graph()

    def read_configuration(self, fname):
        """Read configuration file.
        Args:
           fname: Name of configuration file
        """
        with open(fname, "rb") as fin:
            conf = toml.load(fin)

        self.conf_dir = os.path.split(fname)[0]

        self.description = conf["description"]
        self.components = conf["components"]

    def read_grid(self):
        """Read in the grid as a graph"""

        # Iterate through the components
        for component, class_name in COMPONENTS.items():
            try:
                class_ = getattr(elkgraf.components, class_name)
            except:
                print("This should not have happened.")
                raise
            # Find signature of the class_ constructor
            parameters = inspect.signature(class_).parameters
            # Ensure that we have a list of components
            if isinstance(self.components[component], str):
                comp_list = [self.components[component]]
            else:
                compl_list = self.components[component]
            for comp in comp_list:
                fname = os.path.join(self.conf_dir, comp)
                with open(fname) as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        comp_args = self.create_args(parameters, row)
                        obj = class_(**comp_args)
                        if isinstance(obj, elkgraf.components.Node):
                            self.graph.add_node(obj.name, data=obj)
                        else:
                            self.graph.add_edge(obj.t_bus, obj.f_bus, data=obj)

    def create_args(self, parameters, comp):
        """Create the arguments for creating components.
        Args:
            parameters: The constructor's parameters
            comp: component to read
        returns:
            args: argument dict
            """
        comp_args = dict()
        for key, value in parameters.items():
            try:
                comp_args[key] = comp[key]
            except KeyError:
                if value.default is not inspect._empty:
                    comp_args[key] = value.default
                else:
                    raise KeyError("No value for " + key + " given.")
        return comp_args

    def draw(self):
        """Function for drawing the grid."""
        nx.draw(self.graph)
