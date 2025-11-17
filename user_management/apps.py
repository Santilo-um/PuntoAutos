from django.apps import AppConfig
from django.contrib.auth import get_user_model

class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth'

    def ready(self):
        Usuario = get_user_model()
        if not Usuario.objects.filter(email="admin@puntoautos.com").exists():
            Usuario.objects.create_superuser(
                username="admin",
                email="s.longo@alumno.um.edu.ar",
                password="diagonal",
                is_admin=True
            )


class UserManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_management'
