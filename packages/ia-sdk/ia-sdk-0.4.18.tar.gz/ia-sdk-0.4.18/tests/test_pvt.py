from lib.dependencies import remove_id_and_timestamp, MyFixture
import json
import pytest
import time
import os
from ia.gaius.agent_client import AgentClient
from ia.gaius.pvt import PerformanceValidationTest
from ia.gaius.pvt.mongo_interface import MongoData
from ia.gaius.manager import AgentManager
from pymongo import MongoClient
from ia.gaius.prediction_models import prediction_ensemble_model_classification, prediction_ensemble_modeled_emotives
from ia.gaius.data_ops import Data, PreparedData
import pathlib

test_dir = pathlib.Path(__file__).parent.resolve()
GENOME = test_dir.joinpath("./genomes/simple.genome")


@pytest.fixture(scope="function")
def setup_and_teardown():
    fixture = MyFixture(GENOME)
    yield fixture
    fixture.teardown(GENOME)


@pytest.fixture(scope="function")
def setup_and_teardown_with_mongo():
    fixture = MyFixture(GENOME, mongo=True)
    yield fixture
    fixture.teardown(GENOME, mongo=True)


address = "localhost:8000"

EXPECTED_IRIS_ACTUALS = [['versicolor'],
                         ['virginica'],
                         ['setosa'],
                         ['virginica'],
                         ['versicolor'],
                         ['versicolor'],
                         ['virginica'],
                         ['virginica'],
                         ['versicolor'],
                         ['setosa'],
                         ['setosa'],
                         ['virginica'],
                         ['versicolor'],
                         ['setosa'],
                         ['setosa'],
                         ['versicolor'],
                         ['virginica'],
                         ['virginica'],
                         ['virginica'],
                         ['versicolor'],
                         ['virginica'],
                         ['setosa'],
                         ['virginica'],
                         ['setosa'],
                         ['virginica'],
                         ['virginica'],
                         ['virginica'],
                         ['setosa'],
                         ['versicolor'],
                         ['versicolor']]

EXPECTED_IRIS_PREDS = [{'P1': 'versicolor'},
                       {'P1': 'virginica'},
                       {'P1': 'setosa'},
                       {'P1': 'versicolor'},
                       {'P1': 'versicolor'},
                       {'P1': 'versicolor'},
                       {'P1': 'virginica'},
                       {'P1': 'virginica'},
                       {'P1': 'versicolor'},
                       {'P1': 'setosa'},
                       {'P1': 'setosa'},
                       {'P1': 'virginica'},
                       {'P1': 'versicolor'},
                       {'P1': 'setosa'},
                       {'P1': 'setosa'},
                       {'P1': 'versicolor'},
                       {'P1': 'virginica'},
                       {'P1': 'virginica'},
                       {'P1': 'virginica'},
                       {'P1': 'versicolor'},
                       {'P1': 'virginica'},
                       {'P1': 'setosa'},
                       {'P1': 'virginica'},
                       {'P1': 'setosa'},
                       {'P1': 'virginica'},
                       {'P1': 'virginica'},
                       {'P1': 'virginica'},
                       {'P1': 'setosa'},
                       {'P1': 'versicolor'},
                       {'P1': 'virginica'}]


def test_pvt_classification(setup_and_teardown):
    INGRESS_NODES = ["P1"]
    QUERY_NODES = ["P1"]
    CLASSIFICATION_DATASET_PATH = str(
        test_dir.joinpath('./datasets/shuffled_iris_flowers'))
    PCT_CHOSEN = 100
    PCT_TRAINING = 80

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}
    agent.set_summarize_for_single_node(False)
    agent.clear_all_memory()

    assert agent.change_genes({'recall_threshold': 0.1}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'max_predictions': 5}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'near_vector_count': 3}) == {
        'P1': 'updated-genes'}

    iris_data = Data(data_directories=[CLASSIFICATION_DATASET_PATH])
    iris_data.prep(percent_of_dataset_chosen=PCT_CHOSEN,
                   percent_reserved_for_training=PCT_TRAINING,
                   shuffle=False)

    # verify that the train and test sequences are exactly as we expect (no shuffle)
    assert [os.path.basename(item) for item in iris_data.train_sequences] == ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56',
                                                                              '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119']
    assert [os.path.basename(item) for item in iris_data.test_sequences] == ['120', '121', '122', '123', '124', '125', '126', '127', '128', '129',
                                                                             '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149']

    pvt = PerformanceValidationTest(agent=agent,
                                    ingress_nodes=INGRESS_NODES,
                                    query_nodes=QUERY_NODES,
                                    test_count=1,
                                    dataset_percentage=PCT_CHOSEN,
                                    training_percentage=PCT_TRAINING,
                                    test_type='classification',
                                    dataset=iris_data,
                                    test_prediction_strategy='noncontinuous',
                                    clear_all_memory_before_training=True,
                                    turn_prediction_off_during_training=True,
                                    shuffle=False,
                                    QUIET=True)

    pvt.conduct_pvt()

    # with open(test_dir.joinpath('results/current_iris_prediction_log.json'), 'w') as f:
    #     json.dump(pvt.predictions, f)

    with open(test_dir.joinpath('results/iris_prediction_log.json')) as f:
        assert pvt.predictions == json.load(f)

    predicted_vals = []

    for preds in pvt.predictions:
        preds_dict = {k: prediction_ensemble_model_classification(
            preds[k]) for k in preds}
        for k in preds_dict.keys():
            if preds_dict[k] is not None:
                preds_dict[k] = preds_dict[k].most_common()[0][0]

        predicted_vals.append(preds_dict)

    assert predicted_vals == EXPECTED_IRIS_PREDS

    assert pvt.actuals == EXPECTED_IRIS_ACTUALS
    assert pvt.pvt_results[0]['P1']['actuals'] == EXPECTED_IRIS_ACTUALS

    for idx, filepath in enumerate(iris_data.test_sequences):
        agent.clear_wm()
        with open(filepath, 'r') as f:
            sequence = f.readlines()
        sequence = [json.loads(item) for item in sequence]

        for item in sequence[:-1]:
            agent.observe(item)

        assert agent.get_predictions() == pvt.predictions[idx]
        agent.clear_wm()

    assert pvt.pvt_results[0]['P1']['metrics'] == {'accuracy': pytest.approx(93.33333333333333),
                                                   'f1': pytest.approx(0.9655172413793104),
                                                   'false_positive': 2.0,
                                                   'precision': pytest.approx(93.33333333333333),
                                                   'response_counts': 30.0,
                                                   'response_percentage': 100.0,
                                                   'true_positive': 28.0,
                                                   'unknown_percentage': 0.0,
                                                   'predicted_class_statistics': {'versicolor': 9, 'virginica': 13, 'setosa': 8},
                                                   'training_counter': {'virginica': 37, 'versicolor': 41, 'setosa': 42},
                                                   'testing_counter': {'versicolor': 9, 'virginica': 13, 'setosa': 8},
                                                   'counter': {'virginica': 50, 'versicolor': 50, 'setosa': 50},
                                                   'true_negative': 0.0,
                                                   'false_negative': 0.0,
                                                   'FPR': pytest.approx(100.0),
                                                   'FDR': pytest.approx(6.666666666666667),
                                                   'TNR': pytest.approx(0.0),
                                                   'TPR': pytest.approx(100.0),
                                                   'NPV': pytest.approx(0.0),
                                                   'FNR': pytest.approx(0.0),
                                                   'FOR': pytest.approx(0.0),
                                                   'LR+': pytest.approx(1.0),
                                                   'LR-': pytest.approx(0.0),
                                                   'PT': pytest.approx(0.5),
                                                   'TS': pytest.approx(93.33333333333333)}
    with open(test_dir.joinpath('results/iris_testing_log.json')) as f:
        known_testing_log = json.load(f)
    assert pvt.testing_log == known_testing_log

    # get individual testing entries
    testing_records = [rec for rec in pvt.testing_log[0]
                       if rec['status'] == 'testing']
    testing_records = sorted(
        testing_records, key=lambda d: d['current_record'])

    # for each testing record, ensure that the running metrics are correct


# This should give identical results to above
def test_pvt_classification_filepath(setup_and_teardown):
    INGRESS_NODES = ["P1"]
    QUERY_NODES = ["P1"]
    CLASSIFICATION_DATASET_PATH = str(
        test_dir.joinpath('./datasets/shuffled_iris_flowers'))
    PCT_CHOSEN = 100
    PCT_TRAINING = 80

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}
    agent.set_summarize_for_single_node(False)
    agent.clear_all_memory()

    assert agent.change_genes({'recall_threshold': 0.1}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'max_predictions': 5}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'near_vector_count': 3}) == {
        'P1': 'updated-genes'}

    pvt = PerformanceValidationTest(agent=agent,
                                    ingress_nodes=INGRESS_NODES,
                                    query_nodes=QUERY_NODES,
                                    test_count=1,
                                    dataset_percentage=PCT_CHOSEN,
                                    training_percentage=PCT_TRAINING,
                                    test_type='classification',
                                    dataset=CLASSIFICATION_DATASET_PATH,
                                    test_prediction_strategy='noncontinuous',
                                    clear_all_memory_before_training=True,
                                    turn_prediction_off_during_training=False,
                                    shuffle=False,
                                    QUIET=False)
    pvt.prepare_datasets()

    # verify that the train and test sequences are exactly as we expect (no shuffle)
    assert [os.path.basename(item) for item in pvt.dataset.train_sequences] == ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55',
                                                                                '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119']
    assert [os.path.basename(item) for item in pvt.dataset.test_sequences] == ['120', '121', '122', '123', '124', '125', '126', '127', '128', '129',
                                                                               '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149']

    pvt.conduct_pvt()
    with open(test_dir.joinpath('results/iris_prediction_log.json')) as f:
        assert pvt.predictions == json.load(f)

    assert pvt.actuals == EXPECTED_IRIS_ACTUALS
    assert pvt.pvt_results[0]['P1']['actuals'] == EXPECTED_IRIS_ACTUALS

    for idx, filepath in enumerate(pvt.dataset.test_sequences):
        agent.clear_wm()
        with open(filepath, 'r') as f:
            sequence = f.readlines()
        sequence = [json.loads(item) for item in sequence]

        for item in sequence[:-1]:
            agent.observe(item)

        assert agent.get_predictions() == pvt.predictions[idx]
        agent.clear_wm()

    assert pvt.pvt_results[0]['P1']['metrics'] == {'accuracy': pytest.approx(93.33333333333333),
                                                   'f1': pytest.approx(0.9655172413793104),
                                                   'false_positive': 2.0,
                                                   'precision': pytest.approx(93.33333333333333),
                                                   'response_counts': 30.0,
                                                   'response_percentage': 100.0,
                                                   'true_positive': 28.0,
                                                   'unknown_percentage': 0.0,
                                                   'predicted_class_statistics': {'versicolor': 9, 'virginica': 13, 'setosa': 8},
                                                   'training_counter': {'virginica': 37, 'versicolor': 41, 'setosa': 42},
                                                   'testing_counter': {'versicolor': 9, 'virginica': 13, 'setosa': 8},
                                                   'counter': {'virginica': 50, 'versicolor': 50, 'setosa': 50},
                                                   'true_negative': 0.0,
                                                   'false_negative': 0.0,
                                                   'FPR': pytest.approx(100.0),
                                                   'FDR': pytest.approx(6.666666666666667),
                                                   'TNR': pytest.approx(0.0),
                                                   'TPR': pytest.approx(100.0),
                                                   'NPV': pytest.approx(0.0),
                                                   'FNR': pytest.approx(0.0),
                                                   'FOR': pytest.approx(0.0),
                                                   'LR+': pytest.approx(1.0),
                                                   'LR-': pytest.approx(0.0),
                                                   'PT': pytest.approx(0.5),
                                                   'TS': pytest.approx(93.33333333333333)}

    with open(test_dir.joinpath('results/iris_testing_log.json')) as f:
        known_testing_log = json.load(f)
    assert pvt.testing_log == known_testing_log

    # get individual testing entries
    testing_records = [rec for rec in pvt.testing_log[0]
                       if rec['status'] == 'testing']
    testing_records = sorted(
        testing_records, key=lambda d: d['current_record'])

    # for each testing record, ensure that the running metrics are correct

