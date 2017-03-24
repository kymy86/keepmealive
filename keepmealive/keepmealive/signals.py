from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
import datetime


@receiver(user_logged_in)
def update_last_login(sender, user, request, **kwargs):
    user.last_login = datetime.now()
    user.save(update_fields['last_login'])
