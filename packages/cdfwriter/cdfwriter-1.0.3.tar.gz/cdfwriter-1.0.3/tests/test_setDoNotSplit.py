from src.cdfwriter.interface import CDFWriter
from .common_functions import (create_cdf_instance)
import datetime

def test_setDoNotSplit():

    cdf = create_cdf_instance()

    cdf.setDoNotSplit(True)
    assert cdf._doNotSplit == True

def test_setDoNotSplitBadArgument():

    # This test is for bad input data type - raises TypeError exception

    cdf = create_cdf_instance()

    cdf.setDoNotSplit(25)
    assert cdf._doNotSplit == 25

def test_setDoNotSplitBadFileBoundary():

    cdf = create_cdf_instance()

    cdf.setDoNotSplit(False, "timeDelta")
    assert cdf._boundary == "timeDelta"

def test_setDoNotSplitFileBoundary():

    cdf = create_cdf_instance()

    new_boundary = datetime.timedelta(hours=1)
    default_boundary = datetime.timedelta(hours=6)

    cdf.setDoNotSplit(False, new_boundary)
    assert cdf._boundary == new_boundary       #  This works
    assert cdf._boundary == default_boundary   # This fails
