from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .decorators import role_required
from .models import Event, GalleryImage, Album
from .forms import EventForm, GalleryImageForm, AlbumForm, MultipleImageUploadForm
from django.http import JsonResponse


def landing(request):
    events = Event.objects.all().order_by('id')
    
    albums = Album.objects.all().order_by('-created_at')

    return render(request, 'landing.html', {
        'events': events,
        'albums': albums
    })
def album_detail(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    context = {
        'album': album
    }
    return render(request, 'album_detail.html', context)

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
    return redirect('landing_page')

@login_required
@role_required('Admin')
def admin_dashboard(request):
    # --- This block handles all form submissions (POST requests) ---
    if request.method == 'POST':
        # --- Handle Deleting an Album ---
        if 'delete_album' in request.POST:
            album_id = request.POST.get('delete_album')
            album = Album.objects.filter(id=album_id)
            if album.exists():
                album.delete()
                # If the request is from our new JavaScript, send a JSON success message
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'success', 'message': 'Album deleted.'})
            # For old-style form submissions, redirect as before
            return redirect('admin_dashboard')

        # --- Handle Deleting a Single Gallery Image ---
        elif 'delete_gallery' in request.POST:
            image_id = request.POST.get('delete_gallery')
            image = GalleryImage.objects.filter(id=image_id)
            if image.exists():
                image.delete()
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'success', 'message': 'Image deleted.'})
            return redirect('admin_dashboard')

        # --- Handle adding a new album ---
        if 'add_album' in request.POST:
            album_form = AlbumForm(request.POST, request.FILES)
            if album_form.is_valid():
                album_form.save()
                return redirect('admin_dashboard')

        # --- Handle multiple image uploads ---
        elif 'add_multiple_images' in request.POST:
            upload_form = MultipleImageUploadForm(request.POST, request.FILES)
            if upload_form.is_valid():
                album = upload_form.cleaned_data['album']
                files = request.FILES.getlist('images')
                for image_file in files:
                    GalleryImage.objects.create(
                        album=album, image=image_file,
                        title=image_file.name, alt_text=image_file.name
                    )
                return redirect('admin_dashboard')
        
        # --- Handle events ---
        elif 'add_event' in request.POST:
            event_form = EventForm(request.POST)
            if event_form.is_valid():
                event_form.save()
            return redirect('admin_dashboard')

        elif 'delete_event' in request.POST:
            Event.objects.filter(id=request.POST.get('delete_event')).delete()
            return redirect('admin_dashboard')

    # --- This block prepares data for the initial page load (GET request) ---
    context = {
        'events': Event.objects.all().order_by('-id'),
        'albums': Album.objects.all().order_by('-created_at'),
        'event_form': EventForm(),
        'album_form': AlbumForm(),
        'multiple_upload_form': MultipleImageUploadForm()
    }
    return render(request, 'admin_dashboard.html', context)