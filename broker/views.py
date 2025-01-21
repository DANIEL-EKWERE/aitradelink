from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from broker.models import Account, Histotry, Withdraw,Deposit, Investment, myAsset,Transfer,Profile,Swap
from broker.models import Dashboard
from django.shortcuts import render
from django.contrib.auth import logout,login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings



# Create your views here.

@login_required(login_url='/signin/')
def index(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'dashboard-index.html')

@login_required(login_url='/signin/')
def log(request):
    details = Dashboard.objects.get(user=request.user)
    # user = request.userjjjjjjjjjjjjjjjjjjjjjjjjj
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'dashboard-log-my-trade.html', {'details':details})


@login_required(login_url='/signin/')
def p2p(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'dashboard-p2p-trading.html')

@login_required(login_url='/signin/')
def transfer(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'dashboard-transfer-money.html')

@login_required(login_url='/signin/')
def withdraw(request):
    user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    details = Dashboard.objects.get(user=request.user)
    if request.method == "POST":
        amount = request.POST.get("amount")
        method = request.POST.get("method")
        address = request.POST.get("address")
        if float(amount) > 0 and method and address and float(amount) <= details.deposit_wallet_balance:
            Withdraw.objects.create(
                user=user,
                amount=amount,
                wallet_Address=address,
                method=method,
            )

            #send mail here
            mail_subject = "WITHDRAW REQUEST PLACED"
            mail_context = {
                'email': request.user.email,
                'name': request.user.username,
            }
            html_message = render_to_string('withdraw-mail.html',mail_context)
            plain_text = strip_tags(html_message)
            from_email = settings.Email_HOST_USER
            recipient_list = [request.user.email]
            try:
                email_message = EmailMessage(mail_subject,plain_text,from_email=from_email,to=recipient_list)
                email_message.send()
            except(Exception) as e:
                print('an error occured')



            return redirect('/broker/dashboard/')
    return render(request, 'dashboard-withdraw.html')

# http://127.0.0.1:5000/accounts/signin/?next=/broker/withdraw/

@login_required(login_url='/signin/')
def deposit(request):
    details = None
    details = Dashboard.objects.get(user=request.user)
    print("details",details)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('method')
             # Fetch the Dashboard object for the user
        
        assets = myAsset.objects.get(user=request.user)
        print("assets",assets.bitcoin,assets.ethereum,details)
        print("details",details)
        if not amount or not payment_method:
            # messages.error(request, "Amount and payment method are required.")
            return redirect('broker:deposit')

        # Redirect to the invoice page with the data in the URL
        return redirect(f'/broker/invoice/{amount}/{payment_method}/', {"details":details})

    return render(request, 'deposit.html',{"details":details})


@login_required(login_url='/signin/')
def invoice(request, amount, payment_method):
    try:
        # Validate the data (e.g., ensure amount is numeric)
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        
        # Add additional validation for payment_method if needed
        valid_methods = {'1': 'USDT'}  # Replace with your actual payment method options
        if payment_method not in valid_methods:
            raise ValueError("Invalid payment method.")

    except ValueError as e:
        # messages.error(request, str(e))
        return redirect('/broker/deposit/')

    # If valid, pass the data to the template for display
    context = {'amount': amount, 'payment_method': valid_methods[payment_method], 'is_ethereum':payment_method == '1'}
    return render(request, 'invoice.html', context)


@login_required(login_url='/signin/')
def confirm_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')

        if not amount or not payment_method:
            # messages.error(request, "Missing payment data.")
            return redirect('/broker/deposit/')

        # Save the deposit to the database
        Deposit.objects.create(
            user=request.user,
            amount=amount,
            payment_method=payment_method,
            status="PENDING"
        )

        #send mail here
        mail_subject = "DEPOSIT REQUEST PLACED"
        mail_context = {
            'email': request.user.email,
            'name': request.user.username,
        }
        html_message = render_to_string('deposit-mail.html',mail_context)
        plain_text = strip_tags(html_message)
        from_email = settings.Email_HOST_USER
        recipient_list = [request.user.email]
        try:
            email_message = EmailMessage(mail_subject,plain_text,from_email=from_email,to=recipient_list)
            email_message.send()
        except(Exception) as e:
            print('an error occured')
        # messages.success(request, "Your payment has been confirmed!")
        return redirect('/broker/dashboard/')

    return redirect('/broker/deposit/')


