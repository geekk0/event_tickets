from django.contrib import admin
from .models import Ticket, Partner, Voucher

admin.site.register(Ticket)
admin.site.register(Partner)
admin.site.register(Voucher)