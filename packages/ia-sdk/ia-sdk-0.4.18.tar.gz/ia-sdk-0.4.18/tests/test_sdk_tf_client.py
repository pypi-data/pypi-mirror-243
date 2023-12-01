import json
import time
from pathlib import Path
from unittest.mock import ANY

import pytest
from ia.gaius.data_ops import Data
from ia.gaius.manager import AgentManager
from ia.gaius.pvt import PerformanceValidationTest
from ia.gaius.thinkflux_client import TFClient

test_dir = Path(__file__).parent.resolve()
GENOME = test_dir.joinpath("genomes/simple.genome")


@pytest.mark.agentManager
def test_tf_client_setup(tmp_path: Path):
    genome_tmp_path = tmp_path.joinpath('./genomes')
    agents_tmp_path = tmp_path.joinpath('./agents')
    tf_tmp_path = tmp_path.joinpath('./thinkflux')
    comcom_tmp_path = tmp_path.joinpath('./comcom')
    am = AgentManager(genome_dir=genome_tmp_path,
                      agents_dir=agents_tmp_path,
                      thinkflux_dir=tf_tmp_path,
                      comcom_dir=comcom_tmp_path)

    am.kill_all_agents()
    am.start_hoster()
    am.update_current_agents()
    assert am.current_agents == {}

    agent = am.start_agent(genome_file=GENOME,
                           agent_id='pytester',
                           user_id='pytest',
                           agent_name='tf-agent',
                           connect_jia=False,
                           api_key='HELLO-WORLD').get_agent_client()

    am.start_tf(tf_name='main-tf',
                api_key="ABCD-1234",
                docker_image='registry.digitalocean.com/intelligent-artifacts/think-flux:develop',
                privileged=True,
                agents_to_connect=['tf-agent']
                )

    try:
        time.sleep(3)
        assert agent.connect() == {'agent': 'simple', 'connection': 'okay'}

        # setup TFClient
        tf_obj = am.current_tfs['main-tf']
        tf_port = tf_obj.port
        tf_info = {'name': 'main-tf',
                   'url': f'https://{tf_obj.container_name}:8080',
                   'api_key': 'ABCD-1234'}
        tf = TFClient(tf_info=tf_info, verify=False)

        assert tf.ping() == 'PONG'
        assert tf.show_status() == {'id': 'localhost',
                                    'message': 'show-status-called',
                                    'mood': {},
                                    'status': 'okay',
                                    'time_stamp': ANY}

        interface_info = agent.get_interface_node_config(
            interface_nodes=['P1'])

        assert tf.add_interface_nodes(interface_info) == {'id': 'localhost',
                                                          'message': 'tf-agent-set',
                                                          'mood': {},
                                                          'status': 'okay',
                                                          'time_stamp': ANY}

        assert tf.list_interface_nodes() == {
            '.gaius-api-pytest-pytester': ['P1']}

        assert tf.delete_interface_nodes(interface_info) == {'id': 'localhost',
                                                             'message': 'tf-agent-deleted',
                                                             'mood': {},
                                                             'status': 'okay',
                                                             'time_stamp': ANY}

        assert tf.list_interface_nodes() == {}

    finally:
        am.kill_all_agents()

