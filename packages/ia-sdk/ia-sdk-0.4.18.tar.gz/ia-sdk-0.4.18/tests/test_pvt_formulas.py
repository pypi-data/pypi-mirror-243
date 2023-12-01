from lib.dependencies import remove_id_and_timestamp, MyFixture
import json
import pytest
import os
import math
from ia.gaius.agent_client import AgentClient
from ia.gaius.pvt import PerformanceValidationTest
from ia.gaius.prediction_models import prediction_ensemble_model_classification, prediction_ensemble_modeled_emotives
from ia.gaius.data_ops import Data
import pathlib
from collections import defaultdict
from ia.gaius.pvt.pvt_utils import false_discovery_rate, f1_score, update_accuracy, update_precision, compute_squared_residual
import numpy as np

test_dir = pathlib.Path(__file__).parent.resolve()

IRIS_TESTING_LOG = test_dir.joinpath('./results/iris_testing_log.json')

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


def test_classification_metrics():

    with open(IRIS_TESTING_LOG) as f:
        KNOWN_IRIS_LOG = json.load(f)

    zipped_results = list([item for item in zip(
        EXPECTED_IRIS_ACTUALS, EXPECTED_IRIS_PREDS)])

    for i, item in enumerate(zipped_results):
        test_step_info = KNOWN_IRIS_LOG[0][i]
        current_preds = item[1]
        current_actuals = item[0]

        # get list of predictions, actuals up to this point
        pred_list = [elem[1] for elem in zipped_results[:i+1]]
        actual_list = [elem[0] for elem in zipped_results[:i+1]]
        zipped_present = zipped_results[:i+1]

        for node in current_preds.keys():
            response_count = len([pred[node]
                                 for pred in pred_list if pred[node] != None])
            # print(f'{zipped_present=}')
            tp = len([pred[node]
                     for actual, pred in zipped_present if pred[node] in actual])
            fp = len([pred[node] for actual, pred in zipped_present if (
                (pred[node] not in actual) and pred[node] != None)])
            fdr = false_discovery_rate(tp=tp, fp=fp)
            f1 = f1_score(tp=tp, fp=fp, fn=0)
            precision = pytest.approx(update_precision(
                tp=tp, tn=0, response_count=response_count))
            accuracy = pytest.approx(update_accuracy(
                tp=tp, tn=0, overall_count=len(zipped_present)))
            resp_percentage = 100 * response_count / len(zipped_present)
            unknown_percentage = 100 * \
                (len(zipped_present) - response_count) / len(zipped_present)

            assert test_step_info['metrics']['response_counts'][node] == response_count
            assert test_step_info['metrics']['true_positive'][node] == tp
            assert test_step_info['metrics']['false_positive'][node] == fp
            assert test_step_info['metrics']['FDR'][node] == fdr
            assert test_step_info['metrics']['f1'][node] == f1
            assert test_step_info['metrics']['precision'][node] == precision
            assert test_step_info['metrics']['accuracy'][node] == accuracy
            assert test_step_info['metrics']['response_percentage'][node] == resp_percentage
            assert test_step_info['metrics']['unknown_percentage'][node] == unknown_percentage

    return


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

BHP_TESTING_LOG = test_dir.joinpath('./results/bhp_testing_log.json')


