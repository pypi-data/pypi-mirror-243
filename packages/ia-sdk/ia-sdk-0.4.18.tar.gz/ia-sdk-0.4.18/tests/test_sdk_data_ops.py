from ia.gaius.data_ops import validate_data
import pytest

def test_validate_data():

    # have a few good gdfs, and a few broken gdfs

    # good, empty gdf
    gdf1 = {"strings": [],
            "vectors": [],
            "emotives": {},
            "metadata": {}}

    # empty gdf with additional field
    gdf2 = {"strings": [],
            "vectors": [],
            "emotives": {},
            "metadata": {},
            "invalid": True}

    # gdf with single string
    gdf3 = {"strings": ["hello"],
            "vectors": [],
            "emotives": {},
            "metadata": {}
            }

    # gdf with single string and vector
    gdf4 = {"strings": ["hello"],
            "vectors": [[1, 2, 3, 4]],
            "emotives": {},
            "metadata": {}
            }

    # gdf with malformed strings field
    gdf5 = {"strings": "hello",
            "vectors": [],
            "emotives": {},
            "metadata": {}
            }

    # gdf with malformed vectors field
    gdf6 = {"strings": ["hello"],
            "vectors": [1, 2, 3, 4],
            "emotives": {},
            "metadata": {}
            }

    # gdf with malformed emotives field
    gdf7 = {"strings": ["hello"],
            "vectors": [[1, 2, 3, 4]],
            "emotives": {"utility": "high"},
            "metadata": {}
            }

    # gdf with valid emotives field
    gdf8 = {"strings": ["hello"],
            "vectors": [[1, 2, 3, 4]],
            "emotives": {"utility": 23.7},
            "metadata": {}
            }
    
    # type is not dict
    gdf9 = [{"strings": ["hello"],
            "vectors": [[1, 2, 3, 4]],
            "emotives": {"utility": 23.7},
            "metadata": {}
            }]
    
    # missing emotives field
    gdf10 = {"strings": ["hello"],
            "vectors": [[1, 2, 3, 4]],
            "metadata": {}
            }
    
    # non string in strings field
    gdf11 = {"strings": [1984, "KEY|HELLO"],
            "vectors": [[1, 2, 3, 4]],
            "emotives": {"utility": 23.7},
            "metadata": {}
            }

    # emotives is list, not dict
    gdf12 = {"strings": ["KEY|HELLO"],
            "vectors": [[1, 2, 3, 4]],
            "emotives": [{"utility": 23.7}],
            "metadata": {}
            }

    # vectors is dict, not list
    gdf13 = {"strings": ["KEY|HELLO"],
            "vectors": {'1': [1, 2, 3, 4]},
            "emotives": {"utility": 23.7},
            "metadata": {}
            }

    # test the gdfs
    try:
        assert validate_data(gdf1) == True
    except Exception:
        pytest.fail("Validation of empty gdf failed")

    try:
        assert validate_data(gdf2) == True
        pytest.fail("GDF with invalid key passed")
    except Exception:
        pass

    try:
        assert validate_data(gdf3) == True
    except Exception:
        pytest.fail("Validation of acceptable gdf failed")

    try:
        assert validate_data(gdf4) == True
    except Exception:
        pytest.fail("Validation of acceptable gdf failed")

    try:
        assert validate_data(gdf5) == True
        pytest.fail("GDF with invalid strings field passed")
    except Exception:
        pass

    try:
        assert validate_data(gdf6) == True
        pytest.fail("GDF with invalid vectors field passed")
    except Exception:
        pass

    try:
        assert validate_data(gdf7) == True
        pytest.fail("GDF with invalid emotives field passed")
    except Exception:
        pass

    try:
        assert validate_data(gdf8) == True
    except Exception as error:
        pytest.fail(f"Validation of acceptable gdf failed: {str(error)}")
        pass

    try:
        assert validate_data(gdf9) == False
        pytest.fail(f"Validation of bad gdf returned true: {str(error)}")
    except Exception as error:
        pass

    try:
        assert validate_data(gdf10) == False
        pytest.fail(f"Validation of bad gdf returned true: {str(error)}")
    except Exception as error:
        pass

    try:
        assert validate_data(gdf11) == False
        pytest.fail(f"Validation of bad gdf returned true: {str(error)}")
    except Exception as error:
        pass

    try:
        assert validate_data(gdf12) == False
        pytest.fail(f"Validation of bad gdf returned true: {str(error)}")
    except Exception as error:
        pass


    try:
        assert validate_data(gdf13) == False
        pytest.fail(f"Validation of bad gdf returned true: {str(error)}")
    except Exception as error:
        pass