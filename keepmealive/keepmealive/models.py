from django.db import models

class Folder(models.Model):
    name = models.CharField(max_length=100, blank=False)
    # define is the directory is a root directory or not.
    isroot = models.BooleanField(default=True)
    idparent = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name', 'created', )
    