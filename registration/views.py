from django.shortcuts import render, redirect
import requests
import random
import json
import hashlib
from datetime import datetime, timezone, timedelta
from . import models
import config

MAILJET_URL = "https://api.mailjet.com/v3/send"
MAILJET_AUTH = config.MAILJET_AUTH

def generate_unique_id(email, code):
    time_now = datetime.now(timezone.utc).isoformat()
    raw_string = f"{email}{code}{time_now}"
    sha = hashlib.sha256(raw_string.encode('utf-8')).hexdigest()
    return sha

def hash_password(password):
    sha = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return sha

def send_code(email, request):
    code = ''.join(random.SystemRandom().choice('0123456789') for _ in range(6))
    unique_id = generate_unique_id(email, code)

    models.Codes.objects.create(email=email, code=code, unique_id=unique_id)

    request.session['email'] = email
    request.session['unique_id'] = unique_id

    # Отправляем email
    payload = json.dumps({
        "FromEmail": config.sender_email,
        "FromName": config.sender_name,
        "Recipients": [{"Email": email}],
        "Subject": "Authentication on <Website>",
        "Text-part": f"This is your code: {code}\n\nFor support: {unique_id}",
        "Html-part": f"This is your code: <h3>{code}</h3><p>For support: <b>{unique_id}</b></p>"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': MAILJET_AUTH
    }
    requests.post(MAILJET_URL, headers=headers, data=payload)

def index(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        password = request.POST.get('password')

        if action == 'email_submit':
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not email or not password:
                return render(request, 'registration/register_email_input.html',
                              {"error": "Enter email and password"})

            if models.Users.objects.filter(email=email).exists():
                return render(request, 'registration/register_email_input.html', {"error": "This email is already registered"})

            request.session['temp_password'] = password

            send_code(email, request)
            return render(request, 'registration/register_email_verification.html', {"email": email})

        elif action == 'code_submit':
            code_input = request.POST.get('code')
            email = request.session.get('email')
            password = request.session.get('temp_password')

            if not email or not code_input or not password:
                return render(request, 'registration/register_email_verification.html',
                              {"error": "Data is incorrect"})

            ten_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=10)
            code_obj = models.Codes.objects.filter(
                email=email,
                code=code_input,
                created_at__gte=ten_minutes_ago,
                is_active=True
            ).first()

            if code_obj:
                models.Users.objects.create(email=email, password=hash_password(password))

                code_obj.is_active = False
                code_obj.save()

                request.session['success_email'] = email
                request.session.pop('temp_password', None)
                return redirect('registration:register_success')
            else:
                return render(request, 'registration/register_email_verification.html',
                              {"error": "Invalid code, code is already used or expired"})

    return render(request, 'registration/register_email_input.html')

def register_success(request):
    email = request.session.get('success_email', None)
    return render(request, 'registration/register_success.html', {'user': {'email': email}})