@login_required(login_url='/signin/')
def market(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'market.html')

@login_required(login_url='/signin/')
def paymentMethod(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'payment-method.html')

@login_required(login_url='/signin/')
def settings(request):
    details = Profile.objects.get(user=request.user)
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'settings.html', {"details":details})

@login_required(login_url='/signin/')
def signout(request):
    logout(request)
    return redirect('/')



@login_required(login_url='/signin/')
def swap(request):

    balance = Dashboard.objects.get(user=request.user).deposit_wallet_balance    

    return render(request, 'swap.html',{'balance':balance})


@login_required(login_url='/signin/')
def process_swap(request):
    balance = Dashboard.objects.get(user=request.user).deposit_wallet_balance    
    if request.method == 'POST':

            network = request.POST.get('network')
            from_token = request.POST.get('from_token')
            to_token = request.POST.get('to_token')
            amount = request.POST.get('amount')

            #store the swap transaction
            Swap.objects.create(
                user=request.user,
                from_token=from_token,
                to_token=to_token,
                amount=amount
            )


            #send mail here
            mail_subject = "SWAP REQUEST PLACED"
            mail_context = {
                'email': request.user.email,
                'name': request.user.username,
            }
            html_message = render_to_string('swap-mail.html',mail_context)
            plain_text = strip_tags(html_message)
            from_email = settings.Email_HOST_USER
            recipient_list = [request.user.email]
            try:
                email_message = EmailMessage(mail_subject,plain_text,from_email=from_email,to=recipient_list)
                email_message.send()
            except(Exception) as e:
                print('an error occured')
            return redirect('/broker/dashboard/')  # Replace 'dashboard' with the name of your dashboard route
    return render(request, 'swap.html',{'balance':balance})


@login_required(login_url='/signin/')
def update_profile(request):
    details = Account.objects.get(user=request.user)
    if request.method == "POST":
        # Get the current user
        user = request.user

        # Retrieve form data
        fname = request.POST.get('fname')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip')
        state = request.POST.get('state')
        bank = request.POST.get('bank')
        account = request.POST.get('account')
        accname = request.POST.get('accname')
        wallet_address = request.POST.get('wallet_address')
        image = request.FILES.get('image')

        # Update user's profile
        try:
            profile = Profile.objects.get(user=user)
            profile.fname = fname
            profile.phone = phone
            profile.country = country
            profile.city = city
            profile.zip_code = zip_code
            profile.state = state
            profile.bank = bank
            profile.account = account
            profile.accname = accname
            profile.wallet_address = wallet_address

            if image:
                profile.image = image  # Update profile picture if provided

            profile.save()
            # messages.success(request, "Your profile has been updated successfully.")
            return redirect('/broker/dashboard/')  # Replace 'dashboard' with the name of your dashboard route
        except Profile.DoesNotExist:
            # messages.error(request, "Profile does not exist. Please contact support.")
            return redirect('profile-setting')  # Replace 'profile-setting' with your profile settings page route

    return render(request, 'settings.html', {'details':details})  # Render the form template for GET requests


