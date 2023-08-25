from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponse
from cars.views import home_view, car_list
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('car_list')  # Redirect to your desired page after signup
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('car_list')  # Redirect to your desired page after login
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')  # Redirect to your desired page after logout

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = form.get_user(form.cleaned_data['email'])
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"http://example.com/reset/{uid}/{token}/"
            send_mail(
                'Password Reset',
                render_to_string('password_reset_email.html', {'reset_url': reset_url}),
                'noreply@example.com',
                [user.email],
                fail_silently=False,
            )
            return HttpResponse('Password reset email sent.')
    else:
        form = PasswordResetForm()
    return render(request, 'auth/password_reset.html', {'form': form})
