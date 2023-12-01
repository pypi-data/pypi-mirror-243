from lib.dependencies import remove_id_and_timestamp, MyFixture
import json
from copy import deepcopy
import pytest
from ia.gaius.agent_client import AgentClient, AgentConnectionError
from ia.gaius.utils import create_gdf
import pathlib

test_dir = pathlib.Path(__file__).parent.resolve()
GENOME = test_dir.joinpath("genomes/simple.genome")
ABS_GENOME = test_dir.joinpath("genomes/borlach_lumpkin2.genome")


@pytest.fixture(scope="function")
def setup_and_teardown():
    fixture = MyFixture(GENOME)
    yield fixture
    fixture.teardown(GENOME)


@pytest.fixture(scope="function")
def setup_and_teardown_abstraction():
    fixture = MyFixture(ABS_GENOME)
    yield fixture
    fixture.teardown(ABS_GENOME)


# Test Python IA-SDK functionality with simple agent
address = "localhost:8000"
with open(GENOME, 'r') as f:
    genome = json.load(f)


def test_agent_client_constructors():
    agent_info1 = {'name': '',
                   'domain': address,
                   'api_key': 'ABCD-1234',
                   'secure': False}

    agent1 = AgentClient(agent_info1)
    assert agent1._url == f"http://{address}/"
    assert agent1._secure == False
    assert agent1._bottle_info == agent_info1
    assert agent1._api_key == "ABCD-1234"
    assert agent1._verify == True

    agent_info2 = {'name': 'abcd',
                   'domain': address,
                   'api_key': 'ABCDEFGH-12345678',
                   'secure': True}

    agent2 = AgentClient(agent_info2, verify=False)
    assert agent2._url == f"https://abcd.{address}/"
    assert agent2._secure == True
    assert agent2._bottle_info == agent_info2
    assert agent2._api_key == 'ABCDEFGH-12345678'
    assert agent2._verify == False

    agent_info3 = {'name': 'abcd',
                   'domain': address,
                   'api_key': 'ABCDEFGH-12345678',
                   'secure': False}

    agent3 = AgentClient(agent_info3)
    assert agent3._url == f"http://abcd.{address}/"
    assert agent3._secure == False
    assert agent3._bottle_info == agent_info3
    assert agent3._api_key == 'ABCDEFGH-12345678'
    assert agent3._verify == True

    agent_info4 = {'name': '',
                   'domain': address,
                   'api_key': 'ABCDEFGH-12345678',
                   'secure': True}

    agent4 = AgentClient(agent_info4)
    assert agent4._url == f"https://{address}/"
    assert agent4._secure == True
    assert agent4._bottle_info == agent_info4
    assert agent4._api_key == 'ABCDEFGH-12345678'
    assert agent4._verify == True

    try:
        agent4.delete_model('blah')
        pytest.fail("Should throw agent connection error")
    except AgentConnectionError as e:
        pass


