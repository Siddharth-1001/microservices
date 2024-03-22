from django import forms

from .constant import USER_TYPE_CHOICES
from .models import CustomUser


class SelectUserTypeForm(forms.Form):
    select_type = forms.ChoiceField(
        label="User Type", required=True, choices=USER_TYPE_CHOICES
    )


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as above, for verification.",
    )

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "password1",
            "password2",
        ]
        widgets = {
            "password1": forms.PasswordInput(),
            "password2": forms.PasswordInput(),
        }

    def clean_email(self):
        return self.cleaned_data["email"].lower()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            parent_user_id = self.cleaned_data.get("parent_user")
            if parent_user_id:
                parent_user = CustomUser.objects.get(pk=parent_user_id)
                user.parents.add(parent_user)
        return user
