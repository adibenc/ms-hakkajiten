from masonite.providers import Provider
from masonite.facades import Auth
from masonite.facades import View
from masonite.environment import env
from masonite.helpers import url
# from masonite.authentication import Auth


class AppProvider(Provider):
	def __init__(self, application):
		self.application = application

	def register(self):
		rootdir = env('APPROOT')
		asset_url = env('APP_ASSET_URL')
		baseurl = url.url()
		
		# user = auth.user()
		# print("prov", user)

		print("x1")
		View.share({
			'd1': "data x",
			'_baseurl': baseurl,
			'asset_url': asset_url,
			'__rootdir': rootdir,
		})
		# pass

	def boot(self):
		# pass
		print("boot")
		print("dir(Auth)")
		print(dir(Auth))
		user = Auth.user()
		
		user = {
			'_user': 22
		}
		user = 22
		d = {
			'd1': "data x2",
			'_user': user
		}
		print("x2")
		print(d)
		View.share(d)
		View.composer("*", d)
