from masonite.routes import Route

ROUTES = [
	# Route.get("/", "WelcomeController@show"),
	Route.get("/", "HomeController@index"),
	Route.get("/j1", "HomeController@j1"),
]
