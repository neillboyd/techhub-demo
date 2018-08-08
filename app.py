from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

animals = [
    {
        "animal_name": "dog",
        "noise": "bark"
    },
    {
        "animal_name": "cat",
        "noise": "meow"
    }
]

class Animal(Resource):
    def get(self, animal_name):
        for animal in animals:
            if(animal_name == animal["animal_name"]):
                return animal, 200
        return "Animal not found", 404

    def post(self, animal_name):
        parser = reqparse.RequestParser()
        parser.add_argument("noise")
        args = parser.parse_args()

        for animal in animals:
            if(animal_name == animal["animal_name"]):
                return "Animal with name {} already exists".format(animal_name), 400

        animal = {
            "animal_name": animal_name,
            "noise": args["noise"],
        }
        animals.append(animal)
        return animal, 201

    def delete(self, animal_name):
        global animals
        animals = [animal for animal in animals if animal["animal_name"] != animal_name]
        return "{} is deleted.".format(animal_name), 200
      
api.add_resource(Animal, "/animal/<string:animal_name>")

app.run(host="0.0.0.0", debug=True, port=80)