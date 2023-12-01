from src.cdfwriter.interface import CDFWriter
from .common_functions import (create_cdf_instance, create_global_attribute_list)

def test_addGlobalAttribute():

    cdf = create_cdf_instance()

    cdf.addGlobalAttribute ('Discipline', "Space Physics>Magnetospheric Science")

    list_of_global_attributes = create_global_attribute_list(cdf)

    assert 'Discipline' in list_of_global_attributes

def test_addGlobalAttributeBadArgument():

    # This test is for bad input data type - raises TypeError exception

    cdf = create_cdf_instance()

    cdf.addGlobalAttribute (25, "Space Physics>Magnetospheric Science")

    list_of_global_attributes = create_global_attribute_list(cdf)

    assert 25 in list_of_global_attributes

def test_addGlobalAttributeMissingData():

    # This test is to make sure data matches what was set.

    cdf = create_cdf_instance()

    cdf.addGlobalAttribute ('Discipline', "Space Physics>Magnetospheric Science")

    for name, value in cdf._global_attrs.items():
        if name == 'Discipline':
            assert 'Space Physics>Magnetospheric Science' == value  # This works
            assert 'Global Attribute Value Mismatch' == value
