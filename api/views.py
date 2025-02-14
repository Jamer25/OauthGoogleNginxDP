from django.shortcuts import render, redirect # Importa las funciones render y redirect de Django, necesarias para renderizar plantillas y redirigir a otras vistas.
from django.contrib.auth import authenticate, login, logout # Importa las funciones authenticate, login y logout de Django, necesarias para autenticar usuarios y gestionar sesiones.
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

def index(request):
    return render(request, 'index.html') #Renderiza la página principal index.html.
# No realiza ninguna lógica, solo muestra la plantilla.

def welcome(request):
    return render(request, "welcome.html")



def signup_view(request):
    if request.method == 'POST': # Si la solicitud es de tipo POST (es decir, se envió un formulario)
        #Recoge los datos del formulario
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

         # 🔹 Verificar si el usuario ya existe
        if CustomUser.objects.filter(username=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return redirect('signup')  # Redirige de vuelta al formulario de registro
        
        #Crea un nuevo usuario con estos datos:
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.save() #Guarda el usuario en la base de datos
        user.backend = 'django.contrib.auth.backends.ModelBackend' 
        login(request, user, backend=user.backend) #Inicia sesión con el nuevo usuario
        messages.success(request, 'Signup successful!')#Muestra un mensaje de éxito
        return redirect('index')  #Redirige al usuario a la página principal
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)#Autentica al usuario con las credenciales proporcionadas
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('welcome')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'index.html')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        print(f"🔍 Buscando usuario con email: {email}")  # 🐞 Debugging

        user = CustomUser.objects.filter(email=email).first()
        
        if user:
            token = get_random_string(32)
            print(f"✅ Token generado: {token}")  # 🐞 Debugging
            
            reset_request = PasswordResetRequest.objects.create(user=user, email=email, token=token)
            reset_request.send_reset_email()

            print(f"📧 Email enviado a {email}")  # 🐞 Debugging
            messages.success(request, 'Reset link sent to your email.')
        else:
            print(f"❌ No se encontró usuario con email: {email}")  # 🐞 Debugging
            messages.error(request, 'Email not found.')
    
    return render(request, 'index.html')


def reset_password_view(request, token):#Define la vista reset_password_view para manejar el proceso de restablecimiento de contraseña.
    reset_request = PasswordResetRequest.objects.filter(token=token).first()#Busca una solicitud de restablecimiento de contraseña con el token proporcionado.
    
    if not reset_request or not reset_request.is_valid():
        messages.error(request, 'Invalid or expired reset link')
        return redirect('index')

    if request.method == 'POST':
        new_password = request.POST['new_password']
        reset_request.user.set_password(new_password)
        reset_request.user.save()
        messages.success(request, 'Password reset successful')
        return redirect('login')

    return render(request, 'reset_password.html', {'token': token})#Renderiza la plantilla reset_password.html con el token proporcionado.


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')
# Define la vista logout_view para manejar el cierre de sesión de un usuario.

