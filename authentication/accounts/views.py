from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, FormView

from .forms import CustomUserCreationForm, SelectUserTypeForm
from .models import CustomUser

USER = get_user_model()


class UserTypeView(FormView):
    template_name = "accounts/user_type.html"
    form_class = SelectUserTypeForm
    success_url = reverse_lazy("registration")

    def form_valid(self, form):
        # Process the data in form.cleaned_data
        # For example, you might save the user type to the session
        self.request.session["user_type"] = form.cleaned_data["select_type"]
        return super().form_valid(form)


class UserRegistrationView(CreateView):
    template_name = "accounts/registration.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user_type = self.request.session.get("user_type")
        if user_type == "0" and CustomUser.objects.filter(is_parent=True).exists():
            queryset = CustomUser.objects.filter(is_parent=True)
            choices = [("", "Select Parent")] + list(
                queryset.values_list("id", "email")
            )
            form.fields["parent_user"] = forms.ChoiceField(
                choices=choices,
                label="Select Parent",
                required=True,
            )
        return form


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