@login_required(login_url='/signin/')
def dashboard(request):
    user = request.user

    # Initialize variables with default values
    details = None
    # pending = None
    # approved = None
    # cancelled = None
    # deposits = None
    # withdraws = None
    profile = None
    assets = None

    try:
        # Fetch the Dashboard object for the user
        details = Dashboard.objects.get(user=user)
        assets = myAsset.objects.get(user=user)
        print("assets",assets.bitcoin,assets.ethereum)



        deposits = Deposit.objects.filter(user=user).order_by("-date")
        withdraws = Withdraw.objects.filter(user=user)
        # profile = Account.objects.get(user=user)
        for x in deposits:
            if x.status == "APPROVED":
                details.deposit_wallet_balance += int(x.amount)

        for x in withdraws:
            if x.status == "APPROVED":
                details.deposit_wallet_balance -= int(x.amount)
        # Fetch History objects based on transaction type
        # pending = Histotry.objects.filter(user=user, tType="PENDING")
        # approved = Histotry.objects.filter(user=user, tType="APPROVED")
        # cancelled = Histotry.objects.filter(user=user, tType="CANCELLED")

        # deposits = Deposit.objects.filter(user=user).order_by("-date")
        # withdraws = Withdraw.objects.filter(user=user)
        profile = Account.objects.get(user=user)
        # for x in deposits:
        #     if x.status == "APPROVED":
        #         details.deposit_wallet_balance += int(x.amount)

        # for x in withdraws:
        #     if x.status == "APPROVED":
        #         details.deposit_wallet_balance -= int(x.amount)
        
        # if withdraws.amount == 0.0:
        #     print(0)
        # else:
        #     print("its not")
    except ObjectDoesNotExist:
        # Handle case where Dashboard or related objects do not exist
        print("No Dashboard object or related data found for the user.",user)

    # Pass all required data to the template
    return render(
        request, 
        'dashboard-index.html', 
        {
            'details': details,
            # 'pending': pending,
            # 'approved': approved,
            # 'cancelled': cancelled,
            # 'deposits': deposits,
            # 'withdraws':withdraws,
            'profile':profile,
            'myAsset':assets,
        }
    )


@login_required
def profile(request):
    user = request.user
    profile = Account.objects.get(user=user)

    return render(request, 'profile.html',{'profile':profile})

# @login_required
# def withdraw(request):
#     return render(request, 'dashboard-withdraw.html')

@login_required
def withdrawcrypto(request):
    user = request.user
    dashboard = None
    errors = []
    if request.method == "POST":
            amount = request.POST.get('amount')
            address = request.POST.get('copy')
            try:
                dashboard = Dashboard.objects.get(user=user)
                if int(dashboard.deposit_wallet_balance) < int(amount):
                    errors.append("your account balance is not sufficient to place this withdrawal")
                    return render(request, 'withdraw-crypto.html',{'errors':errors})
            except ObjectDoesNotExist:
                dashboard = None
            withdraw = Withdraw.objects.create(
                user=user,
                amount=amount,
                wallet_Address=address
            )

            history = Histotry.objects.create(
                user=user,
                amount=amount,
                wallet_Address=address,
                tType="Withdraw"
            )
            return redirect('/dashboard/')

    return render(request, 'withdraw-crypto.html')



@login_required
def depositcrypto(request):
    user = request.user
    if request.method == "POST":
        amount = request.POST.get('amount')
        address = request.POST.get('copy')

        deposit = Deposit.objects.create(
            user=user,
            amount=amount,
            wallet_Address=address
        )

        history = Histotry.objects.create(
            user=user,
            amount=amount,
            wallet_Address=address,
            tType="Deposit"
        )


        return redirect('/dashboard/')


    return render(request, 'deposit-crypto.html')


# from django.views.decorators.csrf import csrf_exempt

# def invoice(request, payment_method,amount):
#     Deposit.objects.create(
#         user=request.user,
#         payment_method=payment_method,
#         amount=amount
#     )
    
    return render(request, 'dashboard-index')


