import binascii,os
from django.db import models
from django.contrib.auth.models import User


class Token(models.Model):  
    """
    The default authorization token model.
    """
    key = models.CharField("Key", max_length=40, primary_key=True)
    user = models.ForeignKey(User, verbose_name='User',
                             related_name='tokens', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField("Created", auto_now_add=True)

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

class Address(models.Model):
    """Storing the address of the user"""
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    latitude = models.CharField(max_length=20,blank=True,null=True)
    longitude = models.CharField(max_length=20,blank=True,null=True)
    
