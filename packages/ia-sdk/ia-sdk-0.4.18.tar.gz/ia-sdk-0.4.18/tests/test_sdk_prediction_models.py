from ia.gaius.utils import create_gdf
from ia.gaius.prediction_models import prediction_ensemble_modeled_emotives, average_emotives, prediction_ensemble_model_classification
import pytest
from lib.dependencies import remove_id_and_timestamp, MyFixture
from ia.gaius.agent_client import AgentClient
from ia.gaius.utils import create_gdf
import pathlib

test_dir = pathlib.Path(__file__).parent.resolve()
GENOME = test_dir.joinpath("genomes/simple.genome")

address = "localhost:8000"


@pytest.fixture(scope="function")
def setup_and_teardown():
    fixture = MyFixture(GENOME)
    yield fixture
    fixture.teardown(GENOME)


def test_prediction_modeled_emotives(setup_and_teardown):
    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}

    agent.set_ingress_nodes(nodes=['P1'])
    agent.set_query_nodes(nodes=['P1'])

    agent.clear_all_memory()

    # Learn Sequences for emotive functions

    gdf_sequence1 = [create_gdf(strings=['hello']),
                     create_gdf(strings=['world'], emotives={'DONE': 100, 'HAPPY': 50})]
    gdf_sequence2 = [create_gdf(strings=['goodbye']),
                     create_gdf(strings=['cruel']),
                     create_gdf(strings=['world'], emotives={'DONE': 100, 'HAPPY': -50})]
    gdf_sequence2_2 = [create_gdf(strings=['world']),
                       create_gdf(strings=['goodbye']),
                       create_gdf(strings=['cruel']),
                       create_gdf(strings=['world'], emotives={'DONE': 100, 'HAPPY': -75})]

    for gdf in gdf_sequence1:
        agent.observe(gdf)
    assert agent.learn() == 'MODEL|7d0678ba6305341ce0d25133ab086208656a562f'

    assert agent.show_status() == {'AUTOLEARN': False,
                                   'PREDICT': True,
                                   'HYPOTHESIZED': False,
                                   'SLEEPING': False,
                                   'SNAPSHOT': False,
                                   'emotives': {'DONE': 100, 'HAPPY': 50},
                                   'last_learned_model_name': '7d0678ba6305341ce0d25133ab086208656a562f',
                                   'models_kb': '{KB| objects: 1}',
                                   'name': 'P1',
                                   'num_observe_call': 0,
                                   'size_WM': 0,
                                   'target': '',
                                   'time': 2,
                                   'vector_dimensionality': -1,
                                   'vectors_kb': '{KB| objects: 0}'}

    agent.observe(gdf_sequence1[0])

    EXPECTED_PRED_1 = [{'confidence': 1,
                        'confluence': 0.5,
                        'emotives': {'DONE': 100, 'HAPPY': 50},
                        'entropy': 0.5,
                        'evidence': 0.5,
                        'extras': [],
                        'fragmentation': 0,
                        'frequency': 1,
                        'future': [['world']],
                        'grand_hamiltonian': 0.5,
                        'hamiltonian': 0,
                        'itfdf_similarity': 1,
                        'matches': ['hello'],
                        'missing': [],
                        'name': '7d0678ba6305341ce0d25133ab086208656a562f',
                        'past': [],
                        'potential': 3.5,
                        'present': [['hello']],
                        'similarity': 0.6666666666666666,
                        'snr': 1,
                        'type': 'prototypical'}]

    assert agent.get_predictions() == EXPECTED_PRED_1

    # only one prediction, so it should be the same as
    # the emotives present in that model
    assert prediction_ensemble_modeled_emotives(EXPECTED_PRED_1) == {
        'HAPPY': 50, 'DONE': 100}

    agent.clear_wm()

    for gdf in gdf_sequence2:
        agent.observe(gdf)
    assert agent.learn() == 'MODEL|3b5c9cdc4424988308922d2ec8c7bc06b7c6ac21'

    assert agent.show_status() == {'AUTOLEARN': False,
                                   'PREDICT': True,
                                   'HYPOTHESIZED': False,
                                   'SLEEPING': False,
                                   'SNAPSHOT': False,
                                   'emotives': {'DONE': 100, 'HAPPY': -50},
                                   'last_learned_model_name': '3b5c9cdc4424988308922d2ec8c7bc06b7c6ac21',
                                   'models_kb': '{KB| objects: 2}',
                                   'name': 'P1',
                                   'num_observe_call': 0,
                                   'size_WM': 0,
                                   'target': '',
                                   'time': 6,
                                   'vector_dimensionality': -1,
                                   'vectors_kb': '{KB| objects: 0}'}

    # observe "world" symbol
    agent.observe(create_gdf(strings=['world']))

    EXPECTED_PRED_2 = [{'confidence': 1,
                        'confluence': 0.3,
                        'emotives': {'DONE': 100, 'HAPPY': 50},
                        'entropy': 0.5287712379549449,
                        'evidence': 0.5,
                        'extras': [],
                        'fragmentation': 0,
                        'frequency': 1,
                        'future': [],
                        'grand_hamiltonian': 0.2643856189774724,
                        'hamiltonian': 0,
                        'itfdf_similarity': 1,
                        'matches': ['world'],
                        'missing': [],
                        'name': '7d0678ba6305341ce0d25133ab086208656a562f',
                        'past': [['hello']],
                        'potential': 3.5,
                        'present': [['world']],
                        'similarity': 0.6666666666666666,
                        'snr': 1,
                        'type': 'prototypical'},
                       {'confidence': 1,
                        'confluence': 0.3,
                        'emotives': {'DONE': 100, 'HAPPY': -50},
                        'entropy': 0.5287712379549449,
                        'evidence': 0.3333333333333333,
                        'extras': [],
                        'fragmentation': 0,
                        'frequency': 1,
                        'future': [],
                        'grand_hamiltonian': 0.2643856189774724,
                        'hamiltonian': 0,
                        'itfdf_similarity': 1,
                        'matches': ['world'],
                        'missing': [],
                        'name': '3b5c9cdc4424988308922d2ec8c7bc06b7c6ac21',
                        'past': [['goodbye'], ['cruel']],
                        'potential': 3.333333333333333,
                        'present': [['world']],
                        'similarity': 0.5,
                        'snr': 1,
                        'type': 'prototypical'}]

    assert agent.get_predictions() == EXPECTED_PRED_2

    # Expect DONE emotive to be 100, HAPPY emotive to be 0
    assert average_emotives([p['emotives'] for p in EXPECTED_PRED_2]) == {
        'DONE': 100, 'HAPPY': 0}

    assert prediction_ensemble_modeled_emotives(EXPECTED_PRED_2) == {
        'DONE': 100.0, 'HAPPY': 1.2195121951219505}

    agent.clear_wm()

    for gdf in gdf_sequence2_2:
        agent.observe(gdf)
    assert agent.learn() == 'MODEL|a524ea4c15d721e694f0df9c800cc11ce22bceae'

    agent.clear_wm()

    agent.observe(create_gdf(strings=['world']))

    EXPECTED_PRED_2_2 = [{'confidence': 1,
                          'confluence': 0.16666666666666666,
                          'emotives': {'DONE': 100, 'HAPPY': 50},
                          'entropy': 0.5,
                          'evidence': 0.5,
                          'extras': [],
                          'fragmentation': 0,
                          'frequency': 1,
                          'future': [],
                          'grand_hamiltonian': 0.25,
                          'hamiltonian': 0,
                          'itfdf_similarity': 1,
                          'matches': ['world'],
                          'missing': [],
                          'name': '7d0678ba6305341ce0d25133ab086208656a562f',
                          'past': [['hello']],
                          'potential': 3.5,
                          'present': [['world']],
                          'similarity': 0.6666666666666666,
                          'snr': 1,
                          'type': 'prototypical'},
                         {'confidence': 1,
                         'confluence': 0.16666666666666666,
                          'emotives': {'DONE': 100, 'HAPPY': -50},
                          'entropy': 0.5,
                          'evidence': 0.3333333333333333,
                          'extras': [],
                          'fragmentation': 0,
                          'frequency': 1,
                          'future': [],
                          'grand_hamiltonian': 0.25,
                          'hamiltonian': 0,
                          'itfdf_similarity': 1,
                          'matches': ['world'],
                          'missing': [],
                          'name': '3b5c9cdc4424988308922d2ec8c7bc06b7c6ac21',
                          'past': [['goodbye'], ['cruel']],
                          'potential': 3.333333333333333,
                          'present': [['world']],
                          'similarity': 0.5,
                          'snr': 1,
                          'type': 'prototypical'},
                         {'confidence': 1,
                         'confluence': 0.16666666666666666,
                          'emotives': {'DONE': 100, 'HAPPY': -75},
                          'entropy': 0.5,
                          'evidence': 0.25,
                          'extras': [],
                          'fragmentation': 0,
                          'frequency': 1,
                          'future': [['goodbye'], ['cruel'], ['world']],
                          'grand_hamiltonian': 0.25,
                          'hamiltonian': 0,
                          'itfdf_similarity': 1,
                          'matches': ['world'],
                          'missing': [],
                          'name': 'a524ea4c15d721e694f0df9c800cc11ce22bceae',
                          'past': [],
                          'potential': 3.25,
                          'present': [['world']],
                          'similarity': 0.4,
                          'snr': 1,
                          'type': 'prototypical'}]

    # agent.get_predictions()

    assert agent.get_predictions() == EXPECTED_PRED_2_2

    assert average_emotives([p['emotives'] for p in EXPECTED_PRED_2_2]) == {
        'DONE': 100, 'HAPPY': -25}

    assert prediction_ensemble_modeled_emotives(EXPECTED_PRED_2_2) == {
        'DONE': 100.0, 'HAPPY': -12.692097534321434}


