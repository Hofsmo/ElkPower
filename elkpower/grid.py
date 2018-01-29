"""Module for reading and writing data."""
import pytoml as toml
import networkx as nx
import csv
import inspect
import os
import numpy as np

import elkpower.components


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
        self.gen_list = []
        self.load_list = []

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
        self.system = conf["system"]
        self.system["z_base"] =\
            self.system["V_base"]**2/self.system["base_mva"]

    def read_grid(self):
        """Read in the grid as a graph"""
        # Iterate through the components
        for component, class_name in COMPONENTS.items():
            # If the component type is not the file
            if component not in self.components.keys():
                continue
            try:
                class_ = getattr(elkpower.components, class_name)
            except:
                print("This should not have happened.")
                raise
            # Find signature of the class_ constructor
            parameters = inspect.signature(class_).parameters
            # Ensure that we have a list of components
            if isinstance(self.components[component], str):
                comp_list = [self.components[component]]
            else:
                comp_list = self.components[component]
            for comp in comp_list:
                fname = os.path.join(self.conf_dir, comp)
                with open(fname) as csvfile:
                    dialect = csv.Sniffer().sniff(csvfile.read(1024))
                    csvfile.seek(0)
                    reader = csv.DictReader(csvfile, dialect=dialect)
                    for row in reader:
                        comp_args = self.create_args(parameters, row)
                        obj = class_(**comp_args)
                        if isinstance(obj, elkpower.components.Node):
                            self.graph.add_node(obj.bus, data=obj)
                            if isinstance(obj, elkpower.components.Generator):
                                self.gen_list.append(obj.bus)
                                if obj.x:
                                    g_node = "G"+str(obj.bus)
                                    self.graph.add_node(g_node, data=obj)
                                    z_base = obj.base_v**2/obj.base_p/obj.n_gen
                                    line = elkpower.components.Line(
                                        f_bus=g_node,
                                        t_bus=obj.bus,
                                        x=obj.x,
                                        z_base=z_base)
                                    self.graph.add_edge(g_node,
                                                        obj.bus, data=line)
                                    self.gen_list.pop()
                                    self.gen_list.append(g_node)
                                    self.load_list.append(obj.bus)
                            else:
                                self.load_list.append(obj.bus)
                        else:
                            if not obj.z_base:
                                obj.z_base = self.system["z_base"]
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
                comp_args[key] = float(comp[key])
            except ValueError:
                comp_args[key] = comp[key]
            except KeyError:
                if value.default is not inspect._empty:
                    comp_args[key] = value.default
                else:
                    raise KeyError("No value for " + key + " given.")
        return comp_args

    def draw(self):
        """Function for drawing the grid."""
        nx.draw_networkx(self.graph, with_labels=True)

    def number_of_generators(self):
        """Return number of generators."""
        return len(self.gen_list)

    def number_of_loads(self):
        """Return number of loads."""
        return len(self.load_list)

    def nodal_susceptance_matrix(self):
        """Find nodal susceptance matrix.
        Return:
            The nodal susceptance matrix.
            """
        n_nodes = self.graph.number_of_nodes()
        b_matrix = np.zeros([n_nodes, n_nodes])
        idx = 0
        nodes = self.gen_list + self.load_list

        for node in nodes:
            for nbr in nx.all_neighbors(self.graph, node):
                edge = self.graph[node][nbr]['data']
                susceptance = 1/(edge.x*edge.z_base/self.system["z_base"])
                b_matrix[idx][idx] += susceptance
                b_matrix[idx][nodes.index(nbr)] -= susceptance
            idx += 1

        return b_matrix

    def dc_coupling_constants(self):
        """Constatns needed for dynamic simulation linearization."""
        b_matrix = self.nodal_susceptance_matrix()
        n_gen = self.number_of_generators()
        n_nodes = self.graph.number_of_nodes()

        y_11 = b_matrix[0:n_gen, 0:n_gen]
        y_12 = b_matrix[0:n_gen, n_gen:n_nodes]

        y_21 = b_matrix[n_gen:n_nodes, 0:n_gen]
        y_22 = b_matrix[n_gen:n_nodes, n_gen:n_nodes]

        y_22_inv = np.linalg.inv(y_22)

        return np.concatenate((y_11-np.matmul(np.matmul(y_12, y_22_inv), y_21),
                              np.matmul(y_12, y_22_inv)), axis=1)
# def dc_state_matrix(self):
# """Method for returning state space matrix."""
# states_per_gen = 5
# n_gen = self.number_of_generators()
# n_states = states_per_gen*n_gen
# a_matrix = np.zeros([n_states, n_states])
# s_base = self.system["base_mva"]

# for idx, gen in enumerate(self.gen_list):
# # Find index of generator angle
# theta_i = idx*states_per_gen
# a_matrix[theta_i,theta_i+1] = 1
# a_matrix[theta_i+1,0] = -s_base*np.pi*
# for
