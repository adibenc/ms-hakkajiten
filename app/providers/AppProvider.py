from masonite.providers import Provider
from masonite.facades import View
from masonite.environment import env
from masonite.helpers import url

class AppProvider(Provider):
	def __init__(self, application):
		self.application = application

	def register(self):
		rootdir = env('APPROOT')
		asset_url = env('APP_ASSET_URL')
		baseurl = url.url()
		View.share({
			'd1': "data x",
			'_baseurl': baseurl,
			'asset_url': asset_url,
			'__rootdir': rootdir,
		})
		pass

	def boot(self):
		pass
