from urllib import request
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

def role_required(*roles):
    def check_role(user):
        if user.is_authenticated:
            if user.is_superuser or user.groups.filter(name__in=roles).exists():
                return True
        messages.error(request, "You don't have permission to access this page")
        return False
    
    return user_passes_test(check_role, login_url='landing')