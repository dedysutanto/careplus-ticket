from wagtail.core import hooks

@hooks.register('construct_main_menu')
def hide_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != 'help']
