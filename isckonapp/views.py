from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib import messages
from .decorators import role_required
from .models import Event, GalleryImage

# Create your views here.
def landing(request):
    events = Event.objects.all().order_by('id')
    gallery = GalleryImage.objects.filter(show_in_homepage=True)
    return render(request, 'landing.html', {
        'events': events,
        'gallery': gallery
    })


@csrf_protect
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        DEMO_ADMIN_USERNAME = "admin"
        DEMO_ADMIN_PASSWORD = "admin123"
        
        user = authenticate(request, username=username, password=password)
        
        if user is None and username == DEMO_ADMIN_USERNAME and password == DEMO_ADMIN_PASSWORD:
            from django.contrib.auth.models import User, Group
            user, created = User.objects.get_or_create(
                username=DEMO_ADMIN_USERNAME,
                defaults={
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            if created:
                admin_group, _ = Group.objects.get_or_create(name='Admin')
                user.groups.add(admin_group)
                user.set_password(DEMO_ADMIN_PASSWORD)
                user.save()
            user = authenticate(request, username=username, password=password)
        
        if user is not None and (user.is_staff or user.groups.filter(name='Admin').exists()):
            auth_login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid admin credentials")
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('landing')

from .forms import EventForm, GalleryImageForm
@login_required
@role_required('Admin')

def admin_dashboard(request):
    events = Event.objects.all().order_by('-id')
    gallery_images = GalleryImage.objects.all().order_by('-id')

    if request.method == 'POST':
        if 'add_event' in request.POST:
            event_form = EventForm(request.POST)
            if event_form.is_valid():
                event_form.save()
                return redirect('admin_dashboard')

        elif 'add_gallery' in request.POST:
            gallery_form = GalleryImageForm(request.POST, request.FILES)
            if gallery_form.is_valid():
                gallery_form.save()
                return redirect('admin_dashboard')

        elif 'delete_event' in request.POST:
            Event.objects.get(id=request.POST['delete_event']).delete()
            return redirect('admin_dashboard')

        elif 'delete_gallery' in request.POST:
            GalleryImage.objects.get(id=request.POST['delete_gallery']).delete()
            return redirect('admin_dashboard')

    else:
        event_form = EventForm()
        gallery_form = GalleryImageForm()

    return render(request, 'admin_dashboard.html', {
        'events': events,
        'gallery_images': gallery_images,
        'event_form': event_form,
        'gallery_form': gallery_form
    })