def test_emotive_value_metrics():
    with open(BHP_TESTING_LOG) as f:
        KNOWN_BHP_LOG = json.load(f)

    zipped_results = list([item for item in zip(
        EXPECTED_BHP_ACTUALS, EXPECTED_BHP_PREDS)])

    for i, item in enumerate(zipped_results):
        test_step_info = KNOWN_BHP_LOG[0][i]
        current_preds = item[1]
        current_actuals = item[0]

        # get list of predictions, actuals up to this point
        pred_list = [elem[1] for elem in zipped_results[:i+1]]
        actual_list = [elem[0] for elem in zipped_results[:i+1]]
        zipped_present = zipped_results[:i+1]

        for node in current_preds.keys():
            for emotive in current_preds[node]:

                response_count = len(
                    [pred[node][emotive] for pred in pred_list if pred[node].get(emotive, None)])
                residual = current_actuals[emotive] - \
                    current_preds[node][emotive]
                abs_residual = abs(residual)
                sqr_residual = math.pow(residual, 2)

                current_residual_list = [act[emotive] - pred[node][emotive] for act, pred in zipped_present if (
                    act.get(emotive, None) and pred[node].get(emotive, None))]
                abs_residual_list = [abs(residual)
                                     for residual in current_residual_list]
                sqr_residual_list = [math.pow(residual, 2)
                                     for residual in current_residual_list]

                rmse = math.sqrt(sum(sqr_residual_list) /
                                 len(sqr_residual_list))

                # SMAPE
                current_pred_list = [pred[node][emotive]
                                     for pred in pred_list if pred[node].get(emotive, None)]
                current_actual_list = [actual[emotive]
                                       for actual in actual_list if actual.get(emotive, None)]

                smape = 0.0
                for i, abs_residual in enumerate(abs_residual_list):
                    smape += (abs_residual) / \
                        ((abs(current_actual_list[i] +
                         abs(current_pred_list[i]))) / 2)

                smape *= 100  # convert to percent
                smape /= len(current_pred_list)

                actual_emotive_count = len(
                    [act[emotive] for act in actual_list if act.get(emotive, None)])
                resp_percentage = 100 * response_count / actual_emotive_count
                unknown_percentage = 100 * \
                    (actual_emotive_count - response_count) / actual_emotive_count

                assert test_step_info['metrics']['residuals'][node][emotive] == pytest.approx(
                    residual)
                assert test_step_info['metrics']['abs_residuals'][node][emotive] == pytest.approx(
                    abs_residual)
                assert test_step_info['metrics']['squared_residuals'][node][emotive] == pytest.approx(
                    sqr_residual)
                assert test_step_info['metrics']['rmse'][node][emotive] == pytest.approx(
                    rmse)
                assert test_step_info['metrics']['smape'][node][emotive] == pytest.approx(
                    smape)
                assert test_step_info['metrics']['response_counts'][node][emotive] == response_count
                assert test_step_info['metrics']['response_percentage'][node][emotive] == resp_percentage
                assert test_step_info['metrics']['unknown_percentage'][node][emotive] == unknown_percentage

    return


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

HR_TESTING_LOG = test_dir.joinpath('./results/hr_testing_log.json')


def test_emotive_polarity_metrics():
    with open(HR_TESTING_LOG) as f:
        KNOWN_HR_LOG = json.load(f)

    zipped_results = list([item for item in zip(
        EXPECTED_HR_ACTUALS, EXPECTED_HR_PREDS)])

    for i, item in enumerate(zipped_results):
        test_step_info = KNOWN_HR_LOG[0][i]
        current_preds = item[1]
        current_actuals = item[0]

        # get list of predictions, actuals up to this point
        pred_list = [elem[1] for elem in zipped_results[:i+1]]
        actual_list = [elem[0] for elem in zipped_results[:i+1]]
        zipped_present = zipped_results[:i+1]

        for node in current_preds.keys():
            for emotive in current_preds[node]:

                current_pred_list = [pred[node][emotive]
                                     for pred in pred_list if pred[node].get(emotive, None)]
                current_actual_list = [actual[emotive]
                                       for actual in actual_list if actual.get(emotive, None)]

                pred_signs = [np.sign(pred) for pred in current_pred_list]
                actual_signs = [np.sign(actual)
                                for actual in current_actual_list]
                zipped_signs = [item for item in zip(pred_signs, actual_signs)]

                tp = sum([1 for p, a in zipped_signs if (p > 0 and a > 0)])
                tn = sum([1 for p, a in zipped_signs if (p < 0 and a < 0)])
                fn = sum([1 for p, a in zipped_signs if (a > 0 and not p > 0)])
                fp = sum([1 for p, a in zipped_signs if (a < 0 and not p < 0)])
                response_count = sum([1 for p, a in zipped_signs if (p != 0)])

                actual_emotive_count = len(
                    [act[emotive] for act in actual_list if act.get(emotive, None)])
                resp_percentage = 100 * response_count / actual_emotive_count
                unknown_percentage = 100 * \
                    (actual_emotive_count - response_count) / actual_emotive_count

                accuracy = update_accuracy(
                    tp=tp, tn=tn, overall_count=actual_emotive_count)
                precision = update_precision(
                    tp=tp, tn=tn, response_count=response_count)

                assert test_step_info['metrics']['overall']['true_positive'][node][emotive] == tp
                assert test_step_info['metrics']['overall']['false_positive'][node][emotive] == fp
                assert test_step_info['metrics']['overall']['true_negative'][node][emotive] == tn
                assert test_step_info['metrics']['overall']['false_negative'][node][emotive] == fn
                assert test_step_info['metrics']['overall']['unknown_percentage'][node][emotive] == unknown_percentage
                assert test_step_info['metrics']['overall']['response_percentage'][node][emotive] == resp_percentage
                assert test_step_info['metrics']['overall']['response_counts'][node][emotive] == response_count
                assert test_step_info['metrics']['overall']['accuracy'][node][emotive] == accuracy
                assert test_step_info['metrics']['overall']['precision'][node][emotive] == precision
                assert test_step_info['metrics']['testing_counter'][emotive]['overall'] == actual_emotive_count
    return
