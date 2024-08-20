from masonite.views import View
from masonite.controllers import Controller
from masonite.request import Request
from masonite.response import Response

class BaseController(Controller):
	"""BaseController Controller Class."""

	force_show_data = True

	def __init__(self):
		pass

	def base_json(self, request: Request, response: Response, http_code=200, code=None, success="success", msg="-", data=None):
		json = {
			"success": success if success else False,
			"message": msg,
		}

		if data or self.force_show_data:
			json["data"] = data

		if code:
			json["code"] = code

		return response.status(http_code).json(json)

	def success(self, request: Request, response: Response, msg="success", data=None, http_code=200):
		return self.base_json(request, response, http_code, msg=msg, data=data)

	def user_fail(self, request: Request, response: Response, msg="Maaf ada kesalahan user", data=None):
		return self.base_json(request, response, http_code=400, success=False, msg=msg, data=data)

	def validation_fail(self, request: Request, response: Response, http_code, msg, data):
		return self.base_json(request, response, http_code, success=False, msg=msg, data=data)

	def server_fail(self, request: Request, response: Response, msg, data={}):
		return self.base_json(request, response, http_code=500, success=False, msg=msg, data=data)

	def common_server_fail(self, request: Request, response: Response):
		return self.base_json(request, response, http_code=500, success=False, msg='Maaf, terjadi kegagalan pada server kami.', data={})
