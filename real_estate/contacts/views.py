from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

from .models import Contact


def contact(request):
	if request.method == "POST":
		listing_id = request.POST['listing_id']
		listing = request.POST['listing']
		name = request.POST['name']
		email = request.POST['email']
		phone = request.POST['phone']
		message = request.POST['message']
		user_id = request.POST['user_id']
		realtor_email = request.POST['realtor_email']
		
		# Check for duplicate inquiries (contacts)
		if request.user.is_authenticated:
			user_id = request.user.id
			has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id).exists()
			if has_contacted:
				messages.error(request, 'Inquiry Already Made.')
				return redirect('/listings/' + listing_id)
		
		new_contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message,
													user_id=user_id)
		new_contact.save()
		
		# Send mail
		# send_mail(
		# 	'Property Listing Inquiry',
		# 	'There has been an Inquiry for ' + listing + '. Sign into the admin panel for more info.',
		# 	'traversty.brad@gmail.com',
		# 	[realtor_email, 'd.valiev@student.inha.uz'],
		# 	fail_silently=False
		# )
		
		messages.success(request, "Request Submitted. Realtor will contact you soon.")
		return redirect('/listings/' + listing_id)