def test_agent_client_connect(setup_and_teardown):
    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}

    # we don't care if the styling information is altered
    # (for some reason it is???)
    ignore_keys = ['style', 'description']
    assert {k: v for k, v in genome.items() if k not in ignore_keys} == \
        {k: v for k, v in agent.genome.topology.items() if k not in ignore_keys}

    agent_info = {'name': '',
                  'domain': 'jsonplaceholder.typicode.com',
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    try:

        agent.connect()
        pytest.fail('connect on example site should have failed')
    except AgentConnectionError as e:
        pass

    try:
        agent.show_status()
        pytest.fail('show status should fail on disconnected agent')
    except AgentConnectionError as e:
        pass

    assert agent.__repr__() == '<.jsonplaceholder.typicode.com| secure: False, connected: False, gaius_agent: None,                   ingress_nodes: 0, query_nodes: 0>'


def test_agent_client_show_status(setup_and_teardown):
    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}

    assert agent.show_status() == {'AUTOLEARN': False,
                                   'PREDICT': True,
                                   'HYPOTHESIZED': False,
                                   'SLEEPING': False,
                                   'SNAPSHOT': False,
                                   'emotives': {},
                                   'last_learned_model_name': '',
                                   'models_kb': '{KB| objects: 0}',
                                   'name': 'P1',
                                   'num_observe_call': 0,
                                   'size_WM': 0,
                                   'target': '',
                                   'time': 0,
                                   'vector_dimensionality': -1,
                                   'vectors_kb': '{KB| objects: 0}'
                                   }

    assert agent.set_ingress_nodes(
        ['P1']) == [{'id': 'p46b6b076c', 'name': 'P1'}]
    assert agent.set_query_nodes(
        ['P1']) == [{'id': 'p46b6b076c', 'name': 'P1'}]

    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['hello']))) == {'auto_learned_model': '',
                                                                                     'prediction_made': False,
                                                                                     'status': 'observed'
                                                                                     }
    assert agent.show_status() == {'AUTOLEARN': False,
                                   'PREDICT': True,
                                   'HYPOTHESIZED': False,
                                   'SLEEPING': False,
                                   'SNAPSHOT': False,
                                   'emotives': {},
                                   'last_learned_model_name': '',
                                   'models_kb': '{KB| objects: 0}',
                                   'name': 'P1',
                                   'num_observe_call': 1,
                                   'size_WM': 1,
                                   'target': '',
                                   'time': 1,
                                   'vector_dimensionality': -1,
                                   'vectors_kb': '{KB| objects: 0}'
                                   }

    assert agent.stop_predicting() == 'deactivated-predictions'

    assert agent.show_status() == {'AUTOLEARN': False,
                                   'PREDICT': False,
                                   'HYPOTHESIZED': False,
                                   'SLEEPING': False,
                                   'SNAPSHOT': False,
                                   'emotives': {},
                                   'last_learned_model_name': '',
                                   'models_kb': '{KB| objects: 0}',
                                   'name': 'P1',
                                   'num_observe_call': 1,
                                   'size_WM': 1,
                                   'target': '',
                                   'time': 1,
                                   'vector_dimensionality': -1,
                                   'vectors_kb': '{KB| objects: 0}'
                                   }

    assert agent.start_predicting() == 'activated-predictions'

    assert agent.show_status() == {'AUTOLEARN': False,
                                   'PREDICT': True,
                                   'HYPOTHESIZED': False,
                                   'SLEEPING': False,
                                   'SNAPSHOT': False,
                                   'emotives': {},
                                   'last_learned_model_name': '',
                                   'models_kb': '{KB| objects: 0}',
                                   'name': 'P1',
                                   'num_observe_call': 1,
                                   'size_WM': 1,
                                   'target': '',
                                   'time': 1,
                                   'vector_dimensionality': -1,
                                   'vectors_kb': '{KB| objects: 0}'
                                   }

    assert agent.start_autolearning() == 'activated-autolearn'

    assert agent.show_status() == {'AUTOLEARN': True,
                                   'PREDICT': True,
                                   'HYPOTHESIZED': False,
                                   'SLEEPING': False,
                                   'SNAPSHOT': False,
                                   'emotives': {},
                                   'last_learned_model_name': '',
                                   'models_kb': '{KB| objects: 0}',
                                   'name': 'P1',
                                   'num_observe_call': 1,
                                   'size_WM': 1,
                                   'target': '',
                                   'time': 1,
                                   'vector_dimensionality': -1,
                                   'vectors_kb': '{KB| objects: 0}'
                                   }

    assert agent.stop_autolearning() == 'deactivated-autolearn'

    assert agent.show_status() == {'AUTOLEARN': False,
                                   'PREDICT': True,
                                   'HYPOTHESIZED': False,
                                   'SLEEPING': False,
                                   'SNAPSHOT': False,
                                   'emotives': {},
                                   'last_learned_model_name': '',
                                   'models_kb': '{KB| objects: 0}',
                                   'name': 'P1',
                                   'num_observe_call': 1,
                                   'size_WM': 1,
                                   'target': '',
                                   'time': 1,
                                   'vector_dimensionality': -1,
                                   'vectors_kb': '{KB| objects: 0}'
                                   }

    assert agent.start_sleeping() == 'asleep'

    assert agent.show_status() == {'AUTOLEARN': False,
                                   'PREDICT': True,
                                   'HYPOTHESIZED': False,
                                   'SLEEPING': True,
                                   'SNAPSHOT': False,
                                   'emotives': {},
                                   'last_learned_model_name': '',
                                   'models_kb': '{KB| objects: 0}',
                                   'name': 'P1',
                                   'num_observe_call': 0,
                                   'size_WM': 0,
                                   'target': '',
                                   'time': 1,
                                   'vector_dimensionality': -1,
                                   'vectors_kb': '{KB| objects: 0}'
                                   }

    assert agent.stop_sleeping() == 'awake'

    assert agent.show_status() == {'AUTOLEARN': False,
                                   'PREDICT': True,
                                   'HYPOTHESIZED': False,
                                   'SLEEPING': False,
                                   'SNAPSHOT': False,
                                   'emotives': {},
                                   'last_learned_model_name': '',
                                   'models_kb': '{KB| objects: 0}',
                                   'name': 'P1',
                                   'num_observe_call': 0,
                                   'size_WM': 0,
                                   'target': '',
                                   'time': 1,
                                   'vector_dimensionality': -1,
                                   'vectors_kb': '{KB| objects: 0}'
                                   }

    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['hello']))) == {'auto_learned_model': '',
                                                                                     'prediction_made': False,
                                                                                     'status': 'observed'
                                                                                     }
    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['world']))) == {'auto_learned_model': '',
                                                                                     'prediction_made': False,
                                                                                     'status': 'observed'
                                                                                     }

    assert agent.show_status() == {'AUTOLEARN': False,
                                   'PREDICT': True,
                                   'HYPOTHESIZED': False,
                                   'SLEEPING': False,
                                   'SNAPSHOT': False,
                                   'emotives': {},
                                   'last_learned_model_name': '',
                                   'models_kb': '{KB| objects: 0}',
                                   'name': 'P1',
                                   'num_observe_call': 2,
                                   'size_WM': 2,
                                   'target': '',
                                   'time': 3,
                                   'vector_dimensionality': -1,
                                   'vectors_kb': '{KB| objects: 0}'
                                   }

    assert agent.learn() == 'MODEL|7d0678ba6305341ce0d25133ab086208656a562f'

    assert agent.show_status() == {'AUTOLEARN': False,
                                   'PREDICT': True,
                                   'HYPOTHESIZED': False,
                                   'SLEEPING': False,
                                   'SNAPSHOT': False,
                                   'emotives': {},
                                   'last_learned_model_name': '7d0678ba6305341ce0d25133ab086208656a562f',
                                   'models_kb': '{KB| objects: 1}',
                                   'name': 'P1',
                                   'num_observe_call': 0,
                                   'size_WM': 0,
                                   'target': '',
                                   'time': 3,
                                   'vector_dimensionality': -1,
                                   'vectors_kb': '{KB| objects: 0}'
                                   }

    assert agent.receive_unique_ids(False) == False
    assert 'unique_id' not in agent.observe(create_gdf(strings=['hello']))

    assert agent.receive_unique_ids(True) == True
    assert 'unique_id' in agent.observe(create_gdf(strings=['hello']))


