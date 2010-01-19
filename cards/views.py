from django.core import serializers
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django.core.mail import send_mail
from django.db import IntegrityError
from django.contrib import auth
from django.template import RequestContext
from datetime import datetime
from mhc.cards.models import cardSet, card, userProfile, userSet, userSetScore

# Create your views here.

# (HELPER FUNCTION)
# Gets or Creates a Profile linked to specified user
def get_or_create_profile(user):
	try:
		profile = user.get_profile()
	except ObjectDoesNotExist:
		#Create Profile
		profile = userProfile(user=user, info=' ', currentSet=cardSet.objects.get(pk=1))
		profile.save()
	return profile

def get_or_create_userset(user, cardset):
	try:
		userset = userSet.objects.get(user=user, cardSet=cardset)
	except ObjectDoesNotExist:
		userset = userSet(user=user, cardSet=cardset)
		userset.save()
	return userset

def newUser(request):
	#Check for existing username and email (could be written better)
	user_list = auth.models.User.objects.filter(username=request.POST['username'])
	email_list = auth.models.User.objects.filter(email=request.POST['email'])
	noU=True
	noE=True
	for user in user_list:
		noU=False
	for email in email_list:
		noE=False
	#If username isn't taken
	if noU:
		#If email isn't taken
		if noE:
			#Create user
			user = auth.models.User.objects.create_user(username = request.POST['username'], 
														password = request.POST['password'], 
														email = request.POST['email'])
			user.save()
			#Create Profile
			user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
			user.userprofile = get_or_create_profile(user)
			if user is not None and user.is_active:
				auth.login(request, user)
		else:
			a=1
	else:
		a=1
	return HttpResponseRedirect('/')

def login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = auth.authenticate(username=username, password=password)
	if user is not None and user.is_active:
		auth.login(request, user)
		return HttpResponseRedirect('/main')
	else:
		return HttpResponseRedirect('/')

def logout(request):
	if request.user.is_authenticated():
		auth.logout(request)
	return HttpResponseRedirect('/')

def showLogin(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/main')
	else:
		return render_to_response('login.html',)

def showSet(request):
	if request.user.is_authenticated():
		profile = get_or_create_profile(request.user)
		Set = profile.currentSet
		return render_to_response('card.html', {'set': Set}, context_instance=RequestContext(request))
	else:
		#Return user to login/register page
		return HttpResponseRedirect('/')

def processSet(request):
	if request.user.is_authenticated():
		profile = get_or_create_profile(request.user)
		current_set = profile.currentSet #cardSet.objects.get(pk=request.POST['set'])
		userset = get_or_create_userset(request.user, current_set)
		userset.attempts = userset.attempts+1
		userset.save()
		usersetscore = userSetScore(userSet=userset, total=request.POST['total'], correct=request.POST['correct'], iterations=request.POST['iterations'], attempt=userset.attempts)
		usersetscore.save()
		calcResults(request)
		usersetscores = userset.usersetscore_set.all().order_by('attempt')
		return render_to_response('graph.html', {'scores': usersetscores})
	else:
		#Return user to login/register page
		return HttpResponseRedirect('/')

def isFirstSet(set):
	if set.order == 1:
		return True
	else:
		return False

def isLastSet(set):
	all_sets = cardSet.objects.all()
	for curSet in all_sets:
		if curSet.order > set.order:
			return False
	return True

def calcResults(request):
	if request.user.is_authenticated():
		profile = get_or_create_profile(request.user)
		userset = get_or_create_userset(request.user, profile.currentSet)
		usersetscores = userset.usersetscore_set.all().order_by('-attempt')
		# minimum of 3 attempts
		if userset.attempts>3:
			percent = usersetscores[0].percent()
			total = usersetscores[0].total
			iterations = usersetscores[0].iterations
			# Faster and More Accurate plus at least one full cycle
			if percent >= usersetscores[1].percent() and total >= usersetscores[1].total and iterations > 0:
				setId = profile.currentSet.id
				if not isLastSet(get_object_or_404(cardSet, pk=setId)):
					newSet = get_object_or_404(cardSet, pk=setId+1)
					profile.currentSet = newSet
					profile.save()
				return 1
			# Slower and less accurate
			elif percent < usersetscores[1].percent() and total < usersetscores[1].total:
				setId = profile.currentSet.id
				if not isFirstSet(get_object_or_404(cardSet, pk=setId)):
					newSet = get_object_or_404(cardSet, pk=setId-1)
					profile.currentSet = newSet
					profile.save()
				return -1
			# Neither of the Above
			else:
				return 0
		# First Attempt, maybe return 0 as well
		else:
			return 2
	else:
		return 3
