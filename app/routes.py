from flask_restful import Resource

class UserResource(Resource):
    def get(self):
        return {"message": "List of users"}

def initialize_routes(api):
    api.add_resource(UserResource, '/users')
