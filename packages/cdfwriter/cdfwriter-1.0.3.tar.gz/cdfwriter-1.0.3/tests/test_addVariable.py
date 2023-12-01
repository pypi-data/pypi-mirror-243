from src.cdfwriter.interface import CDFWriter
from .common_functions import (create_cdf_instance, create_variable_name_list)
from spacepy import pycdf

def test_addVariable():

    cdf = create_cdf_instance()

    cdf.addVariable("Epoch", pycdf.const.CDF_TIME_TT2000)

    list_of_all_variable_names = create_variable_name_list(cdf)

    # No need to check for empty list
    # raises an excepion IF the expression is false

    assert 'Epoch' in list_of_all_variable_names

def test_addVariableBadArgument():

    cdf = create_cdf_instance()

    # This test is for bad input data type - raises TypeError exception
    # Currently, only 1 argument is tested for validity.

    cdf.addVariable(25, pycdf.const.CDF_TIME_TT2000)

    list_of_all_variable_names = create_variable_name_list(cdf)

    # No need to check for empty list
    # raises an excepion IF the expression is false

    assert 25 in list_of_all_variable_names

def test_addVariableCaseSensitive():

    cdf = create_cdf_instance()

    cdf.addVariable('Epoch', pycdf.const.CDF_TIME_TT2000)

    list_of_all_variable_names = create_variable_name_list(cdf)

    # causes this module to fail

    assert 'epoch' in list_of_all_variable_names

def test_addVariableUndefinedVariable():

    cdf = create_cdf_instance()

    cdf.addVariable('Epoch', pycdf.const.CDF_TIME_TT2000)

    list_of_all_variable_names = create_variable_name_list(cdf)

    # causes this module to fail

    assert 'MissingVariable' in list_of_all_variable_names
