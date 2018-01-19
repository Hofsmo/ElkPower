"""Test module for grid reading."""
import os

from pydy import pydygrid

def test_toml():
    """Dummy test."""
    cwd = os.getcwd()
    grid = pydygrid.PydyGrid()
    
    fname = os.path.join("..", cwd, "examples/simple/simple.toml")

    grid.read_configuration(fname)
    assert grid.description["name"] == "simple"
