from pyramid.view import view_config

@view_config(route_name='graph', renderer='empty.mak')
def graph(request):
    
    return {}
