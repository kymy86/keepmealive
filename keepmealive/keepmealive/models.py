from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
import uuid

class PasswordForgotRequest(models.Model):
    hash = models.UUIDField(blank=False, editable=False)
    user = models.ForeignKey(User, related_name="password_requests")
    date = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    ip_addr = models.GenericIPAddressField(blank=False, default='0.0.0.0')

    class Meta:
        ordering = ('date', )

    @property
    def uuid_str(self):
        return str(self.hash)

@receiver(pre_save, sender=PasswordForgotRequest)
def generate_hash(sender, instance, *args, **kwargs):
    if instance.pk is None:
        instance.hash = uuid.uuid4()