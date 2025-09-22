from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    email = request.user.username
    show_dashboard_btn = True if request.user.is_authenticated else False
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'logout':
            logout(request)
            return redirect('index')
    return render(request, 'dashboard/dashboard.html', {"email": email, "show_dashboard_btn": show_dashboard_btn})
