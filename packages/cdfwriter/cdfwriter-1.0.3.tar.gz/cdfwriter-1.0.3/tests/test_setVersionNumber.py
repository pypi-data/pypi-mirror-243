from src.cdfwriter.interface import CDFWriter
from .common_functions import (create_cdf_instance)

def test_setVersionNumber():

    cdf = create_cdf_instance()

    cdf.setVersionNumber('4.2.0')
    assert cdf._version == "4.2.0"

def test_setVersionNumberBadArgument():
    # This test is for bad input data type - raises TypeError exception

    cdf = create_cdf_instance()

    cdf.setVersionNumber(25)
    assert cdf._version == 25

def test_setVersionNumberBadLevels():
    # Version Number expects 3 levels - raises ValueError exception

    cdf = create_cdf_instance()

    cdf.setVersionNumber('4.2')
    assert cdf._version == "4.2"

def test_setVersionNumberBadDataType():
    # Another test for bad input - raises TypeError exception

    cdf = create_cdf_instance()

    cdf.setVersionNumber('a.b.c')
    assert cdf._version == "a.b.c"

def test_setVersionNumberWrongVersion():

    cdf = create_cdf_instance()

    cdf.setVersionNumber('4.2.0')
    assert cdf._version == "4.1.0"

