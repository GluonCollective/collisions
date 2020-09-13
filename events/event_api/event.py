import subprocess
import pandas as pd


def _read_generated_particles(file):
    return pd.read_csv(file).drop(['event'], axis='columns')

def generate_event(process: str = None,
                   seed: int = None,
                   n_events: int = None,
                   generator_executable='/collisions/build/generate'):
    """Generate an event with pythia.

    Args:
        process: the physics process to be generated.
        seed: the random seed that will be used to generate the event.
        n_events: how many events pythia should generate.

    """
    arguments = []

    if process is not None:
        arguments += ['--process', process]

    if seed is not None:
        arguments += ['--seed', seed]

    if n_events is not None:
        arguments += ['--events', n_events]

    generator = subprocess.run([generator_executable] + arguments,
                               stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    generator.check_returncode()
    

    particles = _read_generated_particles("/tmp/particles.csv")
    mothers = _read_generated_particles("/tmp/mothers.csv")
    daughters = _read_generated_particles("/tmp/daughters.csv")

    return {'particles': particles.to_dict(), 'mothers': mothers.to_dict(), 'daughters': daughters.to_dict()}
