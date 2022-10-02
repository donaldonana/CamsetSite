from django.shortcuts import render, redirect
from django.contrib import messages
from validate_email import validate_email
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
# from helpers.decorators import auth_user_should_not_access
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
# from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading

# Create your views here.




def register(request):
    if request.method == "POST":
        context = {'has_error': False, 
                    'data': request.POST,
                    'pw_error' : "",
                    'pw2_error': "",
                    'email_error':"",
                    'user_error' : "",
                    'user_taken' : "",
                    'email_taken' : ""
                    }

        email = request.POST.get('myemail')
        username = request.POST.get('myusername')
        password = request.POST.get('mypassword')
        password2 = request.POST.get('password2')


        if len(password) < 4:
            messages.add_message(request, messages.ERROR,
                                 'Password should be at least 4 characters')
            context['has_error'] = True
            context['pw_error'] = "Password should be at least 4 characters"

        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'Password mismatch')
            context['has_error'] = True
            context['pw2_error'] = "Password mismatch"


        if not validate_email(email):
            messages.add_message(request, messages.ERROR,
                                 'Enter a valid email address')
            context['has_error'] = True
            context['email_error'] = "Enter a valid email address"


        if not username:
            messages.add_message(request, messages.ERROR,
                                 'Username is required')
            context['has_error'] = True
            context['user_error'] = "Username is required"


        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,
                                 'Username is taken, choose another one')
            context['has_error'] = True
            context['user_taken'] = "Username is taken, choose another one"


            return render(request, 'AppAuth/register.html', context, status=409)

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 'Email is taken, choose another one')
            context['has_error'] = True
            context['email_taken'] = "Email is taken, choose another one"


            return render(request, 'AppAuth/register.html', context, status=409)

        if context['has_error']:
            return render(request, 'AppAuth/register.html', context)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()

        # if not context['has_error']:

            # send_activation_email(user, request)

            # messages.add_message(request, messages.SUCCESS,
            #                      'We sent you an email to verify your account')
        return redirect('login')

    return render(request, 'AppAuth/register.html')


def login_user(request):

    if request.method == 'POST':
        context = {'data': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request, username=username, password=password)

        # if user and not user.is_email_verified:
        #     messages.add_message(request, messages.ERROR,
        #                          'Email is not verified, please check your email inbox')
        #     return render(request, 'AppAuth/login.html', context, status=401)

        if not user:
            error = "Identifiant incorect veillez reessayer"
            context["error"] = error
            return render(request, 'AppAuth/login.html', context, status=401)

        login(request, user)

        messages.add_message(request, messages.SUCCESS,
                             f'Welcome {user.username}')

        return redirect(reverse('home'))

    return render(request, 'AppAuth/login.html')



def logout_user(request):

    logout(request)

    messages.add_message(request, messages.SUCCESS,
                         'Successfully logged out')

    return redirect(reverse('login'))



