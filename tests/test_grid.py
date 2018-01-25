"""Test module for grid reading."""
import os
import pytest
import networkx as nx
import numpy as np
from elkpower.grid import Grid


@pytest.fixture(scope="session")
def grid():
    """Read conf."""
    cwd = os.getcwd()
    grid = Grid()

    fname = os.path.join("..", cwd, "examples/simple/simple.toml")
    grid.read_configuration(fname)
    return grid


def test_toml(grid):
    """Reading of toml file."""
    assert grid.description["name"] == "simple"


def test_read_connected(grid):
    """Reading of simple grid."""

    grid.read_grid()
    assert nx.is_connected(grid.graph)


def test_susceptance_matrix(grid):
    """Test that the suceptance matrix is correct."""

    correct = np.array([
        [242.242, 0, -242.242, 0, 0],
        [0, 2424.2, 0, -2424.2, 0],
        [-242.4242, 0, 242.6242,  0, -0.2],
        [0, -2424.2, 0, 2424.4, -0.2],
        [0, 0, -0.2, -0.2, 0.4]])

    grid.read_grid()
    test = grid.nodal_susceptance_matrix()

    # Sort the matrices
    test.sort(axis=0)
    test.sort(axis=1)

    correct.sort(axis=0)
    correct.sort(axis=1)

    np.testing.assert_allclose(test, correct, 1e-3)
