from lib.dependencies import remove_id_and_timestamp, MyFixture
import json
import pytest
from ia.gaius.agent_client import AgentClient
from ia.gaius.utils import create_gdf
from ia.gaius.kb_ops import list_models, list_symbols, get_models_containing_symbol,\
    get_models_containing_symbol_strict, is_abstracted_symbol, get_kb_subset, remove_abstracted_symbols
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


def test_list_models_symbols(setup_and_teardown):

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}

    assert agent.clear_all_memory() == 'all-cleared'

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
    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['world']))) == {'auto_learned_model': '',
                                                                                     'prediction_made': False,
                                                                                     'status': 'observed'
                                                                                     }

    assert agent.learn() == 'MODEL|7d0678ba6305341ce0d25133ab086208656a562f'

    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['goodbye']))) == {'auto_learned_model': '',
                                                                                       'prediction_made': False,
                                                                                       'status': 'observed'
                                                                                       }
    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['cruel']))) == {'auto_learned_model': '',
                                                                                     'prediction_made': False,
                                                                                     'status': 'observed'
                                                                                     }
    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['world']))) == {'auto_learned_model': '',
                                                                                     'prediction_made': True,
                                                                                     'status': 'observed'
                                                                                     }

    assert agent.learn() == 'MODEL|3b5c9cdc4424988308922d2ec8c7bc06b7c6ac21'

    assert list_symbols(agent=agent) == {
        'P1': ['cruel', 'goodbye', 'hello', 'world']}
    assert list_models(agent=agent) == {'P1': ['3b5c9cdc4424988308922d2ec8c7bc06b7c6ac21',
                                               '7d0678ba6305341ce0d25133ab086208656a562f']}

    # should recover from unconnected agent gracefully
    agent = AgentClient(agent_info)
    assert list_symbols(agent=agent) == {
        'P1': ['cruel', 'goodbye', 'hello', 'world']}

    agent = AgentClient(agent_info)
    assert list_models(agent=agent) == {'P1': ['3b5c9cdc4424988308922d2ec8c7bc06b7c6ac21',
                                               '7d0678ba6305341ce0d25133ab086208656a562f']}

    agent_info['name'] = 'invalid'
    agent_info['domain'] = 'goodbye:1234'

    agent = AgentClient(agent_info)
    agent._connected = True
    try:
        result = list_models(agent=agent)
        print(result)
        pytest.fail(
            'did not raise an exception when could not connect to agent')
    except Exception as error:
        pass

    try:
        result = list_symbols(agent=agent)
        print(result)
        pytest.fail(
            'did not raise an exception when could not connect to agent')
    except Exception as error:
        pass


def test_get_models_containing_symbol(setup_and_teardown):

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)

    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}

    assert agent.clear_all_memory() == 'all-cleared'

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

    # before observing anything, these functions should have empty responses
    assert get_models_containing_symbol(
        agent=agent, symbol_set=set(["world"])) == {'P1': set([])}
    assert get_models_containing_symbol_strict(
        agent=agent, symbol_set=set(["hello", "world"])) == {'P1': set([])}

    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['hello']))) == {'auto_learned_model': '',
                                                                                     'prediction_made': False,
                                                                                     'status': 'observed'
                                                                                     }
    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['world']))) == {'auto_learned_model': '',
                                                                                     'prediction_made': False,
                                                                                     'status': 'observed'
                                                                                     }

    assert agent.learn() == 'MODEL|7d0678ba6305341ce0d25133ab086208656a562f'

    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['goodbye']))) == {'auto_learned_model': '',
                                                                                       'prediction_made': False,
                                                                                       'status': 'observed'
                                                                                       }
    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['cruel']))) == {'auto_learned_model': '',
                                                                                     'prediction_made': False,
                                                                                     'status': 'observed'
                                                                                     }
    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['world']))) == {'auto_learned_model': '',
                                                                                     'prediction_made': True,
                                                                                     'status': 'observed'
                                                                                     }

    assert agent.learn() == 'MODEL|3b5c9cdc4424988308922d2ec8c7bc06b7c6ac21'

    assert get_models_containing_symbol(agent=agent, symbol_set=set(["world"])) == {'P1': set(['3b5c9cdc4424988308922d2ec8c7bc06b7c6ac21',
                                                                                              '7d0678ba6305341ce0d25133ab086208656a562f'])}

    assert get_models_containing_symbol_strict(
        agent=agent, symbol_set=set(["world"])) == {'P1': set([])}

    assert get_models_containing_symbol_strict(agent=agent, symbol_set=set(
        ["hello", "world"])) == {'P1': set(["7d0678ba6305341ce0d25133ab086208656a562f"])}

    assert get_kb_subset(agent=agent, model_dict={'P1': ['3b5c9cdc4424988308922d2ec8c7bc06b7c6ac21']}) == {
        'P1': {'metadata': {},
               'models_kb': {'3b5c9cdc4424988308922d2ec8c7bc06b7c6ac21': {'emotives': {},
                                                                          'frequency': 1,
                                                                          'length': 3,
                                                                          'metadata': [{}, {}, {}],
                                                                          'name': '3b5c9cdc4424988308922d2ec8c7bc06b7c6ac21',
                                                                          'sequence': [['goodbye'],
                                                                                       ['cruel'],
                                                                                       ['world']]}
                             },
               'symbols_kb': {'cruel': {'features': {'frequency': 1,
                                                     'model_member_frequency': 1},
                                        'name': 'cruel'},
                              'goodbye': {'features': {'frequency': 1,
                                                       'model_member_frequency': 1},
                                          'name': 'goodbye'},
                              'world': {'features': {'frequency': 1,
                                                     'model_member_frequency': 1},
                                        'name': 'world'}},
               'vectors_kb': {}}
    }


