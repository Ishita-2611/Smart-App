from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Profile
from .models import LoginTrack

from django.contrib.auth import login, get_backends

def register(request):
    if request.method == "POST":
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'home.html', {'email': email, 'full_name': full_name})

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already taken. Please sign in.")
            return render(request, 'login.html', {'email': email})

        user = User(username=email, email=email)
        user.set_password(password)
        user.save()

        profile = Profile.objects.create(user=user, full_name=full_name)
        profile.save()

        # Specify the backend explicitly
        backend = get_backends()[0]
        user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

        login(request, user)
        return redirect('dashboard')

    return render(request, 'home.html')


def dashboard(request):
    login_track = LoginTrack.objects.filter(user=request.user).first()
    return render(request, 'dashboard.html', {
        'user': request.user,
        'last_login': login_track.last_login if login_track else None
    })



from django.contrib.auth import authenticate, login, get_backends

def user_login(request):
    if request.method == 'POST':
        email = request.POST['username']  # Treat email as the username
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                # Specify the backend explicitly
                backend = get_backends()[0]
                user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

                login(request, user)

                LoginTrack.objects.update_or_create(
                    user=user, defaults={'last_login': user.last_login}
                )
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
        
        return render(request, 'login.html', {'email': email})

    return render(request, 'login.html')



from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    # Render the profile page for the logged-in user
    return render(request, 'profile.html', {'user': request.user})

from django.contrib.auth import logout
from django.contrib import messages

def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')  # Redirect to the login page after logout