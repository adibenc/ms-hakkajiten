from masonite.providers import Provider
from masonite.facades import View


class AppProvider(Provider):
	def __init__(self, application):
		self.application = application

	def register(self):
		View.share({
			'd1': "data x"
		})
		pass

	def boot(self):
		pass
