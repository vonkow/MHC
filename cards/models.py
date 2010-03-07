from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


# Create your models here.

class cardSet(models.Model):
	name = models.CharField(max_length=100)
	order = models.IntegerField()
	length = models.IntegerField()
	content = models.TextField()
	def __unicode__(self):
		return self.name
		
class card(models.Model):
	name = models.CharField(max_length=100)
	cardSet = models.ForeignKey(cardSet)
	order = models.IntegerField()
	question = models.TextField()
	answer = models.TextField()
	def __unicode__(self):
		return self.name

class userProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	joinDate = models.DateTimeField(default=datetime.now())
	currentSet = models.ForeignKey(cardSet)
	currentSetProgress = models.IntegerField(default=0)
	info = models.TextField(default=' ')
	sex = models.CharField(max_length=1, default=' ')
	dob = models.DateTimeField(null=True,blank=True)
	birth_city = models.CharField(max_length=255, default=' ')
	birth_country = models.CharField(max_length=255, default=' ')
	city = models.CharField(max_length=255, default=' ')
	country = models.CharField(max_length=255, default=' ')
	zip = models.IntegerField(default=0)
	religion = models.CharField(max_length=255, default=' ')
	marital_status = models.CharField(max_length=255, default=' ')
	marriages = models.IntegerField(default=0)
	children = models.IntegerField(default=0)
	grandchildren = models.IntegerField(default=0)
	brothers = models.IntegerField(default=0)
	sisters = models.IntegerField(default=0)
	birth_order = models.IntegerField(default=0)
	education = models.CharField(max_length=255, default=' ')
	occupation = models.CharField(max_length=255, default=' ')
	former_occupation = models.CharField(max_length=255, default=' ')
	spouse_education = models.CharField(max_length=255, default=' ')
	spouse_occupation = models.CharField(max_length=255, default=' ')
	mother_education = models.CharField(max_length=255, default=' ')
	mother_occupation = models.CharField(max_length=255, default=' ')
	father_education = models.CharField(max_length=255, default=' ')
	father_occupation = models.CharField(max_length=255, default=' ')
	def __unicode__(self):
		return self.user.username

class userSet(models.Model):
	user = models.ForeignKey(User)
	cardSet = models.ForeignKey(cardSet)
	attempts = models.IntegerField(default=0)
	def __unicode__(self):
		return u'%s - %s' % (self.user.username, self.cardSet.name)

class userSetScore(models.Model):
	userSet = models.ForeignKey(userSet)
	attempt = models.IntegerField(default=0)
	attemptDate = models.DateTimeField(default=datetime.now())
	total = models.IntegerField()
	correct = models.IntegerField()
	iterations = models.IntegerField()
	def percent(self):
		return (float(self.correct)/float(self.total))*100
	def __unicode__(self):
		return u'%s - %s - %s' % (self.userSet.user.username, self.userSet.cardSet.name, str(self.attempt))
