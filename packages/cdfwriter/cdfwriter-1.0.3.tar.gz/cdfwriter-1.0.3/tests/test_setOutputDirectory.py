from src.cdfwriter.interface import CDFWriter
from .common_functions import (create_cdf_instance)

def test_setOutputDirectory():

    cdf = create_cdf_instance()

    cdf.setOutputDirectory ('/home/cgonzalez/MERIT/data_files/')
    assert cdf._outputDirectory == "/home/cgonzalez/MERIT/data_files/"

def test_setOutputDirectoryBadArgument():

    # This test is for bad input data type - raises TypeError exception

    cdf = create_cdf_instance()

    cdf.setOutputDirectory(25)
    assert cdf._outputDirectory == "25/"

def test_setOutputDirectoryWrongOutputDirectory():

    # Since setOutputDirectory will append a '/' character at the end
    # if there is not one already there, this test will fail on comparison.

    cdf = create_cdf_instance()

    cdf.setOutputDirectory ('/home/cgonzalez/MERIT/data_files')
    assert cdf._outputDirectory == "/home/cgonzalez/MERIT/data_files"
