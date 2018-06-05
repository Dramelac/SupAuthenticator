from django.urls import path
from SupAuthenticator import views as app_view

urlpatterns = [
    path('', app_view.index, name="home"),
    path('index/', app_view.index, name="home"),
    path('login/', app_view.login, name="login"),
    path('login/connect', app_view.connect, name="connect"),
    path('register/', app_view.register, name="register"),
    path('register/create', app_view.registeruser, name="registeruser"),
    path('logout/', app_view.logout, name="logout"),
    path('generator/', app_view.generator, name="generator"),
    path('generator/validate', app_view.validate_mfa, name="validate"),
]
