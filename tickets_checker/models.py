import secrets
import string

from django.db import models
from django.contrib.auth.models import User


class Partner(models.Model):
    name = models.CharField(verbose_name="Partner name", max_length=100)
    image = models.ImageField(upload_to='partner_images', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="User")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Patrners'


class Package(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    partners = models.ManyToManyField(Partner)
    tickets = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name='packages', null=True, blank=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    code = models.CharField(max_length=100, verbose_name='Ticket unique number', unique=True, null=True, blank=True)
    vouchers = models.ForeignKey(Partner, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Vouchers')
    holder = models.CharField(max_length=250, verbose_name='Ticket holder name', blank=True, null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Package')
    number = models.IntegerField(verbose_name='Ticket number', unique=True, blank=True, null=True)

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        if not self.number:
            self.number = self.id
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    @staticmethod
    def generate_unique_code():
        while True:
            code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9))
            if not Ticket.objects.filter(code=code).exists():
                return code

    # def get(self, ticket_uid):
    #     return Tickets.objects.get(uid=ticket_uid)


class Voucher(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('used', 'Used'),
        #('expired', 'Expired'),
    ]

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_vouchers', null=True, blank=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="Partner")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"Voucher for {self.partner} (Ticket: {self.ticket.code})"

    class Meta:
        verbose_name = 'Voucher'
        verbose_name_plural = 'Vouchers'



