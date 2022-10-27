from django.db import models
from djongo import models


from django.contrib.auth.models import AbstractUser
from AppComments.models import Comment

class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
    commentaires = models.ManyToManyField(Comment, related_name='commentaires', through='comments')
    index = models.IntegerField(default = 1)
    checked = models.ManyToManyField(Comment, related_name='checked_comments')

    def __str__(self):
        return self.email


class comments(models.Model):

	person = models.ForeignKey(User, on_delete=models.CASCADE,
        blank=True, null = True)
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
        blank=True, null = True)
	reponse = models.CharField(max_length = 25, blank=True, null = True)


