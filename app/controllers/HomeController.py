"""A WelcomeController Module."""
from masonite.views import View
from masonite.controllers import Controller
from .BaseController import BaseController
from masonite.request import Request
from masonite.response import Response

class HomeController(BaseController):
	"""WelcomeController Controller Class."""

	def index(self, view: View):
		return view.render("welcome")
	
	def j1(self, req: Request, res: Response):
		return self.success(req, res, "Ok", {
			"d1": 1337
		})