def test_agent_common(setup_and_teardown):

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)

    nodes = {'p46b6b076c': {'always_update_frequencies': False,
                            'auto_act_method': 'none',
                            'auto_act_threshold': 0.8,
                            'auto_learn_method': 'none',
                            'classifier': 'CVC',
                            'datastore': 'mongodb',
                            'dynamic_sequence_length': True,
                            'faveColor': '#6FB1FC',
                            'faveShape': 'hexagon',
                            'height': 25,
                            'id': 'p46b6b076c',
                            'manipulatives': [],
                            'max_predictions': 100,
                            'max_sequence_length': 0,
                            'name': 'P1',
                            'persistence': 5,
                            'quiescence': 3,
                            'process_predictions': True,
                            'recall_threshold': 0.1,
                            'search_depth': 10,
                            'smoothness': 3,
                            'sort': True,
                            'sources': ['observables'],
                            'type': 'primitive',
                            'width': 30}
             }

    agent.set_timeout(15)

    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}

    assert agent.genome.get_nodes() == tuple([nodes, {}])

    assert agent.genome.get_primitive_map() == {'P1': 'p46b6b076c'}

    assert agent.set_ingress_nodes(
        ['P1']) == [{'id': 'p46b6b076c', 'name': 'P1'}]
    assert agent.set_query_nodes(
        ['P1']) == [{'id': 'p46b6b076c', 'name': 'P1'}]

    assert agent.clear_all_memory() == "all-cleared"
    assert agent.clear_wm() == "wm-cleared"

    assert agent.get_time() == '0'

    assert agent.show_status() == {'AUTOLEARN': False,
                                   'PREDICT': True,
                                   'HYPOTHESIZED': False,
                                   'SLEEPING': False,
                                   'SNAPSHOT': False,
                                   'emotives': {},
                                   'last_learned_model_name': '',
                                   'models_kb': '{KB| objects: 0}',
                                   'name': 'P1',
                                   'num_observe_call': 0,
                                   'size_WM': 0,
                                   'target': '',
                                   'time': 0,
                                   'vector_dimensionality': -1,
                                   'vectors_kb': '{KB| objects: 0}'
                                   }

    assert remove_id_and_timestamp(agent.observe({'strings': ['hello'], 'vectors': [], 'emotives': {}})) == {'status': 'observed',
                                                                                                             'prediction_made': False,
                                                                                                             'auto_learned_model': ''}
    assert agent.ping() == {'status': 'okay'}
    assert agent.ping(nodes=["P1"]) == 'okay'

    assert agent.get_name() == "P1"

    assert agent.get_wm() == [['hello']]

    assert agent.get_time() == '1'

    assert agent.get_gene("SORT") == {"SORT": "sorting"}

    assert agent.change_genes({"SORT": False}) == "updated-genes"

    assert agent.get_gene("SORT") == {"SORT": "not sorting"}

    assert agent.get_gene("UNLIKELY_GENE") == {
        "UNLIKELY_GENE": 'faulty-genes-provided'}

    # disable receiving of unique_ids
    assert agent.receive_unique_ids(should_set=False) == False

    result = agent.observe(
        {'strings': ['hello'], 'vectors': [], 'emotives': {}})

    expected_keys = ['status', 'auto_learned_model',
                     'timestamp', 'prediction_made']
    assert all(key in expected_keys for key in result.keys())
    assert remove_id_and_timestamp(result) == {'status': 'observed',
                                               'prediction_made': False,
                                               'auto_learned_model': ''}

    assert agent.get_cognition_data() == {'command': '',
                                          'emotives': {},
                                          'metadata': {},
                                          'path': ['P1-p46b6b076c-process'],
                                          'predictions': [],
                                          'strings': ['hello'],
                                          'symbols': ['hello'],
                                          'vectors': [],
                                          'working_memory': [['hello'],
                                                             ['hello']]
                                          }

    assert agent.get_percept_data() == {'emotives': {},
                                        'metadata': {},
                                        'path': ['P1-p46b6b076c-process'],
                                        'strings': ['hello'],
                                        'vectors': []}

    assert agent.get_all_genes() == {'genes': {'SORT': 'not sorting',
                                               'always_update_frequencies': False,
                                               'auto_learn_algorithm': 'basic',
                                               'auto_learn_metric': 'wm_size',
                                               'classifier': 'CVC',
                                               'enable_genome_snapshots': 'genome snapshots enabled',
                                               'enable_predictions_kb': 'prediction_kb disabled',
                                               'enable_snapshots': 'WM snapshots disabled',
                                               'max_predictions': 100,
                                               'max_sequence_length': 0,
                                               'near_vector_count': 3,
                                               'persistence': 5,
                                               'predict_on_nth_event': 1,
                                               'prediction_sort_metric': 'potential',
                                               'prediction_threshold': 0,
                                               'prediction_threshold_direction': 'greater than',
                                               'prediction_threshold_metric': 'potential',
                                               'recall_threshold': 0.1,
                                               'search_depth': 10,
                                               'smoothness': 3,
                                               'snapshot_gen_predictions': 'prediction generation on snapshot load disabled',
                                               'snapshot_sync_keys': '[]',
                                               'wm_resolution': 'symbol'}
                                     }

    assert agent.increment_recall_threshold(
        0.05) == {'recall_threshold': '0.150000'}
    assert agent.get_all_genes() == {'genes': {'SORT': 'not sorting',
                                               'always_update_frequencies': False,
                                               'auto_learn_algorithm': 'basic',
                                               'auto_learn_metric': 'wm_size',
                                               'classifier': 'CVC',
                                               'enable_genome_snapshots': 'genome snapshots enabled',
                                               'enable_predictions_kb': 'prediction_kb disabled',
                                               'enable_snapshots': 'WM snapshots disabled',
                                               'max_predictions': 100,
                                               'max_sequence_length': 0,
                                               'near_vector_count': 3,
                                               'persistence': 5,
                                               'predict_on_nth_event': 1,
                                               'prediction_sort_metric': 'potential',
                                               'prediction_threshold': 0,
                                               'prediction_threshold_direction': 'greater than',
                                               'prediction_threshold_metric': 'potential',
                                               'recall_threshold': pytest.approx(0.15),
                                               'search_depth': 10,
                                               'smoothness': 3,
                                               'snapshot_gen_predictions': 'prediction generation on snapshot load disabled',
                                               'snapshot_sync_keys': '[]',
                                               'wm_resolution': 'symbol'}
                                     }
    assert agent.increment_recall_threshold(-0.05, nodes=['P1']) == {
        'recall_threshold': '0.100000'}

    assert agent.change_genes({'classifier': 'DVC'}, nodes=[
                              'P1']) == 'updated-genes'

    assert agent.change_genes(
        {'classifier-bad': 'TEST'}, nodes=['P1']) == 'faulty-genes-provided'

    assert agent.set_ingress_nodes() == []
    assert agent.set_query_nodes() == []


