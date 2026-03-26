from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import NameForm, DistanceForm, TimeForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import F


def home(requests):
    return render(requests, 'base/home.html')

@login_required
def distances(requests):
    distances = Distance.objects.all()
    context = {'distances': distances}
    return render(requests, 'base/distances.html', context)

@login_required
def times(requests, length):
    times = Distance.objects.filter(Distance=length)
    context = {'times': times}
    return render(request, 'base/time.html', context)

@login_required
def nameform(requests):
    form = NameForm()
    context = {"form": form}

    if requests.method == "POST":
        name = requests.POST.get("your_name")
        context["greeting"] = f"Welcome {name}!"
    return render(requests, "base/nameform.html", context)

@login_required
def add_distance(requests):
    if requests.method == "POST":
        form = DistanceForm(requests.POST)
        if form.is_valid():
            form.save()
            messages.success(requests, "Distance added succesfully")
            return redirect("distances")

    else:
        form = DistanceForm()

    context = {"form": form}

    return render(requests, "base/distanceform.html", context)

@login_required
def edit_distance(requests, pk):
    distance = Distance.objects.get(pk=pk)

    if requests.method == "POST":
        form = DistanceForm(requests.POST, instance=distance)
        if form.is_valid():
            form.save()
            messages.success(requests, "Distance updated succesfully")
            return redirect("distances")
    else:
        form = DistanceForm(instance=distance)
    context = {"form": form}
    return render(requests, "base/distanceform.html", context)
    
def register(requests):
    if requests.method == "POST":
        form = UserCreationForm(requests.POST)
        if form.is_valid():
            user = form.save()
            login(requests, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    context = {"form":form}
    return render(requests, "registration/register.html", context)

@login_required
def new_time(requests):
    if requests.method == "POST":
        form = TimeForm(requests.POST)
        if form.is_valid():
            time = form.save(commit=False)
            time.user = requests.user
            time.save()
            messages.success(requests, "Time added sucessfully")
            return redirect("newtime")
    else:
        form = TimeForm()
    
    context = {"form":form}

    return render(requests, "base/newtime.html", context)

@staff_member_required
def unapproved_times(requests):
    times = Time.objects.filter(approved=False)
    context = {"times":times}
    return render(requests, "base/unapproved_times.html", context)

@staff_member_required
def approve_times(requests, pk):
    time = Time.objects.get(pk=pk)
    time.approved = True
    time.approved_by = requests.user
    time.save()
    messages.success(requests, "Time approved.")
    return redirect("unapproved_times")

@staff_member_required
def deny_time(requests, pk):
    time = Time.objects.get(pk=pk)
    time.delete()
    messages.success(requests, "Time denied.")
    return redirect("unapproved_times")

@login_required
def my_times(requests):
    times = Time.objects.filter(user=requests.user)
    context = {"times":times}
    return render(requests, "base/my_times.html", context)

    
@login_required
def edit_time(request, pk):
    time = Time.objects.get(pk=pk)

    # Check ownership
    if time.user != request.user:
        messages.error(request, "You are not allowed to edit this time.")
        return redirect("my_times")

    if request.method == "POST":
        form = TimeForm(request.POST, instance=time)
        if form.is_valid():
            updated_time = form.save(commit=False)
            updated_time.approved = False
            updated_time.save()
            messages.success(request, "Time updated successfully.")
            return redirect("my_times")
    else:
        form = TimeForm(instance=time)

    context = {"form": form}
    return render(request, "base/newtime.html", context)


@login_required
def fastest_time_per_distance(request):
    approved_times = Time.objects.filter(approved=True)
    fastest_times = []
    distances = Distance.objects.all()
    for distance in distances:
        fastest_time = approved_times.filter(distance=distance).order_by('time_in_minutes').first()
        if fastest_time:
            fastest_times.append(fastest_time)

    context = {'fastest_times': fastest_times}
    return render(request, "base/fastest_times.html", context)

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("edit_profile")  # redirect to the same page or a profile page
    else:
        form = ProfileForm(instance=profile)
    context = {"form": form}
    return render(request, "base/edit_profile.html", context)