from django import forms
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField()
    # email = forms.EmailField(disabled=True)
    password = forms.CharField(widget=forms.PasswordInput)

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(username=email)
    #     except models.User.DoesNotExist:
    #         raise forms.ValidationError("User does not exist")
    #     return email

    # def clean_password(self):
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
    #     try:
    #         user = models.User.objects.get(username=email)
    #         if user.check_password(password):
    #             pass
    #         else:
    #             raise forms.ValidationError("Password is wrong")
    #     except models.User.DoesNotExist:
    #         pass

    #     return password

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                # raise forms.ValidationError("Password is wrong")
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            # raise forms.ValidationError("User does not exist")
            self.add_error("email", forms.ValidationError("User does not exist"))
