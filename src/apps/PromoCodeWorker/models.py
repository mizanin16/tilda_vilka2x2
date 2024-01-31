from django.db import models


class Promocode(models.Model):
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.code
