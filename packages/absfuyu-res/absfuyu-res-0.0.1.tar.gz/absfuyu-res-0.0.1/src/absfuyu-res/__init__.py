"""
Absfuyu: Resources
"""


# Module level
###########################################################################
__title__ = "absfuyu-res"
__author__ = "AbsoluteWinter"
__license__ = "MIT License"
__version__ = "0.0.1"


# Library
###########################################################################
from importlib.resources import files


class DATA:
    PASSWORDLIB = files("absfuyu-res").joinpath("passwordlib_res.pkl")


# Module level
###########################################################################
def is_loaded():
    return True




# Run
###########################################################################
if __name__ == "__main__":
    print(DATA.PASSWORDLIB)