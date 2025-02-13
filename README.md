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


