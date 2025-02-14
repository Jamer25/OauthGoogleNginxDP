from django.urls import path
from .views import * # Importa todas las vistas definidas en api/views.py

urlpatterns = [#Define las rutas de la aplicación
    path('signup/', signup_view, name='signup'),#Define la ruta de registro, que llama a la vista signup_view
    path('login/', login_view, name='login'),#Define la ruta de inicio de sesión, que llama a la vista login_view
    path('forgot-password/', forgot_password_view, name='forgot_password'),#Define la ruta de olvido de contraseña, que llama a la vista forgot_password_view
    path('reset-password/<str:token>/', reset_password_view, name='reset_password'),#Define la ruta de restablecimiento de contraseña, que llama a la vista reset_password_view
    path('logout/', logout_view, name='logout'),#Define la ruta de cierre de sesión, que llama a la vista logout_view
]