import json
import pathlib
import os
from ia.scripts.spawn_agent import retrieve_genome

test_dir = pathlib.Path(__file__).parent.resolve()
GENOME = test_dir.joinpath("./genomes/simple.genome")


def test_retrieve_genome_path():
    """Attempt genome retrieval by path
    """

    genome = retrieve_genome(str(GENOME.absolute()))
    genome2 = retrieve_genome(str(GENOME.relative_to(os.getcwd())))

    assert genome.topology == genome2.topology

    # testing using pathlib Path
    genome3 = retrieve_genome(GENOME.relative_to(os.getcwd()))


def test_retrieve_genome_json():
    """Attempt genome retrieval by path
    """
    with open(GENOME) as f:
        genome_str = f.read()
        f.seek(0)
        json_obj = json.load(f)

    genome = retrieve_genome(json_obj)
    genome2 = retrieve_genome(json.dumps(json_obj))
    genome3 = retrieve_genome(genome_str)

    assert genome.topology == genome2.topology
    assert genome2.topology == genome3.topology
