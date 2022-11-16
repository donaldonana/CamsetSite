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



class CommentStats(models.Model):
	"""docstring for CommentStats"""

	def save(self, *args, **kwargs):
		if not self.pk and CommentStats.objects.exists():
		# if you'll not check for self.pk 
		# then error will also raised in update of exists model
			raise ValidationError('There is can be only one JuicerBaseSettings instance')
		return super(CommentStats, self).save(*args, **kwargs)

	nbr_comment = models.IntegerField(default = 4)

	nbr_categorie = models.IntegerField(default = 7221)

	def __str__(self):
		return str(self.texte)
	
		