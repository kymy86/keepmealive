import base64
from django.db import models
from folders.models import Folder
from Crypto.Cipher import AES
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Item(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    password = models.TextField(blank=False)
    username = models.CharField(max_length=250, blank=False)
    url = models.URLField(blank=True)
    folder = models.ForeignKey(Folder, related_name='items')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name', 'created', )

    @property
    def pwd(self):
        secret = AES.new(settings.MASTER_KEY[:32])
        raw_decrypt = secret.decrypt(base64.b64decode(self.password))
        clear_val = raw_decrypt.rstrip(b"\0")
        return clear_val

@receiver(pre_save, sender=Item)
def encrypt_password(sender, instance, *args, **kwargs):
    #encrypt password before saving it
    secret = AES.new(settings.MASTER_KEY[:32])
    tag = (str(instance.password) + (AES.block_size -
                                    len(str(instance.password)) % AES.block_size) * "\0")
    cypher = base64.b64encode(secret.encrypt(tag))
    instance.password = cypher
