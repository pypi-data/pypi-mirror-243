from src.cdfwriter.interface import CDFWriter
from .common_functions import (create_cdf_instance, create_constant_name_list)
from spacepy import pycdf

def test_addConstant():

    cdf = create_cdf_instance()

    cdf.addConstant ("HELIUM_ENERGY", pycdf.const.CDF_FLOAT, [11])

    list_of_all_constant_names = create_constant_name_list(cdf)

    # No need to check for empty list
    # raises an excepion IF the expression is false

    assert 'HELIUM_ENERGY' in list_of_all_constant_names

def test_addConstantBadArgument():

    cdf = create_cdf_instance()

    # This test is for bad input data type - raises TypeError exception
    # Currently, only 1 argument is tested for validity.

    cdf.addConstant (25, pycdf.const.CDF_FLOAT, [11])

    list_of_all_constant_names = create_constant_name_list(cdf)

    # No need to check for empty list
    # raises an excepion IF the expression is false

    assert 25 in list_of_all_constant_names

def test_addConstantCaseSensitive():

    cdf = create_cdf_instance()

    cdf.addConstant ("HELIUM_ENERGY", pycdf.const.CDF_FLOAT, [11])

    list_of_all_constant_names = create_constant_name_list(cdf)

    # causes this module to fail

    assert 'helium_energy' in list_of_all_constant_names

def test_addConstantUndefinedConstant():

    cdf = create_cdf_instance()

    cdf.addConstant ("HELIUM_ENERGY", pycdf.const.CDF_FLOAT, [11])

    list_of_all_constant_names = create_constant_name_list(cdf)

    # causes this module to fail

    assert 'MissingConstant' in list_of_all_constant_names
