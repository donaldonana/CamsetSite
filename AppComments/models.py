from django.db import models
from django.utils import timezone
from djongo import models



# Create your models here.


class Comment(models.Model):
	"""docstring for Comment"""

	CAT = (
    ('politique', 'politique'),
    ('sport', 'sport'),
    ('social', 'social'),
    ('Autre', 'Autre'),
    
    ) 

	categorie = models.CharField(max_length=25, choices=CAT, default="social")  
	post_titre = models.CharField(max_length=25,  blank=True, null = True) 
	post_img = models.CharField(max_length=25,  blank=True, null = True) 
	post_url = models.CharField(max_length=25) 
	texte = models.TextField(unique = True)
	haineux = models.IntegerField(default = 0)
	offensif = models.IntegerField(default = 0)
	non_offensif = models.IntegerField(default = 0)
	vote_final =  models.CharField(max_length=25, default="")
	file_name = models.CharField(max_length=25,  blank=True, null = True)
	totaux_votes = models.IntegerField(default = 0)


	 
	publied_at = models.DateTimeField(default = timezone.now)



	def __str__(self):
		return str(self.texte)

 