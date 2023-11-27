"""
Absfuyu: Resources
"""


# Module level
###########################################################################
__title__ = "absfuyu_res"
__author__ = "AbsoluteWinter"
__license__ = "MIT License"
__version__ = "0.0.3"


# Library
###########################################################################
try:
    from importlib.resources import files
except:
    from importlib_resources import files


class DATA:
    PASSWORDLIB = files("absfuyu_res").joinpath("passwordlib_res.pkl")


# Module level
###########################################################################
def is_loaded():
    return True




# Run
###########################################################################
if __name__ == "__main__":
    print(DATA.PASSWORDLIB)