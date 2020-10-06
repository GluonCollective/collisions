from functools import cached_property

import numpy as np
import pandas as pd
import requests

_event_generator_api_url = 'http://generator:5000/'


def _add_to_arguments(arg_dict, argument_name, argument_value):
    """Add a variable to the argument dict that will be requested to the event generation API.

    Args:
        arg_dict: dictionary with the arguments.
        argument_name: name of the variable in the API (key in the dict).
        argument_value: value of the variable in the API (value in the dict).
    """
    if argument_value is not None:
        arg_dict[argument_name] = str(argument_value)


def _separate_by_event(events):
    return [x[1] for x in pd.DataFrame(events).groupby('Event')]


def available_processes():
    """Returns a list with the available physical processes. """
    server_response = requests.get(_event_generator_api_url + 'processes')
    if server_response.status_code != 200:
        raise RuntimeError("The event generator server did not answer with a "
                           "valid message.")
    return server_response.json()['processes']


def generate_event(process=None, seed=None, n_events=None):
    """Generate events with pythia.
    Args:
        process: the physics process to be generated. You can check the
                 available processes by calling available_processes()
        seed: the random seed that will be used to generate the event.
        n_events: how many events pythia should generate.

    Returns:
        A list with n_events Events.
    """
    arguments = dict()

    _add_to_arguments(arguments, 'process', process)
    _add_to_arguments(arguments, 'seed', seed)
    _add_to_arguments(arguments, 'n_events', n_events)

    url = _get_generator_url(arguments)

    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError('It was not possible to obtain this event. Check the input values.')

    json_response = response.json()

    particles_list = _separate_by_event(json_response['particles'])
    mothers_list = _separate_by_event(json_response['mothers'])
    daughters_list = _separate_by_event(json_response['daughters'])

    return [Event(part, mother, daughter)
            for part, mother, daughter in
            zip(particles_list, mothers_list, daughters_list)]


def _get_generator_url(arguments: dict):
    """Builds the URL to be requested in the generation API.

    Args:
        arguments: a dict with the arguments to be passed to the API.

    Returns:
        The url passing the values of arguments to api.
    """
    url = _event_generator_api_url + 'generate'
    if len(arguments) > 0:
        url += '?'
        for name, value in arguments.items():
            url += f'&{name}={value}'
    return url


def _make_clean_dataframe(df):
    return pd.DataFrame(df).drop('Event', axis='columns').set_index('Id')


def _add_line_continuation(particles, alpha, suffix):
    """ In case of stable particles, there is no sensible approach to decide until when the trajectories should be
    shown (it should be, technically, until infinite!). I have opted to show them for a fixed path.

    Args:
        particles: a dataframe with the particle information.
        alpha: for how long should stable tracks should be propagated.
        suffix: suffix to be added to the "vertex" (point) until when the trajectory should be drawn.
    Returns:
        A new dataframe with the addiction of the (point) until when the trajectory should be drawn.
    """
    df = particles.copy()
    total_momentum = np.sqrt(df['Px'] ** 2 + df['Py'] ** 2 + df['Pz'] ** 2)

    distance_to_propagate = alpha - _distances_to_primary_vertex(df)

    df['Vx' + suffix] = df['Vx'] + distance_to_propagate * df['Px'] / total_momentum
    df['Vy' + suffix] = df['Vy'] + distance_to_propagate * df['Py'] / total_momentum
    df['Vz' + suffix] = df['Vz'] + distance_to_propagate * df['Pz'] / total_momentum
    return df


def calculate_trajectories(particles, daughters, alpha=1.):
    """Calculates the trajectories of the particles.

    Args:
        particles: a dataframe with the particle information.
        daughters: a dataframe where each line represents a daughter for the particles.
        alpha: for how long should stable tracks should be propagated.
    """

    particles_for_lines = particles.copy()

    distances_to_primary_vertex = _distances_to_primary_vertex(particles_for_lines)

    alpha = 1.1 * distances_to_primary_vertex.max()

    particles_for_lines['NDaughters'] = daughters.groupby('Id').apply(len)
    particles_for_lines['NDaughters'] = particles_for_lines['NDaughters'].fillna(0.).astype(int)

    # Particles with daughters
    lines_daughters = particles_for_lines.join(daughters, how='inner')
    lines_daughters = lines_daughters.join(particles_for_lines[['Vx', 'Vy', 'Vz']], on='DaughterId', rsuffix='_decay')

    # Particles WITHOUT daughters
    lines_single = _add_line_continuation(particles_for_lines[particles_for_lines['NDaughters'] == 0], alpha, '_decay')

    lines = pd.concat([lines_daughters, lines_single])
    decay_length = _decay_length(lines)

    return lines[decay_length > 0]


def _distances_to_primary_vertex(particles_for_lines):
    distances_to_primary_vertex = np.sqrt(particles_for_lines['Vx'] ** 2 +
                                          particles_for_lines['Vy'] ** 2 +
                                          particles_for_lines['Vz'] ** 2)
    return distances_to_primary_vertex


def _decay_length(df, suffix='_decay'):
    decay_length = np.sqrt((df['Vx'] - df['Vx' + suffix]) ** 2 +
                           (df['Vy'] - df['Vy' + suffix]) ** 2 +
                           (df['Vz'] - df['Vz' + suffix]) ** 2)
    return decay_length


class Event:
    """Represents the products of the collision. """

    def __init__(self, particles, mothers, daughters):
        self.particles = _make_clean_dataframe(particles)
        self.mothers = _make_clean_dataframe(mothers)
        self.daughters = _make_clean_dataframe(daughters)

    @cached_property
    def trajectories(self):
        """Returns the trajectories to be drawn for this event. """
        return calculate_trajectories(self.particles, self.daughters)

    def __repr__(self):
        return f"<{str(self.__class__.__name__)} with {len(self.particles)} particles>"
