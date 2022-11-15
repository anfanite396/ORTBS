from django.shortcuts import render, redirect
from .models import Restaurant, provider_group, consumer_group, TableBooking
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RestaurantCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.core.mail import send_mail
from .forms import CustomUserForm

# Create your views here.


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups, login_url='403')


def registerConsumer(request):
    page = 'register'
    form = CustomUserForm()

    if (request.method == "POST"):
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            my_group = Group.objects.get(name='Consumer')
            my_group.user_set.add(user)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    context = {'page': page, 'form': form}
    return render(request, 'base/login.html', context)


def registerProvider(request):
    page = 'register'
    form = UserCreationForm()

    if (request.method == "POST"):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            my_group = Group.objects.get(name='Provider')
            my_group.user_set.add(user)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    context = {'page': page, 'form': form}
    return render(request, 'base/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    restaurants = Restaurant.objects.all()
    context = {'restaurants': restaurants}
    return render(request, 'base/home.html', context)


@login_required(login_url='loginPage')
def rest(request, pk):
    restaurant = Restaurant.objects.get(id=pk)
    context = {'restaurant': restaurant}
    return render(request, 'base/rest.html', context)


def loginPage(request):
    page = 'login'
    if (request.user.is_authenticated):
        return redirect('home')

    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)
        print("I was here", username, password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "username or password does not exist")

    context = {'page': page}
    return render(request, 'base/login.html', context)


@login_required(login_url='loginPage')
def bookTable(request, pk):
    # form = TableBookingForm()
    # if request.method == "POST":
    #     form = TableBookingForm(request.POST)
    #     if (form.is_valid()):
    #         table = form.save(commit=False)
    #         table.host = request.user
    #         table.rest_id = pk
    #         table.save()
    #         return redirect('home')
    # context = {'form': form}
    if request.method == "POST":
        TableBooking.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            numGuests=request.POST.get('numGuests'),
            phone=request.POST.get('phone'),
            date=request.POST.get('date'),
            time=request.POST.get('time'),
            message=request.POST.get('message'),

            cust_id=request.user.id,
            rest_id=pk,
        )
        return redirect('home')
    return render(request, 'base/bookTable.html')


@login_required(login_url='loginPage')
@group_required("Provider")
def createRestaurant(request):
    form = RestaurantCreationForm()

    if request.method == "POST":
        form = RestaurantCreationForm(request.POST)
        if (form.is_valid()):
            restaurant = form.save(commit=False)
            restaurant.host = request.user
            restaurant.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/createRest.html', context)


def requests(request, pk):
    requests = TableBooking.objects.filter(rest_id=pk)
    context = {'requests': requests}
    if request.method == "POST":
        status = request.POST.getlist('status')
        for i in requests:
            if str(i.id) in status:
                print(i.status)
                if i.status == False:
                    subject = 'Booking Confirmation Mail'
                    message = f'Hi {i.name}, Your table has been reserved in {Restaurant.objects.get(id=i.rest_id)} on dated {i.date} at {i.time}.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [i.email, ]
                    send_mail(subject, message, email_from, recipient_list)
                    print("Mail sent")
                i.status = True
                i.save()
            else:
                i.status = False
                i.save()
        # for i in status:
        #     ans = int(i)
        #     request = requests.objects.filter(id=i)
        #     print(request)
        return render(request, 'base/requests.html', context)
    return render(request, 'base/requests.html', context)


@login_required(login_url='login')
def profile(request, pk):
    requests = TableBooking.objects.filter(cust_id=pk)
    context = {'requests': requests}
    return render(request, 'base/profile.html', context)
