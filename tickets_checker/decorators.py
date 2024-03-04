from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def admin_required(view_func):
    """
    Decorator that checks if the user is an admin.
    """
    def _check_admin(user):
        return user.is_authenticated and user.is_superuser  # Adjust this condition as needed

    actual_decorator = user_passes_test(_check_admin, login_url='/login/')
    return actual_decorator(view_func)
