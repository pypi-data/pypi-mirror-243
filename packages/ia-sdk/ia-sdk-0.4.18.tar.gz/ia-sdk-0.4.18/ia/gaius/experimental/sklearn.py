import statistics
import time
import uuid
from collections import Counter, defaultdict
from copy import deepcopy
from math import floor
from sys import stdout
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy.special import softmax
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin
from sklearn.utils.multiclass import unique_labels
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y
from tqdm.auto import tqdm

from ia.gaius.data_ops import validate_data
from ia.gaius.data_structures import PredictionEnsemble
from ia.gaius.manager import AgentManager
from ia.gaius.prediction_models import (
    most_common_ensemble_model_classification,
    prediction_ensemble_model_classification)
from ia.gaius.utils import create_gdf


class GAIuSClassifier(BaseEstimator, ClassifierMixin):
    """GAIuS Classifier using a single node, for use with Scikit-Learn"""

    def __init__(self, recall_threshold: float = 0.1, max_predictions: int = 10, near_vector_count: int = 5, use_vectors=True):

        self.use_vectors = use_vectors
        self.recall_threshold = recall_threshold
        self.max_predictions = max_predictions

        self.am = AgentManager()
        self.am.start_hoster()
        # self.am.kill_all_agents()
        self.uuid_extension = uuid.uuid4().hex[:4]
        self.unique_agent_name = f"classif-{self.uuid_extension}"
        self.agent = self.am.start_agent(genome_name="simple.genome",
                                         agent_name=self.unique_agent_name,
                                         agent_id=self.unique_agent_name).get_agent_client()

        time.sleep(2.0)
        self.agent.connect()
        self.agent.set_ingress_nodes(["P1"])
        self.agent.set_query_nodes(["P1"])

        self.agent.change_genes({'SORT': False,
                                 'max_predictions': max_predictions,
                                 'recall_threshold': recall_threshold,
                                 'near_vector_count': near_vector_count})
        self.classes_ = None
        self.X_ = None
        self.y_ = None

    # Deleting (Calling destructor)
    def __del__(self):
        tqdm.write(f'DELETING AGENT', stdout)
        self.am.delete_agent(agent_name=self.unique_agent_name)

    def fit(self, X: np.ndarray, y: np.ndarray):

        # Check that X and y have correct shape
        X, y = check_X_y(X, y, dtype=object)

        # Store the classes seen during fit
        self.classes_ = unique_labels(y)

        self.X_ = X
        self.y_ = y

        for row in self.X_:
            for gdf in row[0]:
                if not validate_data(data=gdf):
                    raise ValueError(f"Bad gdf found in sequence: {gdf=}")

        self.agent.clear_all_memory()
        self.agent.stop_predicting()
        for i, seq in enumerate(tqdm(self.X_, leave=False)):
            self.agent.clear_wm()
            for event in seq[0]:
                self.agent.observe(event)

            label_gdf = create_gdf(strings=[str(self.y_[i])])
            self.agent.observe(label_gdf)
            self.agent.learn()
        self.agent.start_predicting()
        # Return the classifier
        return self

    def predict(self, X: np.ndarray):

        # Check if fit has been called
        check_is_fitted(self)

        # Input validation
        X = check_array(X, dtype=object)

        output = []
        self.agent.start_predicting()
        pbar = tqdm(X, leave=False)
        for seq in pbar:
            self.agent.clear_wm()
            for gdf in seq[0]:
                self.agent.observe(gdf)

            ensemble = self.agent.get_predictions()
            classif = prediction_ensemble_model_classification(
                ensemble).most_common()[0][0]
            output.append(classif)
        del pbar
        return np.array(output)

    def predict_proba(self, X: np.ndarray):
        print('in predict_proba')
        # Check if fit has been called
        check_is_fitted(self)

        # Input validation
        X = check_array(X, dtype=object)

        output = []
        for seq in X:
            self.agent.clear_wm()
            for gdf in seq[0]:
                self.agent.observe(gdf)

            ensemble = self.agent.get_predictions()
            classif_dict = prediction_ensemble_model_classification(ensemble)
            total = sum(classif_dict.values(), 0.0)

            for key in classif_dict:
                classif_dict[key] /= total

            probs = [classif_dict.get(str(classif), 0.0)
                     for classif in self.classes_]
            output.append(softmax(probs))

        return np.array(output)


