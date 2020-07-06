# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Dataverse data model tests."""
import json
import os
import platform

import jsonschema

import pytest
from pyDataverse.models import Dataverse, DVObject

# Global Variables
TEST_DIR = os.path.dirname(os.path.realpath(__file__))
FILENAME_DATA_FULL = 'tests/data/dataverse_upload_full.json'
FILENAME_DATA_MIN = 'tests/data/dataverse_upload_min.json'
FILENAME_SCHEMA = 'schemas/json/dataverse_upload_schema.json'
FILENAME_JSON_OUTPUT = os.path.join(TEST_DIR + '/data/output/dataverse_pytest.json')

INVALID_FILENAME_STRINGS = ['wrong', '']
INVALID_FILENAME_TYPES = [(), [], 12, 12.12, set(), True, False]
INVALID_VALIDATE_TYPES = [None, 'wrong', {}, []]
INVALID_JSON_DATA_TYPES = [[], (), 12, set(), True, False, None]
INVALID_SET_TYPES = INVALID_FILENAME_TYPES + ['', 'wrong']
INVALID_JSON_STRINGS = INVALID_FILENAME_STRINGS
INVALID_DATA_FORMAT_TYPES = INVALID_FILENAME_TYPES
INVALID_DATA_FORMAT_STRINGS = INVALID_FILENAME_STRINGS

def read_file(filename, mode='r'):
    """Read in a file.

    Parameters
    ----------
    filename : string
        Filename with full path.
    mode : string
        Read mode of file. Defaults to `r`. See more at
        https://docs.python.org/3.5/library/functions.html#open

    Returns
    -------
    string
        Returns data as string.

    """
    with open(filename, mode) as f:
        data = f.read()
    return data


def write_json(filename, data, mode='w', encoding='utf-8'):
    """Write data to a json file.

    Parameters
    ----------
    filename : string
        Filename with full path.
    data : dict
        Data to be written in the json file.
    mode : string
        Write mode of file. Defaults to `w`. See more at
        https://docs.python.org/3/library/functions.html#open

    """
    with open(filename, mode, encoding=encoding) as f:
        json.dump(data, f, indent=2)


def data_object():
    """Get Dataverse object.

    Returns
    -------
    pydataverse.models.Dataverse
        Dataverse object.
    """
    return Dataverse()


def dict_flat_set_min():
    """Get flat dict for set() of minimum Dataverse.

    Returns
    -------
    dict
        Flat dict with minimum Dataverse data.
    """
    data = {
        'alias': 'test-pyDataverse',
        'name': 'Test pyDataverse',
        'dataverseContacts': [
            {'contactEmail': 'info@aussda.at'}
        ]
    }
    return data


def dict_flat_set_full():
    """Get flat dict for set() of full Dataverse.

    Returns
    -------
    dict
        Flat dict with full Dataverse data.

    """
    data = {
        'name': 'Scientific Research',
        'alias': 'science',
        'dataverseContacts': [
            {'contactEmail': 'pi@example.edu'},
            {'contactEmail': 'student@example.edu'}
        ],
        'affiliation': 'Scientific Research University',
        'description': 'We do all the science.',
        'dataverseType': 'LABORATORY'
    }
    return data


def object_data_init():
    """Get dictionary for Dataverse with initial attributes.

    Returns
    -------
    dict
        Dictionary of init data attributes set.

    """
    data = {
        '_Dataverse_default_json_format': 'dataverse_upload',
        '_Dataverse_default_json_schema_filename': FILENAME_SCHEMA,
        '_Dataverse_allowed_json_formats': ['dataverse_upload', 'dataverse_download'],
        '_Dataverse_json_dataverse_upload_attr': [
            'affiliation',
            'alias',
            'dataverseContacts',
            'dataverseType',
            'description',
            'name'
        ],
        '_internal_attributes': []
    }
    return data


def object_data_min():
    """Get dictionary for Dataverse with minimum attributes.

    Returns
    -------
    pyDataverse.Dataverse()
        :class:Dataverse() with minimum attributes set.

    """
    data = {
        'alias': 'test-pyDataverse',
        'name': 'Test pyDataverse',
        'dataverseContacts': [{'contactEmail': 'info@aussda.at'}]
    }
    return data


