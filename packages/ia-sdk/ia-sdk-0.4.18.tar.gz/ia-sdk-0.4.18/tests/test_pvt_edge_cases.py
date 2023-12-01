from lib.dependencies import MyFixture
import pytest
import traceback
from ia.gaius.agent_client import AgentClient
from ia.gaius.pvt import PerformanceValidationTest
from ia.gaius.data_ops import Data
import pathlib

test_dir = pathlib.Path(__file__).parent.resolve()


@pytest.fixture(scope="function")
def setup_and_teardown(request):
    print(f'{request.keywords=}')
    GENOME = request.keywords['setup_and_teardown'].kwargs['GENOME']
    fixture = MyFixture(GENOME)
    yield fixture
    fixture.teardown(GENOME)

# @pytest.fixture(scope="function")
# def setup_and_teardown_with_mongo(GENOME):
#     fixture = MyFixture(GENOME, mongo=True)
#     yield fixture
#     fixture.teardown(GENOME, mongo=True)


address = "localhost:8000"


@pytest.mark.setup_and_teardown(GENOME=test_dir.joinpath("./genomes/gundahad_inglorion.json"))
def test_emotive_value_high_rt(setup_and_teardown):
    INGRESS_NODES = ["P1", "P2", "P3", "P4", "P5"]
    QUERY_NODES = ["P1", "P2", "P3", "P4", "P5"]
    BHP_DATASET_PATH = str(
        test_dir.joinpath('./datasets/shuffled_bhp'))
    PCT_CHOSEN = 10
    PCT_TRAINING = 80

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'gundahad_inglorion'}
    agent.set_summarize_for_single_node(False)
    agent.clear_all_memory()

    bhp_data = Data(data_directories=[BHP_DATASET_PATH])
    bhp_data.prep(percent_of_dataset_chosen=PCT_CHOSEN,
                  percent_reserved_for_training=PCT_TRAINING,
                  shuffle=False)

    try:
        pvt = PerformanceValidationTest(agent=agent,
                                        ingress_nodes=INGRESS_NODES,
                                        query_nodes=QUERY_NODES,
                                        test_count=1,
                                        test_type='emotives_value',
                                        dataset=bhp_data,
                                        test_prediction_strategy='noncontinuous',
                                        learning_strategy='after_every',
                                        clear_all_memory_before_training=True,
                                        turn_prediction_off_during_training=True,
                                        shuffle=False,
                                        QUIET=True,
                                        DISABLE_TQDM=False)

        pvt.conduct_pvt()

    except KeyError as e:
        traceback.print_exc()
        pytest.fail(reason=f'{type(e).__name__}: {str(e)}')

    pass


@pytest.mark.setup_and_teardown(GENOME=test_dir.joinpath("./genomes/gundahad_inglorion.json"))
def test_emotive_value_all_train(setup_and_teardown):
    INGRESS_NODES = ["P1", "P2", "P3", "P4", "P5"]
    QUERY_NODES = ["P1", "P2", "P3", "P4", "P5"]
    BHP_DATASET_PATH = str(
        test_dir.joinpath('./datasets/shuffled_bhp'))
    PCT_CHOSEN = 10
    PCT_TRAINING = 100

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'gundahad_inglorion'}
    agent.set_summarize_for_single_node(False)
    agent.clear_all_memory()

    bhp_data = Data(data_directories=[BHP_DATASET_PATH])
    bhp_data.prep(percent_of_dataset_chosen=PCT_CHOSEN,
                  percent_reserved_for_training=PCT_TRAINING,
                  shuffle=False)

    try:
        pvt = PerformanceValidationTest(agent=agent,
                                        ingress_nodes=INGRESS_NODES,
                                        query_nodes=QUERY_NODES,
                                        test_count=1,
                                        test_type='emotives_value',
                                        dataset=bhp_data,
                                        test_prediction_strategy='noncontinuous',
                                        learning_strategy='after_every',
                                        clear_all_memory_before_training=True,
                                        turn_prediction_off_during_training=True,
                                        shuffle=False,
                                        QUIET=True,
                                        DISABLE_TQDM=False)

        pvt.conduct_pvt()

    except Exception as error:
        traceback.print_exc()
        pytest.fail(reason=f'{type(e).__name__}: {str(error)}')

    pass
