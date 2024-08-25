import os
import re

from masonite.controllers import Controller
from masonite.views import View
from masonite.environment import env
from masonite.request import Request
from masonite.response import Response

from .BaseController import BaseController
from app.helpers.common import scan_dir_rc

class ArtController(BaseController):
	prename = "reddits"

	def index(self, view: View):
		return view.render("admin/d1/index")

	def list(self, req: Request, res: Response, view: View):
		try:
			prename = self.prename
			rootdir = env('APPROOT')
			fname = f"{rootdir}templates/{prename}"
			print(fname)
			
			list_of_files = scan_dir_rc(fname)
			list_of_files = map(lambda x: 
				re.sub('(\.html$|\.php$)', '', x), 
				list_of_files)
			# print(list_of_files)
			# wip use auth mw
			vr = f"{prename}.list"
			print("vr", vr)

			return view.render(vr, {
				"prename": prename, 
				"files": list_of_files
			})
		except Exception as e:
			return self.fail(req, res, str(e), [1])

	def d(self, req: Request, res: Response, view: View, f=None):
		try:
			prename = self.prename
			f = f or "f3-bio"
			return view.render(f"{prename}/{f}")
		except Exception as e:
			return self.fail(req, res, str(e), [1])

	def dc(self, req: Request, res: Response, view: View,):
		# f, c=None, c1=None, c2=None,

		try:
			prename = self.prename
			ps = req.params
			
			c = ps.get('c')
			f = ps.get('f')
			
			# wip use auth mw
			c1 = ps.get('c1')
			c2 = ps.get('c2')

			f = f or "f3-bio"
			if c and f:
				return view.render(f"{prename}.{c}.{f}")
			
			if c1 and c2 and f:
				return view.render(f"{prename}.{c1}.{c2}.{f}")
		except Exception as e:
			return self.fail(req, res, str(e), [1])

	@property
	def prename(self):
		return self._prename

	@prename.setter
	def prename(self, value):
		self._prename = value