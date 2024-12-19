from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dotfm.core"

    def ready(self):
        # This prevents django-fastdev from raising an error when accessing the signup page.
        # We do not ask for a username or email validation on the signup page.
        # If you change this logic, you should update or remove this code.
        from allauth.account.forms import SignupForm

        SignupForm.clean_username = None
        SignupForm.clean_email2 = None
