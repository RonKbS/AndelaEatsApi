from app.controllers.base_controller import BaseController


class BotController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)

	def bot(self):
		pass

	def interactions(self):
		pass