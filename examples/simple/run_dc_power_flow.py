import matplotlib.pyplot as plt
from elkgraf.grid import Grid

grid = Grid()

fname = "simple.toml"
grid.read_configuration(fname)
grid.read_grid()

B = grid.nodal_susceptance_matrix()
