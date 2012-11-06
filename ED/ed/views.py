from pyramid.view import view_config


@view_config(route_name='main', renderer='main.mak')
def main(request):
    return {'project':'ED'}
