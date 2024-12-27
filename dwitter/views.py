from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


from .forms import DweetForm
from .models import Dweet, Profile


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created successfully! Welcome, {user.username}.")
            return redirect('dwitter:dashboard')
        else:
            messages.error(request, "There was an error with your signup. Please try again.")
    else:
        form = UserCreationForm()
    return render(request, 'dwitter/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dwitter:dashboard')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, 'dwitter/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('dwitter:login')
    

@login_required
def dashboard(request):
    form = DweetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("dwitter:dashboard")

    followed_dweets = Dweet.objects.filter(
        user__profile__in=request.user.profile.follows.all()
    ).order_by("-created_at")

    return render(
        request,
        "dwitter/dashboard.html",
        {"form": form, "dweets": followed_dweets},
    )

@login_required
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})

@login_required
def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "dwitter/profile.html", {"profile": profile})
