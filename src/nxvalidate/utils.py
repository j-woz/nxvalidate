import re
import sys

if sys.version_info < (3, 10):
    from importlib_resources import files as package_files
else:
    from importlib.resources import files as package_files

import numpy as np
from dateutil.parser import parse
from nexusformat.nexus.tree import string_dtype


name_pattern = re.compile('^[a-zA-Z0-9_]([a-zA-Z0-9_.]*[a-zA-Z0-9_])?$')


def is_valid_name(name):
    """
    Checks if a given name is valid according to the defined name pattern.

    Parameters
    ----------
    name : str
        The name to be validated.

    Returns
    -------
    bool
        True if the name is valid, False otherwise.
    """
    if re.match(name_pattern, name):
        return True
    else:
        return False


def is_valid_iso8601(date_string):
    """
    Checks if a given date is valid according to the ISO 8601 standard.

    Parameters
    ----------
    date_string : str
        The date string to be validated.

    Returns
    -------
    bool
        True if the date string is valid, False otherwise.
    """
    try:
        parse(date_string)
        return True
    except ValueError:
        return False


def is_valid_int(dtype):
    """
    Checks if a given data type is a valid integer type.

    Parameters
    ----------
    dtype : type
        The data type to be validated.

    Returns
    -------
    bool
        True if the data type is a valid integer type, False otherwise.
    """
    return np.issubdtype(dtype, np.integer) 


def is_valid_float(dtype):
    """
    Checks if a given data type is a valid floating point type.

    Parameters
    ----------
    dtype : type
        The data type to be validated.

    Returns
    -------
    bool
        True if the data type is a valid floating point type, False
        otherwise.
    """
    return np.issubdtype(dtype, np.floating)


def is_valid_bool(dtype):
    """
    Checks if a given data type is a valid boolean type.

    Parameters
    ----------
    dtype : type
        The data type to be validated.

    Returns
    -------
    bool
        True if the data type is a valid boolean type, False otherwise.
    """
    return np.issubdtype(dtype, np.bool_) 


def is_valid_char(dtype):
    """
    Checks if a given data type is a valid character type.

    Parameters
    ----------
    dtype : type
        The data type to be validated.

    Returns
    -------
    bool
        True if the data type is a valid character type, False
        otherwise.
    """
    return (np.issubdtype(dtype, np.str_) or  np.issubdtype(dtype, np.bytes_)
            or dtype == string_dtype)


def is_valid_char_or_number(dtype):
    """
    Checks if a given data type is a valid character or number type.

    Parameters
    ----------
    dtype : type
        The data type to be validated.

    Returns
    -------
    bool
        True if the data type is a valid character or number type, False
        otherwise.
    """
    return is_valid_char(dtype) or is_valid_number(dtype)


def is_valid_complex(dtype):
    """
    Checks if a given data type is a valid complex number type.

    Parameters
    ----------
    dtype : type
        The data type to be validated.

    Returns
    -------
    bool
        True if the data type is a valid complex type, False otherwise.
    """
    return np.issubdtype(dtype, np.complex) 


def is_valid_number(dtype):
    """
    Checks if a given data type is a valid number type.

    Parameters
    ----------
    dtype : type
        The data type to be validated.

    Returns
    -------
    bool
        True if the data type is a valid number type, False otherwise.
    """
    return np.issubdtype(dtype, np.number) 


def is_valid_posint(dtype):
    """
    Checks if a given data type is a valid positive integer type.

    Parameters
    ----------
    dtype : type
        The data type to be validated.

    Returns
    -------
    bool
        True if the data type is a valid positive integer type, False
        otherwise.
    """
    if np.issubdtype(dtype, np.integer):
         info = np.iinfo(dtype)
         return info.max > 0
    return False 


def is_valid_uint(dtype):
    """
    Checks if a given data type is a valid unsigned integer type.

    Parameters
    ----------
    dtype : type
        The data type to be validated.

    Returns
    -------
    bool
        True if the data type is a valid unsigned integer type, False
        otherwise.
    """
    return np.issubdtype(dtype, np.unsignedinteger) 


def strip_namespace(element):
    """
    Recursively strips namespace from an XML element and its children.

    Parameters
    ----------
    element : xml.etree.ElementTree.Element
        The XML element to strip namespace from.
    """    
    if '}' in element.tag:
        element.tag = element.tag.split('}', 1)[1]
    for child in element:
        strip_namespace(child)


def convert_xml_dict(xml_dict):
    """
    Convert an XML dictionary to a more readable format.

    Parameters
    ----------
    xml_dict : dict
        The XML dictionary to be converted.

    Returns
    -------
    dict
        The converted XML dictionary.

    Notes
    -----
    If the XML dictionary contains '@type' and '@name', it will be
    converted to a dictionary with '@name' as the key. If the XML
    dictionary contains only '@type', it will be converted to a
    dictionary with '@type' as the key. If the XML dictionary does not
    contain '@type' or '@name', it will be returned as is.
    """
    if '@type' in xml_dict:
        if xml_dict['@type'].startswith('NX_') and '@name' in xml_dict:
            key = '@name'
        else:
            key = '@type'
    elif '@name' in xml_dict:
        key = '@name'
    else:
        return xml_dict
    return {xml_dict[key]: {k: v for k, v in xml_dict.items() if k != key}}


def xml_to_dict(element):
    """
    Convert an XML element to a dictionary.

    Parameters
    ----------
    element : xml element
        The XML element to be converted.

    Returns
    -------
    dict
        A dictionary representation of the XML element.
    """
    result = {}

    if element.attrib:
        attrs = element.attrib
        for attr in attrs:
            result[f"@{attr}"] = attrs[attr]

    for child in element:
        if child.tag == 'doc':
            continue
        elif child.tag == 'enumeration':
            result[child.tag] = [item.attrib['value'] for item in child]
        else:
            child_dict = convert_xml_dict(xml_to_dict(child))       
            if child.tag in result:
                result[child.tag].update(child_dict)
            else:
                result[child.tag] = child_dict

    return result

def merge_dicts(dict1, dict2):
    """
    Recursively merges two dictionaries into one.

    Parameters
    ----------
    dict1 : dict
        The dictionary to be updated.
    dict2 : dict
        The dictionary to update with.

    Returns
    -------
    dict
        The updated dictionary.
    """
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            merge_dicts(dict1[key], value)
        else:
            dict1[key] = value
    return dict1
