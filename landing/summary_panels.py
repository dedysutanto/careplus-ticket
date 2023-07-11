from wagtail.admin.ui.components import Component
from django.db.models import Count
from tickets.models import Tickets, TicketsClass, TicketsUsed
from random import randint
from django.utils.translation import gettext as _
from django.core.exceptions import ObjectDoesNotExist


class TicketsSummaryPanel(Component):
    order = 50
    template_name = "landing/site_summary.html"

    def __init__(self):
        self.tickets_sell = 0
        self.tickets_authorized = 0

        tickets_sells = Tickets.objects.all()
        for ticket_sell in tickets_sells:
            self.tickets_sell = self.tickets_sell + ticket_sell.amount

        tickets_sells = Tickets.objects.filter(authorization=True)
        for ticket_sell in tickets_sells:
            self.tickets_authorized = self.tickets_authorized + ticket_sell.amount
        self.tickets_used = TicketsUsed.objects.filter(is_used=True).count()
        self.tickets_class = TicketsClass.objects.all().count()

        tclasses = TicketsClass.objects.all()


    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        context['total_tickets_authorized'] = self.tickets_authorized
        context['total_tickets_used'] = self.tickets_used
        context['total_tickets_class'] = self.tickets_class
        context['total_tickets_sell'] = self.tickets_sell

        return context

class SellSummaryPanel(Component):
    order = 60
    template_name = "landing/sell_summary.html"

    def __init__(self):
        self.total_sell = 0
        self.total_sell_plus = 0
        tickets_sells = Tickets.objects.filter(
                authorization=True,
                ticket_class_child__isnull=True,
                )
        for ticket_sell in tickets_sells:
            self.total_sell = self.total_sell + ticket_sell.amount * ticket_sell.ticket_class.price

        tickets_sells = Tickets.objects.filter(
                authorization=True,
                ticket_class_child__isnull=False,
                )
        for ticket_sell in tickets_sells:
            self.total_sell_plus = self.total_sell_plus + ticket_sell.faith_promise

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        context['total_sell'] = self.total_sell
        context['total_sell_plus'] = self.total_sell_plus

        return context


class TicketsChartPanel(Component):
    order = 70
    template_name = 'landing/tickets_chart.html'

    def __init__(self):
        self.tickets_classes = {}
        tickets_classes = TicketsClass.objects.all()
        self.total_sell = 0
        self.total_sell_plus = 0

        for tclass in tickets_classes:
            tickets_count = TicketsUsed.objects.filter(ticket__ticket_class=tclass).count()
            self.tickets_classes[tclass.name] = tickets_count
            self.total_sell = self.total_sell + tclass.price * TicketsUsed.objects.filter(ticket__ticket_class=tclass).count()


    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        data_ticket = []
        labels = []
        backgroundColor = []
        chart_title_ticket = _('Ticket per Class')

        #for name in self.networks_name.values():
        counter = 0
        for name in self.tickets_classes:
            counter = counter + 1
            labels.append(name)
            data_ticket.append(self.tickets_classes[name])
            if counter % 3 == 0:
                backgroundColor.append('rgba({}, {}, {}, 1.0'.format(
                    randint(0, 200), 255, 255))
            if counter % 3 == 1:
                backgroundColor.append('rgba({}, {}, {}, 1.0'.format(
                    255, randint(0, 200), 255))
            if counter % 3 == 2:
                backgroundColor.append('rgba({}, {}, {}, 1.0'.format(
                    255, 255, randint(0, 200)))

        context['data_ticket'] = data_ticket
        context['labels'] = labels
        context['backgroundColor'] = backgroundColor
        context['total_sell'] = self.total_sell
        if labels:
            context['chart_title_ticket'] = chart_title_ticket
        else:
            context['chart_title_ticket'] = ''

        #print(context)
        return context


class TicketsSellSummary(Component):
    order = 80
    template_name = 'landing/tickets_sell_summary.html'

    def __init__(self):
        self.tickets_summary = []
        tickets_classes = TicketsClass.objects.all()

        for tclass in tickets_classes:
            tickets_sell = Tickets.objects.filter(ticket_class=tclass)
            tickets_sell_count = 0
            for tsell in tickets_sell:
                tickets_sell_count = tickets_sell_count + tsell.amount

            tickets_auth_count = TicketsUsed.objects.filter(ticket__ticket_class=tclass).count()
            tickets_sold = {
                'class_name': tclass.name,
                'sold': tickets_sell_count,
                'auth': tickets_auth_count
                            }
            self.tickets_summary.append(tickets_sold)

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)

        context['tickets_summary'] = self.tickets_summary
        return context

