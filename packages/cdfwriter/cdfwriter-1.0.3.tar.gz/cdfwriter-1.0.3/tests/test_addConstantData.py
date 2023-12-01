from src.cdfwriter.interface import CDFWriter
from .common_functions import (create_cdf_instance, create_constant_data_name_list)
from spacepy import pycdf
import numpy as np

def test_addConstantData():

    cdf = create_cdf_instance()

    cdf.addConstant ("HELIUM_ENERGY", pycdf.const.CDF_FLOAT, [11])
    cdf.addConstantData ("HELIUM_ENERGY", [7.1, 10, 14, 19.6, 27.4, 38.4, 53.4, 74.8, 104.7, 146.6, 205.2])

    list_of_all_constant_data_names = create_constant_data_name_list(cdf)

    # No need to check for empty list
    # raises an excepion IF the expression is false

    assert 'HELIUM_ENERGY' in list_of_all_constant_data_names

def test_addConstantDataBadArgument():

    cdf = create_cdf_instance()

    # This test is for bad input data type - raises TypeError exception
    # Currently, only 1 argument is tested for validity, not the data.

    cdf.addConstant ("HELIUM_ENERGY", pycdf.const.CDF_FLOAT, [11])
    cdf.addConstantData (25, [7.1, 10, 14, 19.6, 27.4, 38.4, 53.4, 74.8, 104.7, 146.6, 205.2])

    list_of_all_constant_data_names = create_constant_data_name_list(cdf)

    # No need to check for empty list
    # raises an excepion IF the expression is false

    assert 25 in list_of_all_constant_data_names

def test_addConstantDataCaseSensitive():

    cdf = create_cdf_instance()

    cdf.addConstant ("HELIUM_ENERGY", pycdf.const.CDF_FLOAT, [11])
    cdf.addConstantData ("helium_energy", [7.1, 10, 14, 19.6, 27.4, 38.4, 53.4, 74.8, 104.7, 146.6, 205.2])

    list_of_all_constant_data_names = create_constant_data_name_list(cdf)

    # causes this module to fail

    assert 'helium_energy' in list_of_all_constant_data_names

def test_addConstantDataUndefinedData():

    cdf = create_cdf_instance()

    cdf.addConstant ("HELIUM_ENERGY", pycdf.const.CDF_FLOAT, [11])
    cdf.addConstantData ("MISSING_CONSTANT", [7.1, 10, 14, 19.6, 27.4, 38.4, 53.4, 74.8, 104.7, 146.6, 205.2])

    list_of_all_constant_data_names = create_constant_data_name_list(cdf)

    # causes this module to fail

    assert 'MISSING_CONSTANT' in list_of_all_constant_data_names

def test_addConstantDataNotFound():

    cdf = create_cdf_instance()

    cdf.addConstant ("HELIUM_ENERGY", pycdf.const.CDF_FLOAT, [11])
    cdf.addConstantData ("HELIUM_ENERGY", [7.1, 10, 14, 19.6, 27.4, 38.4, 53.4, 74.8, 104.7, 146.6, 205.2])
    cdf.addConstant ("FAKE_ENERGY", pycdf.const.CDF_FLOAT, [11])
    cdf.addConstantData ("FAKE_ENERGY", [107.1, 110, 114, 119.6, 127.4, 138.4, 153.4, 174.8, 204.7, 246.6, 305.2])

    # This returns a list with one element, namely itself

    data_values = cdf._constantData.get("FAKE_ENERGY")

    fake_list = data_values[0]
    assert 107.1 in fake_list    # This passes
    assert 7.1 in fake_list      # This fails
