from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


# Create your models here.

class cardSet(models.Model):
	name = models.CharField(max_length=100)
	order = models.IntegerField()
	length = models.IntegerField()
	def __unicode__(self):
		return self.name

class card(models.Model):
	name = models.CharField(max_length=100)
	cardSet = models.ForeignKey(cardSet)
	order = models.IntegerField()
	question = models.TextField()
	answer = models.TextField()

class userProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	info = models.TextField(default=' ')
	joinDate = models.DateTimeField(default=datetime.now())
	currentSet = models.ForeignKey(cardSet)
	onRandom = models.BooleanField(default=False)

class userSet(models.Model):
	user = models.ForeignKey(User)
	cardSet = models.ForeignKey(cardSet)

class userSetScore(models.Model):
	userSet = models.ForeignKey(userSet)
	attempt = models.IntegerField(default=0)
	attemptDate = models.DateTimeField(default=datetime.now())
	total = models.IntegerField()
	correct = models.IntegerField()
	iterations = models.IntegerField()
	def percent(self):
		return (float(self.correct)/float(self.total))*100
