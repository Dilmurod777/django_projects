from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

from contacts.models import Contact


def register(request):
	if request.method == 'POST':
		# Register User
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		password2 = request.POST['password2']
		
		# Check if Passwords match
		if password == password2:
			# Check duplicate username
			if User.objects.filter(username=username).exists():
				messages.error(request, "Username already taken.")
				return redirect('register')
			else:
				# Check duplicate email
				if User.objects.filter(email=email).exists():
					messages.error(request, "Email already taken.")
					return redirect('register')
				else:
					user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
																					last_name=last_name)
					# Login after Register
					user.save()
					messages.success(request, 'Successfully Register.')
					return redirect('login')
		else:
			messages.error(request, "Passwords do not match.")
			return redirect('register')
	else:
		return render(request, 'accounts/register.html')


def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		
		user = auth.authenticate(username=username, password=password)
		
		if user is not None:
			auth.login(request, user)
			messages.success(request, 'Logged In.')
			return redirect('dashboard')
		else:
			messages.error(request, 'Invalid Credentials.')
			return redirect('login')
	else:
		return render(request, 'accounts/login.html')


def logout(request):
	if request.method == 'POST':
		auth.logout(request)
		messages.success(request, 'LOGGED OUT.')
		return redirect('index')


def dashboard(request):
	user_contacts = Contact.objects.all().filter(user_id=request.user.id).order_by('-contact_date')
	
	context = {
		'contacts': user_contacts
	}
	
	return render(request, 'accounts/dashboard.html', context)
