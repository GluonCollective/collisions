import requests
import pandas as pd

_event_url = 'http://generator:5000/'


def _add_to_arguments(arg_dict, argument_name, argument_value):
    if argument_value is not None:
        arg_dict[argument_name] = str(argument_value)


def generate_event(process=None, seed=None, n_events=None):
    arguments = dict()

    _add_to_arguments(arguments, 'process', process)
    _add_to_arguments(arguments, 'seed', seed)
    _add_to_arguments(arguments, 'n_events', n_events)

    url = _event_url + 'generate'

    if len(arguments) > 0:
        url += '?'

    for name, value in arguments.items():
        url += f'&{name}={value}'

    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(
            'It was not possible to obtain this event. Check the input values.')

    json_response = response.json()

    particles = json_response['particles']
    mothers = json_response['mothers']
    daughters = json_response['daughters']

    if n_events is not None and n_events > 1:
        particles_list = [x[1].reset_index(drop=True)
                          for x in pd.DataFrame(particles).groupby('event')]

        mothers_list = [x[1].reset_index(drop=True)
                        for x in pd.DataFrame(mothers).groupby('event')]

        daughters_list = [x[1].reset_index(drop=True)
                          for x in pd.DataFrame(daughters).groupby('event')]

        return [Event(p, m, d)
                for p, m, d in zip(particles_list, mothers_list, daughters_list)]

    return Event(particles, mothers, daughters)


class Event:
    def __init__(self, particles, mothers, daughters):
        self.particles = pd.DataFrame(particles)
        self.mothers = pd.DataFrame(mothers)
        self.daughters = pd.DataFrame(daughters)
