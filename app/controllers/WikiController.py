import os
from masonite.controllers import Controller
from masonite.views import View
from .ArtController import ArtController

class WikiController(ArtController):
	prename = "wiki"