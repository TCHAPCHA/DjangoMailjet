from django.shortcuts import render, redirect
from registration import models
import hashlib

def hash_password(password):
    sha = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return sha

def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'login/login_form.html', {"error": "Enter email and password"})

        # Хэшируем пароль
        hashed_pw = hash_password(password)

        try:
            # Пытаемся найти пользователя по email и паролю
            user = models.Users.objects.get(email=email, password=hashed_pw)
            return redirect('login:login_success')
        except models.Users.DoesNotExist:
            return render(request, 'login/login_form.html', {"error": "Invalid email or password"})

    return render(request, 'login/login_form.html')

def login_success(request):
    return render(request, 'login/login_success.html')
