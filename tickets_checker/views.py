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
from .models import Ticket, Voucher  # , Partner, Voucher
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
        # Create ticket form instance with POST data
        ticket_form = TicketForm(request.POST)
        # Initialize an empty list to hold voucher form instances
        voucher_forms = []

        if ticket_form.is_valid():
            # Save the ticket form
            ticket = ticket_form.save()
            print(request.POST)
            # Process voucher forms from request.POST
            for prefix in request.POST:
                if prefix.startswith('ticket_vouchers-') and 'partner' in prefix:
                    # Get the form data for this voucher form
                    form_data = request.POST.getlist(prefix)
                    # Create a new voucher form instance with this data
                    voucher_form = VoucherForm(data={'partner': request.POST[prefix]})
                    print(voucher_form)
                    # voucher_form = VoucherFormSet(prefix=prefix, data={'partner': form_data})
                    # Check if the voucher form is valid and has partner selected
                    if voucher_form.is_valid() and voucher_form.cleaned_data.get('partner'):
                        # Save the voucher form
                        voucher = voucher_form.save(commit=False)
                        voucher.ticket = ticket
                        voucher_forms.append(voucher)  # Append the form to the list

            # Save all voucher forms together
            for voucher in voucher_forms:
                voucher.save()

            # Redirect to ticket information page
            return redirect('ticket_info', ticket_code=ticket.code)

    else:
        # Initialize ticket form instance for GET request
        ticket_form = TicketForm()

    # Initialize an empty voucher formset for rendering in the template
    voucher_formset = VoucherFormSet()

    return render(request, 'add_ticket.html', {'ticket_form': ticket_form, 'voucher_formset': voucher_formset})

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
        vouchers = Voucher.objects.filter(ticket=ticket)
        context = {'ticket_info': ticket, 'vouchers': vouchers}
    except Ticket.DoesNotExist:
        context = {'error': 'Ticket not found'}

    return render(request, 'ticket_info.html', context)


def update_ticket_vouchers(request):
    if request.method == 'POST':
        print(request.POST)
        for prefix in request.POST:
            if prefix.startswith('voucher_status_'):
                voucher_id = prefix.replace('voucher_status_', '')
                voucher_status = request.POST[prefix]
                voucher = Voucher.objects.get(id=voucher_id)
                voucher.status = voucher_status
                voucher.save()

        return render(request, 'ticket_info.html')
        # print(form)

