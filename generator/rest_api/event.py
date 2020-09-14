import subprocess
import pandas as pd

_generator_executable = '/pythia_interface/build/generate'


def get_available_processes():
    """Returns a list with the available processes. """
    available = subprocess.check_output(
        [_generator_executable] + ['--available-processes']).decode()
    available = available.replace('\n', '').replace(' ', '').split(',')

    return available


def _read_generated_particles(file):
    return pd.read_csv(file)


def _get_run_arguments(process, seed, n_events):
    arguments = []

    if process is not None:
        arguments += ['--process', str(process)]

    if seed is not None:
        arguments += ['--seed', str(seed)]

    if n_events is not None:
        arguments += ['--events', str(n_events)]
    return arguments


def generate_event(process: str = None,
                   seed: int = None,
                   n_events: int = None):
    """Generate events with pythia.

    Args:
        process: the physics process to be generated.
        seed: the random seed that will be used to generate the event.
        n_events: how many events pythia should generate.

    """
    arguments = _get_run_arguments(process, seed, n_events)

    generator = subprocess.run([_generator_executable] + arguments,
                               stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    generator.check_returncode()

    particles = _read_generated_particles("/tmp/particles.csv")
    mothers = _read_generated_particles("/tmp/mothers.csv")
    daughters = _read_generated_particles("/tmp/daughters.csv")

    return {'particles': particles.to_dict(),
            'mothers': mothers.to_dict(),
            'daughters': daughters.to_dict()}
