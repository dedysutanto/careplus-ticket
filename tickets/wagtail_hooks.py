from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import Tickets, TicketsClass, TicketsUsed, TicketsClassChild


class TicketsUsedAdmin(ModelAdmin):
    model = TicketsUsed
    base_url_path = 'tickets' # customise the URL from default to admin/bookadmin
    menu_label = 'Tickets'  # ditch this to use verbose_name_plural from model
    menu_icon = 'form'  # change as required
    menu_order = 220  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('ticket', 'uuid', 'is_used', 'qr_ticket')
    search_fields = ('uuid', 'ticket__name')


class TicketsClassAdmin(ModelAdmin):
    model = TicketsClass
    base_url_path = 'ticketsclass' # customise the URL from default to admin/bookadmin
    menu_label = 'Tickets Class'  # ditch this to use verbose_name_plural from model
    menu_icon = 'list-ol'  # change as required
    menu_order = 205  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('name', 'price', 'seats')


class TicketsClassChildAdmin(ModelAdmin):
    model = TicketsClassChild
    base_url_path = 'ticketsclassChild' # customise the URL from default to admin/bookadmin
    menu_label = 'Tickets Class Plus'  # ditch this to use verbose_name_plural from model
    menu_icon = 'plus'  # change as required
    menu_order = 206  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('name', 'seats')


class TicketsAdmin(ModelAdmin):
    model = Tickets
    base_url_path = 'ticketssell' # customise the URL from default to admin/bookadmin
    menu_label = 'Tickets Sell'  # ditch this to use verbose_name_plural from model
    menu_icon = 'tick'  # change as required
    menu_order = 210  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('name', 'ticket_class', 'amount', 'created_at')
#    list_filter = ('uuid',)
    search_fields = ('uuid', 'name')

class TicketsGroup(ModelAdminGroup):
    menu_label = 'Tickets'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (TicketsClassAdmin, TicketsAdmin, TicketsUsedAdmin)

# Now you just need to register your customised ModelAdmin class with Wagtail
#modeladmin_register(TicketsUsedAdmin)
#modeladmin_register(TicketsClassAdmin)
modeladmin_register(TicketsGroup)

