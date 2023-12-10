from django.contrib.auth.views import LoginView, LogoutView


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = "/"
