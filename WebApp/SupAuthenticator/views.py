import re
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from SupAuthenticator.models import *
from SupAuthenticator.tools.decorators import json_parser
from SupAuthenticator.tools.server import ServerAuthenticator
from SupAuthenticator.tools.client import ClientAuthenticator
def index(request):    
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


@require_http_methods(["POST"])
@json_parser
def registeruser(request):
    username = request.json.get('username', '').strip()
    first_name = request.json.get('first_name', '').strip()
    last_name = request.json.get('last_name', '').strip()
    email = request.json.get('email', '').strip()
    psw1 = request.json.get('psw1', '')
    psw2 = request.json.get('psw2', '')
    if not username or not email or not psw1 or not psw2:
        return JsonResponse({"message": "Please fill all fields."}, status=400)
    if psw1 != psw2:
        return JsonResponse({"message": "Passwords are different."}, status=400)
    if len(psw1) < 6:
        return JsonResponse({"message": "Password is too short. Should be at least 6 characters long."}, status=400)
    try:
        User.objects.get(username=username)
        return JsonResponse({"message": "User already exist."}, status=400)
    except User.DoesNotExist:
        if re.compile(r"^[a-z0-9._-]+@[a-z0-9._-]+\.[a-z]+").match(email) is None:
            return JsonResponse({"message": "Email address is not valid."}, status=400)
        user = User.objects.create_user(username=username, email=email, password=psw1, first_name=first_name,
                                        last_name=last_name, mfa_key='')
        auth = authenticate(username=username, password=psw1)
        auth_login(request, auth)
        return JsonResponse({
            "message": "Registration successful.",
        }, status=200)


@require_http_methods(["POST"])
@json_parser
def connect(request):
    username = request.json.get('username', '').strip()
    password = request.json.get('password', '')
    auth = authenticate(username=username, password=password)
    if auth is not None:
        user = User.objects.get(id=auth.id)
        auth_login(request, auth)

        return JsonResponse({
            "message": "Login successful.",
        }, status=200)
    else:
        return JsonResponse({"message": "Bad credentials."}, status=401)


@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")


@login_required
@require_http_methods(["POST"])
@json_parser
def validate_mfa(request):
    token = request.json.get('token', '').strip()
    mfa = request.json.get('key', '').strip()
    user = User.objects.get(id=request.user.id)
    authenticator = ServerAuthenticator(mfa)
    print(authenticator.export_key())
    print("client: ", token, "/ server : ", authenticator.generate_token(), authenticator.get_previous_token())
    if token == authenticator.generate_token() or token == authenticator.get_previous_token():
        user.mfa_key = mfa
        user.save()
        return JsonResponse({
            "message":"MFA authenticator successful."
        }, status=200)
    else:
        return JsonResponse({"message": "Bad credentials."}, status=401)


@login_required
def generator(request):
    mfa_key = ServerAuthenticator().export_key()
    token = ClientAuthenticator(mfa_key).generate_token()
    print(token)
    return render(request, 'generator.html', {
        'mfa_key': mfa_key.decode('utf-8')
    })
