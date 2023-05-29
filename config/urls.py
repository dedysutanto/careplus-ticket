from django.contrib import admin
from django.urls import path, include

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from landing.views import landing
from qrscan.views import qr_scan, pin_entry, scanner


urlpatterns = [
    path('', landing, name="landing"),
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    path('admin/', admin.site.urls),
    path('login/', include(wagtailadmin_urls)),
    #path('documents/', include(wagtaildocs_urls)),
    #path('pages/', include(wagtail_urls)),
    path('pin', pin_entry, name="pin"),
    path('qr_scan', qr_scan, name="qr_scan"),
    path('scanner', scanner, name="scanner"),
]
