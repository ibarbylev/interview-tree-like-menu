from django import template
from django.shortcuts import get_object_or_404

from treelikemenu.models import MenuItem

register = template.Library()


@register.inclusion_tag('treelikemenu/nested-menu.html', takes_context=True)
def draw_menu(context, menu_title):

    current_item_id_str = context['request'].GET.get('item-id')
    current_item_id = int(current_item_id_str) if current_item_id_str else None

    items = MenuItem.objects.filter(menu__name=menu_title).values()

    # create tree for top items
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
            parent_item = walk(tree, parent_id, current_item_id)
            nested_items = parent_item.get('nested_items', [])
            new_item = items.filter(id=item['id']).values('id', 'name', 'slug')[0]
            nested_items.append(new_item)
            parent_item['nested_items'] = nested_items

    context['tree'] = tree
    # context['menu_title'] = menu_title
    return context

# {'id': 1, 'menu_id': 1, 'parent_id': None, 'name': 'first', 'slug': 'first'}


def walk(node, key, current_item_id):
    nested_items = node.get('nested_items')
    if nested_items:
        for d in nested_items:
            if d.get('id') == key:
                return d
            res = walk(d, key, current_item_id)
            if res:
                return res
            # if d.get('id') == current_item_id:
            #     break