def test_pvt_classification_pathlib(setup_and_teardown):
    INGRESS_NODES = ["P1"]
    QUERY_NODES = ["P1"]
    CLASSIFICATION_DATASET_PATH = test_dir.joinpath('./datasets/shuffled_iris_flowers')
    PCT_CHOSEN = 100
    PCT_TRAINING = 80

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}
    agent.set_summarize_for_single_node(False)
    agent.clear_all_memory()

    assert agent.change_genes({'recall_threshold': 0.1}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'max_predictions': 5}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'near_vector_count': 3}) == {
        'P1': 'updated-genes'}

    pvt = PerformanceValidationTest(agent=agent,
                                    ingress_nodes=INGRESS_NODES,
                                    query_nodes=QUERY_NODES,
                                    test_count=1,
                                    dataset_percentage=PCT_CHOSEN,
                                    training_percentage=PCT_TRAINING,
                                    test_type='classification',
                                    dataset=CLASSIFICATION_DATASET_PATH,
                                    test_prediction_strategy='noncontinuous',
                                    clear_all_memory_before_training=True,
                                    turn_prediction_off_during_training=False,
                                    shuffle=False,
                                    QUIET=False)
    pvt.prepare_datasets()

    # verify that the train and test sequences are exactly as we expect (no shuffle)
    assert [os.path.basename(item) for item in pvt.dataset.train_sequences] == ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55',
                                                                                '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119']
    assert [os.path.basename(item) for item in pvt.dataset.test_sequences] == ['120', '121', '122', '123', '124', '125', '126', '127', '128', '129',
                                                                               '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149']

    pvt.conduct_pvt()
    with open(test_dir.joinpath('results/iris_prediction_log.json')) as f:
        assert pvt.predictions == json.load(f)

    assert pvt.actuals == EXPECTED_IRIS_ACTUALS
    assert pvt.pvt_results[0]['P1']['actuals'] == EXPECTED_IRIS_ACTUALS

    for idx, filepath in enumerate(pvt.dataset.test_sequences):
        agent.clear_wm()
        with open(filepath, 'r') as f:
            sequence = f.readlines()
        sequence = [json.loads(item) for item in sequence]

        for item in sequence[:-1]:
            agent.observe(item)

        assert agent.get_predictions() == pvt.predictions[idx]
        agent.clear_wm()

    assert pvt.pvt_results[0]['P1']['metrics'] == {'accuracy': pytest.approx(93.33333333333333),
                                                   'f1': pytest.approx(0.9655172413793104),
                                                   'false_positive': 2.0,
                                                   'precision': pytest.approx(93.33333333333333),
                                                   'response_counts': 30.0,
                                                   'response_percentage': 100.0,
                                                   'true_positive': 28.0,
                                                   'unknown_percentage': 0.0,
                                                   'predicted_class_statistics': {'versicolor': 9, 'virginica': 13, 'setosa': 8},
                                                   'training_counter': {'virginica': 37, 'versicolor': 41, 'setosa': 42},
                                                   'testing_counter': {'versicolor': 9, 'virginica': 13, 'setosa': 8},
                                                   'counter': {'virginica': 50, 'versicolor': 50, 'setosa': 50},
                                                   'true_negative': 0.0,
                                                   'false_negative': 0.0,
                                                   'FPR': pytest.approx(100.0),
                                                   'FDR': pytest.approx(6.666666666666667),
                                                   'TNR': pytest.approx(0.0),
                                                   'TPR': pytest.approx(100.0),
                                                   'NPV': pytest.approx(0.0),
                                                   'FNR': pytest.approx(0.0),
                                                   'FOR': pytest.approx(0.0),
                                                   'LR+': pytest.approx(1.0),
                                                   'LR-': pytest.approx(0.0),
                                                   'PT': pytest.approx(0.5),
                                                   'TS': pytest.approx(93.33333333333333)}

    with open(test_dir.joinpath('results/iris_testing_log.json')) as f:
        known_testing_log = json.load(f)
    assert pvt.testing_log == known_testing_log

    # get individual testing entries
    testing_records = [rec for rec in pvt.testing_log[0]
                       if rec['status'] == 'testing']
    testing_records = sorted(
        testing_records, key=lambda d: d['current_record'])

    # for each testing record, ensure that the running metrics are correct



EXPECTED_COLORS_PREDS = [{'P1': None},
                         {'P1': 'red'},
                         {'P1': None},
                         {'P1': 'red'},
                         {'P1': None},
                         {'P1': 'orange'}]
EXPECTED_COLORS_ACTUALS = [['orange'],
                           ['red'],
                           ['blue'],
                           ['red'],
                           ['blue'],
                           ['blue']]


def test_pvt_colors_filepath(setup_and_teardown):
    INGRESS_NODES = ["P1"]
    QUERY_NODES = ["P1"]
    CLASSIFICATION_DATASET_PATH = str(
        test_dir.joinpath('./datasets/shuffled_dummy_colors'))
    PCT_CHOSEN = 100
    PCT_TRAINING = 80

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}
    agent.set_summarize_for_single_node(False)
    agent.clear_all_memory()

    assert agent.change_genes({'recall_threshold': 0.1}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'max_predictions': 5}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'near_vector_count': 3}) == {
        'P1': 'updated-genes'}

    data = Data(data_directories=[CLASSIFICATION_DATASET_PATH])
    data.prep(percent_of_dataset_chosen=PCT_CHOSEN,
              percent_reserved_for_training=PCT_TRAINING,
              shuffle=False)

    # verify that the train and test sequences are exactly as we expect (no shuffle)
    assert [os.path.basename(item) for item in data.train_sequences] == ['0', '1', '2', '3', '4', '5',
                                                                         '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']
    assert [os.path.basename(item) for item in data.test_sequences] == [
        '22', '23', '24', '25', '26', '27']

    pvt = PerformanceValidationTest(agent=agent,
                                    ingress_nodes=INGRESS_NODES,
                                    query_nodes=QUERY_NODES,
                                    test_count=1,
                                    dataset_percentage=PCT_CHOSEN,
                                    training_percentage=PCT_TRAINING,
                                    test_type='classification',
                                    dataset=data,
                                    test_prediction_strategy='noncontinuous',
                                    clear_all_memory_before_training=True,
                                    turn_prediction_off_during_training=True,
                                    shuffle=False,
                                    QUIET=True)

    pvt.conduct_pvt()

    with open(test_dir.joinpath('results/colors_prediction_log.json')) as f:
        assert pvt.predictions == json.load(f)

    predicted_vals = []

    for preds in pvt.predictions:
        preds_dict = {k: prediction_ensemble_model_classification(
            preds[k]) for k in preds}
        for k in preds_dict.keys():
            if preds_dict[k] is not None:
                preds_dict[k] = preds_dict[k].most_common()[0][0]

        predicted_vals.append(preds_dict)

    assert predicted_vals == EXPECTED_COLORS_PREDS

    assert pvt.actuals == EXPECTED_COLORS_ACTUALS
    assert pvt.pvt_results[0]['P1']['actuals'] == EXPECTED_COLORS_ACTUALS

    for idx, filepath in enumerate(data.test_sequences):
        agent.clear_wm()
        with open(filepath, 'r') as f:
            sequence = f.readlines()
        sequence = [json.loads(item) for item in sequence]

        for item in sequence[:-1]:
            agent.observe(item)

        assert agent.get_predictions() == pvt.predictions[idx]
        agent.clear_wm()

    assert pvt.pvt_results[0]['P1']['metrics'] == {'accuracy': pytest.approx(33.33333333333333),
                                                   'f1': pytest.approx(0.8),
                                                   'false_positive': 1.0,
                                                   'precision': pytest.approx(66.66666666666666),
                                                   'response_counts': 3.0,
                                                   'response_percentage': 50.0,
                                                   'true_positive': 2.0,
                                                   'unknown_percentage': 50.0,
                                                   'predicted_class_statistics': {'null': 3, 'red': 2, 'orange': 1},
                                                   'training_counter': {'blue': 2, 'green': 7, 'orange': 9, 'red': 4},
                                                   'testing_counter': {'orange': 1, 'red': 2, 'blue': 3},
                                                   'counter': {'blue': 5, 'green': 7, 'orange': 10, 'red': 6},
                                                   'true_negative': 0.0,
                                                   'false_negative': 0.0,
                                                   'FPR': pytest.approx(100.0),
                                                   'FDR': pytest.approx(33.333333333333336),
                                                   'TNR': pytest.approx(0.0),
                                                   'TPR': pytest.approx(100.0),
                                                   'NPV': pytest.approx(0.0),
                                                   'FNR': pytest.approx(0.0),
                                                   'FOR': pytest.approx(0.0),
                                                   'LR+': pytest.approx(1.0),
                                                   'LR-': pytest.approx(0.0),
                                                   'PT': pytest.approx(0.5),
                                                   'TS': pytest.approx(66.66666666666667)}

    with open(test_dir.joinpath('results/colors_testing_log.json')) as f:
        known_testing_log = json.load(f)
    assert pvt.testing_log == known_testing_log

    # get individual testing entries
    testing_records = [rec for rec in pvt.testing_log[0]
                       if rec['status'] == 'testing']
    testing_records = sorted(
        testing_records, key=lambda d: d['current_record'])

    # for each testing record, ensure that the running metrics are correct


