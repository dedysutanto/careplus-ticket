from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
import os

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from landing.views import landing, counter
from qrscan.views import qr_scan, pin_entry, scanner
from tickets import views


urlpatterns = [
    path('', landing, name="landing"),
    path('counter/', counter, name="counter"),
    #path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    path('tickets/qr_code/<str:ticket_id>/', views.qr_code),
    path('tickets/authorize/<str:ticket_id>/', views.authorize_ticket, name='authorize_ticket'),
    path('tickets/mail/<str:ticket_id>/', views.mail_tickets, name='mail_tickets'),
    path('tickets/telegram/<str:ticket_id>/', views.telegram_tickets, name='telegram_tickets'),
    #path('tickets/order/', views.order_request, name='order_ticket'),
    path('admin/', admin.site.urls),
    path('login/', include(wagtailadmin_urls)),
    #path('documents/', include(wagtaildocs_urls)),
    #path('pages/', include(wagtail_urls)),
    path('pin', pin_entry, name="pin"),
    path('qr_scan', qr_scan, name="qr_scan"),
    path('scanner', scanner, name="scanner"),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns() # tell gunicorn where static files are in dev mode
    urlpatterns += static(settings.MEDIA_URL + 'tickets/', document_root=os.path.join(settings.MEDIA_ROOT, 'tickets'))

