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

def get_set_list():
	return cardSet.objects.all()

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
			profile = get_or_create_profile(user)
			if request.POST['sex']:
				if request.POST['sex']=='male':
					profile.sex = 'm'
				else:
					profile.sex = 'f'
			if request.POST['birth_city']:
				profile.birth_city = request.POST['birth_city']
			if request.POST['birth_country']:
				profile.birth_country = request.POST['birth_country']
			if request.POST['city']:
				profile.city = request.POST['city']
			if request.POST['country']:
				profile.country = request.POST['country']
			if request.POST['zip']:
				profile.zip = int(request.POST['zip'])
			if request.POST['religion']:
				profile.religion = request.POST['religion']
			if request.POST['marital_status']:
				profile.marital_status = request.POST['marital_status']
			if request.POST['marriages']:
				profile.marriages = int(request.POST['marriages'])
			if request.POST['children']:
				profile.children = int(request.POST['children'])
			if request.POST['grandchildren']:
				profile.grandchildren = int(request.POST['grandchildren'])
			if request.POST['brothers']:
				profile.brothers = int(request.POST['brothers'])
			if request.POST['sisters']:
				profile.sisters = int(request.POST['sisters'])
			if request.POST['birth_order']:
				profile.birth_order = int(request.POST['birth_order'])
			if request.POST['education']:
				profile.education = request.POST['education']
			if request.POST['occupation']:
				profile.occupation = request.POST['occupation']
			if request.POST['former_occupation']:
				profile.former_occupation = request.POST['former_occupation']
			if request.POST['spouse_education']:
				profile.spouse_education = request.POST['spouse_education']
			if request.POST['spouse_occupation']:
				profile.spouse_occupation = request.POST['spouse_occupation']
			if request.POST['mother_education']:
				profile.mother_education = request.POST['mother_education']
			if request.POST['mother_occupation']:
				profile.mother_occupation = request.POST['mother_occupation']
			if request.POST['father_education']:
				profile.father_education = request.POST['father_education']
			if request.POST['father_occupation']:
				profile.father_occupation = request.POST['father_occupation']
			profile.save()
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

def showAllView(request):
	if request.user.is_authenticated():
		set_list = cardSet.objects.all()
		return render_to_response('all_single.html', {'all_sets':set_list}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def showSetView(request, setId):
	if request.user.is_authenticated():
		set_list = cardSet.objects.all()
		Set = get_object_or_404(cardSet, pk=setId)
		return render_to_response('set_single.html', {'all_sets':set_list, 'set':Set}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def showCardView(request, setId, cardId):
	if request.user.is_authenticated():
		set_list = cardSet.objects.all()
		Set = get_object_or_404(cardSet, pk=setId)
		Card = get_object_or_404(card, cardSet=Set, order=cardId)
		return render_to_response('card_single.html', {'all_sets':set_list, 'card':Card}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def selectSet(request, setNum):
	if request.user.is_authenticated():
		profile = get_or_create_profile(request.user)
		Set = get_object_or_404(cardSet, pk=setNum)
		profile.currentSet = Set
		profile.save()
		return HttpResponseRedirect('/main')
	else:
		return render_to_response('login.html',)

def showSet(request):
	if request.user.is_authenticated():
		set_list = get_set_list()
		profile = get_or_create_profile(request.user)
		Set = profile.currentSet
		random_order = 0
		userset = get_or_create_userset(request.user, Set)
		if userset.attempts > 0:
			random_order = 1
		return render_to_response('card.html', {'set': Set, 'random_order':random_order, 'set_list': set_list}, context_instance=RequestContext(request))
	else:
		#Return user to login/register page
		return HttpResponseRedirect('/')

def processSet(request):
	if request.user.is_authenticated():
		set_list = get_set_list()
		profile = get_or_create_profile(request.user)
		current_set = profile.currentSet #cardSet.objects.get(pk=request.POST['set'])
		userset = get_or_create_userset(request.user, current_set)
		userset.attempts = userset.attempts+1
		userset.save()
		usersetscore = userSetScore(userSet=userset, total=request.POST['total'], correct=request.POST['correct'], iterations=request.POST['iterations'], attempt=userset.attempts)
		usersetscore.save()
		calcResults(request)
		usersetscores = userset.usersetscore_set.all().order_by('attempt')
		return render_to_response('graph.html', {'scores': usersetscores, 'set_list': set_list}, context_instance=RequestContext(request))
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
