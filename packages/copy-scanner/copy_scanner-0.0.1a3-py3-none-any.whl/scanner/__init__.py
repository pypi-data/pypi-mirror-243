import toml
import os

def get_version():
    pyproject = os.path.join(os.path.dirname(__file__), '..', 'pyproject.toml')
    with open(pyproject, 'r') as toml_file:
        pyproject_data = toml.load(toml_file)
    return pyproject_data['tool']['poetry']['version']

__version__ = get_version()
from . import pp, tl, pl
