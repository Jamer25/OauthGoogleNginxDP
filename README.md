# OauthGoogleNginxDP
Se añadirá la autenticación con google a los servicios que tendremos en un docker-compose.yml los cuales son: nginx, django,postgresql, pgadmin

# Primero agregamos Dockerfile, requirements.txt, docker-compose.yml
Agregamos todos los servicios como ya lo hemos hecho:
nginx, django,postgresql, pgadmin

# Para usar autenticación con google necesitamos:
en requirements.txt:
django-allauth
Sería:
            Django==4.2.9
            psycopg2-binary==2.9.10 
            pillow==11.1.0
            django-allauth

# Ahora en settings.py agregar:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',\
    "allauth.account.middleware.AccountMiddleware",  
]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default backend
    'allauth.account.auth_backends.AuthenticationBackend',    # for google

]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'colocar el id de gcp',
            'secret': 'colocar el secrect de gcp',
            'key': ''
        }
    }
}

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'welcome'
ACCOUNT_LOGOUT_REDIRECT_URL = 'login'



# Usar el template de django admin
crear una carpeta templates, dentro de esa carpeta otra llamada admin y luego dentro de eso 
un archivo llamado login.html
y si queremos agregar estilos una carpeta dentro de template llamada static y dentro de eso el .css

login.html:
    # Utiliza Django Template Language (DTL) para estructurar y renderizar dinámicamente el contenido.
    {% extends "admin/base_site.html" %}# Extiende la plantilla base de Django admin.
    #base_site.html :ya contiene la estructura general del sitio (HTML, CSS, JavaScript, encabezados, etc.).

    {% block content %}#Django Admin tiene bloques predefinidos en base_site.html, como content, title, branding, etc.
        <div class="login-container"># Contenedor div de inicio de sesión. Para agrupar visualmente el formulario de inicio de sesión.
            <h2>Iniciar sesión ahora</h2>
            <form method="post">
                {% csrf_token %} # Para proteger el formulario de ataques CSRF.
                {{ form.as_p }} # Renderiza el formulario de inicio de sesión.
                <button type="submit">Acceder</button>
            </form>
        </div>
    {% endblock %}

 #   login.html igual que el por defecto:
    
   {% extends "admin/login.html" %}# Esto extiende el diseño original de Django



{% block branding %}# Esto modifica el bloque branding del diseño original
    <h1 style="color: #f8f8f8;">Django Administration</h1>
{% endblock %}

{% block content %}#  contiene todo el formulario de login.
    {{ block.super }}  # Esto mantiene el diseño original y solo agrega cambios extra 
{% endblock %}

# Agregando botón google:
Cuando agregas esta línea al inicio de login.html:

html
Copiar
Editar
{% load socialaccount %}
le estás diciendo a Django que cargue los template tags de django-allauth.socialaccount, lo que permite usar:

html
Copiar
Editar
{% provider_login_url 'google' %}

# Sería:
{% extends "admin/login.html" %}


{% load socialaccount %} 
{% block branding %}
    <h1 style="color: #f8f8f8;">Django Administration</h1>
{% endblock %}

{% block content %}
    {{ block.super }} 
    <div class="media-options">
        <a href="{% provider_login_url 'google' %}" class="field google">
            <i class="fa-brands fa-google googleicon"></i>
            <span>Login with Google</span>
        </a>
    </div>
{% endblock %}



