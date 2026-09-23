from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 

from .forms import RegistrationForm, LoginForm


def register(request):

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data['password']
            )

            user.role = 'Member'

            user.save()

            login(request, user)

            return redirect('dashboard')

    else:

        form = RegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


def user_login(request):

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                email=email,
                password=password
            )

            if user is not None:

                login(request, user)

                return redirect('home')

            else:

                form.add_error(
                    None,
                    'Invalid email or password.'
                )

    else:

        form = LoginForm()

    return render(
        request,
        'accounts/login.html',
        {'form': form}
    )


def user_logout(request):

    logout(request)

    return redirect('home')