@pytest.mark.skip(reason="Transitioning to using Hypotheses, currently broken")
@pytest.mark.agentManager
def test_tf_client_setup(tmp_path: Path):
    genome_tmp_path = tmp_path.joinpath('./genomes')
    agents_tmp_path = tmp_path.joinpath('./agents')
    tf_tmp_path = tmp_path.joinpath('./thinkflux')
    comcom_tmp_path = tmp_path.joinpath('./comcom')
    am = AgentManager(genome_dir=genome_tmp_path,
                      agents_dir=agents_tmp_path,
                      thinkflux_dir=tf_tmp_path,
                      comcom_dir=comcom_tmp_path)

    am.kill_all_agents()
    am.start_hoster()
    am.update_current_agents()
    assert am.current_agents == {}

    agent = am.start_agent(genome_file=GENOME,
                           agent_id='pytester',
                           user_id='pytest',
                           agent_name='tf-agent',
                           connect_jia=False,
                           api_key='HELLO-WORLD').get_agent_client()

    am.start_tf(tf_name='main-tf',
                api_key="ABCD-1234",
                docker_image='registry.digitalocean.com/intelligent-artifacts/think-flux:develop',
                privileged=True,
                agents_to_connect=['tf-agent']
                )

    try:
        time.sleep(3)
        assert agent.connect() == {'agent': 'simple', 'connection': 'okay'}

        # setup TFClient
        tf_obj = am.current_tfs['main-tf']
        tf_port = tf_obj.port
        tf_info = {'name': 'main-tf',
                   'url': f'https://{tf_obj.container_name}:8080',
                   'api_key': 'ABCD-1234'}

        tf = TFClient(tf_info=tf_info, verify=False)
        assert tf.ping() == 'PONG'

        interface_info = agent.get_interface_node_config(
            interface_nodes=['P1'])

        assert tf.add_interface_nodes(interface_info) == {'id': 'localhost',
                                                          'message': 'tf-agent-set',
                                                          'mood': {},
                                                          'status': 'okay',
                                                          'time_stamp': ANY}

        assert tf.list_interface_nodes() == {
            '.gaius-api-pytest-pytester': ['P1']}

        
        # Allocate Nodes for Training and Testing
        ingress_nodes = ["P1"]
        query_nodes = ["P1"]

        # Data settings
        GDF_DIR = test_dir.joinpath('./datasets/shuffled_iris_flowers')
        RESULTS_DIR = None
        
        agent.change_genes({'recall_threshold': 0.1})
        agent.change_genes({'max_predictions': 10})
        agent.change_genes({'near_vector_count': 3})

        data = Data(data_directories=[GDF_DIR])
        data.prep(percent_of_dataset_chosen=100,
                percent_reserved_for_training=80,
                shuffle=False)
        
        pvt = PerformanceValidationTest(
            agent=agent,
            ingress_nodes=ingress_nodes,
            query_nodes=query_nodes,
            test_count=1,
            dataset=data,
            results_filepath=RESULTS_DIR,
            test_type='classification',
            test_prediction_strategy="noncontinuous",
            clear_all_memory_before_training=True,
            turn_prediction_off_during_training=True,
            shuffle=False,
            QUIET=True,
            PLOT=False
        )
        pvt.conduct_pvt()
        
        tf.clear_concepts_and_instances()
        assert tf.get_concepts() == {}
        
        bootstrap_response = tf.bootstrap_concepts(labelled=True)
        assert bootstrap_response.status_code == 200
        # with open(test_dir.joinpath('./results/tf_bootstrap_results.json'), 'w') as f:
        #     json.dump(bootstrap_response.json()['message'], f)

        with open(test_dir.joinpath('./results/tf_bootstrap_results.json'), 'r') as f:
            KNOWN_BOOTSTRAP_RESULTS = json.load(f)
        assert bootstrap_response.json()['message'] == KNOWN_BOOTSTRAP_RESULTS
        
        assert tf.get_concepts() == KNOWN_BOOTSTRAP_RESULTS
        
        tf.clear_concepts_and_instances()
        
        bootstrap_response2 = tf.bootstrap_concepts(labelled=True, use_labels_for_concepts=True)
        assert bootstrap_response2.status_code == 200
        # with open(test_dir.joinpath('./results/tf_bootstrap_results2.json'), 'w') as f:
        #     KNOWN_BOOTSTRAP_RESULTS2 = json.dump(bootstrap_response2.json()['message'], f)

        with open(test_dir.joinpath('./results/tf_bootstrap_results2.json'), 'r') as f:
            KNOWN_BOOTSTRAP_RESULTS2 = json.load(f)
        assert bootstrap_response2.json()['message'] == KNOWN_BOOTSTRAP_RESULTS2

        
        labelled_concepts: dict = bootstrap_response2.json()['message']
        assert list(labelled_concepts.keys()) == ['setosa', 'versicolor', 'virginica']

    finally:
        am.kill_all_agents()