# @csrf_exempt  # Use only if CSRF is not needed (not recommended for authenticated forms)
def process_transfer(request):
    if request.method == 'POST':
        # Extract form data
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        balance = Dashboard.objects.get(user=request.user).deposit_wallet_balance
        
        # Perform validation and business logic here
        if email and amount:
            # Example logic: Ensure the amount is within bounds
            if 1000 <= float(amount) <= 10000 and float(balance) <= float(amount):
                # Simulate processing
                print(balance)
                Transfer.objects.create(
                    user= request.user,
                    amount=amount,
                    receiver_email=email,

                )

            #send mail here
            mail_subject = "TRANSFER REQUEST PLACED"
            mail_context = {
                'email': request.user.email,
                'name': request.user.username,
            }
            html_message = render_to_string('transfer-mail.html',mail_context)
            plain_text = strip_tags(html_message)
            from_email = settings.Email_HOST_USER
            recipient_list = [request.user.email]
            try:
                email_message = EmailMessage(mail_subject,plain_text,from_email=from_email,to=recipient_list)
                email_message.send()
            except(Exception) as e:
                print('an error occured')


                return JsonResponse({'success': True, 'message': 'Transfer processed successfully!'})
            else:
                return JsonResponse({'success': False, 'message': 'Amount must be between 1000 and 10000 USD, and withdraw amount must not be greater than the balance.'})
        return JsonResponse({'success': False, 'message': 'Invalid data submitted.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def signup(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        password = request.POST.get('password')
        confirm_password = request.POST.get('ConfirmPassword')
        email = request.POST.get('email')
        country = request.POST.get('country')
        phone = request.POST.get('phone')
        referrer = request.POST.get('referrer')

        address = request.POST.get('aadress')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipCode')
       
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
            return render(request, 'signup.html', {'errors': errors})

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
            # country=country,
            phone=phone,
            # referral=referrer,
            # address=address,
            # city=city,
            # state=state,
            # zipcode=zipcode
        )

        Dashboard.objects.create(
            user=user,
            deposit_wallet_balance=10.0,
            interest_wallet_balance=0.0,
            total_invest_balance=0.0,
            total_deposit=0.0,
            total_withdraw=0.0,
            referral_balance=0.0,
            referral_code=referrer

        )
        # Deposit.objects.create(user=user,amount=0.0,wallet_Address="N/A",status="PENDING")
        # Withdraw.objects.create(user=user,amount=0.0,wallet_Address="N/A",status="PENDING")


        login(request, user)
        return redirect('/dashboard/')

    # Render the signup form
    return render(request, 'signup.html')

def signin(request):

    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user=user)
            # messages.success(request,"login successful")
            return render(request, 'dashboard.html')
    # messages.error(request,"login not successful, check details and try again.")
    return render(request, 'signin.html')

def resetpassword(request):
    return render(request, 'reset-password.html')


def plans(request):
    return render(request, 'plans.html')

def privacyPolicy(request):
    return render(request, 'privacy-policy.html')

def licensing(request):
    return render(request, 'licensing.html')

# def subscribe(request):
#     if request.method == "POST":
#         email = request.POST.get('newsletter')
#         Subscribe.objects.create(email=email)
#         return redirect("/")
#     return redirect(request.path)

# def contactus(request):
#     if request.method == "POST":
#         fullName = request.POST.get("fullName")
#         email = request.POST.get("email")
#         message = request.POST.get("Message")

#         ContactUs.objects.create(
#             full_name=fullName,
#             email=email,
#             message=message
#         )
#         return redirect("/")

#     return render(request, 'contact.html')

def about(request):
    return render(request, 'aboutus.html')

# def signup(request):

#     return render(request, 'signup.html')

@login_required
def transaction(request):
    user = request.user
    deposits = None
    withdraws = None
    try:
        history = Histotry.objects.filter(user=user)
        deposits = Deposit.objects.filter(user=user).order_by("-date")
        withdraws = Withdraw.objects.filter(user=user)
    except ObjectDoesNotExist:
        history = None

    return render(request, 'transaction.html',{'history':history,'deposits':deposits,'withdraws':withdraws})

@login_required
def investment(request):
    user = request.user
    investment = None
    try:
        investment = Investment.objects.get(user=user)
    except ObjectDoesNotExist:
        investment = None
    return render(request, 'investment.html',{'investment':investment})