class GDFTransformer(BaseEstimator, TransformerMixin):
    """Transform dataset from numerical data into GDF format (each record is a list of GDFs)
    """

    def __init__(self, as_vector: bool = False):
        self.as_vector = as_vector
        self.fit_args = {}

    def fit(self, X, y=None, **kwargs):
        self.fit_args = kwargs
        return self

    def transform(self, X: np.ndarray, y=None, feature_names: List[str] = None):
        _X = X
        # print(f'Input shape: {X.shape}')
        pd_feature_names = None
        if isinstance(X, pd.DataFrame):
            _X = X.values
            pd_feature_names = X.columns.tolist()

        if feature_names is None:
            if 'feature_names' in self.fit_args:
                feature_names = self.fit_args['feature_names']
            elif pd_feature_names is not None:
                feature_names = pd_feature_names
            else:
                feature_names = [str(i) for i in range(_X.shape[1])]

        if len(feature_names) != _X.shape[1]:
            raise Exception(
                f"length of feature_names ({len(feature_names)}) does not match data shape ({_X.shape[1]})")

        new_X = np.zeros(shape=(_X.shape[0], 1), dtype=object)

        row: np.ndarray
        for i, row in enumerate(tqdm(_X, leave=False)):
            if self.as_vector:
                new_X[i][0] = [create_gdf(vectors=[row.tolist()])]
            else:
                new_X[i][0] = [create_gdf(
                    strings=[f'{one}|{two}' for one, two in zip(feature_names, row.tolist())])]

        # todo convert input rows into gdf format
        return new_X


def flatten(l: List[List[str]]) -> List[str]:
    """Flatten list of lists into a single list

    Args:
        l (List[List[str]]): _description_

    Returns:
        List[str]: _description_
    """
    return [item for sublist in l for item in sublist]


def ensemble2vec(ensemble: PredictionEnsemble, sorted_symbol_names: List[str], max_predictions: int = 5, prediction_fields: List[str] = None) -> np.ndarray:
    """Get a sparse 'presence' vector that depicts whether the symbol was present in prediction

    Args:
        ensemble (PredictionEnsemble): Prediction Ensemble to vectorize
        sorted_symbol_names (List[str]): list of all symbols possibly present (symbols from symbols_kb + model names, sorted)
        max_predictions (int, optional): max number of predictions to include in the feature vector. Defaults to 5.
        prediction_fields (List[str], optional): Which fields to extract from prediction objects to make feature vector. Defaults to None.

    Raises:
        Exception: Indexing out of bounds

    Returns:
        np.ndarray: feature vector
    """

    nodes = list(ensemble.ensemble.keys())
    assert len(nodes) == 1  # for now only supporting the "simple" case

    if prediction_fields is None:
        prediction_fields = ["matches", "missing", "future"]

    prediction_field_count = len(prediction_fields)
    prediction_feature_count = len(sorted_symbol_names)

    single_pred_feature_length = prediction_field_count * \
        (prediction_feature_count)
    total_length = prediction_field_count * \
        max_predictions * (prediction_feature_count)

    resultant_vector = np.zeros(total_length, dtype=np.bool_)

    for i, pred in enumerate(ensemble.ensemble[nodes[0]]):
        if i >= max_predictions:
            break

        for j, field in enumerate(prediction_fields):
            field_data = pred._prediction[field]
            if field == "name":
                field_data = [f'MODEL|{field_data}']

            if not field_data:
                continue
            if isinstance(field_data[0], list):
                field_data = flatten(field_data)

            for symbol in field_data:
                try:
                    # get index of symbol

                    sorted_sym_position = sorted_symbol_names.index(symbol)
                    sym_index = i * (single_pred_feature_length) + \
                        j * prediction_feature_count + sorted_sym_position
                    if sym_index >= total_length:
                        raise Exception(
                            f"Sym index ({sym_index}) greater than length {total_length}!!!")

                    resultant_vector[sym_index] = 1

                except:
                    print(
                        f'Symbol {symbol} not found in symbols_kb, continuing')
                    pass

    return resultant_vector


