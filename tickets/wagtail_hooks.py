from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import Tickets, TicketsClass, TicketsUsed


class TicketsUsedAdmin(ModelAdmin):
    model = TicketsUsed
    base_url_path = 'tickets' # customise the URL from default to admin/bookadmin
    menu_label = 'Tickets'  # ditch this to use verbose_name_plural from model
    menu_icon = 'form'  # change as required
    menu_order = 220  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('ticket', 'ticket_number', 'is_used', 'time_used', 'uuid', 'qr_ticket')
    #search_fields = ('ticket')


class TicketsClassAdmin(ModelAdmin):
    model = TicketsClass
    base_url_path = 'ticketsclass' # customise the URL from default to admin/bookadmin
    menu_label = 'Tickets Class'  # ditch this to use verbose_name_plural from model
    menu_icon = 'list-ol'  # change as required
    menu_order = 205  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('name', 'price')


class TicketsAdmin(ModelAdmin):
    model = Tickets
    base_url_path = 'ticketssell' # customise the URL from default to admin/bookadmin
    menu_label = 'Tickets Sell'  # ditch this to use verbose_name_plural from model
    menu_icon = 'tick'  # change as required
    menu_order = 210  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('name', 'uuid', 'ticket_class', 'amount', 'created_at')
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

