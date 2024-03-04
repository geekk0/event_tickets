from django.db import models
from django.utils import timezone
# from django.utils.translation import ugettext_lazy as _


class Partner(models.Model):
    name = models.CharField(verbose_name="Partner name", max_length=100)
    image = models.ImageField(upload_to='partner_images', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Patrners'


class Ticket(models.Model):
    code = models.CharField(max_length=100, verbose_name='Ticket unique number', unique=True)
    vouchers = models.ForeignKey(Partner, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Vouchers')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    # def get(self, ticket_uid):
    #     return Tickets.objects.get(uid=ticket_uid)


class Voucher(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('used', 'Used'),
        #('expired', 'Expired'),
    ]

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_vouchers')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="partner_org")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"Voucher for {self.partner} (Ticket: {self.ticket.code})"

    class Meta:
        verbose_name = 'Voucher'
        verbose_name_plural = 'Vouchers'