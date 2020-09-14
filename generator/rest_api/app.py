from flask import Flask
from flask_restful import Resource, Api, reqparse
from event import generate_event, get_available_processes

app = Flask(__name__)
api = Api(app)


class AvailableProcesses(Resource):
    def get(self):
        return {'process': get_available_processes()}


class GenerateEvent(Resource):
    def __init__(self):
        super(Resource, self).__init__()
        self.req_parser = reqparse.RequestParser()

        self.req_parser.add_argument('process',
                                     type=str,
                                     help='The physics process to be generated.',
                                     default=None)

        self.req_parser.add_argument('seed',
                                     type=int,
                                     help='the random seed that will be used to generate the event.',
                                     default=None)

        self.req_parser.add_argument('n_events',
                                     type=int,
                                     help='how many events pythia should generated.',
                                     default=None)
        self.args = self.req_parser.parse_args()

    def get(self):
        return generate_event(self.args['process'], self.args['seed'], self.args['n_events'])


class GenerateEventDefault(Resource):
    def get(self):
        return generate_event()


api.add_resource(GenerateEvent, '/generate')
api.add_resource(AvailableProcesses, '/processes')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
