from wagtail.core import hooks

@hooks.register("construct_settings_menu")
def hide_user_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != "help"]
