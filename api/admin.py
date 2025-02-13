from django.contrib import admin # Importa el módulo de administración de Django, necesario para registrar modelos en el panel de administración.

# Register your models here.
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin # Importa la clase UserAdmin de Django, que se utiliza para personalizar la administración de usuarios.
from .models import CustomUser # Importa el modelo CustomUser de la aplicación api.


# Define a custom admin class for the CustomUser model
class CustomUserAdmin(DefaultUserAdmin):
    # Define los campos visibles en la edición de usuarios
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        
    )
    #Este bloque personaliza qué datos se pueden editar y visualizar en el formulario de edición de usuarios en el panel de administración.
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    # Define qué columnas se ven en la lista de usuarios

    # Personaliza qué usuarios puede ver cada usuario
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # # Superusuarios ven todos los usuarios
        return queryset.filter(is_superuser=False)  # Staff solo ve usuarios que no son superusuarios

# Registra el modelo CustomUser en el panel de administración de Django con la clase personalizada CustomUserAdmin.
admin.site.register(CustomUser, CustomUserAdmin)