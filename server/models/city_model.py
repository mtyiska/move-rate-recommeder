from db import db

class CityModel(db.Model):
	__tablename__ = 'cities'
	id =db.Column(db.Integer, primary_key=True)
	cityname = db.Column(db.String(80))
	rating = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	image = db.Column(db.String(80))
	# user_id = db.Column(db.Integer)

	user = db.relationship('UserModel')

	def __init__(self, cityname, rating, user_id, image):
		self.cityname = cityname
		self.rating = rating
		self.user_id = user_id
		self.image = image

	def json(self):
		return {'city_id':self.id,'cityname': self.cityname, 'rating': self.rating, 'user_id': self.user_id, 'image':self.image}


	@classmethod
	def find_by_name(cls, cityname):
		return cls.query.filter_by(cityname=cityname).first()

	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first()


	def save_to_db(self):
		db.session.add(self)
		db.session.commit()


	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