# getting setup to test mongodb connections for pvt (as used on brainiac to store results)
def test_mongodb_upload(setup_and_teardown_with_mongo):
    """Testing our mongodb upload and retrieval functions to ensure our shuffled dataset locally
    is retrieved in specifically the same order we have it locally. Spawns an agent and a mongodb container locally
    """
    INGRESS_NODES = ["P1"]
    QUERY_NODES = ["P1"]
    CLASSIFICATION_DATASET_PATH = str(
        test_dir.joinpath('./datasets/shuffled_iris_flowers'))
    PCT_CHOSEN = 100
    PCT_TRAINING = 80

    mongo = MongoClient('localhost:27017')
    mongo_db = mongo['main_db']

    dataset_details = {"user_id": "user-1234",
                       "dataset_name": "shuffled_iris",
                       "dataset_id": "iris",
                       "data_files_collection_name": "dataset_files",
                       "dataset_collection_name": "datasets"}
    MongoData.upload_dataset(mongo_db=mongo_db,
                             dataset_details=dataset_details,
                             filepath=test_dir.joinpath('datasets/shuffled_iris_flowers.zip'))
    try:
        md = MongoData(mongo_dataset_details=dataset_details,
                       data_files_collection_name=dataset_details['data_files_collection_name'],
                       dataset_collection_name=dataset_details['dataset_collection_name'],
                       mongo_db=mongo_db)
    except Exception as error:
        print(f'failed to get MongoData object: {str(error)}')
        pytest.fail(f'failed to get MongoData object: {str(error)}')

    md.prep(percent_of_dataset_chosen=PCT_CHOSEN,
            percent_reserved_for_training=PCT_TRAINING,
            shuffle=False)

    iris_data = Data(data_directories=[CLASSIFICATION_DATASET_PATH])
    iris_data.prep(percent_of_dataset_chosen=PCT_CHOSEN,
                   percent_reserved_for_training=PCT_TRAINING,
                   shuffle=False)

    mongo_train_seqs = [md.getSequence(record=seq_id)
                        for seq_id in md.train_sequences]

    file_train_seqs = []
    for rec in iris_data.train_sequences:
        with open(rec) as f:
            seq = tuple([json.loads(line) for line in f.readlines()])
        file_train_seqs.append(seq)

    assert mongo_train_seqs == file_train_seqs

    mongo_test_seqs = [md.getSequence(record=seq_id)
                       for seq_id in md.test_sequences]

    file_test_seqs = []
    for rec in iris_data.test_sequences:
        with open(rec) as f:
            seq = tuple([json.loads(line) for line in f.readlines()])
        file_test_seqs.append(seq)

    assert mongo_test_seqs == file_test_seqs

    # test deletion of dataset
    assert MongoData.delete_dataset(
        mongo_db=mongo_db, dataset_details=dataset_details) == 'deleted'

    assert MongoData.delete_dataset(
        mongo_db=mongo_db, dataset_details=dataset_details) == 'dataset-not-found'


# getting setup to test mongodb connections for pvt (as used on brainiac to store results)
def test_classification_iris_mongodb(setup_and_teardown_with_mongo):
    """Testing running test with mongodb dataset.
    Spawns an agent and a mongodb container locally
    """
    INGRESS_NODES = ["P1"]
    QUERY_NODES = ["P1"]
    CLASSIFICATION_DATASET_PATH = str(
        test_dir.joinpath('./datasets/shuffled_iris_flowers'))
    PCT_CHOSEN = 100
    PCT_TRAINING = 80

    mongo = MongoClient('localhost:27017')
    mongo_db = mongo['main_db']

    dataset_details = {"user_id": "user-1234",
                       "dataset_name": "shuffled_iris",
                       "dataset_id": "iris",
                       "data_files_collection_name": "dataset_files",
                       "dataset_collection_name": "datasets",
                       "results_collection": "tests",
                       "logs_collection": "testing_logs"
                       }
    MongoData.upload_dataset(mongo_db=mongo_db,
                             dataset_details=dataset_details,
                             filepath=test_dir.joinpath('datasets/shuffled_iris_flowers.zip'))
    try:
        md = MongoData(mongo_dataset_details=dataset_details,
                       data_files_collection_name=dataset_details['data_files_collection_name'],
                       dataset_collection_name=dataset_details['dataset_collection_name'],
                       mongo_db=mongo_db)
    except Exception as error:
        print(f'failed to get MongoData object: {str(error)}')
        pytest.fail(f'failed to get MongoData object: {str(error)}')

    md.prep(percent_of_dataset_chosen=PCT_CHOSEN,
            percent_reserved_for_training=PCT_TRAINING,
            shuffle=False)

    iris_data = Data(data_directories=[CLASSIFICATION_DATASET_PATH])
    iris_data.prep(percent_of_dataset_chosen=PCT_CHOSEN,
                   percent_reserved_for_training=PCT_TRAINING,
                   shuffle=False)

    mongo_train_seqs = [md.getSequence(record=seq_id)
                        for seq_id in md.train_sequences]

    file_train_seqs = []
    for rec in iris_data.train_sequences:
        with open(rec) as f:
            seq = tuple([json.loads(line) for line in f.readlines()])
        file_train_seqs.append(seq)

    assert mongo_train_seqs == file_train_seqs

    mongo_test_seqs = [md.getSequence(record=seq_id)
                       for seq_id in md.test_sequences]

    file_test_seqs = []
    for rec in iris_data.test_sequences:
        with open(rec) as f:
            seq = tuple([json.loads(line) for line in f.readlines()])
        file_test_seqs.append(seq)

    assert mongo_test_seqs == file_test_seqs

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}
    agent.set_summarize_for_single_node(False)
    agent.clear_all_memory()

    assert agent.change_genes({'recall_threshold': 0.1}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'max_predictions': 5}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'near_vector_count': 3}) == {
        'P1': 'updated-genes'}

    pvt = PerformanceValidationTest(agent=agent,
                                    ingress_nodes=INGRESS_NODES,
                                    query_nodes=QUERY_NODES,
                                    test_count=1,
                                    dataset_percentage=PCT_CHOSEN,
                                    training_percentage=PCT_TRAINING,
                                    test_type='classification',
                                    dataset=md,
                                    test_prediction_strategy='noncontinuous',
                                    clear_all_memory_before_training=True,
                                    turn_prediction_off_during_training=True,
                                    shuffle=False,
                                    QUIET=True,
                                    dataset_info=dataset_details,
                                    mongo_db=mongo_db)

    pvt.conduct_pvt()

    results = pvt.mongo_results.retrieveResults()

    final_results = results['final_results']
    pvt_results = final_results['metrics']['pvt_results'][0]['P1']
    actuals = pvt_results['actuals']
    predictions = pvt_results['predictions']
    p1_metrics = pvt_results['metrics']

    # ensure results saved in mongo are the same recorded by PVT
    assert actuals == pvt.pvt_results[0]['P1']['actuals']
    assert predictions == pvt.pvt_results[0]['P1']['predictions']
    assert p1_metrics == pvt.pvt_results[0]['P1']['metrics']

    # ensure results are same as expected results
    assert actuals == EXPECTED_IRIS_ACTUALS
    for i, pred in enumerate(EXPECTED_IRIS_PREDS):
        assert predictions[i] == pred['P1']
    assert p1_metrics == {'accuracy': pytest.approx(93.33333333333333),
                          'f1': pytest.approx(0.9655172413793104),
                          'false_positive': 2.0,
                          'precision': pytest.approx(93.33333333333333),
                          'response_counts': 30.0,
                          'response_percentage': 100.0,
                          'true_positive': 28.0,
                          'unknown_percentage': 0.0,
                          'predicted_class_statistics': {'versicolor': 9, 'virginica': 13, 'setosa': 8},
                          'training_counter': {'virginica': 37, 'versicolor': 41, 'setosa': 42},
                          'testing_counter': {'versicolor': 9, 'virginica': 13, 'setosa': 8},
                          'counter': {'virginica': 50, 'versicolor': 50, 'setosa': 50},
                          'true_negative': 0.0,
                          'false_negative': 0.0,
                          'FPR': pytest.approx(100.0),
                          'FDR': pytest.approx(6.666666666666667),
                          'TNR': pytest.approx(0.0),
                          'TPR': pytest.approx(100.0),
                          'NPV': pytest.approx(0.0),
                          'FNR': pytest.approx(0.0),
                          'FOR': pytest.approx(0.0),
                          'LR+': pytest.approx(1.0),
                          'LR-': pytest.approx(0.0),
                          'PT': pytest.approx(0.5),
                          'TS': pytest.approx(93.33333333333333)}

    # assert final_result == {}
    delete_result = pvt.mongo_results.deleteResults()
    assert 'status' in delete_result
    assert delete_result['status'] == 'deleted'

    # test deletion of dataset
    assert MongoData.delete_dataset(
        mongo_db=mongo_db, dataset_details=dataset_details) == 'deleted'


