import sqlite3
from flask_restful import Resource, reqparse
from models.user_model import UserModel

class UserRegister(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
        required=True,
        help="This field cannot be left blank!"
	)

	parser.add_argument('password',
		type=str,
        required=True,
        help="This field cannot be left blank!"
	)

	def get(self, id):
		# data = UserModel.find_by_username(name)
		data = UserModel.find_by_id(id)
		if data:
			return data.json()
		return {'message': 'User not found'}, 404

	def post(self, name):
		# if UserModel.find_by_username(data['username']):
		if UserModel.find_by_username(name):
			return {'message': "A user with that username already exists."}, 400

		data = UserRegister.parser.parse_args()
		user = UserModel(**data)
		user.save_to_db()

		return user.json(), 201

class UserByName(Resource):
	def get(self, name):
		data = UserModel.find_by_username(name)
		if data:
			return data.json()
		return {'message': 'User not found'}, 404

		