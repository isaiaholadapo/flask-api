from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://tutorial:tutorial@localhost/flask_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())


class CreateUser(Resource):
    response = {
        "status": 400,
        "message": "User not created"
    }

    def post(self):
        user_data = request.get_json()
        first_name = user_data['first_name']
        last_name = user_data['last_name']
        email = user_data['email']
        user = User(first_name=first_name, last_name=last_name, email=email)
        db.session.add(user)
        db.session.commit()

        self.response['status'] = 201
        self.response['message'] = 'User created successfully'

        return self.response, 201


class Users(Resource):
    response = {
        "status": 404,
        "message": "Users not available"
    }
    def get(self):
        users = User.query.all()
        if users:
            all_users = []
            for user in users:
                user_details = {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                }
                all_users.append(user_details)
            self.response['status'] = 200
            self.response['message'] = all_users
            return self.response, 200
        else:
            return self.response, 404


class GetUser(Resource):
    response = {
        "status": 404,
        "message": "Users not available"
    }

    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            user_details = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            self.response['status'] = 200
            self.response['message'] = user_details

            return self.response, 200
        else:
            return self.response, 404


class UpdateUser(Resource):
    response = {
        "status": 404,
        "message": "Users not available"
    }

    def put(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            user_data = request.get_json()
            first_name = user_data['first_name']
            last_name = user_data['last_name']
            email = user_data['email']
            user.first_name = first_name
            user.last_name = last_name
            user.email = email

            db.session.commit()
            self.response['status'] = 200
            self.response['message'] = 'User updated successfully'
            return self.response, 200
        else:
            return self.response, 404


class DeleteUser(Resource):
    response = {
        "status": 404,
        "message": "User not available"
    }

    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            self.response['status'] = 200
            self.response['message'] = 'User deleted successfully'
            return self.response, 200
        else:
            return self.response, 404


api.add_resource(CreateUser, '/api/create')
api.add_resource(Users, '/api/users')
api.add_resource(GetUser, '/api/user/<int:user_id>/')
api.add_resource(UpdateUser, '/api/update/<int:user_id>')
api.add_resource(DeleteUser, '/api/delete/<int:user_id>')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)
    db.create_all()
