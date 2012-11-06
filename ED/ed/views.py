from pyramid.view import view_config

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project':'ED'}


@view_config(route_name='main', renderer='main.mak')
def main(request):
    return {'project':'ED'}
