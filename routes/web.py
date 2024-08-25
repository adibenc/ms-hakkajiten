from masonite.routes import Route

ROUTES = [
	# Route.get("/", "WelcomeController@show"),
	Route.get("/", "HomeController@index"),
	Route.get("/j1", "HomeController@j1"),

	Route.get("wiki/", "WikiController@list"),
	Route.get("wiki/list", "WikiController@list"),
	Route.get("wiki/d/@f", "WikiController@d"),
	Route.get("wiki/c/@c/@f", "WikiController@dc"),
	Route.get("wiki/c/@c1/@c2/@f", "WikiController@dc"),
]
