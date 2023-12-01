import networkx as nx
from ia.gaius.data_structures import Prediction, PredictionEnsemble

PRED_1 = {"confidence": 1,
          "confluence": -2.7688342155159886,
          "emotives": {},
          "entropy": -89.0480393484581,
          "evidence": 0.06896551724137931,
          "extras": [], "fragmentation": 0,
          "frequency": 1,
          "future": [["AXIS0|1", "AXIS1|1", "AXIS2|3", "AXIS3|4", "AXIS3|LESS"],
                     ["AXIS0|1", "AXIS1|1", "AXIS2|3", "AXIS3|2", "AXIS3|LESS"],
                     ["AXIS0|1", "AXIS1|2", "AXIS1|GREATER",
                         "AXIS2|3", "AXIS3|0", "AXIS3|LESS"],
                     ["AXIS0|1", "AXIS1|2", "AXIS2|2", "AXIS2|LESS", "AXIS3|0"],
                     ["AXIS0|1", "AXIS1|2", "AXIS2|2", "AXIS3|0"],
                     ["AXIS0|1", "AXIS1|2", "AXIS2|2", "AXIS3|0"],
                     ["AXIS0|1", "AXIS1|2", "AXIS2|2", "AXIS3|0"],
                     ["AXIS0|1", "AXIS1|2", "AXIS2|2", "AXIS3|0"],
                     ["AXIS0|1", "AXIS1|2", "AXIS2|1", "AXIS2|LESS", "AXIS3|0"],
                     ["AXIS0|1", "AXIS1|1", "AXIS1|LESS",
                         "AXIS2|1", "AXIS3|1", "AXIS3|GREATER"],
                     ["AXIS0|1", "AXIS1|2", "AXIS1|GREATER", "AXIS2|1", "AXIS3|0", "AXIS3|LESS"]],
          "grand_hamiltonian": -18.147549372336265,
          "hamiltonian": 0.40759009418101233,
          "itfdf_similarity": 1,
          "matches": ["AXIS0|1", "AXIS1|1", "AXIS2|3", "AXIS3|6"],
          "missing": [],
          "name": "07b762a3ad05f762b2ca7411b235f009474d3da0",
          "past": [],
          "potential": 3.068965517241379,
          "present": [["AXIS0|1", "AXIS1|1", "AXIS2|3", "AXIS3|6"]],
          "similarity": 0.12903225806451613,
          "snr": 1,
          "type": "prototypical"}


def test_prediction_constructor():

    pred = Prediction(**PRED_1)
    pred_copy = Prediction(prediction=PRED_1)
    assert pred == pred_copy

    assert pred._prediction == PRED_1
    assert pred_copy._prediction == PRED_1

    for key, value in PRED_1.items():
        assert getattr(pred, key) == value

    assert len(pred.events) == len(
        PRED_1['past']) + len(PRED_1['present']) + len(PRED_1['future'])

    pass


def test_prediction_json():

    pred = Prediction(**PRED_1)
    pred_copy = Prediction(prediction=PRED_1)

    assert pred.toJSON() == PRED_1
    assert pred_copy.toJSON() == PRED_1

    pass


def test_prediction_past_graph():

    pred = Prediction(**PRED_1)

    past_graph: nx.Graph = pred.toPastStateGraph()

    # past state is empty in PRED_1
    assert past_graph.number_of_nodes() == 0
    assert past_graph.number_of_edges() == 0

    pass


def test_prediction_present_graph():

    pred = Prediction(**PRED_1)

    present_graph: nx.Graph = pred.toPresentStateGraph()

    # 4 symbols in present state in PRED_1
    # TODO: make distinction between symbol graph
    # and event graphs in function names
    assert present_graph.number_of_nodes() == 4
    assert present_graph.number_of_edges() == 3

    pass


def test_prediction_directed_graph():

    pred = Prediction(**PRED_1)

    directed_graph: nx.DiGraph = pred.toLoopingEventGraph()

    assert directed_graph.number_of_nodes() == 9
    assert directed_graph.number_of_edges() == 9

    pass
