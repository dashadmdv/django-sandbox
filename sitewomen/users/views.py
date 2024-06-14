from django.contrib.auth.views import LoginView

from users.forms import LoginUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}

    # def get_success_url(self):
    #     return reverse_lazy("home")


# def login_user(request):
#     if request.method == "POST":
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd["username"], password=cd["password"])
#             if user and user.is_active:
#                 login(request, user)
#                 return redirect("home")
#     else:
#         form = LoginUserForm()
#     return render(request, "users/login.html", {"form": form})


# def logout_user(request):
#     logout(request)
#     return redirect("users:login")