def object_data_full():
    """Get dictionary for Dataverse with full attributes.

    Returns
    -------
    pyDataverse.Dataverse()
        :class:Dataverse() with full attributes set.

    """
    data = {
        'alias': 'science',
        'name': 'Scientific Research',
        'dataverseContacts': [{'contactEmail': 'pi@example.edu'}, {'contactEmail': 'student@example.edu'}],
        'affiliation': 'Scientific Research University',
        'description': 'We do all the science.',
        'dataverseType': 'LABORATORY'
    }
    return data


def dict_flat_get_min():
    """Get flat dict for :func:`get()` with minimum data of Dataverse.

    Returns
    -------
    dict
        Minimum Dataverse dictionary returned by :func:`get().

    """
    data = {
        'alias': 'test-pyDataverse',
        'name': 'Test pyDataverse',
        'dataverseContacts': [
            {'contactEmail': 'info@aussda.at'}
        ]
    }
    return data


def dict_flat_get_full():
    """Get flat dict for :func:`get()` of full data of Dataverse.

    Returns
    -------
    dict
        Full Datafile dictionary returned by :func:`get().

    """
    data = {
        'name': 'Scientific Research',
        'alias': 'science',
        'dataverseContacts': [
            {'contactEmail': 'pi@example.edu'},
            {'contactEmail': 'student@example.edu'}
        ],
        'affiliation': 'Scientific Research University',
        'description': 'We do all the science.',
        'dataverseType': 'LABORATORY',
    }
    return data


def json_upload_min():
    """Get JSON string of minimum Dataverse.

    Returns
    -------
    str
        JSON string.

    """
    data = read_file(FILENAME_DATA_MIN)
    return data


def json_upload_full():
    """Get JSON string of full Dataverse.

    Returns
    -------
    str
        JSON string.

    """
    data = read_file(FILENAME_DATA_FULL)
    return data


def json_dataverse_upload_attr():
    """List of attributes import or export in format `dataverse_upload`.

    Returns
    -------
    list
        List of attributes, which will be used for import and export.

    """
    data = [
        'affiliation',
        'alias',
        'dataverseContacts',
        'dataverseType',
        'description',
        'name'
    ]
    return data


def json_dataverse_upload_required_attr():
    """List of attributes required for `dataverse_upload` JSON.

    Returns
    -------
    list
        List of attributes, which will be used for import and export.

    """
    data = [
        'alias',
        'dataverseContacts',
        'name'
    ]
    return data


