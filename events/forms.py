from django import forms


class PasswordForm(forms.Form):
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(),
        label="Enter password"
    )
    password2 = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(),
        label="Re-enter password"
    )

    def clean_password2(self):
        password = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("Confirmation password doesn't match.")
        return password2


# form for registration
class RegisterForm(PasswordForm):
    first_name = forms.CharField(
        label="Firstname",
        max_length=50,
        required=True,
    )
    last_name = forms.CharField(
        label="Lastname",
        max_length=50,
        required=True,
    )
    email = forms.EmailField(
        label="Email",
        max_length=255,
        required=True,
    )
    username = forms.CharField(
        label="Username",
        max_length=255,
        required=True,
    )


# form for logging in
class LoginForm(forms.Form):
    password = forms.CharField(
        label="Password",
        max_length=128,
        widget=forms.PasswordInput(),
        required=True
    )
    username = forms.CharField(
        label="Username",
        max_length=255,
        required=True,
    )