def test_classification_iris_mongodb_continuous(setup_and_teardown_with_mongo):
    """Testing running test with mongodb dataset.
    Spawns an agent and a mongodb container locally
    """
    INGRESS_NODES = ["P1"]
    QUERY_NODES = ["P1"]
    CLASSIFICATION_DATASET_PATH = str(
        test_dir.joinpath('./datasets/shuffled_iris_flowers'))
    PCT_CHOSEN = 100
    PCT_TRAINING = 80

    mongo = MongoClient('localhost:27017')
    mongo_db = mongo['main_db']

    dataset_details = {"user_id": "user-1234",
                       "dataset_name": "shuffled_iris",
                       "dataset_id": "iris",
                       "data_files_collection_name": "dataset_files",
                       "dataset_collection_name": "datasets",
                       "results_collection": "tests",
                       "logs_collection": "testing_logs"
                       }
    MongoData.upload_dataset(mongo_db=mongo_db,
                             dataset_details=dataset_details,
                             filepath=test_dir.joinpath('datasets/shuffled_iris_flowers.zip'))
    try:
        md = MongoData(mongo_dataset_details=dataset_details,
                       data_files_collection_name=dataset_details['data_files_collection_name'],
                       dataset_collection_name=dataset_details['dataset_collection_name'],
                       mongo_db=mongo_db)
    except Exception as error:
        print(f'failed to get MongoData object: {str(error)}')
        pytest.fail(f'failed to get MongoData object: {str(error)}')

    md.prep(percent_of_dataset_chosen=PCT_CHOSEN,
            percent_reserved_for_training=PCT_TRAINING,
            shuffle=False)

    iris_data = Data(data_directories=[CLASSIFICATION_DATASET_PATH])
    iris_data.prep(percent_of_dataset_chosen=PCT_CHOSEN,
                   percent_reserved_for_training=PCT_TRAINING,
                   shuffle=False)

    mongo_train_seqs = [md.getSequence(record=seq_id)
                        for seq_id in md.train_sequences]

    file_train_seqs = []
    for rec in iris_data.train_sequences:
        with open(rec) as f:
            seq = tuple([json.loads(line) for line in f.readlines()])
        file_train_seqs.append(seq)

    assert mongo_train_seqs == file_train_seqs

    mongo_test_seqs = [md.getSequence(record=seq_id)
                       for seq_id in md.test_sequences]

    file_test_seqs = []
    for rec in iris_data.test_sequences:
        with open(rec) as f:
            seq = tuple([json.loads(line) for line in f.readlines()])
        file_test_seqs.append(seq)

    assert mongo_test_seqs == file_test_seqs

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}
    agent.set_summarize_for_single_node(False)
    agent.clear_all_memory()

    assert agent.change_genes({'recall_threshold': 0.1}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'max_predictions': 5}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'near_vector_count': 3}) == {
        'P1': 'updated-genes'}

    pvt = PerformanceValidationTest(agent=agent,
                                    ingress_nodes=INGRESS_NODES,
                                    query_nodes=QUERY_NODES,
                                    test_count=1,
                                    dataset_percentage=PCT_CHOSEN,
                                    training_percentage=PCT_TRAINING,
                                    test_type='classification',
                                    dataset=md,
                                    test_prediction_strategy='continuous',
                                    clear_all_memory_before_training=True,
                                    turn_prediction_off_during_training=True,
                                    shuffle=False,
                                    QUIET=True,
                                    dataset_info=dataset_details,
                                    mongo_db=mongo_db)

    pvt.conduct_pvt()

    results = pvt.mongo_results.retrieveResults()

    final_results = results['final_results']
    pvt_results = final_results['metrics']['pvt_results'][0]['P1']
    actuals = pvt_results['actuals']
    predictions = pvt_results['predictions']
    p1_metrics = pvt_results['metrics']

    assert actuals == pvt.pvt_results[0]['P1']['actuals']
    assert predictions == pvt.pvt_results[0]['P1']['predictions']
    assert p1_metrics == pvt.pvt_results[0]['P1']['metrics']

    assert p1_metrics == {'accuracy': pytest.approx(93.33333333333333),
                          'f1': pytest.approx(0.9655172413793104),
                          'false_positive': 2.0,
                          'precision': pytest.approx(93.33333333333333),
                          'response_counts': 30.0,
                          'response_percentage': 100.0,
                          'true_positive': 28.0,
                          'unknown_percentage': 0.0,
                          'predicted_class_statistics': {'versicolor': 9, 'virginica': 13, 'setosa': 8},
                          'training_counter': {'virginica': 37, 'versicolor': 41, 'setosa': 42},
                          'testing_counter': {'versicolor': 9, 'virginica': 13, 'setosa': 8},
                          'counter': {'virginica': 50, 'versicolor': 50, 'setosa': 50},
                          'true_negative': 0.0,
                          'false_negative': 0.0,
                          'FPR': pytest.approx(100.0),
                          'FDR': pytest.approx(6.666666666666667),
                          'TNR': pytest.approx(0.0),
                          'TPR': pytest.approx(100.0),
                          'NPV': pytest.approx(0.0),
                          'FNR': pytest.approx(0.0),
                          'FOR': pytest.approx(0.0),
                          'LR+': pytest.approx(1.0),
                          'LR-': pytest.approx(0.0),
                          'PT': pytest.approx(0.5),
                          'TS': pytest.approx(93.33333333333333)}

    # ensure results are same as expected results
    with open(test_dir.joinpath('results/iris_continuous_prediction_log.json')) as f:
        assert pvt.predictions == json.load(f)
    with open(test_dir.joinpath('results/iris_continuous_testing_log.json')) as f:
        known_testing_log = json.load(f)
    assert pvt.testing_log == known_testing_log

    # assert final_result == {}
    delete_result = pvt.mongo_results.deleteResults()
    assert 'status' in delete_result
    assert delete_result['status'] == 'deleted'

    # test deletion of dataset
    assert MongoData.delete_dataset(
        mongo_db=mongo_db, dataset_details=dataset_details) == 'deleted'


EXPECTED_BHP_ACTUALS = [{'utility': 14400},
                        {'utility': 24500},
                        {'utility': 13500},
                        {'utility': 19900},
                        {'utility': 36200},
                        {'utility': 18500},
                        {'utility': 22200},
                        {'utility': 42300},
                        {'utility': 31500},
                        {'utility': 36100},
                        {'utility': 27900},
                        {'utility': 14900},
                        {'utility': 16600},
                        {'utility': 17700},
                        {'utility': 20200},
                        {'utility': 28600},
                        {'utility': 12700},
                        {'utility': 20600},
                        {'utility': 16500},
                        {'utility': 20400},
                        {'utility': 19600},
                        {'utility': 42800},
                        {'utility': 20600},
                        {'utility': 28500},
                        {'utility': 22600},
                        {'utility': 5000},
                        {'utility': 23400},
                        {'utility': 20800},
                        {'utility': 18400},
                        {'utility': 31100},
                        {'utility': 28400},
                        {'utility': 21500},
                        {'utility': 10800},
                        {'utility': 19300},
                        {'utility': 20200},
                        {'utility': 17800},
                        {'utility': 13100},
                        {'utility': 31600},
                        {'utility': 31200},
                        {'utility': 17400},
                        {'utility': 33100},
                        {'utility': 23500},
                        {'utility': 17600},
                        {'utility': 22200},
                        {'utility': 15600},
                        {'utility': 33100},
                        {'utility': 18900},
                        {'utility': 10200},
                        {'utility': 48800},
                        {'utility': 8700},
                        {'utility': 18800},
                        {'utility': 13100},
                        {'utility': 37000},
                        {'utility': 14100},
                        {'utility': 24700},
                        {'utility': 19300},
                        {'utility': 20100},
                        {'utility': 22200},
                        {'utility': 18500},
                        {'utility': 20300},
                        {'utility': 10200},
                        {'utility': 50000},
                        {'utility': 7200},
                        {'utility': 21600},
                        {'utility': 8800},
                        {'utility': 33200},
                        {'utility': 22000},
                        {'utility': 17900},
                        {'utility': 14300},
                        {'utility': 20300},
                        {'utility': 14500},
                        {'utility': 32900},
                        {'utility': 26200},
                        {'utility': 11000},
                        {'utility': 23000},
                        {'utility': 20100},
                        {'utility': 35400},
                        {'utility': 22500},
                        {'utility': 13400},
                        {'utility': 50000},
                        {'utility': 11900},
                        {'utility': 22700},
                        {'utility': 25000},
                        {'utility': 21400},
                        {'utility': 34600},
                        {'utility': 24800},
                        {'utility': 22800},
                        {'utility': 9700},
                        {'utility': 24200},
                        {'utility': 19400},
                        {'utility': 23700},
                        {'utility': 26700},
                        {'utility': 33300},
                        {'utility': 13800},
                        {'utility': 31700},
                        {'utility': 23200},
                        {'utility': 29000},
                        {'utility': 20600},
                        {'utility': 7000},
                        {'utility': 29400},
                        {'utility': 14200},
                        {'utility': 21700}]

EXPECTED_BHP_PREDS = [{'P1': {'utility': 25340.625917931517}},
                      {'P1': {'utility': 23759.417057420178}},
                      {'P1': {'utility': 20950.59768679089}},
                      {'P1': {'utility': 28683.233152673693}},
                      {'P1': {'utility': 25340.625977801064}},
                      {'P1': {'utility': 24906.249969892444}},
                      {'P1': {'utility': 23493.643844794526}},
                      {'P1': {'utility': 37778.85949597406}},
                      {'P1': {'utility': 43071.35023992657}},
                      {'P1': {'utility': 26370.58565859952}},
                      {'P1': {'utility': 28791.340598990908}},
                      {'P1': {'utility': 11531.25001281731}},
                      {'P1': {'utility': 19420.567480848465}},
                      {'P1': {'utility': 13737.5000103401}},
                      {'P1': {'utility': 13737.500010340136}},
                      {'P1': {'utility': 25340.625914855493}},
                      {'P1': {'utility': 13737.500010340063}},
                      {'P1': {'utility': 25126.563882047853}},
                      {'P1': {'utility': 21171.79821987763}},
                      {'P1': {'utility': 25140.626029251845}},
                      {'P1': {'utility': 18288.370275870682}},
                      {'P1': {'utility': 22630.879739943608}},
                      {'P1': {'utility': 25340.627392781833}},
                      {'P1': {'utility': 28791.341360681505}},
                      {'P1': {'utility': 19473.18294101185}},
                      {'P1': {'utility': 20980.978931918045}},
                      {'P1': {'utility': 24798.278840399158}},
                      {'P1': {'utility': 19094.85068601992}},
                      {'P1': {'utility': 17402.73435830852}},
                      {'P1': {'utility': 26557.57504411349}},
                      {'P1': {'utility': 27996.184806415622}},
                      {'P1': {'utility': 15637.040276212825}},
                      {'P1': {'utility': 12384.944054810974}},
                      {'P1': {'utility': 23175.013428353337}},
                      {'P1': {'utility': 21554.52075883596}},
                      {'P1': {'utility': 17406.24999831239}},
                      {'P1': {'utility': 15637.040276271851}},
                      {'P1': {'utility': 41822.018078179586}},
                      {'P1': {'utility': 24633.158139848536}},
                      {'P1': {'utility': 23467.257114605727}},
                      {'P1': {'utility': 24868.376439948657}},
                      {'P1': {'utility': 25340.627392910206}},
                      {'P1': {'utility': 24906.249969892753}},
                      {'P1': {'utility': 23498.67921973088}},
                      {'P1': {'utility': 17266.34230792101}},
                      {'P1': {'utility': 30373.73556279551}},
                      {'P1': {'utility': 21171.81785086767}},
                      {'P1': {'utility': 12849.614247346568}},
                      {'P1': {'utility': 34306.25}},
                      {'P1': {'utility': 14872.993676825832}},
                      {'P1': {'utility': 21200.0}},
                      {'P1': {'utility': 21452.0545093898}},
                      {'P1': {'utility': 33876.67162238447}},
                      {'P1': {'utility': 14556.281380747147}},
                      {'P1': {'utility': 25340.628523950672}},
                      {'P1': {'utility': 22788.392481945924}},
                      {'P1': {'utility': 21148.676450337087}},
                      {'P1': {'utility': 25745.318194405805}},
                      {'P1': {'utility': 23215.724949511707}},
                      {'P1': {'utility': 17406.249998312393}},
                      {'P1': {'utility': 15509.876524982774}},
                      {'P1': {'utility': 21428.811613396178}},
                      {'P1': {'utility': 8913.182331095319}},
                      {'P1': {'utility': 17406.24999831239}},
                      {'P1': {'utility': 11628.653220111488}},
                      {'P1': {'utility': 29246.319694234033}},
                      {'P1': {'utility': 25809.03713048586}},
                      {'P1': {'utility': 17552.909560193493}},
                      {'P1': {'utility': 13737.500010340063}},
                      {'P1': {'utility': 23626.322300306594}},
                      {'P1': {'utility': 20977.075952159517}},
                      {'P1': {'utility': 34830.490934946756}},
                      {'P1': {'utility': 25049.54959152978}},
                      {'P1': {'utility': 9717.600003507278}},
                      {'P1': {'utility': 17299.66983876879}},
                      {'P1': {'utility': 23009.76966655978}},
                      {'P1': {'utility': 27098.235570850677}},
                      {'P1': {'utility': 26103.217296110703}},
                      {'P1': {'utility': 14900.000031161508}},
                      {'P1': {'utility': 33306.51464823035}},
                      {'P1': {'utility': 31344.285757009955}},
                      {'P1': {'utility': 18713.14611682356}},
                      {'P1': {'utility': 20051.964119771288}},
                      {'P1': {'utility': 27805.7755936635}},
                      {'P1': {'utility': 25642.590420385877}},
                      {'P1': {'utility': 26103.217296110703}},
                      {'P1': {'utility': 34306.24999999999}},
                      {'P1': {'utility': 25340.62590320907}},
                      {'P1': {'utility': 23988.92035403769}},
                      {'P1': {'utility': 25340.627392910206}},
                      {'P1': {'utility': 23385.84026047572}},
                      {'P1': {'utility': 19600.0}},
                      {'P1': {'utility': 25340.628286049017}},
                      {'P1': {'utility': 25340.625900205752}},
                      {'P1': {'utility': 33804.4903640866}},
                      {'P1': {'utility': 11628.653220111488}},
                      {'P1': {'utility': 19600.0}},
                      {'P1': {'utility': 19738.760238104107}},
                      {'P1': {'utility': 14588.319819086948}},
                      {'P1': {'utility': 24940.740749814155}},
                      {'P1': {'utility': 20263.602873604792}},
                      {'P1': {'utility': 21171.818695636106}}]


