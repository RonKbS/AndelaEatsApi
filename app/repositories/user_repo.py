from app.repositories.base_repo import BaseRepo
from app.models.user import User

class UserRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, User)
		
	def new_user(self, email, first_name, last_name, image, location):
		user = User(email=email, first_name=first_name, last_name=last_name, image=image, location=location)
		user.save()
		return user
	
	def find_or_create(self, **user):
		email = user['email']
		user = self.filter_by(**{'email':email})
		if user:
			return user
		else:
			try:
				first_name = user['first_name']
				last_name = user['last_name']
				image = user['image']
				location = user['location']
				user = self.new_user(email, first_name, last_name, image, location)
				return user
			except Exception as e:
				return None