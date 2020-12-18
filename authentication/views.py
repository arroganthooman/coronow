from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import auth, User
# Create your views here.



def login(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request, user)
			return redirect("index")

	if request.user.is_authenticated:
		return redirect("index")

	return render(request, "login.html")


def register(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]
		password = request.POST["password"]
		password1 = request.POST["password1"]


		try:
			user = User.objects.get(username=username)
			return redirect("register")
			
		
		except User.DoesNotExist:
			user = User.objects.create_user(username=username, email=email, password=password)
			user.save()
			user = auth.authenticate(username=username, password=password)
			auth.login(request, user)
			return redirect("index")


	if request.user.is_authenticated:
		return redirect("index")

	return render(request, "register.html")


def logging_out(request):
	logout(request)
	return redirect("index")
	