def test_emotive_value_pvt(setup_and_teardown, tmp_path):
    """Test basic emotive value pvt on pre-shuffled dataset

    """

    INGRESS_NODES = ["P1"]
    QUERY_NODES = ["P1"]
    EMOTIVE_VALUE_DATASET_PATH = str(
        test_dir.joinpath('./datasets/shuffled_bhp'))
    PCT_CHOSEN = 100
    PCT_TRAINING = 80

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}
    agent.set_summarize_for_single_node(False)
    agent.clear_all_memory()

    assert agent.change_genes({'recall_threshold': 0.1}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'max_predictions': 5}) == {
        'P1': 'updated-genes'}

    bhp_data = Data(data_directories=[EMOTIVE_VALUE_DATASET_PATH])
    bhp_data.prep(percent_of_dataset_chosen=PCT_CHOSEN,
                  percent_reserved_for_training=PCT_TRAINING,
                  shuffle=False)

    # verify that the train and test sequences are exactly as we expect (no shuffle)
    assert [os.path.basename(item) for item in bhp_data.train_sequences] == ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125', '126', '127', '128', '129', '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149', '150', '151', '152', '153', '154', '155', '156', '157', '158', '159', '160', '161', '162', '163', '164', '165', '166', '167', '168', '169', '170', '171', '172', '173', '174', '175', '176', '177', '178', '179', '180', '181', '182', '183', '184', '185', '186', '187', '188', '189', '190', '191', '192', '193', '194', '195', '196', '197', '198', '199', '200', '201', '202', '203', '204',
                                                                             '205', '206', '207', '208', '209', '210', '211', '212', '213', '214', '215', '216', '217', '218', '219', '220', '221', '222', '223', '224', '225', '226', '227', '228', '229', '230', '231', '232', '233', '234', '235', '236', '237', '238', '239', '240', '241', '242', '243', '244', '245', '246', '247', '248', '249', '250', '251', '252', '253', '254', '255', '256', '257', '258', '259', '260', '261', '262', '263', '264', '265', '266', '267', '268', '269', '270', '271', '272', '273', '274', '275', '276', '277', '278', '279', '280', '281', '282', '283', '284', '285', '286', '287', '288', '289', '290', '291', '292', '293', '294', '295', '296', '297', '298', '299', '300', '301', '302', '303', '304', '305', '306', '307', '308', '309', '310', '311', '312', '313', '314', '315', '316', '317', '318', '319', '320', '321', '322', '323', '324', '325', '326', '327', '328', '329', '330', '331', '332', '333', '334', '335', '336', '337', '338', '339', '340', '341', '342', '343', '344', '345', '346', '347', '348', '349', '350', '351', '352', '353', '354', '355', '356', '357', '358', '359', '360', '361', '362', '363', '364', '365', '366', '367', '368', '369', '370', '371', '372', '373', '374', '375', '376', '377', '378', '379', '380', '381', '382', '383', '384', '385', '386', '387', '388', '389', '390', '391', '392', '393', '394', '395', '396', '397', '398', '399', '400', '401', '402', '403']
    assert [os.path.basename(item) for item in bhp_data.test_sequences] == ['404', '405', '406', '407', '408', '409', '410', '411', '412', '413', '414', '415', '416', '417', '418', '419', '420', '421', '422', '423', '424', '425', '426', '427', '428', '429', '430', '431', '432', '433', '434', '435', '436', '437', '438', '439', '440', '441', '442', '443', '444', '445', '446', '447', '448', '449',
                                                                            '450', '451', '452', '453', '454', '455', '456', '457', '458', '459', '460', '461', '462', '463', '464', '465', '466', '467', '468', '469', '470', '471', '472', '473', '474', '475', '476', '477', '478', '479', '480', '481', '482', '483', '484', '485', '486', '487', '488', '489', '490', '491', '492', '493', '494', '495', '496', '497', '498', '499', '500', '501', '502', '503', '504', '505']
    pvt = PerformanceValidationTest(agent=agent,
                                    ingress_nodes=INGRESS_NODES,
                                    query_nodes=QUERY_NODES,
                                    test_count=1,
                                    dataset_percentage=PCT_CHOSEN,
                                    training_percentage=PCT_TRAINING,
                                    test_type='emotives_value',
                                    results_filepath=tmp_path,
                                    dataset=bhp_data,
                                    test_prediction_strategy='noncontinuous',
                                    clear_all_memory_before_training=True,
                                    turn_prediction_off_during_training=True,
                                    shuffle=False,
                                    QUIET=True)

    pvt.conduct_pvt()
    with open(test_dir.joinpath('results/bhp_prediction_log.json')) as f:
        assert pvt.predictions == json.load(f)

    predicted_vals = []

    for i, preds in enumerate(pvt.predictions):
        pred_dict = {node: pvt.predictions[i][node]
                     for node in pvt.query_nodes}
        for key in pred_dict:
            pred_dict[key] = prediction_ensemble_modeled_emotives(
                pred_dict[key])
        predicted_vals.append(pred_dict)

    assert predicted_vals == EXPECTED_BHP_PREDS

    assert pvt.actuals == EXPECTED_BHP_ACTUALS
    assert pvt.pvt_results[0]['P1']['utility']['actuals'] == [
        actual['utility'] for actual in EXPECTED_BHP_ACTUALS]

    for idx, filepath in enumerate(bhp_data.test_sequences):
        agent.clear_wm()
        with open(filepath, 'r') as f:
            sequence = f.readlines()
        sequence = [json.loads(item) for item in sequence]

        for item in sequence:
            agent.observe(item)

        assert agent.get_predictions() == pvt.predictions[idx]
        agent.clear_wm()

    assert pvt.pvt_results[0]['P1']['utility']['metrics'] == {'response_counts': 102.0,
                                                              'response_percentage': 100.0,
                                                              'unknown_percentage': 0.0,
                                                              'counter': 506,
                                                              'training_counter': 404,
                                                              'testing_counter': 102,
                                                              'rmse': pytest.approx(7162.839400021328),
                                                              'smape': pytest.approx(23.705771744246748),
                                                              '1-smape': pytest.approx(76.29422825575325)}

    with open(test_dir.joinpath('results/bhp_testing_log.json')) as f:
        known_testing_log = json.load(f)
    assert pvt.testing_log == known_testing_log

    # get individual testing entries
    testing_records = [rec for rec in pvt.testing_log[0]
                       if rec['status'] == 'testing']
    testing_records = sorted(
        testing_records, key=lambda d: d['current_record'])

    # for each testing record, ensure that the running metrics are correct


EXPECTED_HR_PREDS = [{'P1': {'utility': 100.0}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 17.45369256175329}},
                     {'P1': {'utility': 3.8841428556438515}},
                     {'P1': {'utility': -30.210609106850267}},
                     {'P1': {'utility': 74.48828136039513}},
                     {'P1': {'utility': -100.0}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 18.07123235771467}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 79.55643806170767}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': -100.0}},
                     {'P1': {'utility': 79.58958947726471}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': -41.4498441955313}},
                     {'P1': {'utility': 21.905216964943314}},
                     {'P1': {'utility': 30.191932271004923}},
                     {'P1': {'utility': 54.18341322040904}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': -32.90516032162435}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 79.591556566356}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': -21.922949996741604}},
                     {'P1': {'utility': 61.14828895622607}},
                     {'P1': {'utility': 68.69788387856018}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': -20.602838823576683}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 4.719881787274794}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': -100.0}},
                     {'P1': {'utility': -100.0}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': -60.01760110059407}},
                     {'P1': {'utility': -100.0}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 68.82815256804831}},
                     {'P1': {'utility': 17.484756367318443}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 73.7553070632366}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 22.328422143042303}},
                     {'P1': {'utility': 74.65142058463772}},
                     {'P1': {'utility': -2.9822958201428413}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 100.0}},
                     {'P1': {'utility': 100.0}}]


