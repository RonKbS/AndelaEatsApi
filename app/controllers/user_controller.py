from app.controllers.base_controller import BaseController

class UserController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
	