def test_is_abstracted_symbol():

    symbol1 = 'PRIMITIVE|p0c243de45|7dfb11200f3f6c87c5ff2da58d336c1468648f6f|matches|VECTOR|a8a8a7c21374a1467481b84d02c751155a66e112'
    symbol2 = 'PRIMITIVE|HELLO|MODEL|banana|goodbye'
    symbol3 = 'PRIMITIVE|HELLO'
    symbol4 = 'PRIMITIVE|p23012312|hasher|tonight|72'
    symbol5 = 'NODE|p23012312|goodbye|hello|world'
    symbol6 = 'PRIMITIVE|p23012312|'

    assert is_abstracted_symbol(symbol=symbol1) == True
    assert is_abstracted_symbol(symbol=symbol2) == False
    assert is_abstracted_symbol(symbol=symbol3) == False
    assert is_abstracted_symbol(symbol=symbol4) == False
    assert is_abstracted_symbol(symbol=symbol5) == False
    assert is_abstracted_symbol(symbol=symbol6) == False


def test_remove_abstracted_symbols(setup_and_teardown_abstraction):

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'borlach_lumpkin'}

    assert agent.clear_all_memory() == {'P1': 'all-cleared',
                                        'P2': 'all-cleared'}

    assert agent.show_status() == {'P1':
                                   {'AUTOLEARN': False,
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
                                    },
                                   'P2':
                                   {'AUTOLEARN': False,
                                    'PREDICT': True,
                                    'HYPOTHESIZED': False,
                                    'SLEEPING': False,
                                    'SNAPSHOT': False,
                                    'emotives': {},
                                    'last_learned_model_name': '',
                                    'models_kb': '{KB| objects: 0}',
                                    'name': 'P2',
                                    'num_observe_call': 0,
                                    'size_WM': 0,
                                    'target': '',
                                    'time': 0,
                                    'vector_dimensionality': -1,
                                    'vectors_kb': '{KB| objects: 0}'
                                    }}

    assert agent.set_ingress_nodes(
        ['P1']) == [{'id': 'pbb2fabdc', 'name': 'P1'}]
    assert agent.set_query_nodes(
        ['P2']) == [{'id': 'p98fdaf83d', 'name': 'P2'}]

    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['hello']))) == {'auto_learned_model': '',
                                                                                     'prediction_made': False,
                                                                                     'status': 'observed'
                                                                                     }
    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['world']))) == {'auto_learned_model': '',
                                                                                     'prediction_made': False,
                                                                                     'status': 'observed'
                                                                                     }

    assert agent.learn() == {
        'P1': 'MODEL|7d0678ba6305341ce0d25133ab086208656a562f',
        'P2': None}

    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['hello']))) == {'auto_learned_model': '',
                                                                                     'prediction_made': True,
                                                                                     'status': 'observed'
                                                                                     }

    assert agent.show_status() == {'P1':
                                   {'AUTOLEARN': False,
                                    'PREDICT': True,
                                    'HYPOTHESIZED': False,
                                    'SLEEPING': False,
                                    'SNAPSHOT': False,
                                    'emotives': {},
                                    'last_learned_model_name': '7d0678ba6305341ce0d25133ab086208656a562f',
                                    'models_kb': '{KB| objects: 1}',
                                    'name': 'P1',
                                    'num_observe_call': 1,
                                    'size_WM': 1,
                                    'target': '',
                                    'time': 3,
                                    'vector_dimensionality': -1,
                                    'vectors_kb': '{KB| objects: 0}'
                                    },
                                   'P2':
                                   {'AUTOLEARN': False,
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
                                    }}

    assert remove_id_and_timestamp(agent.observe(create_gdf(strings=['world']))) == {'auto_learned_model': '',
                                                                                     'prediction_made': True,
                                                                                     'status': 'observed'
                                                                                     }

    assert agent.show_status() == {'P1':
                                   {'AUTOLEARN': False,
                                    'PREDICT': True,
                                    'HYPOTHESIZED': False,
                                    'SLEEPING': False,
                                    'SNAPSHOT': False,
                                    'emotives': {},
                                    'last_learned_model_name': '7d0678ba6305341ce0d25133ab086208656a562f',
                                    'models_kb': '{KB| objects: 1}',
                                    'name': 'P1',
                                    'num_observe_call': 2,
                                    'size_WM': 2,
                                    'target': '',
                                    'time': 4,
                                    'vector_dimensionality': -1,
                                    'vectors_kb': '{KB| objects: 0}'
                                    },
                                   'P2':
                                   {'AUTOLEARN': False,
                                    'PREDICT': True,
                                    'HYPOTHESIZED': False,
                                    'SLEEPING': False,
                                    'SNAPSHOT': False,
                                    'emotives': {},
                                    'last_learned_model_name': '',
                                    'models_kb': '{KB| objects: 0}',
                                    'name': 'P2',
                                    'num_observe_call': 3,
                                    'size_WM': 3,
                                    'target': '',
                                    'time': 3,
                                    'vector_dimensionality': -1,
                                    'vectors_kb': '{KB| objects: 0}'
                                    }}

    assert agent.learn() == {
        'P1': 'MODEL|7d0678ba6305341ce0d25133ab086208656a562f',
        'P2': 'MODEL|3b58db9d48b6959f7d7b1b70f8655fe356502933'}

    assert agent.get_model('MODEL|3b58db9d48b6959f7d7b1b70f8655fe356502933', nodes=['P2']) == {'emotives': {},
                                                                                               'frequency': 1,
                                                                                               'length': 3,
                                                                                               'metadata': [{}, {}, {}],
                                                                                               'predecessor_model': [],
                                                                                               'name': '3b58db9d48b6959f7d7b1b70f8655fe356502933',
                                                                                               'sequence': [['PRIMITIVE|pbb2fabdc|7d0678ba6305341ce0d25133ab086208656a562f|name|7d0678ba6305341ce0d25133ab086208656a562f'],
                                                                                                            ['PRIMITIVE|pbb2fabdc|7d0678ba6305341ce0d25133ab086208656a562f|future|world'],
                                                                                                            ['PRIMITIVE|pbb2fabdc|7d0678ba6305341ce0d25133ab086208656a562f|name|7d0678ba6305341ce0d25133ab086208656a562f']]
                                                                                               }

    assert remove_abstracted_symbols(agent=agent, symbols=['PRIMITIVE|pbb2fabdc|7d0678ba6305341ce0d25133ab086208656a562f|name|7d0678ba6305341ce0d25133ab086208656a562f',
                                                           'PRIMITIVE|pbb2fabdc|7d0678ba6305341ce0d25133ab086208656a562f|future|world',
                                                           'hello']) == None

    assert agent.show_status() == {'P1':
                                   {'AUTOLEARN': False,
                                    'PREDICT': True,
                                    'HYPOTHESIZED': False,
                                    'SLEEPING': False,
                                    'SNAPSHOT': False,
                                    'emotives': {},
                                    'last_learned_model_name': '7d0678ba6305341ce0d25133ab086208656a562f',
                                    'models_kb': '{KB| objects: 0}',
                                    'name': 'P1',
                                    'num_observe_call': 0,
                                    'size_WM': 0,
                                    'target': '',
                                    'time': 4,
                                    'vector_dimensionality': -1,
                                    'vectors_kb': '{KB| objects: 0}'
                                    },
                                   'P2':
                                   {'AUTOLEARN': False,
                                    'PREDICT': True,
                                    'HYPOTHESIZED': False,
                                    'SLEEPING': False,
                                    'SNAPSHOT': False,
                                    'emotives': {},
                                    'last_learned_model_name': '3b58db9d48b6959f7d7b1b70f8655fe356502933',
                                    'models_kb': '{KB| objects: 0}',
                                    'name': 'P2',
                                    'num_observe_call': 0,
                                    'size_WM': 0,
                                    'target': '',
                                    'time': 3,
                                    'vector_dimensionality': -1,
                                    'vectors_kb': '{KB| objects: 0}'
                                    }}
