from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def index(request):
    next_url = request.GET.get('next', '/')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'login/login_form.html', {"error": "Enter email and password"})

    #     try:
    #         if check_password(password, models.Users.objects.get(email=email).password):
    #             return redirect('login:login_success')
    #         else:
    #             return render(request, 'login/login_form.html', {"error": "Invalid email or password"})
    #     except models.Users.DoesNotExist:
    #         return render(request, 'login/login_form.html', {"error": "Invalid email or password"})
    # return render(request, 'login/login_form.html')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.POST.get('next')) if request.POST.get('next') != '/' else redirect('dashboard')
        else:
            return render(request, "login/login_form.html", {"error": "Invalid email or password", "next": next_url})

    return render(request, 'login/login_form.html', {"next": next_url})

def login_success(request):
    return render(request, 'login/login_success.html')
