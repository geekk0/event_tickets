import os

# from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
# from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
# from VideoUploader import settings
from .forms import LoginForm, ResetPassword, AddTicketForm, TicketForm, VoucherFormSet, VoucherForm
from .models import Ticket, Voucher, Package  # , Partner, Voucher
from django.urls import reverse_lazy
# from videofiles.models import Files
# from django.utils.translation import ugettext as _


class LoginView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, 'login.html', context)

    @staticmethod
    def post(request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

                # Redirect to the next URL if provided, otherwise, redirect to a default URL
                next_url = request.GET.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    # If 'next' parameter is not provided, redirect to a default URL
                    return HttpResponseRedirect(reverse_lazy("main"))

        return render(request, 'login.html', {'form': form})


@login_required(login_url='/login/')
def default_redirect_view(request):
    # This view can be used as the default redirection view
    # when the 'next' parameter is not provided
    return HttpResponseRedirect(reverse_lazy('default_redirect_url'))


class ResetPasswordView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        form = ResetPassword(request.POST or None)
        form.initial['username'] = request.user.username
        context = {'form': form}
        return render(request, 'password_reset.html', context)

    @staticmethod
    def post(request, *args, **kwargs):
        current_user = request.user
        form = ResetPassword(request.POST or None)

        if form.is_valid():
            current_user.set_password(form.cleaned_data['new_password'])
            current_user.save()
            return HttpResponseRedirect('/')
        return render(request, 'password_reset.html', {'form': form})


# @login_required(login_url='/login/')
# def add_ticket(request):
#     if request.method == 'POST':
#         form = AddTicketForm(request.POST)
#         if form.is_valid():
#             # Process the form data
#             new_ticket = form.save(commit=False)
#             new_ticket.save()
#             # Further processing logic goes here
#             return redirect('success_url')
#     else:
#         form = AddTicketForm()
#     return render(request, 'add_ticket.html', {'form': form})


from django.shortcuts import render, redirect
from .forms import TicketForm, VoucherFormSet


@admin_required
def add_ticket(request):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))

        ticket_form = TicketForm(request.POST)
        if ticket_form.is_valid():
            for i in range(quantity):
                ticket_holder = ticket_form.cleaned_data['holder']
                selected_package = ticket_form.cleaned_data['package']

                ticket = Ticket.objects.create(holder=ticket_holder, package=selected_package)
                ticket.save()

                package = ticket.package

                for partner in package.partners.all():
                    voucher = Voucher.objects.create(ticket=ticket, partner=partner)
                    if partner.facilitator:
                        voucher.activities = True
                    voucher.save()

            return redirect('main')
            # if ticket:
            #     return redirect('ticket_info', ticket_code=ticket.code)
            # else:
            #     return redirect('main')
        else:
            error_message = ticket_form.errors
            packages = Package.objects.all()
            return render(request, 'add_ticket.html',
                          {'ticket_form': ticket_form, 'packages': packages, 'error_message': error_message})

    else:
        ticket_form = TicketForm()
        packages = Package.objects.all()

        return render(request, 'add_ticket.html',
                      {'ticket_form': ticket_form,
                       'packages': packages})

def show_success_page(request):
    return render(request, 'success_page.html')

def user_logout(request):
    request.user.set_unusable_password()
    logout(request)
    return HttpResponseRedirect('/')


def main(request):
    context = {}

    # user_agent = request.META['HTTP_USER_AGENT']

    # if 'Mobile' in user_agent:
    #     return render(request, 'mobile_main.html', context)
    # else:
    #     return render(request,  'main.html', context)

    return render(request, 'main.html', context)


def ticket_info(request, ticket_code):
    try:
        ticket = Ticket.objects.get(code=ticket_code)
        partners = ticket.package.partners.all()
        for partner in partners:
            if not Voucher.objects.filter(ticket=ticket, partner=partner).exists():
                voucher = Voucher.objects.create(ticket=ticket, partner=partner)
                voucher.save()
        vouchers = Voucher.objects.filter(ticket=ticket, partner__facilitator=False)
        activities = Voucher.objects.filter(ticket=ticket, partner__facilitator=True)
        packages = Package.objects.all()
        context = {'ticket_info': ticket, 'vouchers': vouchers,
                   'activities': activities, 'packages': packages}
    except Ticket.DoesNotExist:
        context = {'error': 'Ticket not found'}

    return render(request, 'ticket_info.html', context)


@login_required(login_url='/login/')
def update_ticket_vouchers(request, ticket_code):
    if request.method == 'POST':
        ticket = Ticket.objects.get(code=ticket_code)

        for prefix in request.POST:
            if prefix.startswith('voucher_status_'):
                voucher_id = prefix.replace('voucher_status_', '')
                voucher_status = request.POST[prefix]
                voucher = Voucher.objects.get(id=voucher_id)
                voucher.status = voucher_status
                voucher.save()
            elif prefix == 'package':
                ticket.package = Package.objects.get(id=request.POST[prefix])
            elif 'csrf' not in prefix:
                setattr(ticket, prefix, request.POST[prefix])

        ticket.save()

    # return redirect('ticket_info', ticket_code=ticket_code)
    return ticket_info(request, ticket_code)


def send_all_tickets_info(request):
    Ticket.send_all_tickets_info()
    return redirect('main')


def send_tickets_info_attached_to_partner(request):
    Ticket.send_tickets_info_attached_to_partner()
    return redirect('main')

def create_ticket_qr_code(request, ticket_code):
    ticket = Ticket.objects.get(code=ticket_code)
    ticket.create_qr_code()
    ticket.save()