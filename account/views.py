from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from friend.utils import get_friend_request_or_false
from friend.friend_request_status import FriendRequestStatus

from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from .models import Account
from friend.models import FriendList, FriendRequest
from django.db.models import Q


def register_view(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated: 
		return HttpResponse("You are already authenticated as " + str(user.email))
	
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			destination = get_redirect_if_exists(request)
			if destination:
				return redirect(destination)
			return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)


def logout_view(request):
	logout(request)
	return redirect("home")


def login_view(request):
	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid:
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			if user:
				login(request, user)
				destination = get_redirect_if_exists(request)
				if destination:
					return redirect(destination)
				return redirect("home")
			# else:
			# 	context['login_form'] = form
		else:
			context['login_form'] = form
	
	return render(request, "account/login.html",context)


def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect


def account_view(request, *args, **kwargs):
	"""
	Logic here is kind of tricky
	-is_self (boolean)
		is_friend (boolean)
			-1: NO_REQUEST_SENT
			0: THEM_SENT_TO_YOU
			1: YOU_SENT_TO_THEM
	"""

	context = {}
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk=user_id)
	except Account.DoesNotExist:
		return HttpResponse("That user doesn't exist.")
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.email
		context['profile_image'] = account.profile_image
		context['hide_email'] = account.hide_email
	try:
		friend_list = FriendList.objects.get(user=account)
	except FriendList.DoesNotExist:
		friend_list = FriendList(user=account)
		friend_list.save()
	friends = friend_list.friends.all()
	context['friends'] = friends
	#Define state template variables
	is_self = True
	is_friend = False
	user = request.user
	request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
	friend_requests = None
	if user.is_authenticated and user != account:
		is_self = False
		if friends.filter(pk=user.id):
			is_friend = True
		else:
			is_friend = False
			#Case1: Request has been sent from THEM to YOU:  
			# FriendRequestStatus.THEM_SENT_TO_YOU
			if get_friend_request_or_false(sender=account, receiver=user) != False:
				request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
				context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
			#Case2: Request has been sent from YOU to THEM:  
			# FriendRequestStatus.YOU_SENT_TO_THEM
			elif get_friend_request_or_false(sender=user, receiver=account) != False:
				request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
			#CASE3: No request has been sent  
			# FriendRequestStatus.NO_REQUEST_SENT
			else:
				request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
	
	elif not user.is_authenticated:
		is_self = False
	else:
		try:
			friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
		except:
			pass

	context['is_self'] = is_self
	context['is_friend'] = is_friend
	context['BASE_URL'] = settings.BASE_URL
	context['request_sent'] = request_sent
	context['friend_requests'] = friend_requests
	return render(request, 'account/account.html', context)


def account_search_view(request, *args, **kwargs):
	context = {}

	if request.method == "GET":
		search_query = request.GET.get("q")
		if len(search_query) > 0:
			search_results = Account.objects.filter(
				Q(email__icontains=search_query) | Q(username__icontains=search_query)
				)
			user = request.user
			accounts = []
			if user.is_authenticated:
				auth_user_friend_list = FriendList.objects.get(user=user)
				for account in search_results:
					accounts.append((account, auth_user_friend_list.is_mutual_friend(account)))
				context['accounts'] = accounts
			else:
				for account in search_results:
					accounts.append((account, False))
				context['accounts'] = accounts

	return render(request, "account/search_results.html", context)


def edit_account_view(request, *args, **kwargs):
	if not request.user.is_authenticated:
		return redirect("login")
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk=user_id)
	except Account.DoesNotExist:
		return HttpResponse("Something went wrong")
	if account.pk != request.user.id:
		return HttpResponse("You cannot edit someone elses profile")
	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect("account:view", user_id=account.pk)
		else:
			form = AccountUpdateForm(request.POST, instance=request.user,
							initial={
								"id": account.pk,
								"email": account.email,
								"username": account.username,
								"profile_image": account.profile_image,
								"hide_email": account.hide_email
							}
							)
			context["form"] = form
			
	else:
		form = AccountUpdateForm(
							initial={
								"id": account.pk,
								"email": account.email,
								"username": account.username,
								"profile_image": account.profile_image,
								"hide_email": account.hide_email
							}
							)
		context["form"] = form
	context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
	return render(request, "account/edit_account.html", context)
