from flask import Flask, render_template, g, jsonify, json, request
import os
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.city import City, CityList
from resources.user import UserRegister, UserByName

from models.city_model import CityModel
import sqlite3
import pandas as pd
import numpy as np


DEBUG = True
PORT = 4200
HOST = '127.0.0.1'

app = Flask(__name__, template_folder='.')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)
api = Api(app)


@app.before_first_request
def create_tables():
	db.create_all()

# /auth
jwt = JWT(app, authenticate, identity)
api.add_resource(CityList, '/cities')
api.add_resource(City, '/city/<int:id>')
api.add_resource(UserRegister, '/user/<int:id>')
api.add_resource(UserByName, '/user/<string:name>')


@app.route('/', methods=['POST','GET'])
def get_all():
	username ='admin1'
	conn = sqlite3.connect('data.db')
	myratings = pd.read_sql("SELECT * FROM cities WHERE user_id ='9'", conn)
	conn.close()

	# recomender
	index = 'user_id'
	columnName = 'cityname'
	metric = 'rating'

	# City Ratings = pivot of ratings
	# userRatings = myratings.pivot_table(index=[index],columns=[columnName],values=metric)
	alldata = myratings.to_json()
	# print(alldata)
	return alldata


@app.route('/update', methods=['POST','GET'])
def updateRecommendations():
	data = request.get_json()
	print(data)
	username ='admin1'
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	query = "UPDATE cities SET rating=? WHERE user_id =? AND cityname=?"
	result = cursor.execute(query, (data['rating'], data['userid'], data['cityname']))
	row = result.fetchone()
	conn.commit()
	conn.close()

	return 'alldata'



@app.route('/myrec', methods=['POST','GET'])
def get_data():
	username ='admin1'
	conn = sqlite3.connect('data.db')
	ratings = pd.read_sql('SELECT * FROM cities', conn)
	myratings = pd.read_sql("SELECT * FROM cities WHERE user_id ='67'", conn)

	conn.close()

	# recomender
	index = 'user_id'
	columnName = 'cityname'
	metric = 'rating'

	# City Ratings = pivot of ratings
	userRatings = ratings.pivot_table(index=[index],columns=[columnName],values=metric)


	ratingStats = ratings.groupby(columnName).agg({metric:[np.size, np.mean]})
	ratingStats.sort_values((metric,'size'), ascending=False, inplace=True)

	threshold = ratingStats[(metric,'size')].mean()
	correltionMethod ='pearson'
	# similarMoves = correlations with all cities but only cities where more than the threshold rated
	corrMatrix = userRatings.corr(method=correltionMethod, min_periods=threshold)
	corrWith = userRatings.corrwith(userRatings['Los Angeles'])

	# This builds the ratings for specific user
	temp = userRatings.copy()
	temp = temp.reset_index()
	myindex = temp.index.values[temp[index]==67+1]
	myRatings = userRatings.iloc[myindex[0]].dropna()

	# Find Recommended Movies
	simCandidates = pd.Series()
	# correlate each of my ratings with ratings of the whole
	for i in range(0, len(myRatings.index)):
		sims = userRatings.corrwith(userRatings[myRatings.index[i]]).dropna()
		sims = sims.map(lambda x: x* myRatings[i])
		simCandidates = simCandidates.append(sims)

	simCandidates = simCandidates.groupby(simCandidates.index).sum()
	simCandidates.sort_values(inplace=True, ascending = False)
	filteredSims = simCandidates.drop(myRatings.index)
	filteredSims = simCandidates.to_frame(name=None)
	filteredSims.rename(index=str, columns={0: metric}, inplace=True)
	filteredSims[metric] = filteredSims[metric].astype(int)
	suggestedCity = filteredSims.head(7).to_dict()
	print(suggestedCity)


	# print("**** RECOMMENDED ********")
	# print(filteredSims)
	# print("***** MY RATINGS ********")
	# print(myRatings)
	# print("****** ALL RATINGS *******")
	# print(ratings)
	# print("****** CORRELATION *******")
	# print(corrMatrix)

	# print(simCandidates)

	mydata = jsonify(suggestedCity)


	return mydata



if __name__ == '__main__':
	from db import db 
	db.init_app(app)
	app.run(host=HOST, port=PORT, debug=DEBUG)




