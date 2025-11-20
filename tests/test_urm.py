import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from urm import URM

def sum_of_two(x: int, y: int):
    urm = URM(registers=f"{x} {y}", program=[
        "J(3, 2, 5)",
        "S(1)",
        "S(3)",
        "J(1, 1, 1)",
        "Z(3)"
    ])
    urm.run()
    return urm

def non_negative_minus_one(x: int):
    urm = URM(registers=f"{x}", program=[
        "J(1, 4, 9)",
        "S(3)",
        "J(1, 3, 7)",
        "S(2)",
        "S(3)",
        "J(1, 1, 3)",
        "T(2, 1)"
    ])
    urm.run()
    return urm

def divide_by_two(x: int):
    urm = URM(registers=f"{x}", program=[
        "J(1, 2, 6)",
        "S(3)",
        "S(2)",
        "S(2)",
        "J(1, 1, 1)",
        "T(3, 1)"
    ])
    urm.run()
    return urm

def bool_x_are_non_zero(x: int):
    urm = URM(registers=f"{x}", program=[
        "J(1, 2, 4)",
        "Z(1)",
        "S(1)",
    ])
    urm.run()
    return urm

