from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.city_model import CityModel
import sqlite3
from flask import render_template
import pandas as pd
from flask import Flask, request


class City(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('user_id',type=int,required=True,help="Every city needs a store id")
	# limit to passing only certain data
	parser.add_argument('rating',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )


	# @jwt_required()
	def get(self, id):
		city = CityModel.find_by_id(id)
		if city:
			return city.json()
		return {'message': 'City not found'}, 404


	# @jwt_required()
	def post(self, name):
		if CityModel.find_by_name(name):
			return {'message': "An city with name '{}' already exists. ".format()}, 400

		data = City.parser.parse_args()
		city = CityModel(name, **data)

		try:
			city.save_to_db()
		except:
			return {"message": "An error occurred inserting the city."}, 500
		return city.json(), 201


	# @jwt_required()
	def delete(self, name):
		city = city.find_by_name(name)
		if city:
			city.delete_from_db()
		return {'message': 'City deleted'}

	# @jwt_required()
	def put(self, id):
		data = request.get_json()
		city = CityModel.find_by_id(data['id'])

		city.rating = data['rating']

		print(data)

		city.save_to_db()
		return city.json()


class CityList(Resource):
	def get(self):
		# return {'cities': [city.json() for city in CityModel.query.all()]}
		data = {'cities': [city for city in CityModel.query.all()]}
		df = pd.DataFrame.from_dict(data, orient='columns', dtype=None)

		# return render_template('templates/batchresult.html', mydata=[df.head(5).to_html()])
		return render_template('templates/batchresult.html')





