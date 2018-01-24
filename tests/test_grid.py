"""Test module for grid reading."""
import os
import pytest
import networkx as nx
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

# def test_susceptance_matrix(grid):
    # """Test that the suceptance matrix is correct."""