EXPECTED_HR_ACTUALS = [{'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': -100},
                       {'utility': 100},
                       {'utility': -100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': -100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': -100},
                       {'utility': -100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': -100},
                       {'utility': -100},
                       {'utility': 100},
                       {'utility': -100},
                       {'utility': 100},
                       {'utility': -100},
                       {'utility': -100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': -100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': -100},
                       {'utility': -100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': -100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': -100},
                       {'utility': 100},
                       {'utility': 100},
                       {'utility': 100}]


def test_emotive_polarity_pvt(setup_and_teardown):
    """Test basic emotive value pvt on pre-shuffled dataset

    """

    INGRESS_NODES = ["P1"]
    QUERY_NODES = ["P1"]
    EMOTIVE_POLARITY_DATASET_PATH = str(
        test_dir.joinpath('./datasets/shuffled_hr_attrition'))
    PCT_CHOSEN = 2
    PCT_TRAINING = 80

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}
    agent.set_summarize_for_single_node(False)
    agent.clear_all_memory()

    assert agent.change_genes({'recall_threshold': 0.1}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'max_predictions': 5}) == {
        'P1': 'updated-genes'}

    hr_data = Data(data_directories=[EMOTIVE_POLARITY_DATASET_PATH])
    hr_data.prep(percent_of_dataset_chosen=PCT_CHOSEN,
                 percent_reserved_for_training=PCT_TRAINING,
                 shuffle=False)

    # verify that the train and test sequences are exactly as we expect (no shuffle)
    assert [os.path.basename(item) for item in hr_data.train_sequences] == ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121',
                                                                            '122', '123', '124', '125', '126', '127', '128', '129', '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149', '150', '151', '152', '153', '154', '155', '156', '157', '158', '159', '160', '161', '162', '163', '164', '165', '166', '167', '168', '169', '170', '171', '172', '173', '174', '175', '176', '177', '178', '179', '180', '181', '182', '183', '184', '185', '186', '187', '188', '189', '190', '191', '192', '193', '194', '195', '196', '197', '198', '199', '200', '201', '202', '203', '204', '205', '206', '207', '208', '209', '210', '211', '212', '213', '214', '215', '216', '217', '218', '219', '220', '221', '222', '223', '224', '225', '226', '227', '228', '229', '230', '231', '232', '233', '234', '235', '236', '237', '238']
    assert [os.path.basename(item) for item in hr_data.test_sequences] == ['239', '240', '241', '242', '243', '244', '245', '246', '247', '248', '249', '250', '251', '252', '253', '254', '255', '256', '257', '258', '259', '260', '261', '262', '263',
                                                                           '264', '265', '266', '267', '268', '269', '270', '271', '272', '273', '274', '275', '276', '277', '278', '279', '280', '281', '282', '283', '284', '285', '286', '287', '288', '289', '290', '291', '292', '293', '294', '295', '296', '297', '298']
    pvt = PerformanceValidationTest(agent=agent,
                                    ingress_nodes=INGRESS_NODES,
                                    query_nodes=QUERY_NODES,
                                    test_count=1,
                                    dataset_percentage=PCT_CHOSEN,
                                    training_percentage=PCT_TRAINING,
                                    test_type='emotives_polarity',
                                    dataset=hr_data,
                                    test_prediction_strategy='noncontinuous',
                                    clear_all_memory_before_training=True,
                                    turn_prediction_off_during_training=True,
                                    shuffle=False,
                                    QUIET=True)

    pvt.conduct_pvt()
    with open(test_dir.joinpath('results/hr_prediction_log.json')) as f:
        assert pvt.predictions == json.load(f)

    predicted_vals = []

    for i, preds in enumerate(pvt.predictions):
        pred_dict = {node: pvt.predictions[i][node]
                     for node in pvt.query_nodes}
        for key in pred_dict:
            pred_dict[key] = prediction_ensemble_modeled_emotives(
                pred_dict[key])
        predicted_vals.append(pred_dict)

    assert predicted_vals == EXPECTED_HR_PREDS

    assert pvt.actuals == EXPECTED_HR_ACTUALS
    assert pvt.pvt_results[0]['P1']['utility']['actuals'] == [
        actual['utility'] for actual in EXPECTED_HR_ACTUALS]

    for idx, filepath in enumerate(hr_data.test_sequences):
        agent.clear_wm()
        with open(filepath, 'r') as f:
            sequence = f.readlines()
        sequence = [json.loads(item) for item in sequence]

        for item in sequence:
            agent.observe(item)

        assert agent.get_predictions() == pvt.predictions[idx]
        agent.clear_wm()

    assert pvt.pvt_results[0]['P1']['utility']['metrics']['overall'] == {'true_positive': 43,
                                                                         'false_positive': 5,
                                                                         'true_negative': 10,
                                                                         'false_negative': 2,
                                                                         'unknown_percentage': 0.0,
                                                                         'response_counts': 60,
                                                                         'response_percentage': 100.0,
                                                                         'accuracy': pytest.approx(88.33333333333333),
                                                                         'precision': pytest.approx(88.33333333333333),
                                                                         'training_counter': 239,
                                                                         'testing_counter': 60,
                                                                         'counter': 299,
                                                                         'FPR': pytest.approx(33.333333333333336),
                                                                         'FDR': pytest.approx(10.416666666666666),
                                                                         'TNR': pytest.approx(66.66666666666667),
                                                                         'TPR': pytest.approx(95.55555555555556),
                                                                         'NPV': pytest.approx(83.33333333333333),
                                                                         'FNR': pytest.approx(4.444444444444445),
                                                                         'FOR': pytest.approx(16.666666666666668),
                                                                         'LR+': pytest.approx(2.8666666666666667),
                                                                         'LR-': pytest.approx(0.06666666666666667),
                                                                         'PT': pytest.approx(0.37131607851430676),
                                                                         'TS': 86.0}

    assert pvt.pvt_results[0]['P1']['utility']['metrics']['positive'] == {'true_positive': 43,
                                                                          'false_positive': 0,
                                                                          'true_negative': 0,
                                                                          'false_negative': 2,
                                                                          'unknown_percentage': 0.0,
                                                                          'response_percentage': 100.0,
                                                                          'response_counts': 45,
                                                                          'accuracy': 95.55555555555556,
                                                                          'precision': 95.55555555555556,
                                                                          'training_counter': 170,
                                                                          'testing_counter': 45,
                                                                          'counter': 215,
                                                                          'FPR': pytest.approx(0.0),
                                                                          'FDR': pytest.approx(0.0),
                                                                          'TNR': pytest.approx(0.0),
                                                                          'TPR': pytest.approx(95.55555555555556),
                                                                          'NPV': pytest.approx(0.0),
                                                                          'FNR': pytest.approx(4.444444444444445),
                                                                          'FOR': pytest.approx(100.0),
                                                                          'LR+': pytest.approx(0.0),
                                                                          'LR-': pytest.approx(0.0),
                                                                          'PT': pytest.approx(0.0),
                                                                          'TS': pytest.approx(95.55555555555556)}
    assert pvt.pvt_results[0]['P1']['utility']['metrics']['negative'] == {'true_positive': 0,
                                                                          'false_positive': 5,
                                                                          'true_negative': 10,
                                                                          'false_negative': 0,
                                                                          'unknown_percentage': 0.0,
                                                                          'response_percentage': 100.0,
                                                                          'response_counts': 15,
                                                                          'accuracy': 66.66666666666667,
                                                                          'precision': 66.66666666666667,
                                                                          'training_counter': 69,
                                                                          'testing_counter': 15,
                                                                          'counter': 84,
                                                                          'FPR': pytest.approx(33.333333333333336),
                                                                          'FDR': pytest.approx(100.0),
                                                                          'TNR': pytest.approx(66.66666666666667),
                                                                          'TPR': pytest.approx(0.0),
                                                                          'NPV': pytest.approx(100.0),
                                                                          'FNR': pytest.approx(0.0),
                                                                          'FOR': pytest.approx(0.0),
                                                                          'LR+': pytest.approx(0.0),
                                                                          'LR-': pytest.approx(0.0),
                                                                          'PT': pytest.approx(1.0),
                                                                          'TS': pytest.approx(0.0)}
    with open(test_dir.joinpath('results/hr_testing_log.json')) as f:
        known_testing_log = json.load(f)
    assert pvt.testing_log == known_testing_log

    # get individual testing entries
    testing_records = [rec for rec in pvt.testing_log[0]
                       if rec['status'] == 'testing']
    testing_records = sorted(
        testing_records, key=lambda d: d['current_record'])

    # for each testing record, ensure that the running metrics are correct


@pytest.mark.agentManager
def test_prepared_obj_pvt():
    """Test basic classification pvt using prepared Data object and AgentManager

    """

    INGRESS_NODES = ["P1"]
    QUERY_NODES = ["P1"]
    CLASSIFICATION_DATASET_PATH = str(
        test_dir.joinpath('./datasets/shuffled_dummy_colors'))
    PCT_CHOSEN = 100
    PCT_TRAINING = 80

    am = AgentManager()
    am.start_hoster()
    am.kill_all_agents()

    # AgentManager agent_context
    with am.agent_context(genome_file=test_dir.joinpath('./genomes/simple.genome'), agent_id='pvt-colors-test', api_key='PVT_TESTING') as agent:
        time.sleep(5)
        assert agent.connect() == {'connection': 'okay',
                                   'agent': 'simple'}
        agent.set_summarize_for_single_node(False)
        agent.clear_all_memory()

        assert agent.change_genes({'recall_threshold': 0.1}) == {
            'P1': 'updated-genes'}
        assert agent.change_genes({'max_predictions': 5}) == {
            'P1': 'updated-genes'}
        assert agent.change_genes({'near_vector_count': 3}) == {
            'P1': 'updated-genes'}


        # directly provide GDF sequences to data object
        files = [int(file) for file in os.listdir(CLASSIFICATION_DATASET_PATH)]
        files = [str(file) for file in sorted(files)]

        train_sequences = []
        test_sequences = []
        assert files == ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
                         '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27']
        for file in files:
            with open(f'{CLASSIFICATION_DATASET_PATH}/{file}') as f:
                data_sequence = [json.loads(line) for line in f.readlines()]

            if file in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']:
                train_sequences.append(data_sequence)
            else:
                test_sequences.append(data_sequence)
        # verify that the train and test sequences are exactly as we expect (no shuffle)

        data = PreparedData(dataset=train_sequences + test_sequences, prep_enabled=False)
        data.train_sequences = train_sequences
        data.test_sequences = test_sequences

        pvt = PerformanceValidationTest(agent=agent,
                                        ingress_nodes=INGRESS_NODES,
                                        query_nodes=QUERY_NODES,
                                        test_count=1,
                                        dataset_percentage=PCT_CHOSEN,
                                        training_percentage=PCT_TRAINING,
                                        test_type='classification',
                                        dataset=data,
                                        test_prediction_strategy='noncontinuous',
                                        clear_all_memory_before_training=True,
                                        turn_prediction_off_during_training=True,
                                        shuffle=False,
                                        QUIET=True)

        pvt.conduct_pvt()

        with open(test_dir.joinpath('results/colors_prediction_log.json')) as f:
            assert pvt.predictions == json.load(f)

        predicted_vals = []

        for preds in pvt.predictions:
            preds_dict = {k: prediction_ensemble_model_classification(
                preds[k]) for k in preds}
            for k in preds_dict.keys():
                if preds_dict[k] is not None:
                    preds_dict[k] = preds_dict[k].most_common()[0][0]

            predicted_vals.append(preds_dict)

        assert predicted_vals == EXPECTED_COLORS_PREDS

        assert pvt.actuals == EXPECTED_COLORS_ACTUALS
        assert pvt.pvt_results[0]['P1']['actuals'] == EXPECTED_COLORS_ACTUALS

        # run again with prep_enabled = False
        data = PreparedData(dataset=train_sequences +
                            test_sequences, prep_enabled=True)

        pvt = PerformanceValidationTest(agent=agent,
                                        ingress_nodes=INGRESS_NODES,
                                        query_nodes=QUERY_NODES,
                                        test_count=1,
                                        dataset_percentage=PCT_CHOSEN,
                                        training_percentage=PCT_TRAINING,
                                        test_type='classification',
                                        dataset=data,
                                        test_prediction_strategy='noncontinuous',
                                        clear_all_memory_before_training=True,
                                        turn_prediction_off_during_training=True,
                                        shuffle=False,
                                        QUIET=True)

        pvt.conduct_pvt()

        with open(test_dir.joinpath('results/colors_prediction_log.json')) as f:
            assert pvt.predictions == json.load(f)

        predicted_vals = []

        for preds in pvt.predictions:
            preds_dict = {k: prediction_ensemble_model_classification(
                preds[k]) for k in preds}
            for k in preds_dict.keys():
                if preds_dict[k] is not None:
                    preds_dict[k] = preds_dict[k].most_common()[0][0]

            predicted_vals.append(preds_dict)

        assert predicted_vals == EXPECTED_COLORS_PREDS

        assert pvt.actuals == EXPECTED_COLORS_ACTUALS
        assert pvt.pvt_results[0]['P1']['actuals'] == EXPECTED_COLORS_ACTUALS

        assert pvt.pvt_results[0]['P1']['metrics'] == {'accuracy': pytest.approx(33.33333333333333),
                                                       'f1': pytest.approx(0.8),
                                                       'false_positive': 1.0,
                                                       'precision': pytest.approx(66.66666666666666),
                                                       'response_counts': 3.0,
                                                       'response_percentage': 50.0,
                                                       'true_positive': 2.0,
                                                       'unknown_percentage': 50.0,
                                                       'predicted_class_statistics': {'null': 3, 'red': 2, 'orange': 1},
                                                       'training_counter': {'blue': 2, 'green': 7, 'orange': 9, 'red': 4},
                                                       'testing_counter': {'orange': 1, 'red': 2, 'blue': 3},
                                                       'counter': {'blue': 5, 'green': 7, 'orange': 10, 'red': 6},
                                                       'true_negative': 0.0,
                                                       'false_negative': 0.0,
                                                       'FPR': pytest.approx(100.0),
                                                       'FDR': pytest.approx(33.333333333333336),
                                                       'TNR': pytest.approx(0.0),
                                                       'TPR': pytest.approx(100.0),
                                                       'NPV': pytest.approx(0.0),
                                                       'FNR': pytest.approx(0.0),
                                                       'FOR': pytest.approx(0.0),
                                                       'LR+': pytest.approx(1.0),
                                                       'LR-': pytest.approx(0.0),
                                                       'PT': pytest.approx(0.5),
                                                       'TS': pytest.approx(66.66666666666667)}

        with open(test_dir.joinpath('results/colors_testing_log.json')) as f:
            known_testing_log = json.load(f)
        assert pvt.testing_log == known_testing_log

        # get individual testing entries
        testing_records = [rec for rec in pvt.testing_log[0]
                           if rec['status'] == 'testing']
        testing_records = sorted(
            testing_records, key=lambda d: d['current_record'])


