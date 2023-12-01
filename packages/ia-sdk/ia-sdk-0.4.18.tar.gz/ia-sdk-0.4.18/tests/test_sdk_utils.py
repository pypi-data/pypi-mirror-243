from ia.gaius.utils import create_gdf, abstract_names, write_gdf_to_file,\
    merge_gdfs, GDFFormatError, retrieve_bottom_level_records
import json
import os
import tempfile
import warnings
import pytest

def test_create_gdf():

    # here are the expected gdfs
    gdf1 = {"strings": [],
            "vectors": [],
            "emotives": {},
            "metadata": {}
            }
    gdf2 = {"strings": ["hello"],
            "vectors": [],
            "emotives": {},
            "metadata": {}
            }
    gdf3 = {"strings": ["hello"],
            "vectors": [[1, 2, 3, 4]],
            "emotives": {},
            "metadata": {}
            }
    gdf4 = {"strings": ["hello"],
            "vectors": [[1, 2, 3, 4]],
            "emotives": {"utility": 50},
            "metadata": {}
            }
    gdf5 = {"strings": ["hello"],
            "vectors": [[1, 2, 3, 4]],
            "emotives": {"utility": 50},
            "metadata": {"hello": "world"}
            }
    
    # strings not list
    gdf6 = {
        "strings": {},
        "vectors": [[1, 2, 3, 4]],
        "emotives": {"utility": 50},
        "metadata": {"hello": "world"}
    }
    
    # emotives not dict
    gdf7 = {
        "strings": [],
        "vectors": [[1, 2, 3, 4]],
        "emotives": [],
        "metadata": {"hello": "world"}
    }
    
    # metadata not dict
    gdf8 = {
        "strings": [],
        "vectors": [[1, 2, 3, 4]],
        "emotives": {"utility": 50},
        "metadata": []
    }
    
    # vectors not list
    gdf9 = {
        "strings": [],
        "vectors": set([]),
        "emotives": {"utility": 50},
        "metadata": {"hello": "world"}
    }
    # individual vector not list
    gdf10 = {
        "strings": [],
        "vectors": ['hello', 42],
        "emotives": {"utility": 50},
        "metadata": {"hello": "world"}
    }

    # now test the function
    assert create_gdf() == gdf1
    assert create_gdf(strings=["hello"]) == gdf2
    assert create_gdf(strings=["hello"], vectors=[[1, 2, 3, 4]]) == gdf3
    assert create_gdf(strings=["hello"], vectors=[[1, 2, 3, 4]], emotives={"utility": 50}) == gdf4
    assert create_gdf(strings=["hello"], vectors=[[1, 2, 3, 4]], emotives={"utility": 50}, metadata={"hello": "world"}) == gdf5

    warnings.filterwarnings("error")
    try:
        create_gdf(**gdf6)
        pytest.fail("bad gdf")
    except GDFFormatError:
        pass
    try:
        create_gdf(**gdf7)
        pytest.fail("bad gdf")
    except GDFFormatError:
        pass
    try:
        create_gdf(**gdf8)
        pytest.fail("bad gdf")
    except GDFFormatError:
        pass
    try:
        create_gdf(**gdf9)
        pytest.fail("bad gdf")
    except GDFFormatError:
        pass
    try:
        create_gdf(**gdf10)
        pytest.fail("bad gdf")
    except GDFFormatError:
        pass

def test_abstract_names():

    # example prediction sequences
    ensemble1 = []
    ensemble2 = [{"name": "MODEL|1"},
                 {"name": "MODEL|2"},
                 {"name": "MODEL|3"},
                 {"name": "MODEL|4"},
                 {"name": "MODEL|5"}]
    ensemble3 = [{"name": "MODEL|0"},
                 {"name": "MODEL|0"},
                 {"name": "MODEL|0"},
                 {"name": "MODEL|0"},
                 {"name": "MODEL|0"}]

    assert abstract_names(ensemble1) == []
    assert sorted(abstract_names(ensemble2)) == sorted(["MODEL|1", "MODEL|2", "MODEL|3", "MODEL|4", "MODEL|5"])
    assert abstract_names(ensemble3) == ['MODEL|0']


def test_write_gdf_to_file():
    tmp_dir = tempfile.gettempdir()
    temporary_gdf_path = os.path.join(tmp_dir, "tmp_gdf")
    if os.path.exists(temporary_gdf_path):
        os.remove(temporary_gdf_path)

    # sequence to write
    seq = [create_gdf(strings=["goodbye"], vectors=[[1, 2, 3, 1, 2, 3]]),
           create_gdf(strings=["cruel"], emotives={"utility": -50}),
           create_gdf(strings=["world"], metadata={"sequence": "over"})]

    assert write_gdf_to_file(directory_name=tmp_dir,
                             filename="tmp_gdf",
                             sequence=seq) == 'success'

    with open(temporary_gdf_path, 'r') as f:
        file_data = f.readlines()
        file_data = [json.loads(line) for line in file_data]

    os.remove(temporary_gdf_path)
    assert seq == file_data


