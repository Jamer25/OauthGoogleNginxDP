from django.shortcuts import render, redirect # Importa las funciones render y redirect de Django, necesarias para renderizar plantillas y redirigir a otras vistas.
from django.contrib.auth import authenticate, login, logout # Importa las funciones authenticate, login y logout de Django, necesarias para autenticar usuarios y gestionar sesiones.
from django.http import JsonResponse  # 📌 Importar JsonResponse para API
from .models import CustomUser, PasswordResetRequest # Importa los modelos CustomUser y PasswordResetRequest de la aplicación api.
from django.utils import timezone # Importa el módulo timezone de Django, necesario para trabajar con zonas horarias.
from django.contrib import messages # Importa el módulo de mensajes de Django, necesario para mostrar mensajes al usuario.
from django.core.mail import send_mail # Importa la función send_mail de Django, necesaria para enviar correos electrónicos.
from django.conf import settings # Importa el módulo de configuración de Django, necesario para acceder a la configuración de la aplicación.
from django.utils.crypto import get_random_string # Importa la función get_random_string de Django, necesaria para generar tokens aleatorios.

# Define la vista index, que renderiza la plantilla index.html
# Este código define varias vistas en Django para manejar la autenticación de usuarios, incluyendo:

#Registro (signup_view)
#Inicio de sesión (login_view)
#Olvido de contraseña (forgot_password_view)
#Restablecimiento de contraseña (reset_password_view)
#Cierre de sesión (logout_view)

#Antes: Django servía el frontend y renderizaba index.html y welcome.html.
#Ahora: Django solo devuelve JSON y Nginx se encarga de servir las páginas HTML.


# 🔹 Elimina la vista index, ya no es necesaria porque la maneja Nginx

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if CustomUser.objects.filter(username=email).exists():
            return JsonResponse({"error": "A user with this email already exists."}, status=400)

        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user, backend=user.backend)

        return JsonResponse({"message": "Signup successful!", "user": email}, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful", "user": email}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()

        if user:
            token = get_random_string(32)
            reset_request = PasswordResetRequest.objects.create(user=user, email=email, token=token)
            reset_request.send_reset_email()
            return JsonResponse({"message": "Reset link sent to your email"}, status=200)
        else:
            return JsonResponse({"error": "Email not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def reset_password_view(request, token):
    reset_request = PasswordResetRequest.objects.filter(token=token).first()

    if not reset_request or not reset_request.is_valid():
        return JsonResponse({"error": "Invalid or expired reset link"}, status=400)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        reset_request.user.set_password(new_password)
        reset_request.user.save()
        return JsonResponse({"message": "Password reset successful"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def logout_view(request):
    logout(request)
    return JsonResponse({"message": "You have been logged out."}, status=200)