def test_traceback_agent_client(setup_and_teardown_abstraction):

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)

    agent.set_timeout(15)
    agent.set_summarize_for_single_node(False)

    assert agent.connect() == {'connection': 'okay',
                               'agent': 'borlach_lumpkin'}

    assert agent.genome.get_primitive_map() == {'P1': 'pbb2fabdc',
                                                'P2': 'p98fdaf83d'}

    assert agent.set_ingress_nodes(
        ['P1']) == [{'id': 'pbb2fabdc', 'name': 'P1'}]
    assert agent.set_query_nodes(
        ['P2']) == [{'id': 'p98fdaf83d', 'name': 'P2'}]

    assert agent.clear_all_memory() == {'P1': "all-cleared",
                                        'P2': 'all-cleared'}

    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['A', 'B', 'C']), nodes=['P1'])) == {'P1': {'status': 'observed',
                                                                                                                'auto_learned_model': '',
                                                                                                                'prediction_made': False,
                                                                                                                }
                                                                                                         }
    assert remove_id_and_timestamp(agent.observe(create_gdf(vectors=[[1, 2, 3, 4]]), nodes=['P1'])) == {'P1': {'status': 'observed',
                                                                                                               'auto_learned_model': '',
                                                                                                               'prediction_made': False,
                                                                                                               }
                                                                                                        }

    assert agent.learn(nodes=['P1']) == {
        'P1': 'MODEL|668ada4d5e7059d5b5ba4e932511f2ae1d426a96'}

    assert agent.clear_wm() == {'P1': 'wm-cleared',
                                'P2': 'wm-cleared'}

    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['A', 'B', 'C']), nodes=['P1'])) == {'P1': {'status': 'observed',
                                                                                                                'prediction_made': True,
                                                                                                                'auto_learned_model': ''
                                                                                                                }
                                                                                                         }

    assert agent.show_status() == {'P1': {'AUTOLEARN': False,
                                          'PREDICT': True,
                                          'HYPOTHESIZED': False,
                                          'SLEEPING': False,
                                          'SNAPSHOT': False,
                                          'emotives': {},
                                          'last_learned_model_name': '668ada4d5e7059d5b5ba4e932511f2ae1d426a96',
                                          'models_kb': '{KB| objects: 1}',
                                          'name': 'P1',
                                          'num_observe_call': 1,
                                          'size_WM': 3,
                                          'target': '',
                                          'time': 3,
                                          'vector_dimensionality': 4,
                                          'vectors_kb': '{KB| objects: 1}'
                                          },
                                   'P2': {'AUTOLEARN': False,
                                          'PREDICT': True,
                                          'HYPOTHESIZED': False,
                                          'SLEEPING': False,
                                          'SNAPSHOT': False,
                                          'emotives': {},
                                          'last_learned_model_name': '',
                                          'models_kb': '{KB| objects: 0}',
                                          'name': 'P2',
                                          'num_observe_call': 2,
                                          'size_WM': 2,
                                          'target': '',
                                          'time': 2,
                                          'vector_dimensionality': -1,
                                          'vectors_kb': '{KB| objects: 0}'
                                          }
                                   }

    assert agent.learn(nodes=['P2']) == {
        'P2': 'MODEL|dadab00fe92e9dbafa600a1b36b4e81dbc27a904'}

    assert agent.clear_wm() == {'P1': 'wm-cleared',
                                'P2': 'wm-cleared'}

    investigate_query1 = {'query': {'name': 'dadab00fe92e9dbafa600a1b36b4e81dbc27a904',
                                    'node_id': 'P2',
                                    'record': 'dadab00fe92e9dbafa600a1b36b4e81dbc27a904'},
                          'results': {'bottomLevel': False,
                                      'model': {'emotives': {},
                                                'frequency': 1,
                                                'length': 2,
                                                'predecessor_model': [],
                                                'metadata': [{},
                                                             {}],
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
    assert agent.investigate(
        record='MODEL|dadab00fe92e9dbafa600a1b36b4e81dbc27a904') == investigate_query1
    # model that is definitely not in P1 or P2
    assert agent.investigate(record='MODEL|UNKNOWN') == {}
    assert agent.investigate(record='PRIMITIVE|P1') == {}
    assert agent.investigate(record='PRIMITIVE|HELLO|WORLD') == {}

    # assert agent.get_model('dadab00fe92e9dbafa600a1b36b4e81dbc27a904') == {}
    investigate_query2 = deepcopy(investigate_query1)
    investigate_query2['query']['node_id'] = 'p98fdaf83d'
    investigate_query2['query']['record'] = 'PRIMITIVE|p98fdaf83d|dadab00fe92e9dbafa600a1b36b4e81dbc27a904|hello'
    assert agent.investigate(
        record='PRIMITIVE|p98fdaf83d|dadab00fe92e9dbafa600a1b36b4e81dbc27a904|hello') == investigate_query2

    assert agent._AgentClient__get_model_details(
        model=None, node=['P1'], topLevel=True) == None

    assert agent.get_symbol('VECTOR|8523ac8438628a846a1bf7ae02c4c9a13e883573') == {'P1': {'name': 'VECTOR|8523ac8438628a846a1bf7ae02c4c9a13e883573',
                                                                                          'features': {'frequency': 1,
                                                                                                       'model_member_frequency': 1}},
                                                                                   'P2': None}
    assert agent.get_symbol('VECTOR|8523ac8438628a846a1bf7ae02c4c9a13e883573', nodes=['P1']) == {'P1': {'name': 'VECTOR|8523ac8438628a846a1bf7ae02c4c9a13e883573',
                                                                                                        'features': {'frequency': 1,
                                                                                                                     'model_member_frequency': 1}}
                                                                                                 }
    assert agent.get_symbol('VECTOR|MISSING', nodes=['P1']) == {'P1': None}


def test_genome_funcs_agent_client(setup_and_teardown_abstraction):

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)

    agent.set_timeout(15)
    agent.set_summarize_for_single_node(False)

    assert agent.connect() == {'connection': 'okay',
                               'agent': 'borlach_lumpkin'}

    assert agent.genome.get_primitive_map() == {'P1': 'pbb2fabdc',
                                                'P2': 'p98fdaf83d'}

    assert agent.genome.get_nodes() == ({'p98fdaf83d': {'always_update_frequencies': False,
                                                        'auto_act_method': 'none',
                                                        'auto_act_threshold': 0.8,
                                                        'auto_learn_method': 'none',
                                                        'classifier': 'CVC',
                                                        'datastore': 'mongodb',
                                                        'dynamic_sequence_length': True,
                                                        'id': 'p98fdaf83d',
                                                        'manipulatives': [],
                                                        'max_predictions': 100,
                                                        'max_sequence_length': 0,
                                                        'name': 'P2',
                                                        'persistence': 5,
                                                        'process_predictions': True,
                                                        'quiescence': 3,
                                                        'recall_threshold': 0.1,
                                                        'search_depth': 10,
                                                        'smoothness': 3,
                                                        'sort': True,
                                                        'sources': ['observables'],
                                                        'type': 'primitive'},
                                         'pbb2fabdc': {'always_update_frequencies': False,
                                                       'auto_act_method': 'none',
                                                       'auto_act_threshold': 0.8,
                                                       'auto_learn_method': 'none',
                                                       'classifier': 'CVC',
                                                       'datastore': 'mongodb',
                                                       'dynamic_sequence_length': True,
                                                       'id': 'pbb2fabdc',
                                                       'manipulatives': ['m060db7e70',
                                                                         'mf972cbb32'],
                                                       'max_predictions': 5,
                                                       'max_sequence_length': 0,
                                                       'name': 'P1',
                                                       'persistence': 5,
                                                       'process_predictions': True,
                                                       'quiescence': 3,
                                                       'recall_threshold': 0.1,
                                                       'search_depth': 10,
                                                       'smoothness': 3,
                                                       'sort': True,
                                                       'sources': ['observables'],
                                                       'type': 'primitive'}},
                                        {'m060db7e70': {'category': 'standard',
                                                        'description': '',
                                                        'displayName': 'abstraction',
                                                        'genes': {'field': {'alleles': ['name', 'past', 'present', 'future', 'missing', 'extras', 'matches',                                                 'classification'],                                     'mutability': 0,                                     'value': ['name'],                                     'volatility': 0},                           'primitives': {'alleles': [],                                          'mutability': 0,                                          'value': ['p98fdaf83d'],                                          'volatility': 0},                           'sources': {'alleles': [],                                       'mutability': 0,                                       'value': ['cognition-data'],                                       'volatility': 0}},                 'id': 'm060db7e70',                 'mtype': 'output',                 'name': 'abstraction',                 'primitive': 'pbb2fabdc',                 'tags': ['abstraction',                          'name',                          'present',                          'past',                          'future',                          'missing',                          'matches',                          'extras',                          'output',                          'forward',                          'abstract',                          'emotives',                          'strings',                          'emotive',                          'classification'],                 'type': 'manipulative'},  'mf972cbb32': {'category': 'standard',                 'description': '',                 'displayName': 'abstraction',                 'genes': {'field': {'alleles': ['name',                                                 'past',                                                 'present',                                                 'future',                                                 'missing',                                                 'extras',                                                 'matches',                                                 'classification'],                                     'mutability': 0,                                     'value': ['future'],                                     'volatility': 0},                           'primitives': {'alleles': [],                                          'mutability': 0,                                          'value': ['p98fdaf83d'],                                          'volatility': 0},                           'sources': {'alleles': [],                                       'mutability': 0,                                       'value': ['cognition-data'],                                       'volatility': 0}},                 'id': 'mf972cbb32',                 'mtype': 'output',                 'name': 'abstraction',                 'primitive': 'pbb2fabdc',                 'tags': ['abstraction',                          'name',                          'present',                          'past',                          'future',                          'missing',                          'matches',                          'extras',                          'output',                          'forward',                          'abstract',                          'emotives',                          'strings',                          'emotive',                          'classification'],                 'type': 'manipulative'}},)

    assert agent.genome.get_manipulative_map() == {'m060db7e70': 'abstraction',
                                                   'mf972cbb32': 'abstraction'}
