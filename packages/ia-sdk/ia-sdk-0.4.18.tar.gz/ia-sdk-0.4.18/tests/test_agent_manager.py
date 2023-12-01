import pytest
from ia.gaius.manager import AgentManager
from pathlib import Path
import time
import traceback
import docker

test_dir = Path(__file__).parent.resolve()
GENOME = test_dir.joinpath("genomes/simple.genome")


@pytest.mark.agentManager
def test_agent_manager_simple_spawn(tmp_path: Path):

    genome_tmp_path = tmp_path.joinpath('./genomes')
    agents_tmp_path = tmp_path.joinpath('./agents')
    tf_tmp_path = tmp_path.joinpath('./thinkflux')
    comcom_tmp_path = tmp_path.joinpath('./comcom')
    am = AgentManager(genome_dir=genome_tmp_path, agents_dir=agents_tmp_path,
                      thinkflux_dir=tf_tmp_path, comcom_dir=comcom_tmp_path)

    am.kill_all_agents()
    am.start_hoster()
    am.update_current_agents()
    assert am.current_agents == {}

    try:
        agent = am.start_agent(genome_file=GENOME,
                               agent_id='pytester',
                               user_id='pytest',
                               agent_name='pytest1',
                               connect_jia=False,
                               api_key='HELLO-WORLD').get_agent_client()

        time.sleep(3)

        assert agent._api_key == 'HELLO-WORLD'
        assert agent.connect() == {'agent': 'simple', 'connection': 'okay'}
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
                                       'vectors_kb': '{KB| objects: 0}',
                                       }
        assert am.get_all_agent_status() == {'pytest1': True}
        assert am.list_genomes() == ['simple.genome']

        try:
            am.delete_genome(genome_name='simple.genome')
            pytest.fail(
                'deleting genome of active agent should throw exception')
        except Exception as error:
            pass

    except Exception as error:
        traceback.print_exc()

    finally:
        am.kill_all_agents()
        am.stop_hoster()


@pytest.mark.agentManager
def test_agent_manager_orphan_agent(tmp_path: Path):

    genome_tmp_path = tmp_path.joinpath('./genomes')
    agents_tmp_path = tmp_path.joinpath('./agents')
    tf_tmp_path = tmp_path.joinpath('./thinkflux')
    comcom_tmp_path = tmp_path.joinpath('./comcom')

    am = AgentManager(genome_dir=genome_tmp_path,
                      agents_dir=agents_tmp_path,
                      thinkflux_dir=tf_tmp_path,
                      comcom_dir=comcom_tmp_path)

    am.start_hoster()
    am.update_current_agents()
    assert am.current_agents == {}

    try:
        agent = am.start_agent(genome_file=GENOME,
                               agent_id='pytester',
                               user_id='pytest',
                               agent_name='pytest2',
                               connect_jia=False,
                               api_key='HELLO-WORLD').get_agent_client()

        time.sleep(3)

        assert agent._api_key == 'HELLO-WORLD'
        assert agent.connect() == {'agent': 'simple', 'connection': 'okay'}
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
                                       'vectors_kb': '{KB| objects: 0}',
                                       }

        docker_client = docker.from_env()
        gapi = docker_client.containers.get('gaius-api-pytest-pytester')
        gapi.stop()

        am.remediate_dead_agents()
        am.update_current_agents()
        assert am.current_agents == {}

    finally:
        am.kill_all_agents()


@pytest.mark.agentManager
def test_am_spawn_thinkflux(tmp_path: Path):

    genome_tmp_path = tmp_path.joinpath('./genomes')
    agents_tmp_path = tmp_path.joinpath('./agents')
    tf_tmp_path = tmp_path.joinpath('./thinkflux')
    comcom_tmp_path = tmp_path.joinpath('./comcom')

    am = AgentManager(genome_dir=genome_tmp_path,
                      agents_dir=agents_tmp_path,
                      thinkflux_dir=tf_tmp_path,
                      comcom_dir=comcom_tmp_path)

    am.start_hoster()
    am.update_current_agents()
    assert am.current_agents == {}

    try:
        agent = am.start_agent(genome_file=GENOME,
                               agent_id='pytester',
                               user_id='pytest',
                               agent_name='pytest2',
                               connect_jia=False,
                               api_key='HELLO-WORLD').get_agent_client()

        time.sleep(3)

        assert agent._api_key == 'HELLO-WORLD'
        assert agent.connect() == {'agent': 'simple', 'connection': 'okay'}
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
                                       'vectors_kb': '{KB| objects: 0}',
                                       }

        tf = am.start_tf(tf_name='test1',
                         api_key="ABCD-1234",
                         docker_image='registry.digitalocean.com/intelligent-artifacts/think-flux:develop',
                         privileged=True,
                         agents_to_connect=['pytest2']
                         )

        tf.kill()
        
        docker_client = docker.from_env()
        gapi = docker_client.containers.get('gaius-api-pytest-pytester')
        gapi.stop()

        am.remediate_dead_agents()
        am.update_current_agents()
        assert am.current_agents == {}

    finally:
        am.kill_all_agents()
