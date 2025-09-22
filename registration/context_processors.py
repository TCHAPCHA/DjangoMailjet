def show_dashboard_btn(request):
    return {"show_dashboard_btn": request.user.is_authenticated}