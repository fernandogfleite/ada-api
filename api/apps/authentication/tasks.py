from django.core import mail
from django.template.loader import render_to_string
from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task(name="send_email")
def task_send_email(subject, to, template, data):
    logger.info("Sending email...")

    connection = mail.get_connection()
    connection.open()
    message_html = render_to_string(template, data)

    email = mail.EmailMultiAlternatives(
        subject,
        to=[to],
        connection=connection
    )

    email.attach_alternative(message_html, "text/html")

    email.send()

    connection.close()

    logger.info("Email sent")

    return True
