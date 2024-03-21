from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm

USER = get_user_model()


class UserRegistrationView(CreateView):
    template_name = "accounts/registration.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")


class LoginView(View):
    template_name = "accounts/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("registration")
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")
            if email and password:
                user = authenticate(
                    request=request, username=str(email).lower(), password=password
                )
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        next_url = request.GET.get("next")
                        if next_url:
                            return redirect(next_url)
                        else:
                            return redirect("registration")
                    else:
                        messages.error(
                            request,
                            "Your account is currently inactive.",
                        )
                else:
                    messages.error(request, "Email or password is incorrect")
            else:
                messages.error(request, "Email and password are required")
        except Exception as e:
            messages.error(request, "An error occurred while logging in")
        return render(request, self.template_name)
