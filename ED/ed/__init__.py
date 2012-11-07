from pyramid.config import Configurator
import urllib2
from views import GraphController



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=0)
    config.add_route('main', '/')
    config.add_route('count', '/count')
    config.add_route('betweenness', '/betweenness')
    config.add_route('random', '/random')
    config.add_route('page_rank', '/page_rank')
    config.scan()
    return config.make_wsgi_app()
