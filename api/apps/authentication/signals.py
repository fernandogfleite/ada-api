
from api.apps.authentication.models.user import UserConfirmation
from api.apps.authentication.tasks import task_send_email
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_rest_passwordreset.signals import reset_password_token_created

from decouple import config


@receiver(post_save, sender=UserConfirmation)
def send_email_confirmation(sender, instance, created, **kwargs):
    if created:
        data = {
            "name": instance.user.first_name,
            "link": config('CONFIRM_EMAIL_URL') + f"?identification_code={instance.token}",
        }

        task_send_email.delay(
            subject="Confirmação de email",
            to=instance.user.email,
            template="authentication/email_confirmation.html",
            data=data
        )


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    data = {
        "name": reset_password_token.user.first_name,
        "link": config('RESET_PASSWORD_URL') + f"?token={reset_password_token.key}",
    }

    task_send_email.delay(
        subject="Recuperação de senha",
        to=reset_password_token.user.email,
        template="authentication/reset_password.html",
        data=data
    )
