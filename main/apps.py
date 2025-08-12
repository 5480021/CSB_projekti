from django.apps import AppConfig

# ----------------------------------------
# FLAW 3: Authentication Failure (A07:2021-Identification and Authentication Failures) 
# ----------------------------------------

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from django.contrib.auth.models import User

        # FLAW: creates default admin user with weak password
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'admin',
                'admin@example.com',
                'admin'
            )

        #FIX: Do not use default credentials in production
        #if not User.objects.filter(username='admin').exists():
        #    User.objects.create_superuser(
        #        'admin',
        #        'admin@example.com',
        #        'Strong&SecurePassword2024'
        #)