def test_bad_pvt_constructors(setup_and_teardown):

    INGRESS_NODES = ["P1"]
    QUERY_NODES = ["P1"]
    CLASSIFICATION_DATASET_PATH = str(
        test_dir.joinpath('./datasets/shuffled_dummy_colors'))
    PCT_CHOSEN = 100
    PCT_TRAINING = 80

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}

    agent = AgentClient(agent_info)

    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}

    agent.set_summarize_for_single_node(False)
    agent.clear_all_memory()

    assert agent.change_genes({'recall_threshold': 0.1}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'max_predictions': 5}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'near_vector_count': 3}) == {
        'P1': 'updated-genes'}

    data = PreparedData(data_directories=[CLASSIFICATION_DATASET_PATH])

    # directly provide GDF sequences to data object
    files = [int(file) for file in os.listdir(CLASSIFICATION_DATASET_PATH)]
    files = [str(file) for file in sorted(files)]

    assert files == ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
                     '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27']
    for file in files:
        with open(f'{CLASSIFICATION_DATASET_PATH}/{file}') as f:
            data_sequence = [json.loads(line) for line in f.readlines()]

        if file in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']:
            data.train_sequences.append(data_sequence)
        else:
            data.test_sequences.append(data_sequence)

    # bad prediction strategy
    try:
        pvt = PerformanceValidationTest(agent=agent,
                                        ingress_nodes=INGRESS_NODES,
                                        query_nodes=QUERY_NODES,
                                        test_count=1,
                                        dataset_percentage=PCT_CHOSEN,
                                        training_percentage=PCT_TRAINING,
                                        test_type='classification',
                                        dataset=data,
                                        test_prediction_strategy='every_other',  # INVALID
                                        clear_all_memory_before_training=True,
                                        turn_prediction_off_during_training=True,
                                        shuffle=False,
                                        QUIET=True)
        pytest.fail('expected bad prediction strategy to throw exception')
    except Exception as error:
        pass

    # bad dataset_location
    try:
        pvt = PerformanceValidationTest(agent=agent,
                                        ingress_nodes=INGRESS_NODES,
                                        query_nodes=QUERY_NODES,
                                        test_count=1,
                                        dataset_percentage=PCT_CHOSEN,
                                        training_percentage=PCT_TRAINING,
                                        test_type='classification',
                                        dataset=None,
                                        test_prediction_strategy='continuous',
                                        clear_all_memory_before_training=True,
                                        turn_prediction_off_during_training=True,
                                        shuffle=False,
                                        QUIET=True)
        pytest.fail('expected bad dataset location to throw exception')
    except Exception as error:
        pass

    # bad test_type
    try:
        pvt = PerformanceValidationTest(agent=agent,
                                        ingress_nodes=INGRESS_NODES,
                                        query_nodes=QUERY_NODES,
                                        test_count=1,
                                        dataset_percentage=PCT_CHOSEN,
                                        training_percentage=PCT_TRAINING,
                                        test_type='multi-classification',  # INVALID
                                        dataset=data,
                                        test_prediction_strategy='continuous',
                                        clear_all_memory_before_training=True,
                                        turn_prediction_off_during_training=True,
                                        shuffle=False,
                                        QUIET=True)
        pytest.fail('expected bad test_type to throw exception')
    except Exception as error:
        pass

    # bad test_type, changed after constructor
    try:
        pvt = PerformanceValidationTest(agent=agent,
                                        ingress_nodes=INGRESS_NODES,
                                        query_nodes=QUERY_NODES,
                                        test_count=1,
                                        dataset_percentage=PCT_CHOSEN,
                                        training_percentage=PCT_TRAINING,
                                        test_type='classification',
                                        dataset=data,
                                        test_prediction_strategy='continuous',
                                        clear_all_memory_before_training=True,
                                        turn_prediction_off_during_training=True,
                                        shuffle=False,
                                        QUIET=True)

        pvt.test_type = 'multi-classification'  # INVALID
        pvt.conduct_pvt()
        pytest.fail(f'bad test type should be caught in conduct_pvt')

    except Exception as error:
        pass


# getting setup to test mongodb connections for pvt (as used on brainiac to store results)
def test_classification_iris_mongodb_bad_record(setup_and_teardown_with_mongo):
    """Testing running test with mongodb dataset.
    Spawns an agent and a mongodb container locally
    """
    INGRESS_NODES = ["P1"]
    QUERY_NODES = ["P1"]
    CLASSIFICATION_DATASET_PATH = str(
        test_dir.joinpath('./datasets/shuffled_iris_flowers'))
    PCT_CHOSEN = 100
    PCT_TRAINING = 80

    mongo = MongoClient('localhost:27017')
    mongo_db = mongo['main_db']

    dataset_details = {"user_id": "user-1234",
                       "dataset_name": "shuffled_iris",
                       "dataset_id": "iris",
                       "data_files_collection_name": "dataset_files",
                       "dataset_collection_name": "datasets",
                       "results_collection": "tests",
                       "logs_collection": "testing_logs"
                       }
    MongoData.upload_dataset(mongo_db=mongo_db,
                             dataset_details=dataset_details,
                             filepath=test_dir.joinpath('datasets/shuffled_iris_flowers.zip'))
    try:
        md = MongoData(mongo_dataset_details=dataset_details,
                       data_files_collection_name=dataset_details['data_files_collection_name'],
                       dataset_collection_name=dataset_details['dataset_collection_name'],
                       mongo_db=mongo_db)
    except Exception as error:
        print(f'failed to get MongoData object: {str(error)}')
        pytest.fail(f'failed to get MongoData object: {str(error)}')

    md.prep(percent_of_dataset_chosen=PCT_CHOSEN,
            percent_reserved_for_training=PCT_TRAINING,
            shuffle=False)

    iris_data = Data(data_directories=[CLASSIFICATION_DATASET_PATH])
    iris_data.prep(percent_of_dataset_chosen=PCT_CHOSEN,
                   percent_reserved_for_training=PCT_TRAINING,
                   shuffle=False)

    mongo_record_id = md.train_sequences[-1]
    mongo_record = mongo_db[dataset_details['data_files_collection_name']].find_one(
        mongo_record_id)
    mongo_sequence = md.getSequence(record=mongo_record_id)
    # inject faulty gdf (metadata is list, not dict)
    mongo_sequence[0]['metadata'] = [None]
    mongo_sequence = json.dumps(mongo_sequence).encode('utf-8')

    # print(f'{mongo_sequence=}')
    mongo_db[dataset_details['data_files_collection_name']].update_one(
        {'_id': mongo_record_id}, {'$set': {'file': mongo_sequence}})
    mongo_record = mongo_db[dataset_details['data_files_collection_name']].find_one(
        mongo_record_id)
    # print(f"{mongo_record=}")
    try:
        mongo_train_seqs = [md.getSequence(record=seq_id)
                            for seq_id in md.train_sequences]
        pytest.fail("should throw exception on bad record")
    except Exception as error:
        pass

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}
    agent.set_summarize_for_single_node(False)
    agent.clear_all_memory()

    assert agent.change_genes({'recall_threshold': 0.1}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'max_predictions': 5}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'near_vector_count': 3}) == {
        'P1': 'updated-genes'}

    pvt = PerformanceValidationTest(agent=agent,
                                    ingress_nodes=INGRESS_NODES,
                                    query_nodes=QUERY_NODES,
                                    test_count=1,
                                    dataset_percentage=PCT_CHOSEN,
                                    training_percentage=PCT_TRAINING,
                                    test_type='classification',
                                    dataset=md,
                                    test_prediction_strategy='noncontinuous',
                                    clear_all_memory_before_training=True,
                                    turn_prediction_off_during_training=True,
                                    shuffle=False,
                                    QUIET=True,
                                    dataset_info=dataset_details,
                                    mongo_db=mongo_db)

    try:

        pvt.conduct_pvt()
        pytest.fail('bad record should cause exception during training')

    except Exception as error:
        pass

    # expect training log records to be cleaned up
    assert mongo_db["testing_logs"].count_documents(
        {'test_id': pvt.mongo_results.test_id}) == 0