class TestDataverseGeneric(object):
    """Generic tests for Dataverse()."""

    def test_dataverse_set_and_get_valid(self):
        """Test Dataverse.get() with valid data."""
        data = [
            ((dict_flat_set_min(), object_data_min()), dict_flat_get_min()),
            ((dict_flat_set_full(), object_data_full()), dict_flat_get_full()),
            (({}, {}), {})
        ]

        pdv = data_object()
        pdv.set(dict_flat_set_min())
        assert isinstance(pdv.get(), dict)

        for input, data_eval in data:
            pdv = data_object()
            pdv.set(input[0])
            data = pdv.get()
            for key, val in data_eval.items():
                assert data[key] == input[1][key] == data_eval[key]
            assert len(data) == len(input[1]) == len(data_eval)


    def test_dataverse_set_invalid(self):
        """Test Dataverse.set() with invalid data."""

        # invalid data
        for data in INVALID_SET_TYPES:
            with pytest.raises(AssertionError):
                pdv = data_object()
                pdv.set(data)


    def test_dataverse_from_json_valid(self):
        """Test Dataverse.from_json() with valid data."""
        data = [
            (({json_upload_min()}, {}), object_data_min()),
            (({json_upload_full()}, {}), object_data_full()),
            (({json_upload_min()}, {'data_format': 'dataverse_upload'}), object_data_min()),
            (({json_upload_min()}, {'validate': False}), object_data_min()),
            (({json_upload_min()}, {'filename_schema': '', 'validate': False}), object_data_min()),
            (({json_upload_min()}, {'filename_schema': 'wrong', 'validate': False}), object_data_min()),
            (({json_upload_min()}, {'filename_schema': FILENAME_SCHEMA, 'validate': True}), object_data_min()),
            (({'{}'}, {'validate': False}), {})
        ]

        for input, data_eval in data:
            pdv = data_object()
            args = input[0]
            kwargs = input[1]
            pdv.from_json(*args, **kwargs)

            for key, val in data_eval.items():
                assert getattr(pdv, key) == data_eval[key]
            assert len(pdv.__dict__) - len(object_data_init()) == len(data_eval)


    def test_dataverse_from_json_invalid(self):
        """Test Dataverse.from_json() with invalid data."""
        # invalid data
        for data in INVALID_JSON_DATA_TYPES:
            with pytest.raises(AssertionError):
                pdv = data_object()
                pdv.from_json(data, validate=False)

        if int(platform.python_version_tuple()[1]) >= 5:
            for json_string in INVALID_JSON_STRINGS:
                with pytest.raises(json.decoder.JSONDecodeError):
                    pdv = data_object()
                    pdv.from_json(json_string, validate=False)
        else:
            for json_string in INVALID_JSON_STRINGS:
                with pytest.raises(ValueError):
                    pdv = data_object()
                    pdv.from_json(json_string, validate=False)

        # invalid `filename_schema`
        for filename_schema in INVALID_FILENAME_STRINGS:
            with pytest.raises(FileNotFoundError):
                pdv = data_object()
                pdv.from_json(json_upload_min(), filename_schema=filename_schema)

        for filename_schema in INVALID_FILENAME_TYPES:
            with pytest.raises(AssertionError):
                pdv = data_object()
                pdv.from_json(json_upload_min(), filename_schema=filename_schema)

        # invalid `data_format`
        for data_format in INVALID_DATA_FORMAT_TYPES + INVALID_DATA_FORMAT_STRINGS:
            with pytest.raises(AssertionError):
                pdv = data_object()
                pdv.from_json(json_upload_min(), data_format=data_format, validate=False)

        # invalid `validate`
        for validate in INVALID_VALIDATE_TYPES:
            with pytest.raises(AssertionError):
                pdv = data_object()
                pdv.from_json(json_upload_min(), validate=validate)

        with pytest.raises(jsonschema.exceptions.ValidationError):
            pdv = data_object()
            pdv.from_json('{}')

        for attr in json_dataverse_upload_required_attr():
            with pytest.raises(jsonschema.exceptions.ValidationError):
                pdv = data_object()
                data = json.loads(json_upload_min())
                del data[attr]
                data = json.dumps(data)
                pdv.from_json(data, validate=True)


    def test_dataverse_to_json_valid(self):
        """Test Dataverse.to_json() with valid data."""
        data = [
            ((dict_flat_set_min(), {}), json.loads(json_upload_min())),
            ((dict_flat_set_full(), {}), json.loads(json_upload_full())),
            ((dict_flat_set_min(), {'data_format': 'dataverse_upload'}), json.loads(json_upload_min())),
            ((dict_flat_set_min(), {'validate': False}), json.loads(json_upload_min())),
            ((dict_flat_set_min(), {'filename_schema': '', 'validate': False}), json.loads(json_upload_min())),
            ((dict_flat_set_min(), {'filename_schema': 'wrong', 'validate': False}), json.loads(json_upload_min())),
            ((dict_flat_set_min(), {'filename_schema': FILENAME_SCHEMA, 'validate': True}), json.loads(json_upload_min())),
            (({}, {'validate': False}), {})
        ]

        pdv = data_object()
        pdv.set(dict_flat_set_min())
        assert isinstance(pdv.to_json(), str)

        for input, data_eval in data:
            pdv = data_object()
            pdv.set(input[0])
            kwargs = input[1]
            data = json.loads(pdv.to_json(**kwargs))
            for key, val in data_eval.items():
                assert data[key] == data_eval[key]
            assert len(data) == len(data_eval)


    def test_dataverse_to_json_invalid(self):
        """Test Dataverse.to_json() with non-valid data."""
        # invalid `filename_schema`
        for filename_schema in INVALID_FILENAME_STRINGS:
            with pytest.raises(FileNotFoundError):
                obj = data_object()
                result = obj.to_json(filename_schema=filename_schema)

        for filename_schema in INVALID_FILENAME_TYPES:
            with pytest.raises(AssertionError):
                pdv = data_object()
                pdv.to_json(filename_schema=filename_schema)

        # invalid `data_format`
        for data_format in INVALID_DATA_FORMAT_TYPES + INVALID_DATA_FORMAT_STRINGS:
            with pytest.raises(AssertionError):
                pdv = data_object()
                pdv.set(dict_flat_set_min())
                pdv.to_json(data_format=data_format, validate=False)

        # invalid `validate`
        for validate in INVALID_VALIDATE_TYPES:
            with pytest.raises(AssertionError):
                pdv = data_object()
                pdv.set(dict_flat_set_min())
                pdv.to_json(validate=validate)

        with pytest.raises(jsonschema.exceptions.ValidationError):
            pdv = data_object()
            pdv.set({})
            pdv.to_json()

        for attr in json_dataverse_upload_required_attr():
            with pytest.raises(jsonschema.exceptions.ValidationError):
                pdv = data_object()
                data = json.loads(json_upload_min())
                del data[attr]
                pdv.set(data)
                pdv.to_json(validate=True)


    def test_dataverse_validate_json_valid(self):
        """Test Dataverse.validate_json() with valid data."""
        data = [
            ((dict_flat_set_min(), {}), True),
            ((dict_flat_set_full(), {}), True),
            ((dict_flat_set_min(), {'data_format': 'dataverse_upload'}), True),
            ((dict_flat_set_min(), {'data_format': 'dataverse_upload', 'filename_schema': FILENAME_SCHEMA}), True),
            ((dict_flat_set_min(), {'filename_schema': FILENAME_SCHEMA}), True)
        ]

        for input, data_eval in data:
            pdv = data_object()
            pdv.set(input[0])
            kwargs = input[1]

            assert pdv.validate_json() == data_eval


    def test_dataverse_validate_json_invalid(self):
        """Test Dataverse.validate_json() with non-valid data."""
        # invalid data
        for attr in json_dataverse_upload_required_attr():
            with pytest.raises(jsonschema.exceptions.ValidationError):
                for data in [dict_flat_set_min(), dict_flat_set_full()]:
                    pdv = data_object()
                    pdv.set(data)
                    delattr(pdv, attr)
                    pdv.validate_json()

        # invalid `filename_schema`
        for filename_schema in INVALID_FILENAME_STRINGS:
            with pytest.raises(FileNotFoundError):
                pdv = data_object()
                pdv.set(dict_flat_set_min())
                pdv.validate_json(filename_schema=filename_schema)

        for filename_schema in INVALID_FILENAME_TYPES:
            with pytest.raises(AssertionError):
                pdv = data_object()
                pdv.set(dict_flat_set_min())
                pdv.validate_json(filename_schema=filename_schema)


