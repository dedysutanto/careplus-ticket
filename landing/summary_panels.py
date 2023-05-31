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
        self.tickets = TicketsUsed.objects.all().count()
        self.tickets_used = TicketsUsed.objects.filter(is_used=True).count()
        self.tickets_class = TicketsClass.objects.all().count()
        self.total_sell = 0

        tclasses = TicketsClass.objects.all()


    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        context['total_tickets'] = self.tickets
        context['total_tickets_used'] = self.tickets_used
        context['total_tickets_class'] = self.tickets_class
        context['total_sell'] = self.total_sell

        return context


class TicketsChartPanel(Component):
    order = 60
    template_name = 'landing/tickets_chart.html'

    def __init__(self):
        self.tickets_classes = {}
        tickets_classes = TicketsClass.objects.all()
        self.total_sell = 0

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