def test_emotive_polarity_zero_val(setup_and_teardown, tmp_path):
    """Test basic emotive value pvt on pre-shuffled dataset

    """

    INGRESS_NODES = ["P1"]
    QUERY_NODES = ["P1"]
    EMOTIVE_POLARITY_DATASET_PATH = str(
        test_dir.joinpath('./datasets/shuffled_hr_attrition'))
    PCT_CHOSEN = 2
    PCT_TRAINING = 80

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}
    agent.set_summarize_for_single_node(False)
    agent.clear_all_memory()

    assert agent.change_genes({'recall_threshold': 0.1}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'max_predictions': 5}) == {
        'P1': 'updated-genes'}

    hr_data = PreparedData(data_directories=[EMOTIVE_POLARITY_DATASET_PATH], prep_enabled=True)
    hr_data.prep(percent_of_dataset_chosen=PCT_CHOSEN,
                 percent_reserved_for_training=PCT_TRAINING,
                 shuffle=False)

    # directly provide GDF sequences to data object
    files = [os.path.basename(
        file) for file in hr_data.train_sequences + hr_data.test_sequences]
    files = [int(file) for file in files]
    files = [str(file) for file in sorted(files)]

    # reset hr_data object
    hr_data = PreparedData(data_directories=[EMOTIVE_POLARITY_DATASET_PATH], prep_enabled=False)

    assert files == ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125', '126', '127', '128', '129', '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149', '150', '151', '152', '153', '154', '155',
                     '156', '157', '158', '159', '160', '161', '162', '163', '164', '165', '166', '167', '168', '169', '170', '171', '172', '173', '174', '175', '176', '177', '178', '179', '180', '181', '182', '183', '184', '185', '186', '187', '188', '189', '190', '191', '192', '193', '194', '195', '196', '197', '198', '199', '200', '201', '202', '203', '204', '205', '206', '207', '208', '209', '210', '211', '212', '213', '214', '215', '216', '217', '218', '219', '220', '221', '222', '223', '224', '225', '226', '227', '228', '229', '230', '231', '232', '233', '234', '235', '236', '237', '238', '239', '240', '241', '242', '243', '244', '245', '246', '247', '248', '249', '250', '251', '252', '253', '254', '255', '256', '257', '258', '259', '260', '261', '262', '263', '264', '265', '266', '267', '268', '269', '270', '271', '272', '273', '274', '275', '276', '277', '278', '279', '280', '281', '282', '283', '284', '285', '286', '287', '288', '289', '290', '291', '292', '293', '294', '295', '296', '297', '298']

    for file in files:
        with open(f'{EMOTIVE_POLARITY_DATASET_PATH}/{file}') as f:
            data_sequence = [json.loads(line) for line in f.readlines()]

        if file in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125', '126', '127', '128', '129', '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149', '150', '151', '152', '153', '154', '155', '156', '157', '158', '159', '160', '161', '162', '163', '164', '165', '166', '167', '168', '169', '170', '171', '172', '173', '174', '175', '176', '177', '178', '179', '180', '181', '182', '183', '184', '185', '186', '187', '188', '189', '190', '191', '192', '193', '194', '195', '196', '197', '198', '199', '200', '201', '202', '203', '204', '205', '206', '207', '208', '209', '210', '211', '212', '213', '214', '215', '216', '217', '218', '219', '220', '221', '222', '223', '224', '225', '226', '227', '228', '229', '230', '231', '232', '233', '234', '235', '236', '237', '238']:
            hr_data.train_sequences.append(data_sequence)
        else:
            hr_data.test_sequences.append(data_sequence)

    # inject zero utility value on first testing record. This is not allowed
    hr_data.test_sequences[0][0]['emotives']['utility'] = 0

    # verify that the train and test sequences are exactly as we expect (no shuffle)
    pvt = PerformanceValidationTest(agent=agent,
                                    ingress_nodes=INGRESS_NODES,
                                    query_nodes=QUERY_NODES,
                                    test_count=1,
                                    dataset_percentage=PCT_CHOSEN,
                                    training_percentage=PCT_TRAINING,
                                    test_type='emotives_polarity',
                                    results_filepath=f'{tmp_path}/results_dir',
                                    dataset=hr_data,
                                    test_prediction_strategy='noncontinuous',
                                    clear_all_memory_before_training=True,
                                    turn_prediction_off_during_training=True,
                                    shuffle=False,
                                    QUIET=True)

    try:
        pvt.conduct_pvt()
        pytest.fail(
            f'passing zero emotive value to Emotive Polarity PVT should raise Exception')

    except Exception as error:
        pass


EXPECTED_IRIS_PREDS_ON_ERROR = [{'P1': 'versicolor'},
                                {'P1': 'versicolor'},
                                {'P1': 'setosa'},
                                {'P1': 'virginica'},
                                {'P1': 'versicolor'},
                                {'P1': 'versicolor'},
                                {'P1': 'virginica'},
                                {'P1': 'virginica'},
                                {'P1': 'virginica'},
                                {'P1': 'setosa'},
                                {'P1': 'setosa'},
                                {'P1': 'virginica'},
                                {'P1': 'versicolor'},
                                {'P1': 'setosa'},
                                {'P1': 'setosa'},
                                {'P1': 'virginica'},
                                {'P1': 'virginica'},
                                {'P1': 'virginica'},
                                {'P1': 'virginica'},
                                {'P1': 'versicolor'},
                                {'P1': 'versicolor'},
                                {'P1': 'setosa'},
                                {'P1': 'virginica'},
                                {'P1': 'setosa'},
                                {'P1': 'virginica'},
                                {'P1': 'virginica'},
                                {'P1': 'versicolor'},
                                {'P1': 'setosa'},
                                {'P1': 'versicolor'},
                                {'P1': 'virginica'}
                                ]

def test_pvt_classification_on_error(setup_and_teardown):
    INGRESS_NODES = ["P1"]
    QUERY_NODES = ["P1"]
    CLASSIFICATION_DATASET_PATH = str(
        test_dir.joinpath('./datasets/shuffled_iris_flowers'))
    PCT_CHOSEN = 100
    PCT_TRAINING = 80

    agent_info = {'name': '',
                  'domain': address,
                  'api_key': 'ABCD-1234',
                  'secure': False}
    agent = AgentClient(agent_info)
    assert agent.connect() == {'connection': 'okay',
                               'agent': 'simple'}
    agent.set_summarize_for_single_node(False)
    agent.clear_all_memory()

    assert agent.change_genes({'recall_threshold': 0.1}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'max_predictions': 5}) == {
        'P1': 'updated-genes'}
    assert agent.change_genes({'near_vector_count': 3}) == {
        'P1': 'updated-genes'}

    iris_data = Data(data_directories=[CLASSIFICATION_DATASET_PATH])
    iris_data.prep(percent_of_dataset_chosen=PCT_CHOSEN,
                   percent_reserved_for_training=PCT_TRAINING,
                   shuffle=False)

    # verify that the train and test sequences are exactly as we expect (no shuffle)
    assert [os.path.basename(item) for item in iris_data.train_sequences] == ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56',
                                                                              '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119']
    assert [os.path.basename(item) for item in iris_data.test_sequences] == ['120', '121', '122', '123', '124', '125', '126', '127', '128', '129',
                                                                             '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149']

    pvt = PerformanceValidationTest(agent=agent,
                                    ingress_nodes=INGRESS_NODES,
                                    query_nodes=QUERY_NODES,
                                    test_count=1,
                                    dataset=iris_data,
                                    dataset_percentage=100,
                                    training_percentage=80,
                                    test_type='classification',
                                    test_prediction_strategy="continuous",
                                    learning_strategy="on_error",
                                    clear_all_memory_before_training=True,
                                    turn_prediction_off_during_training=False,
                                    shuffle=False,
                                    )

    pvt.conduct_pvt()

    # with open(test_dir.joinpath('results/current_iris_on_error_prediction_log.json'), 'w') as f:
    #     json.dump(pvt.predictions, f)

    with open(test_dir.joinpath('results/iris_on_error_prediction_log.json')) as f:
        assert pvt.predictions == json.load(f)

    predicted_vals = []

    for preds in pvt.predictions:
        preds_dict = {k: prediction_ensemble_model_classification(
            preds[k]) for k in preds}
        for k in preds_dict.keys():
            if preds_dict[k] is not None:
                preds_dict[k] = preds_dict[k].most_common()[0][0]

        predicted_vals.append(preds_dict)

    assert predicted_vals == EXPECTED_IRIS_PREDS_ON_ERROR

    assert pvt.actuals == EXPECTED_IRIS_ACTUALS
    assert pvt.pvt_results[0]['P1']['actuals'] == EXPECTED_IRIS_ACTUALS

    assert pvt.pvt_results[0]['P1']['metrics'] == {'training_counter': {'virginica': 37, 'versicolor': 41, 'setosa': 42},
                                                   'testing_counter': {'versicolor': 9, 'virginica': 13, 'setosa': 8},
                                                   'counter': {'virginica': 50, 'versicolor': 50, 'setosa': 50},
                                                   'predicted_class_statistics': {'versicolor': 9, 'setosa': 8, 'virginica': 13},
                                                   'response_counts': 30.0,
                                                   'true_positive': 24.0,
                                                   'false_positive': 6.0,
                                                   'precision': 80.0,
                                                   'f1': 0.8888888888888888,
                                                   'accuracy': 80.0,
                                                   'response_percentage': 100.0,
                                                   'unknown_percentage': 0.0,
                                                   'true_negative': 0.0,
                                                   'false_negative': 0.0,
                                                   'FPR': 100.0,
                                                   'FDR': 20.0,
                                                   'TNR': 0.0,
                                                   'TPR': 100.0,
                                                   'NPV': 0.0,
                                                   'FNR': 0.0,
                                                   'FOR': 0.0,
                                                   'LR+': 1.0,
                                                   'LR-': 0.0,
                                                   'PT': 0.5,
                                                   'TS': 80.0}
    with open(test_dir.joinpath('results/iris_on_error_testing_log.json')) as f:
        known_testing_log = json.load(f)
    assert pvt.testing_log == known_testing_log

    # get individual testing entries
    testing_records = [rec for rec in pvt.testing_log[0]
                       if rec['status'] == 'testing']
    testing_records = sorted(
        testing_records, key=lambda d: d['current_record'])

    # for each testing record, ensure that the running metrics are correct
