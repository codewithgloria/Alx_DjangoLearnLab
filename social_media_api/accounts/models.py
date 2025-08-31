from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followers_of') 

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='accounts_user_set',        
        related_query_name='account_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='accounts_user_permissions_set',  
        related_query_name='account_user_permission'
    )

    def __str__(self):
        return self.username