"""
Add dict { menu_name: menu_slag } to save on 1 request and
meet the requirements of the terms of reference.
"""
from treelikemenu.models import Menu


def menu_dict(request):
    menus = Menu.objects.all().values('name', 'slug')
    d = {}
    for menu in menus:
        d[menu['name']] = menu['slug']

    return d
