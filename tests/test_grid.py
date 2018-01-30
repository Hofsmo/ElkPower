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
        [242.424, 0, -242.424, 0, 0],
        [0, 2424.2, 0, -2424.2, 0],
        [-242.4242, 0, 242.6242,  0, -0.2],
        [0, -2424.2, 0, 2424.4, -0.2],
        [0, 0, -0.2, -0.2, 0.4]])

    test = grid.nodal_susceptance_matrix()

    custom_matrix_assert(correct, test, atol=0.1)


def test_number_of_generators(grid):
    """Find number of generators."""

    assert 2 == grid.number_of_generators()


def custom_matrix_assert(mat1, mat2, atol):
    """Compare matrices."""
    sort_two_axes(mat1)
    sort_two_axes(mat2)

    np.testing.assert_allclose(mat1, mat2, atol=atol)


def sort_two_axes(matrix):
    """Sort along two axes."""
    matrix.sort(axis=0)
    matrix.sort(axis=1)


def test_k_matrix(grid):
    """test that the k_matrix is correct."""
    correct = np.array([
        [0.1, -0.1, -0.9996, 0, -0.4998],
        [-0.1, 0.1, -0.0004, -1, -0.5002]])

    test = grid.dc_coupling_constants()
    custom_matrix_assert(correct, test, atol=0.1)


def test_dc_state_matrix(grid):
    """Test the dc_state_matrix"""
    test = grid.dc_state_matrix()
    correct = -0.1*np.pi*3300*50/(300*9.68)
    np.testing.assert_allclose(correct, test[1, 0], atol=0.1)


def test_inertia(grid):
    """Test total inertia."""
    np.testing.assert_allclose(9.68+96.8,
                               grid.system["inertia"])
