import os
import requests
from django.contrib.auth.views import PasswordChangeView
from django.utils import translation
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, reverse, render
from django.contrib import messages
from django.core.files.base import ContentFile
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None and user.email_verified is True:
            login(self.request, user)
            messages.success(self.request, f"Welcome back {user.first_name}!")
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse_lazy("core:home")


def log_out(request):
    logout(request)
    messages.info(request, "You have successfully logged out")
    return redirect(reverse("users:login"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_key=key)
        user.email_verified = True
        user.email_key = ""
        user.save()
        login(request, user)
        messages.info(
            request, f"Hello {user.first_name}! Your account has been verified"
        )
    except models.User.DoesNotExist:
        pass
        # To Do: Message
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
        if code is not None:
            token = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Cannot retrieve access token")
            else:
                access_token = token_json.get("access_token")
                profile = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile.json()
                username = profile_json.get("login")
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please login with: {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            username=email,
                            email=email,
                            first_name=name,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}!")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("We cannot access your Github account")
        else:
            raise GithubException("We cannot access your code")
    except GithubException as error:
        messages.error(request, error)
        return redirect(reverse("users:login"))


def kakao_login(request):
    app_key = os.environ.get("KAKAO_KEY")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        app_key = os.environ.get("KAKAO_KEY")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_key}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error")
        if error is not None:
            raise KakaoException("Cannot retrieve access token")
        else:
            ACCESS_TOKEN = token_json.get("access_token")
            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
            )
            profile_json = profile_request.json()
            kakao_account = profile_json.get("kakao_account")
            email = kakao_account.get("email")
            if email is not None:
                profile = kakao_account.get("profile")
                image = profile.get("profile_image_url")
                name = profile.get("nickname")
                try:
                    user = models.User.objects.get(email=email)
                    if user.login_method != models.User.LOGIN_KAKAO:
                        raise KakaoException(f"Please login with: {user.login_method}")
                except models.User.DoesNotExist:
                    user = models.User.objects.create(
                        username=email,
                        email=email,
                        first_name=name,
                        login_method=models.User.LOGIN_KAKAO,
                        email_verified=True,
                    )
                    user.set_unusable_password
                    user.save()
                    if image:
                        avatar_image = requests.get(image)
                        print(avatar_image)
                        user.avatar.save(
                            f"{name}/avatar", ContentFile(avatar_image.content)
                        )
                login(request, user)
                messages.success(request, f"Welcome back {user.first_name}!")
                return redirect(reverse("core:home"))
            else:
                raise KakaoException("Please include email for verification purposes")
    except KakaoException as error:
        messages.error(request, error)
        return redirect(reverse("users:login"))


def profile_view(request, username):
    user = models.User.objects.get(username=username)
    return render(request, "users/profile.html", context={"logged_in_user": user})


class EditProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/edit-profile.html"
    success_message = "You have successfully edited your profile information"
    fields = (
        "first_name",
        "last_name",
        "avatar",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].widget.attrs = {"placeholder": "First Name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last Name"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate"}
        form.fields["bio"].widget.attrs = {"placeholder": "Bio"}
        return form


class ChangePasswordView(
    mixins.LoggedInOnlyView, mixins.EmailOnlyView, PasswordChangeView
):
    template_name = "users/password-change.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Old Password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New Password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "New Password Confirmation"
        }
        return form

    def get_success_url(self):
        messages.success(self.request, "You have successfully changed your password")
        return self.request.user.get_absolute_url()


@login_required
def switch_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))


def switch_language(request):
    lang = request.GET.get("lang", None)
    if lang is not None:
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return HttpResponse(status=200)