def test_prediction_ensemble_model_classification(setup_and_teardown):

    # Prediction Ensemble Model Classification
    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}

    agent.set_ingress_nodes(nodes=['P1'])
    agent.set_query_nodes(nodes=['P1'])

    agent.clear_all_memory()

    gdf_sequence_3 = [create_gdf(strings=['furry', 'black', 'tail', 'small']),
                      create_gdf(strings=['ANIMAL|CAT'])]
    gdf_sequence_4 = [create_gdf(strings=['furry', 'white', 'tail', 'small']),
                      create_gdf(strings=['ANIMAL|CAT'])]
    gdf_sequence_5 = [create_gdf(strings=['furry', 'orange', 'tail', 'small']),
                      create_gdf(strings=['ANIMAL|CAT'])]
    gdf_sequence_6 = [create_gdf(strings=['slimy', 'spotted', 'small']),
                      create_gdf(strings=['ANIMAL|FROG'])]
    gdf_sequence_7 = [create_gdf(strings=['tall', 'spotted', 'yellow', 'zoo']),
                      create_gdf(strings=['ANIMAL|giraffe', 'TYPE|WILD'])]

    for gdf in gdf_sequence_3:
        agent.observe(gdf)
    assert agent.learn() == 'MODEL|5b0da7c263d03889c2691cdea5843dccf378d6bd'

    agent.observe(create_gdf(strings=['small']))

    EXPECTED_PRED_3 = [{'confidence': 0.25,
                        'confluence': 0.9984,
                        'emotives': {},
                        'entropy': 1.8575424759098897,
                        'evidence': 0.2,
                        'extras': [],
                        'fragmentation': 0,
                        'frequency': 1,
                        'future': [['ANIMAL|CAT']],
                        'grand_hamiltonian': 0.8,
                        'hamiltonian': 0.8613531161467861,
                        'itfdf_similarity': 0.5,
                        'matches': ['small'],
                        'missing': ['black', 'furry', 'tail'],
                        'name': '5b0da7c263d03889c2691cdea5843dccf378d6bd',
                        'past': [],
                        'potential': 1.95,
                        'present': [['black', 'furry', 'small', 'tail']],
                        'similarity': 0.3333333333333333,
                        'snr': 1,
                        'type': 'prototypical'}]

    assert agent.get_predictions() == EXPECTED_PRED_3

    assert prediction_ensemble_model_classification(EXPECTED_PRED_3) == {
        'CAT': 1.95}
    assert prediction_ensemble_model_classification(
        EXPECTED_PRED_3).most_common()[0][0] == 'CAT'

    agent.clear_wm()

    for gdf in gdf_sequence_4:
        agent.observe(gdf)
    assert agent.learn() == 'MODEL|8b1b9c4cfe391d91986576dd805ad11a5f1b9faf'

    agent.observe(create_gdf(strings=['small']))

    EXPECTED_PRED_4 = [{'confidence': 0.25,
                        'confluence': 0.4996,
                        'emotives': {},
                        'entropy': 1.7253496664211536,
                        'evidence': 0.2,
                        'extras': [],
                        'fragmentation': 0,
                        'frequency': 1,
                        'future': [['ANIMAL|CAT']],
                        'grand_hamiltonian': 0.6674563619162032,
                        'hamiltonian': 0.7737056144690831,
                        'itfdf_similarity': 0.7773500981126146,
                        'matches': ['small'],
                        'missing': ['furry', 'tail', 'white'],
                        'name': '8b1b9c4cfe391d91986576dd805ad11a5f1b9faf',
                        'past': [],
                        'potential': 2.2273500981126144,
                        'present': [['furry', 'small', 'tail', 'white']],
                        'similarity': 0.3333333333333333,
                        'snr': 1,
                        'type': 'prototypical'},
                       {'confidence': 0.25,
                        'confluence': 0.4996,
                        'emotives': {},
                        'entropy': 1.7253496664211536,
                        'evidence': 0.2,
                        'extras': [],
                        'fragmentation': 0,
                        'frequency': 1,
                        'future': [['ANIMAL|CAT']],
                        'grand_hamiltonian': 0.6674563619162033,
                        'hamiltonian': 0.7737056144690831,
                        'itfdf_similarity': 0.7773500981126146,
                        'matches': ['small'],
                        'missing': ['black', 'furry', 'tail'],
                        'name': '5b0da7c263d03889c2691cdea5843dccf378d6bd',
                        'past': [],
                        'potential': 2.2273500981126144,
                        'present': [['black', 'furry', 'small', 'tail']],
                        'similarity': 0.3333333333333333,
                        'snr': 1,
                        'type': 'prototypical'}
                       ]

    assert agent.get_predictions() == EXPECTED_PRED_4

    assert prediction_ensemble_model_classification(
        EXPECTED_PRED_4) == {'CAT': 4.454700196225229}
    assert prediction_ensemble_model_classification(
        EXPECTED_PRED_4).most_common()[0][0] == 'CAT'

    agent.clear_wm()

    for gdf in gdf_sequence_5:
        agent.observe(gdf)
    assert agent.learn() == 'MODEL|f91a87e12a85bfb23dd33ba2903c658a2c96d89e'

    agent.observe(create_gdf(strings=['small']))

    EXPECTED_PRED_5 = [{'confidence': 0.25,
                        'confluence': 0.33315555555555554,
                        'emotives': {},
                        'entropy': 1.6536162299729853,
                        'evidence': 0.2,
                        'extras': [],
                        'fragmentation': 0,
                        'frequency': 1,
                        'future': [['ANIMAL|CAT']],
                        'grand_hamiltonian': 0.5890299858348494,
                        'hamiltonian': 0.7124143742160444,
                        'itfdf_similarity': 0.8556489031712803,
                        'matches': ['small'],
                        'missing': ['furry', 'orange', 'tail'],
                        'name': 'f91a87e12a85bfb23dd33ba2903c658a2c96d89e',
                        'past': [],
                        'potential': 2.3056489031712806,
                        'present': [['furry', 'orange', 'small', 'tail']],
                        'similarity': 0.3333333333333333,
                        'snr': 1,
                        'type': 'prototypical'},
                       {'confidence': 0.25,
                        'confluence': 0.33315555555555554,
                        'emotives': {},
                        'entropy': 1.6536162299729853,
                        'evidence': 0.2,
                        'extras': [],
                        'fragmentation': 0,
                        'frequency': 1,
                        'future': [['ANIMAL|CAT']],
                        'grand_hamiltonian': 0.5890299858348494,
                        'hamiltonian': 0.7124143742160444,
                        'itfdf_similarity': 0.8556489031712803,
                        'matches': ['small'],
                        'missing': ['furry', 'tail', 'white'],
                        'name': '8b1b9c4cfe391d91986576dd805ad11a5f1b9faf',
                        'past': [],
                        'potential': 2.3056489031712806,
                        'present': [['furry', 'small', 'tail', 'white']],
                        'similarity': 0.3333333333333333,
                        'snr': 1,
                        'type': 'prototypical'},
                       {'confidence': 0.25,
                        'confluence': 0.33315555555555554,
                        'emotives': {},
                        'entropy': 1.6536162299729853,
                        'evidence': 0.2,
                        'extras': [],
                        'fragmentation': 0,
                        'frequency': 1,
                        'future': [['ANIMAL|CAT']],
                        'grand_hamiltonian': 0.5890299858348494,
                        'hamiltonian': 0.7124143742160444,
                        'itfdf_similarity': 0.8556489031712803,
                        'matches': ['small'],
                        'missing': ['black', 'furry', 'tail'],
                        'name': '5b0da7c263d03889c2691cdea5843dccf378d6bd',
                        'past': [],
                        'potential': 2.3056489031712806,
                        'present': [['black', 'furry', 'small', 'tail']],
                        'similarity': 0.3333333333333333,
                        'snr': 1,
                        'type': 'prototypical'}
                       ]

    assert agent.get_predictions() == EXPECTED_PRED_5

    assert prediction_ensemble_model_classification(
        EXPECTED_PRED_5) == {'CAT': 6.916946709513842}
    assert prediction_ensemble_model_classification(
        EXPECTED_PRED_5).most_common()[0][0] == 'CAT'

    agent.clear_wm()

    for gdf in gdf_sequence_6:
        agent.observe(gdf)
    assert agent.learn() == 'MODEL|4a0dc5959df1e190efcd913dcbfd58190d22bcb4'

    agent.observe(create_gdf(strings=['small']))

    EXPECTED_PRED_6 = [{'confidence': 0.3333333333333333,
                        'confluence': 0.24985420615250037,
                        'emotives': {},
                        'entropy': 0.9203981621400796,
                        'evidence': 0.25,
                        'extras': [],
                        'fragmentation': 0,
                        'frequency': 1,
                        'future': [['ANIMAL|FROG']],
                        'grand_hamiltonian': 0.2770674547581644,
                        'hamiltonian': 0.4771212547196624,
                        'itfdf_similarity': 0.9857022603955158,
                        'matches': ['small'],
                        'missing': ['slimy', 'spotted'],
                        'name': '4a0dc5959df1e190efcd913dcbfd58190d22bcb4',
                        'past': [],
                        'potential': 2.569035593728849,
                        'present': [['slimy', 'small', 'spotted']],
                        'similarity': 0.4,
                        'snr': 1,
                        'type': 'prototypical'},
                       {'confidence': 0.25,
                        'confluence': 0.24993093975644753,
                        'emotives': {},
                        'entropy': 1.537759349660658,
                        'evidence': 0.2,
                        'extras': [],
                        'fragmentation': 0,
                        'frequency': 1,
                        'future': [['ANIMAL|CAT']],
                        'grand_hamiltonian': 0.4629116903605944,
                        'hamiltonian': 0.6020599913279623,
                        'itfdf_similarity': 0.9190308509457032,
                        'matches': ['small'],
                        'missing': ['furry', 'orange', 'tail'],
                        'name': 'f91a87e12a85bfb23dd33ba2903c658a2c96d89e',
                        'past': [],
                        'potential': 2.369030850945703,
                        'present': [['furry', 'orange', 'small', 'tail']],
                        'similarity': 0.3333333333333333,
                        'snr': 1,
                        'type': 'prototypical'},
                       {'confidence': 0.25,
                        'confluence': 0.24993093975644753,
                        'emotives': {},
                        'entropy': 1.537759349660658,
                        'evidence': 0.2,
                        'extras': [],
                        'fragmentation': 0,
                        'frequency': 1,
                        'future': [['ANIMAL|CAT']],
                        'grand_hamiltonian': 0.4629116903605944,
                        'hamiltonian': 0.6020599913279623,
                        'itfdf_similarity': 0.9190308509457032,
                        'matches': ['small'],
                        'missing': ['furry', 'tail', 'white'],
                        'name': '8b1b9c4cfe391d91986576dd805ad11a5f1b9faf',
                        'past': [],
                        'potential': 2.369030850945703,
                        'present': [['furry', 'small', 'tail', 'white']],
                        'similarity': 0.3333333333333333,
                        'snr': 1,
                        'type': 'prototypical'},
                       {'confidence': 0.25,
                        'confluence': 0.24993093975644753,
                        'emotives': {},
                        'entropy': 1.537759349660658,
                        'evidence': 0.2,
                        'extras': [],
                        'fragmentation': 0,
                        'frequency': 1,
                        'future': [['ANIMAL|CAT']],
                        'grand_hamiltonian': 0.4629116903605944,
                        'hamiltonian': 0.6020599913279623,
                        'itfdf_similarity': 0.9190308509457032,
                        'matches': ['small'],
                        'missing': ['black', 'furry', 'tail'],
                        'name': '5b0da7c263d03889c2691cdea5843dccf378d6bd',
                        'past': [],
                        'potential': 2.369030850945703,
                        'present': [['black', 'furry', 'small', 'tail']],
                        'similarity': 0.3333333333333333,
                        'snr': 1,
                        'type': 'prototypical'}
                       ]

    assert agent.get_predictions() == EXPECTED_PRED_6

    assert prediction_ensemble_model_classification(EXPECTED_PRED_6) == {
        'FROG': pytest.approx(2.569035593728849), 'CAT': pytest.approx(7.107092552837109)}

    assert prediction_ensemble_model_classification(
        EXPECTED_PRED_6).most_common()[0][0] == 'CAT'

    agent.clear_wm()

    agent.observe(create_gdf(strings=['slimy']))

    EXPECTED_PRED_6_2 = [{'confidence': 0.3333333333333333,
                          'confluence': 0.24985420615250037,
                          'emotives': {},
                          'entropy': 0.9203981621400796,
                          'evidence': 0.25,
                          'extras': [],
                          'fragmentation': 0,
                          'frequency': 1,
                          'future': [['ANIMAL|FROG']],
                          'grand_hamiltonian': 0.2770674547581644,
                          'hamiltonian': 0.4771212547196624,
                          'itfdf_similarity': 0.23570226039551578,
                          'matches': ['slimy'],
                          'missing': ['small', 'spotted'],
                          'name': '4a0dc5959df1e190efcd913dcbfd58190d22bcb4',
                          'past': [],
                          'potential': 1.8190355937288492,
                          'present': [['slimy', 'small', 'spotted']],
                          'similarity': 0.4,
                          'snr': 1,
                          'type': 'prototypical'}]

    assert agent.get_predictions() == EXPECTED_PRED_6_2

    assert prediction_ensemble_model_classification(EXPECTED_PRED_6_2) == {
        'FROG': 1.8190355937288492}
    assert prediction_ensemble_model_classification(
        EXPECTED_PRED_6_2).most_common()[0][0] == 'FROG'

    agent.clear_wm()

    for gdf in gdf_sequence_7:
        agent.observe(gdf)
    assert agent.learn() == 'MODEL|91ec6e77c6e4fd4e4577b9dee85a4ec0aa309f33'

    agent.observe(create_gdf(strings=['spotted']))

    EXPECTED_PRED_7 = [{'confidence': 0.3333333333333333,
                        'confluence': 0.1998976,
                        'emotives': {},
                        'entropy': 0.9002797331369229,
                        'evidence': 0.25,
                        'extras': [],
                        'fragmentation': 0,
                        'frequency': 1,
                        'future': [['ANIMAL|FROG']],
                        'grand_hamiltonian': 0.2304338222700346,
                        'hamiltonian': 0.40568387108221293,
                        'itfdf_similarity': 0.7182178902359924,
                        'matches': ['spotted'],
                        'missing': ['slimy', 'small'],
                        'name': '4a0dc5959df1e190efcd913dcbfd58190d22bcb4',
                        'past': [],
                        'potential': 2.3015512235693256,
                        'present': [['slimy', 'small', 'spotted']],
                        'similarity': 0.4,
                        'snr': 1,
                        'type': 'prototypical'},
                       {'confidence': 0.25,
                        'confluence': 0.19999897600000002,
                        'emotives': {},
                        'entropy': 0.848771237954945,
                        'evidence': 0.16666666666666666,
                        'extras': [],
                        'fragmentation': 0,
                        'frequency': 1,
                        'future': [['ANIMAL|giraffe', 'TYPE|WILD']],
                        'grand_hamiltonian': 0.2172498095823296,
                        'hamiltonian': 0.511916049619631,
                        'itfdf_similarity': 0.8779644730092272,
                        'matches': ['spotted'],
                        'missing': ['tall', 'yellow', 'zoo'],
                        'name': '91ec6e77c6e4fd4e4577b9dee85a4ec0aa309f33',
                        'past': [],
                        'potential': 2.294631139675894,
                        'present': [['spotted', 'tall', 'yellow', 'zoo']],
                        'similarity': 0.2857142857142857,
                        'snr': 1,
                        'type': 'prototypical'}]

    assert agent.get_predictions() == EXPECTED_PRED_7

    assert prediction_ensemble_model_classification(EXPECTED_PRED_7) == {'FROG': 2.3015512235693256,
                                                                         'giraffe': 2.294631139675894,
                                                                         'WILD': 2.294631139675894}

    assert prediction_ensemble_model_classification(
        EXPECTED_PRED_7).most_common()[0][0] == 'FROG'

    agent.clear_wm()

    agent.observe(create_gdf(strings=['tall']))

    EXPECTED_PRED_7_2 = [{'confidence': 0.25,
                          'confluence': 0.19999897600000002,
                          'emotives': {},
                          'entropy': 0.848771237954945,
                          'evidence': 0.16666666666666666,
                          'extras': [],
                          'fragmentation': 0,
                          'frequency': 1,
                          'future': [['ANIMAL|giraffe', 'TYPE|WILD']],
                          'grand_hamiltonian': 0.2172498095823296,
                          'hamiltonian': 0.511916049619631,
                          'itfdf_similarity': 0.3779644730092272,
                          'matches': ['tall'],
                          'missing': ['spotted', 'yellow', 'zoo'],
                          'name': '91ec6e77c6e4fd4e4577b9dee85a4ec0aa309f33',
                          'past': [],
                          'potential': 1.7946311396758938,
                          'present': [['spotted', 'tall', 'yellow', 'zoo']],
                          'similarity': 0.2857142857142857,
                          'snr': 1,
                          'type': 'prototypical'}]

    assert agent.get_predictions() == EXPECTED_PRED_7_2

    assert prediction_ensemble_model_classification(EXPECTED_PRED_7_2) == {
        'giraffe': 1.7946311396758938, 'WILD': 1.7946311396758938}
