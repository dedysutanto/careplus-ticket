from django.contrib.admin.options import format_html
from wagtail import hooks
from .summary_panels import TicketsSellSummary, TicketsSummaryPanel, TicketsChartPanel, SellSummaryPanel
from django.utils.html import format_html
from crum import get_current_user


@hooks.register('construct_main_menu')
def hide_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != 'help']
    if not request.user.is_superuser:
        menu_items[:] = [item for item in menu_items if item.name != 'reports']


@hooks.register('construct_homepage_panels', order=4)
def add_another_welcome_panel(request, panels):
    panels[:] = [panel for panel in panels if panel.name != "site_summary"]

    current_user = get_current_user()
    panels.append(TicketsSummaryPanel())
    if current_user.username == 'admin' or current_user.is_superuser:
        panels.append(SellSummaryPanel())
    panels.append(TicketsChartPanel())
    panels.append(TicketsSellSummary())


@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
    """Add /static/css/custom.js to the admin."""
    return format_html(
        '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
        )