def make_sklearn_fv(ensemble_data: List[Tuple[Dict[str, dict], List[List[str]]]], kb: Dict[str, dict], max_predictions: int = 5, prediction_fields: List[str] = None) -> Tuple[np.ndarray, np.ndarray]:
    """Make Ensemble feature vectors from a list of (ensemble, actual) tuples.
    This gets the Agent prediction ensemble output into the proper format for ingest into a Scikit learn classifier (to model the output of GAIuS)

    Args:
        ensemble_data (List[Tuple[Dict[str, dict], List[List[str]]]]): Corresponds to zip of pvt.predictions and pvt.actuals
        kb (Dict[str, dict]): _description_
        max_predictions (int, optional): _description_. Defaults to 5.
        prediction_fields (List[str], optional): _description_. Defaults to None.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Feature Vectors, Actual Label arrays in expected Scikit-learn formats
    """

    if prediction_fields is None:
        prediction_fields = ["matches", "missing", "name"]

    prediction_field_count = len(prediction_fields)

    if 'name' in prediction_fields:
        sorted_symbol_names = list(
            kb['symbols_kb'].keys()) + [f'MODEL|{val}' for val in kb['models_kb'].keys()]
    else:
        sorted_symbol_names = list(kb['symbols_kb'].keys())
    sorted_symbol_names = sorted(sorted_symbol_names)

    total_length = prediction_field_count * \
        max_predictions * (len(sorted_symbol_names))

    sparse_array = None
    for ensemble in tqdm(ensemble_data, leave=False):
        if sparse_array is None:
            sparse_array = sp.csr_array(ensemble2vec(ensemble=PredictionEnsemble(ensemble[0]),
                                                     sorted_symbol_names=sorted_symbol_names,
                                                     max_predictions=max_predictions,
                                                     prediction_fields=prediction_fields),
                                        (1, total_length),
                                        dtype=np.bool_)
        else:
            sparse_array = sp.vstack((sparse_array,
                                      sp.csr_array(ensemble2vec(ensemble=PredictionEnsemble(ensemble[0]),
                                                                sorted_symbol_names=sorted_symbol_names,
                                                                max_predictions=max_predictions,
                                                                prediction_fields=prediction_fields),
                                                   dtype=np.bool_)),
                                     dtype=np.bool_)

    y = np.array([ens[1][0] for ens in ensemble_data], dtype=str)

    return sparse_array, y


def get_feature_names_from_weights(coefficients: np.ndarray, kb: Dict[str, dict], prediction_fields: List[str]):

    symbol_count = len(kb['symbols_kb'])
    model_count = len(kb['models_kb'])
    prediction_field_count = len(prediction_fields)

    if 'name' in prediction_fields:
        sorted_symbol_names = list(
            kb['symbols_kb'].keys()) + [f'MODEL|{val}' for val in kb['models_kb'].keys()]
    else:
        sorted_symbol_names = list(kb['symbols_kb'].keys())
    sorted_symbol_names = sorted(sorted_symbol_names)

    prediction_feature_count = len(sorted_symbol_names)
    single_pred_feature_length = prediction_field_count * \
        (prediction_feature_count)
    print(f'{single_pred_feature_length=}')

    feature_dict_template = {'models': defaultdict(lambda: defaultdict(Counter)),
                             'symbols': defaultdict(lambda: defaultdict(Counter))}

    feature_dict = {}

    coefficient_list = coefficients.tolist()
    for j, coefficient_row in enumerate(coefficients):
        sub_feature_dict = deepcopy(feature_dict_template)
        for i, val in enumerate(coefficient_row):
            if not val:
                continue
            try:
                sym_index = i % prediction_feature_count
                prediction_index = floor(
                    int(i)/int(single_pred_feature_length))
                pred_field = floor(
                    int(i)/int(prediction_feature_count)) % prediction_field_count

                if sorted_symbol_names[sym_index].startswith("MODEL"):
                    sub_feature_dict['models'][prediction_index][prediction_fields[pred_field]
                                                                 ][sorted_symbol_names[sym_index]] = val
                else:
                    # symbol
                    sub_feature_dict['symbols'][prediction_index][prediction_fields[pred_field]
                                                                  ][sorted_symbol_names[sym_index]] = val

            except:
                print(
                    f'{i=}, {sym_index=}, {val=}, {prediction_feature_count=}, {symbol_count=}')
                raise

        for pred_key in sub_feature_dict['models']:
            sub_feature_dict['models'][pred_key] = dict(
                sub_feature_dict['models'][pred_key].items())

        for pred_key in sub_feature_dict['symbols']:
            sub_feature_dict['symbols'][pred_key] = dict(
                sub_feature_dict['symbols'][pred_key].items())

        sub_feature_dict['models'] = dict(sub_feature_dict['models'].items())
        sub_feature_dict['symbols'] = dict(sub_feature_dict['symbols'].items())
        feature_dict[j] = sub_feature_dict
    return feature_dict


