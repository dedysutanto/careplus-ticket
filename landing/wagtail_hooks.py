from wagtail import hooks

@hooks.register('construct_main_menu')
def hide_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != 'help']
    if not request.user.is_superuser:
        menu_items[:] = [item for item in menu_items if item.name != 'reports']
