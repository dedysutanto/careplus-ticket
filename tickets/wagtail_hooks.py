from django.urls import reverse
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, ObjectList, PermissionHelper, modeladmin_register)
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel, ObjectList
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from django.utils.translation import gettext_lazy as _
from crum import get_current_user
from .models import Tickets, TicketsClass, TicketsUsed, TicketsClassChild


class TicketsPermissionHelper(PermissionHelper):
    def user_can_list(self, user):
        return True

    def user_can_create(self, user):
        return True

    def user_can_delete_obj(self, user, obj):
        if obj.authorization:
            return False
        else:
            return True

    def user_can_edit_obj(self, user, obj):
        return True


class TicketsButtonHelper(ButtonHelper):
    authorized_classnames = ['button button-small button-success']
    mail_tickets_classnames = ['button button-small button-primary']
    telegram_tickets_classnames = ['button button-small button-primary']

    def authorized_button(self, obj):
        text = _('Authorize')
        return {
            'url': reverse('authorize_ticket', kwargs={'ticket_id': str(obj.uuid)}),
            'label': text,
            'classname': self.finalise_classname(self.authorized_classnames),
            'title': text,
        }

    def mail_tickets_button(self, obj):
        text = _('Mail Tickets')
        return {
            'url': reverse('mail_tickets', kwargs={'ticket_id': str(obj.uuid)}),
            'label': text,
            'classname': self.finalise_classname(self.mail_tickets_classnames),
            'title': text,
        }
    def telegram_tickets_button(self, obj):
        text = _('Telegram Tickets')
        return {
            'url': reverse('telegram_tickets', kwargs={'ticket_id': str(obj.uuid)}),
            'label': text,
            'classname': self.finalise_classname(self.telegram_tickets_classnames),
            'title': text,
        }

    def get_buttons_for_obj(
        self, obj, exclude=None, classnames_add=None, classnames_exclude=None
    ):
        buttons = super().get_buttons_for_obj(
            obj, exclude, classnames_add, classnames_exclude
        )
        current_user = get_current_user()
        if obj.authorization == False:
            if current_user.username == 'admin' or current_user.is_superuser:
                if 'authorized_button' not in (exclude or []):
                    buttons.append(self.authorized_button(obj))
        else:
            if obj.email is not None:
                if 'mail_tickets_button' not in (exclude or []):
                    buttons.append(self.mail_tickets_button(obj))
            if 'telegram_tickets_button' not in (exclude or []):
                buttons.append(self.telegram_tickets_button(obj))

        return buttons


class TicketsUsedAdmin(ModelAdmin):
    model = TicketsUsed
    base_url_path = 'tickets' # customise the URL from default to admin/bookadmin
    menu_label = 'Tickets'  # ditch this to use verbose_name_plural from model
    menu_icon = 'form'  # change as required
    menu_order = 220  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('ticket', 'ticket_number', 'is_used', 'qr_ticket')
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
    list_display = ('__str__', 'price', 'seats', 'seats_sell', 'seats_available', 'description')


class TicketsClassChildAdmin(ModelAdmin):
    model = TicketsClassChild
    base_url_path = 'ticketsclassChild' # customise the URL from default to admin/bookadmin
    menu_label = 'Tickets Class Plus'  # ditch this to use verbose_name_plural from model
    menu_icon = 'plus'  # change as required
    menu_order = 206  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('__str__', 'parent_class', 'minimal_promise', 'description')


class TicketsAdmin(ModelAdmin):
    model = Tickets
    base_url_path = 'ticketssell' # customise the URL from default to admin/bookadmin
    menu_label = 'Tickets Sell'  # ditch this to use verbose_name_plural from model
    menu_icon = 'tick'  # change as required
    menu_order = 210  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('name', 'email', 'ticket_class', 'ticket_class_child', 'amount', 'created_at', 'authorization')
    list_filter = ('authorization',)
    search_fields = ('uuid', 'name')
    button_helper_class = TicketsButtonHelper
    permission_helper_class = TicketsPermissionHelper
    #inspect_view_enabled = True
    form_view_extra_js = ['tickets/js/tickets.js']

    def get_edit_handler(self, instance, request):
        #return super().get_edit_handler()
        basic_panels = [
                MultiFieldPanel(
                    [
                        FieldPanel('name'), 
                        FieldRowPanel([
                            FieldPanel('phonenumber'),
                            FieldPanel('email'), 
                            ]),
                        FieldRowPanel([
                            FieldPanel('amount'),
                            FieldPanel('ticket_class'), 
                            ]),
                        FieldPanel('description'),
                    ],
                    heading=_('Data Pembeli')
                    ),
                MultiFieldPanel(
                    [
                        FieldRowPanel([
                            FieldPanel('faith_promise'), 
                            FieldPanel('ticket_class_child'),
                            ])
                    ],
                    heading=_('Janji Iman')
                    ),
                ]
        basic_panels_authorize = [
                MultiFieldPanel(
                    [
                        FieldPanel('name'),
                        FieldRowPanel([
                            FieldPanel('phonenumber'),
                            FieldPanel('email'), 
                            ]),
                        FieldRowPanel([
                            FieldPanel('amount'),
                            FieldPanel('ticket_class'), 
                            ]),
                        FieldPanel('description'),
                    ],
                    heading=_('Data Pembeli')
                    ),
                MultiFieldPanel(
                    [
                        FieldRowPanel([
                            FieldPanel('faith_promise'), 
                            FieldPanel('ticket_class_child'),
                            ])
                    ],
                    heading=_('Janji Iman')
                    ),
                MultiFieldPanel(
                    [
                        FieldRowPanel([
                            FieldPanel('authorization'), 
                            ])
                    ],
                    heading=_('Authorization for creating Tickets')
                    ),
                ]

        current_user = get_current_user()
        custom_panels = basic_panels
        if current_user.username == 'admin' or current_user.is_superuser:
            custom_panels = basic_panels_authorize
        return ObjectList(custom_panels)

class TicketsGroup(ModelAdminGroup):
    menu_label = 'Tickets'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (TicketsClassAdmin, TicketsClassChildAdmin, TicketsAdmin, TicketsUsedAdmin)

# Now you just need to register your customised ModelAdmin class with Wagtail
#modeladmin_register(TicketsUsedAdmin)
#modeladmin_register(TicketsClassAdmin)
modeladmin_register(TicketsGroup)

