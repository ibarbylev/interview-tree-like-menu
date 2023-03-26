from django import template
from django.shortcuts import get_object_or_404

from treelikemenu.models import MenuItem, Menu

register = template.Library()


@register.inclusion_tag('treelikemenu/nested-menu.html', takes_context=True)
def draw_menu(context, menu_title):
    items = MenuItem.objects.filter(menu__name=menu_title).values()
    tree = {'nested_items': list(items.filter(parent_id=None).values('id', 'name', 'slug'))}

    # get indexes for all levels
    # levels = []
    # level = 1
    # while level <= len(levels):
    #     for item in items:
    #         if item['parent_id'] in levels[level-1]:
    #             if level+1 > len(levels):
    #                 levels.append([])
    #             levels[level].append(item['id'])
    #
    #     level += 1

    # fill in tree dictionary
    for item in items:
        parent_id = item.get('parent_id')
        if parent_id is not None:
            parent_item = walk(tree, parent_id)
            nested_items = parent_item.get('nested_items', [])
            new_item = items.filter(id=item['id']).values('id', 'name', 'slug')[0]
            nested_items.append(new_item)
            parent_item['nested_items'] = nested_items

    context['tree'] = tree
    return context

# {'id': 1, 'menu_id': 1, 'parent_id': None, 'name': 'first', 'slug': 'first'}


def walk(node, key):
    nested_items = node.get('nested_items')
    if nested_items:
        for d in nested_items:
            if d.get('id') == key:
                return d
            res = walk(d, key)
            if res:
                return res



