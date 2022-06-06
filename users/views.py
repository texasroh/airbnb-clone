import os
import requests
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages


# from django.contrib.auth.forms import UserCreationForm
from . import forms, models


# class LoginView(View):

#     """LoginView Definitions"""

#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect(reverse("core:home"))
#         form = forms.LoginForm(initial={"email": "test@test.com"})

#         return render(request, "users/login.html", {"form": form})

#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(request, "users/login.html", {"form": form})


# def login_view(request):
#     if request.method == "GET":
#         pass
#     elif request.method == "POST":
#         pass


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    # initial = {"email": "test@test.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    messages.info(request, f"See you later {request.user.first_name}")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    # form_class = UserCreationForm
    success_url = reverse_lazy("core:home")
    # initial = {
    #     "first_name": "June",
    #     "last_name": "Roh",
    #     "email": "june@roh.com",
    # }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add seuccess message
    except models.User.DoesNotExist:
        # to do: add error message
        pass

    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if not code:
            raise GithubException("Can't get code")
        token_request = requests.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            json={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
            },
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error:
            raise GithubException("Can't get access token")

        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"token {access_token}",
                "Accept": "application/json",
            },
        )
        profile_json = profile_request.json()
        if not profile_json.get("id"):
            raise GithubException("Can't get your profile")
        id = f'{models.User.LOGIN_GITHUB}_{profile_json.get("id")}'

        name = profile_json.get("name")
        email = profile_json.get("email", "")
        email = email if email else ""
        bio = profile_json.get("bio")
        try:
            user = models.User.objects.get(username=id)
            if user.login_method != models.User.LOGIN_GITHUB:
                raise GithubException(f"Please log in with: {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                first_name=name,
                username=id,
                bio=bio,
                login_method=models.User.LOGIN_GITHUB,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()

        login(request, user)
        messages.success(request, f"Welcome back {user.first_name}")
        return redirect("core:home")

    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    REST_API_KEY = os.environ.get("KAKAO_REST_API_KEY")
    REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_REST_API_KEY")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.post(
            # f"https://kauth.kakao.com/oauth/token",
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            # json={
            #     "grant_type": "authorization_code",
            #     "client_id": client_id,
            #     "redirect_uri": redirect_uri,
            #     "code": code,
            # },
        )
        token_json = token_request.json()

        error = token_json.get("error")
        if error:
            raise KakaoException("Can't get authorization code")

        access_token = token_json.get("access_token")

        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                "Authorization": f"Bearer ${access_token}",
            },
        )

        profile_json = profile_request.json()
        id = f'{models.User.LOGIN_KAKAO}_{profile_json.get("id")}'
        email = profile_json.get("kakao_account").get("email")
        if not email:
            raise KakaoException("Please also give me your email")
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")

        try:
            user = models.User.objects.get(username=id)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with: {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                username=id,
                email=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image:
                photo_request = requests.get(profile_image)
                user.avatar.save(f"{id}-avatar.jpg", ContentFile(photo_request.content))

        login(request, user)
        messages.success(request, f"Welcome back {user.first_name}")
        return redirect(reverse("core:home"))

    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))
