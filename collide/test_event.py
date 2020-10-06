import pytest
from event import Event


def example_event():
    particles = {'Event': [0, 0, 0, 0, 0, 0, 0],
                 'Id': [0, 1, 2, 3, 4, 5, 6],
                 'PdgCode': [0, 1, 1, 2, 2, 2, 2],
                 'E': [4., 2., 2., 1., 1., 1., 1.],
                 'Px': [0., 1., -1., 0.5, 0.5, -0.5, -0.5],
                 'Py': [0., -1., 1., -0.5, 0.5, -0.5, 0.5],
                 'Pz': [0., 0., 0., 0., 0., 0., 0.],
                 'Vx': [0., 0., 0., -1., -1, 1., 1.],
                 'Vy': [0., 0., 0., 0., 0., 0., 0.],
                 'Vz': [0., 0., 0., 0., 0., 0., 0.],
                 'Vt': [0., 0., 0., 0., 0., 0., 0.]}
    mothers = {'Event': [0, 0, 0, 0, 0, 0],
               'Id': [1, 2, 3, 4, 5, 6],
               'MotherId': [0, 0, 1, 1, 2, 2]}
    daughters = {'Event': [0, 0, 0, 0, 0, 0],
                 'Id': [0, 0, 1, 1, 2, 2],
                 'DaughterId': [1, 2, 3, 4, 5, 6]}

    return Event(particles, mothers, daughters)


print(example_event().trajectories)


def test_connect_vertexes():
    pass