class TestDataverseSpecific(object):
    """Specific tests for Dataverse()."""

    def test_dataverse_init_valid(self):
        """Test Dataverse.__init__() with valid data."""
        # specific
        data = [
            (Dataverse(), {}),
            (Dataverse(dict_flat_set_min()), object_data_min()),
            (Dataverse(dict_flat_set_full()), object_data_full()),
            (Dataverse({}), {})
        ]

        for pdv, data_eval in data:
            for key, val in data_eval.items():
                print(getattr(pdv, key))
                print(data_eval[key])
                assert getattr(pdv, key) == data_eval[key]
            assert len(pdv.__dict__) - len(object_data_init()) == len(data_eval)


    def test_dataverse_init_invalid(self):
        """Test Dataverse.init() with invalid data."""
        pdv = Dataverse()

        # invalid data
        for data in INVALID_SET_TYPES:
            with pytest.raises(AssertionError):
                pdv.set(data)


if not os.environ.get('TRAVIS'):
    class TestDataverseGenericTravisNot(object):
        """Generic tests for Dataverse(), not running on Travis (no file-write permissions)."""

        def test_dataverse_from_json_to_json_valid(self):
            """Test Dataverse to JSON from JSON with valid data."""
            data = [
                ({json_upload_min()}, {}),
                ({json_upload_full()}, {}),
                ({json_upload_min()}, {'data_format': 'dataverse_upload'}),
                ({json_upload_min()}, {'validate': False}),
                ({json_upload_min()}, {'filename_schema': '', 'validate': False}),
                ({json_upload_min()}, {'filename_schema': 'wrong', 'validate': False}),
                ({json_upload_min()}, {'filename_schema': FILENAME_SCHEMA, 'validate': True}),
                ({'{}'}, {'validate': False})
            ]

            for args_from, kwargs_from in data:
                pdv_start = data_object()
                args = args_from
                kwargs = kwargs_from
                pdv_start.from_json(*args, **kwargs)
                if 'validate' in kwargs:
                    if kwargs['validate'] == False:
                        kwargs = {'validate': False}
                data_out = json.loads(pdv_start.to_json(**kwargs))
                write_json(FILENAME_JSON_OUTPUT, data_out)
                data_in = read_file(FILENAME_JSON_OUTPUT)
                pdv_end = data_object()
                kwargs = kwargs_from
                pdv_end.from_json(data_in, **kwargs)

                for key, val in pdv_end.get().items():
                    assert getattr(pdv_start, key) == getattr(pdv_end, key)
                assert len(pdv_start.__dict__) == len(pdv_end.__dict__,)
