from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from users.forms import LoginForm


def user_login(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data('username')
            password = form.cleaned_data('password')
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('index')

    context = {'form': form }
    return render(request, 'users/login.html', context)
