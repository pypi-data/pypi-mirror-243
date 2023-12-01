from src.cdfwriter.interface import CDFWriter
from .common_functions import (create_cdf_instance, create_variable_data_name_list)
from spacepy import pycdf
import numpy as np

def test_addVariableData():

    cdf = create_cdf_instance()

    cdf.addVariable ("VECT_X_DATA", pycdf.const.CDF_INT4, [30])
    x_vector = np.zeros ((30), dtype=pycdf.const.CDF_INT4)
    for which in range (0, 30):
        x_vector [which] = which
    cdf.addVariableData ("VECT_X_DATA", x_vector)

    list_of_all_variable_data_names = create_variable_data_name_list(cdf)

    # No need to check for empty list
    # raises an excepion IF the expression is false

    assert 'VECT_X_DATA' in list_of_all_variable_data_names

def test_addVariableDataBadNameArgument():

    cdf = create_cdf_instance()

    # This test is for bad input data type - raises TypeError exception
    # Currently, only 1 argument is tested for validity, not the data.

    cdf.addVariable ("VECT_X_DATA", pycdf.const.CDF_INT4, [30])
    x_vector = np.zeros ((30), dtype=pycdf.const.CDF_INT4)
    for which in range (0, 30):
        x_vector [which] = which
    cdf.addVariableData (25, x_vector)

    list_of_all_variable_data_names = create_variable_data_name_list(cdf)

    # No need to check for empty list
    # raises an excepion IF the expression is false

    assert 25 in list_of_all_variable_data_names

def test_addVariableDataBadLastArgument():

    cdf = create_cdf_instance()

    # This test is for bad input data type - raises TypeError exception
    # Currently, only 1 argument is tested for validity, not the data.

    cdf.addVariable ("VECT_X_DATA", pycdf.const.CDF_INT4, [30])
    x_vector = np.zeros ((30), dtype=pycdf.const.CDF_INT4)
    for which in range (0, 30):
        x_vector [which] = which

    # works - cdf.addVariableData ("VECT_X_DATA", x_vector, False)
    cdf.addVariableData ("VECT_X_DATA", x_vector, "False")

    list_of_all_variable_data_names = create_variable_data_name_list(cdf)

    # No need to check for empty list
    # raises an excepion IF the expression is false

    assert "VECT_X_DATA" in list_of_all_variable_data_names

def test_addVariableDataCaseSensitive():

    cdf = create_cdf_instance()

    cdf.addVariable ("VECT_X_DATA", pycdf.const.CDF_INT4, [30])
    x_vector = np.zeros ((30), dtype=pycdf.const.CDF_INT4)
    for which in range (0, 30):
        x_vector [which] = which
    cdf.addVariableData ("vect_x_data", x_vector)

    list_of_all_variable_data_names = create_variable_data_name_list(cdf)

    # causes this module to fail

    assert 'vect_x_data' in list_of_all_variable_data_names

def test_addVariableDataUndefinedData():

    cdf = create_cdf_instance()

    cdf.addVariable ("VECT_X_DATA", pycdf.const.CDF_INT4, [30])
    x_vector = np.zeros ((30), dtype=pycdf.const.CDF_INT4)
    for which in range (0, 30):
        x_vector [which] = which
    cdf.addVariableData ("MISSING_VARIABLE", x_vector)

    list_of_all_variable_data_names = create_variable_data_name_list(cdf)

    # causes this module to fail

    assert 'MISSING_VARIABLE' in list_of_all_variable_data_names

def test_addVariableDataNotFound():

    cdf = create_cdf_instance()

    cdf.addVariable ("VECT_X_DATA", pycdf.const.CDF_INT4, [30])
    x_vector = np.zeros ((30), dtype=pycdf.const.CDF_INT4)
    for which in range (0, 30):
        x_vector [which] = which
    cdf.addVariableData ("VECT_X_DATA", x_vector)

    # This returns a list with one element, namely itself

    data_values = cdf._data.get("VECT_X_DATA")

    data_list = data_values[0]
    assert 7 in data_list    #  This works
    assert 35 in data_list   #  This fails
