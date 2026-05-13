from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered.')
            return redirect('users.login')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'usermodule/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successfully.')
                return redirect(request.GET.get('next') or 'books.lab10_task2_students')
        messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'usermodule/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('users.login')