def split_feature_weights_by_key(symbol_feature_counter: Dict[int, Dict[str, Counter]]):
    features_by_key = defaultdict(
        lambda: defaultdict(lambda: defaultdict(dict)))
    for pred_index, symbol_feature_subcounter in symbol_feature_counter.items():

        for pred_field, pred_field_subcounter in symbol_feature_subcounter.items():
            key: str
            value: float
            for key, value in pred_field_subcounter.items():
                if len(split_key := key.rsplit('|', maxsplit=1)) <= 1:
                    continue
                try:
                    features_by_key[pred_index][split_key[0]
                                                ][pred_field][float(split_key[1])] = value
                except:
                    features_by_key[pred_index][split_key[0]
                                                ][pred_field][split_key[1]] = value
                    pass

        for key, key_features in features_by_key[pred_index].items():
            for sym_key in key_features:
                features_by_key[pred_index][key][sym_key] = dict(
                    sorted(features_by_key[pred_index][key][sym_key].items()))
            features_by_key[pred_index][key] = dict(
                sorted(features_by_key[pred_index][key].items()))  # sort items by key

    for key, key_features in features_by_key.items():
        features_by_key[key] = dict(
            sorted(features_by_key[key].items()))  # sort items by key
    return dict(features_by_key.items())


def get_models_to_drop(sym_features: dict, threshold_multiplier: float = 1.0) -> List[str]:
    """Identify models that should be dropped, based on the provided sym_features dictionary

    Args:
        sym_features (dict): _description_
        threshold_multiplier (float, optional): _description_. Defaults to 1.0.

    Returns:
        List[str]: _description_
    """
    model_weights_dict = {}
    model_name_set = set()

    for pred_index in sym_features:
        for key, symbol_fields in sym_features[pred_index].items():
            for sym_field, sym_counter in symbol_fields.items():
                # print(f'{sym_field=}, {sym_counter=}')
                # model_weights_dict = sym_counter
                for sym, val in sym_counter.items():
                    if sym in model_weights_dict:
                        continue
                    model_weights_dict[sym] = val
        # lets only worry about prediction index 0 for now

    for pred_index in sym_features:
        for key, symbol_fields in sym_features[pred_index].items():
            for sym_field, sym_counter in symbol_fields.items():
                model_name_set.update(sym_counter.keys())

    mean_val = statistics.mean(model_weights_dict.values())
    std_dev = statistics.stdev(model_weights_dict.values())

    threshold = std_dev * threshold_multiplier
    models_to_drop = [key for key, value in model_weights_dict.items(
    ) if mean_val - threshold <= value <= mean_val + threshold]

    return models_to_drop


def max_magnitude(num1: float, num2: float) -> float:
    """Return the number that has the larger magnitude, preserving sign information on
    the number

    Args:
        num1 (float): number to compare
        num2 (float): number to compare

    Returns:
        float: the number with the larger magnitude
    """
    abs_num1 = abs(num1)
    abs_num2 = abs(num2)

    if abs_num1 >= abs_num2:
        return num1
    else:
        return num2


def gm2d(features: dict, threshold_multiplier: float = 1.0) -> List[str]:
    """Get models to delete, from features dict output of "split_feature_weights_by_key"

    Args:
        features (dict): _description_
        threshold_multiplier (float, optional): _description_. Defaults to 1.0.

    Returns:
        List[str]: list of models that should be dropped from the agent (low correlation to ANY class)
    """
    model_weights_dict = Counter()

    for index, sym_features in features.items():
        for pred_index in sym_features:
            for key, symbol_fields in sym_features[pred_index].items():
                for sym_field, sym_counter in symbol_fields.items():
                    for sym, val in sym_counter.items():
                        if sym not in model_weights_dict:
                            model_weights_dict[sym] = val
                        else:
                            model_weights_dict[sym] = max_magnitude(
                                model_weights_dict[sym], val)
            # lets only worry about prediction index 0 for now

    mean_val = statistics.mean(model_weights_dict.values())
    std_dev = statistics.stdev(model_weights_dict.values())

    threshold = std_dev * threshold_multiplier
    models_to_drop = [key for key, value in model_weights_dict.items(
    ) if mean_val - threshold <= value <= mean_val + threshold]

    return models_to_drop