def test_merge_gdfs():
    
    gdf1 = {'strings': ['hello', 'there'],
            'vectors': [[1,2,3,4]],
            'emotives': {'happy':25},
            'metadata': {'sad':'very'}}

    gdf2 = {'strings': ['goodbye', 'here'],
            'vectors': [[2,3,4,5]],
            'emotives': {'annoy':125},
            'metadata': {'hello':'yes'}}
    
    gdf3 = {'strings': ['hello', 'there', 'goodbye', 'here'],
            'vectors': [[1,2,3,4], [2,3,4,5]],
            'emotives': {'happy':25,
                         'annoy':125},
            'metadata': {'sad':'very',
                         'hello':'yes'}}
    
    # bad vector length
    gdf4 = {'strings': ['goodbye', 'here'],
            'vectors': [[2,3,4,5,6]],
            'emotives': {},
            'metadata': {}}
    
    assert merge_gdfs(gdf1=gdf1, gdf2=gdf2) == gdf3
    
    try:
        merge_gdfs(gdf1=gdf1, gdf2=gdf4)
        pytest.fail("merging gdfs with different vector sizes succeeded")
    except:
        pass

def test_retrieve_bottom_level_records():
    investigate_query1 = {'query': {'name': 'dadab00fe92e9dbafa600a1b36b4e81dbc27a904',
                                'node_id': 'P2',
                                'record': 'dadab00fe92e9dbafa600a1b36b4e81dbc27a904'},
                        'results': {'bottomLevel': False,
                                    'model': {'emotives': {},
                                            'frequency': 1,
                                            'length': 2,
                                            'metadata': [{},
                                                            {}],
                                            'predecessor_model': [],
                                            'name': 'dadab00fe92e9dbafa600a1b36b4e81dbc27a904',
                                            'sequence': [['PRIMITIVE|pbb2fabdc|668ada4d5e7059d5b5ba4e932511f2ae1d426a96|name|668ada4d5e7059d5b5ba4e932511f2ae1d426a96'],
                                                            ['PRIMITIVE|pbb2fabdc|668ada4d5e7059d5b5ba4e932511f2ae1d426a96|future|VECTOR|8523ac8438628a846a1bf7ae02c4c9a13e883573']]},
                                    'node': 'P2',
                                    'node_id': 'p98fdaf83d',
                                    'record': 'dadab00fe92e9dbafa600a1b36b4e81dbc27a904',
                                    'subitems': ([{'bottomLevel': False,
                                                    'model': {'emotives': {},
                                                            'frequency': 1,
                                                            'length': 4,
                                                            'metadata': [{},
                                                                        {}],
                                                            'predecessor_model': [],
                                                            'name': '668ada4d5e7059d5b5ba4e932511f2ae1d426a96',
                                                            'sequence': [['A',
                                                                            'B',
                                                                            'C'],
                                                                        ['VECTOR|8523ac8438628a846a1bf7ae02c4c9a13e883573']]},
                                                    'node': 'P1',
                                                    'node_id': 'pbb2fabdc',
                                                    'record': 'PRIMITIVE|pbb2fabdc|668ada4d5e7059d5b5ba4e932511f2ae1d426a96',
                                                    'subitems': (['A',
                                                                'B',
                                                                'C'],
                                                                [{'bottomLevel': True,
                                                                'data': {'hash': '8523ac8438628a846a1bf7ae02c4c9a13e883573',
                                                                            'length': 5.477225575051661,
                                                                            'name': 'VECTOR|8523ac8438628a846a1bf7ae02c4c9a13e883573',
                                                                            'vector': [1,
                                                                                    2,
                                                                                    3,
                                                                                    4]},
                                                                'node': 'P1',
                                                                'node_id': 'pbb2fabdc',
                                                                'record': 'VECTOR|8523ac8438628a846a1bf7ae02c4c9a13e883573',
                                                                'subitems': None,
                                                                'topLevel': False}]),
                                                    'topLevel': False}],),
                                    'topLevel': True}
                        }
    
    assert retrieve_bottom_level_records(traceback=investigate_query1['results']) == [{'bottomLevel': True,
                                                                                      'data': {'hash': '8523ac8438628a846a1bf7ae02c4c9a13e883573',
                                                                                                  'length': 5.477225575051661,
                                                                                                  'name': 'VECTOR|8523ac8438628a846a1bf7ae02c4c9a13e883573',
                                                                                                  'vector': [1,
                                                                                                          2,
                                                                                                          3,
                                                                                                          4]},
                                                                                      'node': 'P1',
                                                                                      'node_id': 'pbb2fabdc',
                                                                                      'record': 'VECTOR|8523ac8438628a846a1bf7ae02c4c9a13e883573',
                                                                                      'subitems': None,
                                                                                      'topLevel': False}]
