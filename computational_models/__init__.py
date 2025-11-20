"""
Computational Models Package

This package implements fundamental computational models:
- Turing Machine: Infinite tape computational model
- Unlimited Register Machine (URM): Register-based computational model
"""

__version__ = "0.1.0"

from .turing_machine import State, TuringMachine
from .urm import URM

__all__ = [
    "State",
    "TuringMachine",
    "URM",
]

