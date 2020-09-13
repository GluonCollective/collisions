from flask import Flask
from flask_restful import Resource, Api
from event import generate_event

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class GenerateEvent(Resource):
    def get(self, process):
        return generate_event(process)

class GenerateEventDefault(Resource):
    def get(self):
        return generate_event()


api.add_resource(GenerateEvent, '/generate/<string:process>')
api.add_resource(GenerateEventDefault, '/generate')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')