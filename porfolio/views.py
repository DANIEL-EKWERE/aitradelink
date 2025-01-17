from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout,login, authenticate
from broker.models import Account, Dashboard, Histotry, Withdraw,Deposit, Investment, myAsset
from django.contrib import messages


# Create your views here.

def index(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'index.html')

def termOfUse(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'terms-of-use.html')

def signup(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password_confirmation')
        email = request.POST.get('email')
        # country = request.POST.get('country')
        phone = request.POST.get('phone')
        trading_platform = request.POST.get('trading_platform')

        # address = request.POST.get('aadress')
        # state = request.POST.get('state')
        # city = request.POST.get('city')
        # zipcode = request.POST.get('zipCode')
       
        # Debug: Log all inputs
        #print("Form Data:", username, first_name, last_name, email, phone, country, address, state, city,zipcode)

        # Validate input
        errors = []
        if password != confirm_password:
            errors.append("Passwords do not match.")
        if User.objects.filter(username=username).exists():
            errors.append("Username already exists.")
        if User.objects.filter(email=email).exists():
            errors.append("Email already exists.")
        if Account.objects.filter(phone=phone).exists():
            errors.append("Phone number already exists.")

         # Debug: Log errors
        print("Errors:", errors)

        if errors:
            # Return errors to the template
            return render(request, 'register.html', {'errors': errors})

        # Create user and account if no errors
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        Account.objects.create(
            first_name = first_name,
            last_name=last_name,
            user=user,
            phone=phone,
           trading_platform=trading_platform,
        )
        myAsset.objects.create(
            user=user,
            bitcoin=10,
            ethereum=10
        )
        Dashboard.objects.create(
            user=user,
            deposit_wallet_balance=10.0,
            interest_wallet_balance=0.0,
            total_invest_balance=0.0,
            total_deposit=0.0,
            total_withdraw=0.0,
            referral_balance=0.0,
            trading_platform=trading_platform

        )
        # Deposit.objects.create(user=user,amount=0.0,wallet_Address="N/A",status="PENDING")
        # Withdraw.objects.create(user=user,amount=0.0,wallet_Address="N/A",status="PENDING")


        login(request, user)
        return redirect('/broker/dashboard/')


    return render(request, 'register.html')

def signin(request):

    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(request,username=username,password=password)
        print(user)
        if user is not None:
            login(request,user=user)
            messages.success(request,"login successful")
            return redirect('/broker/dashboard/')
    messages.error(request,"login not successful, check details and try again.")
    return render(request, 'login.html')

def about(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'about.html')


def privacyPolicy(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'privacy-policy.html')


def watch(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'watch.html')


def forgotpassword(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'forgot-password.html')


def features(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'features.html')


def contact(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'contact.html')


def subscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')
        Subscribe.objects.create(email=email)
        return redirect("/")
    return redirect(request.path)
