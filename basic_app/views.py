import os

from django.conf import settings

from django.shortcuts import render
from basic_app.forms import UserForm, ImageUploadForm,FileUploadForm,GroupImageUploadForm, CourseImageUploadForm
from basic_app.models import TempUser , Profile, Post, TempFriendRequest, Friendship, Comment, Message, Message_Notification, Group, GroupTable,GroupPost,GroupComment,GroupFile
from basic_app.models import Course, CourseTable, CoursePost, CourseComment, CourseFile, Grade, ForgotPwd, Photo_links
from basic_app.models import ImageTable
from django.contrib.auth.models import User
from django.contrib import messages

import urlparse



# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail

import bcrypt
import base64
import datetime
import logging
import jwt
import uuid
import glob

from datetime import datetime, date, time, timedelta

from collections import OrderedDict

from django.core.files.storage import default_storage




import urllib, json
from django.core.serializers.json import DjangoJSONEncoder

secret_key = 'Thisisasecretkey12301902qsd90hwqeuy230489h'


URL_CONFIRM ="https://schoolmash.com/basic_app/confirm/"
#URL_CONFIRM ="localhost:8000/basic_app/confirm/"
#URL_RESET="localhost:8000/reset_pwd/"
URL_RESET="https://schoolmash.com/reset_pwd/"

logging.basicConfig(filename="server.log", level=logging.INFO , format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
#logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def get_image_links_of_all_posts(posts):
	# Below we have to use an Ordered Dict because we want to iterate over dict in the way they are entered in the dictionary.
	# if you dont use orderedDict then when iterating over keys you dont get the order of insertion
	dictionary = OrderedDict()  # dictionary will hold key value pairs. Where key is the post and value is the QuerySet which contains all comments for that post

	for post in posts:
		dictionary[post] = Photo_links.objects.filter(which_post=post)
	# print post.pub_date

	#print("printing inside after dic is made")
	# for key, value in dictionary.iteritems():
	#	print key.pub_date

	return dictionary

def get_comments_of_all_posts(posts):

	#Below we have to use an Ordered Dict because we want to iterate over dict in the way they are entered in the dictionary.
	#if you dont use orderedDict then when iterating over keys you dont get the order of insertion
	dictionary = OrderedDict()  #dictionary will hold key value pairs. Where key is the post and value is the QuerySet which contains all comments for that post

	for post in posts:
		dictionary[post]=Comment.objects.filter(which_post=post)
		#print post.pub_date

	print("printing inside after dic is made")
	#for key, value in dictionary.iteritems():
	#	print key.pub_date

	return dictionary

def get_all_posts_related_to_user(user):
	# get all friends of ow1
	friends = Friendship.objects.all().filter(creator=user)



	posts = Post.objects.all().filter(owner=user)

	# The below for loop gives you the queryset that contains of all the posts of user's friends

	for i in friends:
		posts = Post.objects.all().filter(owner=i.friend) | posts  # the | just acts as OR



	#combine user's posts with friends posts
	#total_posts = friends_posts | user_posts

	#now order the posts by pub date/time
	ordered_posts = posts.order_by('pub_date')

	return ordered_posts

# Create your views here.
def index(request):
	logging.info("Client sent a request for the index page")
	return render(request,'basic_app/index.html')

def welcome(request):
    return render(request,'basic_app/welcome.html')

@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in")

@login_required
def user_logout(request):
	# Log out the user.
	logging.info(" Client " + request.user.username + " wants to logout of the current sesssion. Logging out client and directing them back to index/login page")

	logout(request)
	# Return to homepage.
	return HttpResponseRedirect(reverse('user_login'))


'''def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

            # login the user as well. Below does it
            login(request, user)
            #return render(request, 'basic_app/welcome.html')
            return HttpResponseRedirect('/basic_app/profile')

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'basic_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

'''

def user_login(request):

	if request.method == 'POST':
		# First get the username and password supplied

		username = request.POST.get('username')
		print("email received from client is " + str(username))

		password = request.POST.get('password')
		print("the password received is " + password)

		logging.info(" Client sent a HTTP POST request for login page")
		logging.info(" Username entered: "+username+ "  Password entered: "+password)
		user_check = Profile.objects.filter(email = username)

		if user_check:
			print("The stored password for this account is " + str(user_check[0].password) + " and the salt is : " + user_check[0].password_salt);
			logging.info(" Server found a match for the username: "+username)
			# Django's built-in authentication function:
			# we are doing this because we stored the password in the temp database as a hash. And then user database also hashes the password again before it stores.
			password = bcrypt.hashpw((password + secret_key).encode('UTF-8'),
									 user_check[0].password_salt.encode('UTF-8'))

			print("The onetime hashed password is " + password)

			# By default authenticate will take username and password. It will test and see if a match is found in the User Model (this function only works with User Model)
			# In our case since we have extended the User model through the Profile model, so things we store in the Profile Model are also stored in User Model
			user = authenticate(username=username, password=password)
			logging.info(" Server now checking if entered password matches the stored password")
			# If the credentials provided are good then check if the user account is active
			if user:

				# Check it the account is active
				logging.info(" Password matched now checking if account is active or not")
				if user.is_active:  # this is set to true when user is created by default
					# Log the user in.
					login(request, user)
					logging.info(" Account is active and logging the user in the website. Redirecting Client to the profile page")
					# Send the user back to some page.
					# In this case their homepage.
					# return HttpResponseRedirect(reverse('index'))
					# return render(request,'basic_app/profile.html')
					return redirect('profile')  # redirect the user to profile page
				else:
					# If account is not active:
					logging.info(" User account is not Active. Sending client this message")
					return HttpResponse("Your account is not active.")

			#if user provided invalid credentials then Tell them that details are invalid
			else:
				print("Someone tried to login and failed.")
				print("They used username: {} and password: {}".format(username, password))
				logging.info(" Client used an invalid password for the account")
				return HttpResponse("Invalid login details provided.")


		else:
			logging.info(" Client tried to login with a non-existing username")
			print("No username was found")
			return HttpResponse("No such account exists")


    #If its not a POST request then its a GET request so we simply send the Client the login page
	if request.method == 'GET':

		logging.info(" Client " + request.user.username + " sent a HTTP GET request for the Login page")
		if request.user.is_authenticated():
			return redirect('profile')
		else:
			return render(request, 'basic_app/login.html', {})

def register(request):

	registered = False

	if request.method == 'POST':
		#TempUser.objects.all().delete()

		first_name = request.POST.get('firstname', None)
		if first_name=="":
			messages.add_message(request, messages.INFO, 'Hello world.')
			return HttpResponseRedirect("/#")
		
		last_name = request.POST.get('lastname', None)
		email = request.POST.get('email', None)
		pwd = request.POST.get('password', None)
		account_type = request.POST.get('first_item', None)
		
		hashed = bcrypt.hashpw((email+secret_key).encode('UTF-8'), bcrypt.gensalt())
		
		password_salt= bcrypt.gensalt()		
		pwd = bcrypt.hashpw((pwd+secret_key).encode('UTF-8'), password_salt)
		hash_email = base64.b64encode(hashed)

		link = hash_email
		url_link = URL_CONFIRM + hash_email

		logging.info(" Client has sent the form for the Registration Page via HTTP POST request")
		#TempUser.objects.get(email=email).delete()
		print("We are storing this password in the temp db : " + pwd)
		domain = email[-11:]
		if domain != "utoronto.ca":
			#messages.add_message(request, messages.INFO,"Only Uoft Email address holders can register")
			#messages.error(request, 'Only Uoft email holders can register')

			data = {"data": "Only Uoft email holders can register"}
			return JsonResponse(data, status=201)
			#return HttpResponse('Only Uoft email holders can register')

		temp_user = TempUser(first_name=first_name,last_name=last_name,email=email,password=pwd,link=link, password_salt= password_salt,account_type=account_type)
		temp_user.save()
		
		send_mail('Registration Confirmation at Schoolmash', url_link, 'Schoolmash', ['md.fazal@mail.utoronto.ca',email])
		data = {"data": "Check your email for verification!!!"}
		return JsonResponse(data, status=201)
		#return HttpResponse("Check your email for verification!!!")

	if request.method == 'GET':
		logging.info(" Client has requested for the Registration Page via HTTP GET")
		user_form = UserForm()
		return render(request,'basic_app/registration.html',
                          {'user_form':user_form,
                           'registered':registered})
     
def confirm_sign_up(request, hash):  #change the link hash function to more strong encryption later
	#User.objects.all().delete()
	#req_code=request.path[12:]
	#req_email = cipher.decrypt(base64.b64decode(req_code)).strip()

	temp_user = TempUser.objects.get(link = hash)

	if temp_user:

		new_user = Profile(first_name = temp_user.first_name,last_name=temp_user.last_name,username=temp_user.email,email=temp_user.email, password_salt=temp_user.password_salt,account_type=temp_user.account_type)#,password=temp_user.password)
		print("Storing the onetime hashed password in the actual database: " + temp_user.password)
		new_user.set_password(temp_user.password)
		new_user.save()
		print("Password after it is stored in the actual database(2x hashed): " + new_user.password)
		temp_user.delete()
		string="You email " + new_user.email + " is confirmed and welcome to the platform. You should be now able to login"
		messages.success(request, 'Your Account was confirmed. You can now login.')
		return redirect('user_login')

	else:
		return HttpResponse("What are you doing bro?")

@login_required
def profile(request):
	if request.method == 'GET':
		# Remember to also set login url in settings.py!
		# LOGIN_URL = '/basic_app/user_login/'
		logging.info(" Client " + request.user.username + " requested profile page")
		print("the user name is: " + request.user.username)
		profile=Profile.objects.get(email = request.user.email)

		posts = get_all_posts_related_to_user(profile)

		#post= Post.objects.all().filter(owner=profile)

		#post_clone = posts._clone()
		#we reverse the list because we want to start displaying post from the latest post first
		#posts = reversed(posts)

		#find all friend requests made to this user
		req = TempFriendRequest.objects.filter(requestTo=profile)

		#now we get all comments of all the posts that are related to this user. We simply pass the posts querySet to the function below
		#THis function will return a key:value pair dictionary where each key is a Post object and the
		#associated value is the QuerySet that holds all the comments for that Post object

		if posts:
			last_postID= posts.last().id
		else:
			last_postID = -1

		#find all posts that this user has liked. This is then converted to list which is then used in the template
		#to display Liked or Like on the button. "Liked" will show on buttons for which user has liked the post
		posts_liked_by_user = list(posts.filter(liked_by=profile))

		posts=reversed(posts)


		comments = get_comments_of_all_posts(posts)



		##create a query set for photo links
		posts1 = get_all_posts_related_to_user(profile)
		posts1 = reversed(posts1)
		photo_links = get_image_links_of_all_posts(posts1)

		#for key, link in photo_links.iteritems():
				#print "********************printing url******************"
				#print key
				#print link
				#if link:
					#for li in link:
						#print li.url_link
		#print("Now printing after getting dictionary")
		#for key, value in comments.iteritems():
		#	print key.pub_date
		friendList = Friendship.objects.filter(creator=profile)

		notification = Message_Notification.objects.filter(notification_for=profile)

		if(notification):
			print("notifications exist for this user")
			print notification[0].room
		#post_clone = reversed(post_clone)
		#comments = sorted(comments.items)
		return render(request,'basic_app/profile.html', {'profile':profile, 'req':req, 'comments':comments, 'last_postID': last_postID, 'posts_liked_by_user':posts_liked_by_user,'friendList':friendList,'notification':notification,'photo_links':photo_links}, )

	if request.method == 'POST':
		print "GOT upload_pic POST request"
		form = ImageUploadForm(request.POST, request.FILES)
		if form.is_valid():
			m = Profile.objects.get(email=request.user.email)
			m.profile_pic = form.cleaned_data['image']
			m.save()
			print "Form is valid and saving the POST img request"
			return HttpResponse('image upload success')



@login_required
def post_submit(request):
	# Remember to also set login url in settings.py!
	# LOGIN_URL = '/basic_app/user_login/'

	if request.method == 'POST':

		logging.info(" Client " + request.user.username + " sent a HTTP POST request and wants to submit a post to the wall")

		print("Got the post submit request and inside the router123")
			#received = request.POST['text']

		received = request.POST.get('text', None)

		#handling video url below
		video_url = request.POST.get('video_url', None)



		# = json.loads(request.body)
		print received

		logging.info(" The post content is: " + received)

		profile = Profile.objects.get(email=request.user.email)

		if video_url != "0":
			url_data = urlparse.urlparse(video_url)
			query = urlparse.parse_qs(url_data.query)
			video_id = query["v"][0]
			embedded_url= "https://www.youtube.com/embed/"+ video_id
			post = Post(text=received, owner=profile, pub_date=datetime.now(),video_url=embedded_url)
		else:
			post=Post(text= received, owner= profile, pub_date= datetime.now())

		logging.info(" Saving the post in the Post database")
		post.save()

		logging.info(" Send a status=204 response back to Client. This should reload the page on client side(as instructed by ajax success function on the frontend)")

		print "post primary key is " + str(post.id)


		#messages.success(request, 'Your post was successfully submitted!')


		######## check if post contains any photos
		if len(request.FILES) != 0:    # if length of request.FILES dictionary is 0 then it means that no files are uploaded

			print len(request.FILES)
			print "request has photos"
			randstring1 = str(uuid.uuid4().hex)
			randstring2 = str(uuid.uuid4().int)

			saved_directory = os.path.join(settings.MEDIA_ROOT, 'postID', str(post.id), randstring1, randstring2)

			post.post_photo_directory = saved_directory

			print "saving directory path "+ saved_directory
			post.save()  #update the post with the image directory path




			for filename, file in request.FILES.iteritems():
				name = request.FILES[filename].name
				print "GOT PHOTO UPLOAD POST REQUEST"

				print ("photo name is :" + name)

				save_path = os.path.join(settings.MEDIA_ROOT, 'postID', str(post.id), randstring1, randstring2,name)
				path = default_storage.save(save_path, file)

				url_path  = os.path.join(settings.MEDIA_URL, 'postID', str(post.id), randstring1, randstring2,name)
				links = Photo_links(url_link=url_path, which_post=post)

				links.save()

				print ("saving the photo at the path " + save_path)
		else:
			print "Post has NO PHOTOS"

			########

		return HttpResponse(status=204)
	else:
		return HttpResponse("incorrect post")


@login_required
def comment_submit(request):
	# Remember to also set login url in settings.py!
	# LOGIN_URL = '/basic_app/user_login/'

	if request.method == 'POST':

		logging.info(" Client " + request.user.username + " sent a HTTP POST request and wants to submit a comment to a post")

		print("Got the comment submit request and inside the router123")
			#received = request.POST['text']
		received = request.POST.get('text', None)
		postID = request.POST.get('postID', None)
		# = json.loads(request.body)
		print received

		logging.info(" The comment content is: " + received)
		logging.info(" The post id for the comment is: " + postID)

		post=Post.objects.filter(id=int(postID))

		#to make it harder for client to hack set id of the post to something like hash(post_content + timenow())
		if post:  #if the post exists then add the comment to the db.

			profile = Profile.objects.get(email=request.user.email)

			comment=Comment(text= received, owner= profile, pub_date= datetime.now(), which_post=post[0])

			logging.info(" Saving the comment in the Comment Table")
			comment.save()

			logging.info(" Send a status=204 response back to Client. This should reload the page on client side(as instructed by ajax success function on the frontend)")
			return HttpResponse(status=204)
		else:
			logging.info("No such postID exists..Client may have changed the postID manually!!!")
			return HttpResponse("incorrect post")

	else:
		return HttpResponse("incorrect post")



@login_required
def search_old(request):
	# Remember to also set login url in settings.py!
	# LOGIN_URL = '/basic_app/user_login/'

	print("Got the search request and inside the router")
	if request.method == 'GET':
		logging.info(" Client " + request.user.username + " sent a HTTP GET request and wants to search for someone")

		#received = request.POST['text']
		search_string = request.GET["query"]
		# = json.loads(request.body)
		print search_string
		logging.info(" The search string is " + search_string)

		user = Profile.objects.get(email=request.user.email)

		profile = Profile.objects.filter(email=search_string) #filter returns an array (even if only one profile exists. So to access it we use profile[0].email

		req = TempFriendRequest.objects.filter(requestFrom=user, requestTo=profile) #if the request object already exists in the table then dont show the "send friend request" button in the view

		friend= Friendship.objects.filter(creator=profile, friend=user) #returns a list
		#if profile:
		#	print str(profile[0].email)
			#return HttpResponse("We have found a user matching the search string")
		#	return render(request, 'basic_app/search_results.html', {'profile': profile[0]})


		#else:
		#	return HttpResponse("Nothing Found")
		return render(request, 'basic_app/search_results.html', {'profile': profile , 'request_already_made':req, 'friend':friend})

@login_required
def search(request):

	if request.method == 'GET':
		search_string = request.GET["query"]
		logging.info(" The search string is " + search_string)
		user = Profile.objects.get(email=request.user.email)
		search_result=[]
		profiles = Profile.objects.filter(
			email=search_string)
		if (len(profiles) == 0):
			names = search_string.split(" ")
			if (len(names) == 2):
				profiles = Profile.objects.filter(first_name=names[0],last_name = names[1])
		if(len(profiles)==0):
			profiles = Profile.objects.filter(first_name=search_string)
		if(len(profiles) == 0):
		   profiles = Profile.objects.filter(last_name=search_string)
	   	groups=Group.objects.filter(name=search_string)
	   	courses=Course.objects.filter(code=search_string)
		for item in profiles:
			req = TempFriendRequest.objects.filter(requestFrom=user,requestTo=item)  # if the request object already exists in the table then dont show the "send friend request" button in the view
			friend = Friendship.objects.filter(creator=user, friend=item)  # returns a list
			search_result.append({'profile':item,'req':req,'friend':friend,'type':'person'})
		for group in groups:
			search_result.append({'group': group, 'id': group.id,  'type': 'group'})
		for course in courses:
			search_result.append({'course': course, 'id': course.id,  'type': 'course'})

		profile = Profile.objects.get(email=request.user.email)

		logging.info(" Client " + request.user.username + " wants to view their friend List")
		# find all friends of this user. This query will return a list of friends if possible
		friendList = Friendship.objects.filter(creator=profile)

		return render(request, 'basic_app/search_results.html',
					  {'search_result': search_result, 'friendList':friendList,'profile':profile})
@login_required
def sendFriendRequest(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		logging.info(" Client " + request.user.username + " sent a HTTP POST request and wants to send a friend request to the user: "+ email)


		friend = Profile.objects.filter(email=email) #filter returns an array
		if friend:

				user= Profile.objects.get(email=request.user.email)

				req= TempFriendRequest(requestFrom=user , requestTo=friend[0]) #create tempFriendReq object and save it in db
				req.save()
				return HttpResponse(status=204) #tell client that friend request was successfully sent

		else:
			logging.info(" **CRITICAL** Client " + request.user.username + " modified the friend email!!! ")

			return HttpResponse("Friend email String was manipulated!!!")


@login_required
def friendRequests(request):
	if request.method == 'GET':
		logging.info(" Client " + request.user.username + " sent a HTTP GET request and wants to view the friend requests they have receieved")
		print("Got the GET request for friend requests display and inside the router")

		profile = Profile.objects.get(email=request.user.email)

		# find all friend requests made to this user
		req = TempFriendRequest.objects.filter(requestTo=profile)

		friendList = Friendship.objects.filter(creator=profile)

		return render(request, 'basic_app/friendRequests.html', {'req':req, 'profile':profile,'friendList':friendList})

	if request.method == 'POST':

		print("Got the POST123 request for friend requests display and inside the router")
		email = request.POST.get('email')
		status = request.POST.get('status')

		if (status!="1" and status!="0"):
			logging.info("Status was neither 0 nor 1 in the friend request. Something was wrong!!. Sending Client an error message")
			return HttpResponse("Status was neither 1 nor 0!!! This means friend request frontend action was not set properly at the frontend")

		logging.info(" Client " + request.user.username + " sent a HTTP POST request and wants to take an action with the the friend Request")

		print status
		profile = Profile.objects.get(email=request.user.email)
		friend= Profile.objects.get(email=email)
		# = json.loads(request.body)

		print email

		logging.info("The email of friend is: "+email+"  and the status is :"+status)
		#check if the friend request actually  exists in the temp database

		req = TempFriendRequest.objects.filter(requestFrom=friend, requestTo=profile)  # create tempFriendReq object and save it in db



		if req:  #if the request is actually found then take appropriate action based on status

			logging.info("The friend request record was found in the tempfriend table")
			print("TempFriendRecord was found")

			if status == "1":  #friend request was accepted so we add it to actual friends table
				print("status was one and accepting the friend request")

				logging.info("Since status is 1, the Client wants to accept the friend request from "+ email)
				#add 2 times in the database. One entry for one person and 2nd entry for 2nd person
				req1= Friendship(creator=profile, friend=req[0].requestFrom, created=datetime.now())
				req1.save()
				req2 = Friendship(creator=req[0].requestFrom, friend= profile, created=datetime.now())
				req2.save()

				logging.info("Adding 2 records of friendship in the real Friend Table. One record for each User")

			else:
				print("status was 0 and Declining the friend request")
				logging.info("Since status is 0, the Client wants to Reject the friend request from " + email)

			logging.info("Deleting the friendship request record from the tempFriend database and returning 204 status to client")
			req.delete() #delete the temp friend record object
			print("Deleting the TempFriendRecord and returning 204")
			return HttpResponse(status=204)  # tell client that friend request was successfully sent

		else:
			print("Record was not found")
			logging.info(" **CRITICAL** Client " + request.user.username + " modified the friend email!!! ")

			return HttpResponse("Friend email String was manipulated!!!")


@login_required
def friendList(request):

		print("Got the get request for friend list display and inside the router")

		profile = Profile.objects.get(email=request.user.email)

		logging.info(" Client " + request.user.username + " wants to view their friend List")
		# find all friends of this user. This query will return a list of friends if possible
		friendList = Friendship.objects.filter(creator=profile)
		#print friendList[0].friend
		return render(request, 'basic_app/friendList.html', {'friendList':friendList, 'profile':profile})



@login_required
def check_new_post(request):
	# Remember to also set login url in settings.py!
	# LOGIN_URL = '/basic_app/user_login/'

	if request.method == 'GET':

		logging.info(" Client " + request.user.username + " sent a HTTP GET request and wants to check if a new post has appeared")

		print("Got the post submit request and inside the router123")
			#received = request.POST['text']
		#The client sends us the last postID it has receieved
		receivedID = request.GET.get('last_postID', None)
		# = json.loads(request.body)
		print receivedID

		logging.info(" The Last Post ID is: " + receivedID)

		#Our job now is to get all posts related to client after the last_postID

		profile = Profile.objects.get(email=request.user.email)

		posts= get_all_posts_related_to_user(profile)

		#get all posts greater than lastID
		new_posts= posts.filter(id__gt = int(receivedID))

		#new_posts = reversed(new_posts)

		logging.info("Fetching all posts for user greater than lastID ")

		if new_posts:
			logging.info("Sending new posts to the client ")
			data= "Got a new POST for you . the post contains :" + new_posts[0].text

			data = {
				"post_text": [],
				"post_owner": [],
				"post_ID": [],
				"post_owner_pic": [],
				"video_url": [],
				"pictures_urls": []

			};

			#get the latest posts to be on the top of the feed
			new_posts = reversed(new_posts)
			#need to embed post text, post owner, postID

			for i in new_posts:
				data.setdefault("post_text", []).append(i.text)
				data.setdefault("post_owner", []).append(i.owner.first_name)
				data.setdefault("post_ID", []).append(i.id)
				data.setdefault("post_owner_pic", []).append(i.owner.profile_pic.url)
				if i.video_url:
					data.setdefault("video_url", []).append(i.video_url)
				else:
					data.setdefault("video_url", []).append("0")

				#the below code deals with adding picture urls to the json data object
				links=Photo_links.objects.filter(which_post=i)
				urls_of_photos=[]

				for a in links:
					urls_of_photos.append(a.url_link)


				data.setdefault("pictures_urls", []).append(urls_of_photos)
				#print("the video url for this post is "+ i.video_url)
			#response_data = {"data": data}
			data = {"data": data}
			return JsonResponse(data, status=201)


		#logging.info(" Send a status=204 response back to Client. This should reload the page on client side(as instructed by ajax success function on the frontend)")
		logging.info("There are no new posts for the client ")
		response_data= {"data": "I got nothing for you", "status": 0}
		return JsonResponse(response_data, status=201)




@login_required
def user_messages(request):
	if request.method == 'GET':
		print("Got the get request for messages display and inside the router")

		profile = Profile.objects.get(email=request.user.email)

		logging.info(" Client " + request.user.username + " wants to view their messages")
		# find all friends of this user. This query will return a list of friends if possible

		friendList = Friendship.objects.filter(creator=profile)

		notifications = Message_Notification.objects.filter(notification_for=profile)

		#for i in notifications:


		dictionary= {}
		notifications_by = []
		if(friendList):
			#get all the conversations with all the user's friends
			for friend in friendList:
				if(friend.friend.email > request.user.email):
					chat_room=friend.friend.email + "-" + request.user.email
				else:
					chat_room = request.user.email + "-" + friend.friend.email

				chat = Message.objects.filter(room=chat_room)

				notifications = Message_Notification.objects.filter(notification_for=profile)


				if(notifications):
					for notification in notifications:
						notifications_by.append(notification.notification_by_email)

				if(chat):
					logging.info("chat_room exists") 
					dictionary[friend.friend.email]= chat


			for i in notifications_by:

				print "notification by " + i
			#print friendList[0].friend
		return render(request, 'basic_app/messages.html', {'friendList':friendList, 'chat_messages':dictionary, 'notifications_by':notifications_by, 'profile':profile})





@login_required
def like_post(request):
	if request.method == 'POST':

		print("Client sent a like_post request (HTTP POST request) and inside the router")

		profile = Profile.objects.get(email=request.user.email)

		logging.info(" Client " + request.user.username + " wants to like a Post")


		receivedID = request.POST.get('postID', None)

		print ("PostID received is " + receivedID)
		post = Post.objects.filter(id=int(receivedID))

		#If post is found then increment the like counter for that post and also add the user to the like_by field
		if post:
			print ("Post found")

			if post[0].liked_by.all().filter(email=request.user.email) :
				print ("Post already liked by user, hence unliking it now")
				logging.info("Post Found. And user has already liked it, so now unliking it")
				post[0].likes -= 1
				post[0].liked_by.remove(profile)
				post[0].save()
				logging.info("Decrementing likes count for this post and removing user from liked_by field")
				data = {"data": 0}
				return JsonResponse(data, status=201)
			else:
				logging.info("Post Found and not previously liked by user. Incrementing Like counter and adding user to liked_by field ")
				post[0].likes += 1
				post[0].liked_by.add(profile)
				post[0].save()
				data = {"data": 1}
				return JsonResponse(data, status=201)
		else:
			print("Post not found")
			return HttpResponse("POST not found, or the POST ID was manipulated!!!",status=400)
		#print friendList[0].friend


@login_required
def likedBy(request):
	if request.method == 'POST':

		print("Client sent an Ajax likedBy request (HTTP POST request) and inside the router")

		profile = Profile.objects.get(email=request.user.email)

		logging.info(" Client " + request.user.username + " wants to see who has liked the post")


		receivedID = request.POST.get('postID', None)

		print ("PostID received is " + receivedID)
		post = Post.objects.filter(id=int(receivedID))

		#If post is found then increment the like counter for that post and also add the user to the like_by field
		if post:
			print ("Post found")
			logging.info("Post Found. Incrementing Like counter and adding user to liked_by field ")

			people = post[0].liked_by.all()

			data = {
				"people": [],
			};


			for i in people:
				data.setdefault("people", []).append(i.email)


			# need to embed post text, post owner, postID

			#people_json = json.dumps(list(people), cls=DjangoJSONEncoder)

			# response_data = {"data": data}
			data = {"data": data}
			return JsonResponse(data, status=201)

			print "Sending people list to client and send 200 back to Client"
			return HttpResponse(status=204)
		else:
			print("Post not found")
			return HttpResponse("POST not found, or the POST ID was manipulated!!!",status=404)
		#print friendList[0].friend

@login_required
def chat_auth_token(request):
	# see https://pyjwt.readthedocs.io/en/latest/usage.html for usage of jwt below
	jwt_payload = jwt.encode({
		'exp': datetime.utcnow() + timedelta(seconds=30), #token is valid for only 30 seconds
		'issuedTo' : request.user.email  #could add other things like issuedToIP to strengthen security measures
	}, 'thisisasecretkey123')

	return JsonResponse({"token": jwt_payload}, status=201)

@login_required
def send_message(request):
	if request.method == 'POST':
		print("Client sent a email/message post request (HTTP POST request) and inside the router")

		profile = Profile.objects.get(email=request.user.email)


		receivedMsg = request.POST.get('msgText', None)
		msgTo= request.POST.get('msgTo', None)

		logging.info(" Client " + request.user.username + " sent a message/email post to " + msgTo + " and the msg is " + receivedMsg)

		user_check = Profile.objects.filter(email=msgTo)

		if(user_check):

			#logic to compute the chat_room. Chat room are there for efficient retrieval of msgs from the database
			if(request.user.email > msgTo):
				chat_room = request.user.email + "-" + msgTo
			else:
				chat_room = msgTo + "-" + request.user.email

			req = Message(room=chat_room, messageFrom=profile, messageTo=user_check[0], text=receivedMsg, pub_date=datetime.now())
			req.save()

			check_notification = Message_Notification.objects.filter(room=chat_room, notification_for=user_check[0])
			if(not check_notification):
				print "notification doesnt exist for this chat_room and this user"
				notification= Message_Notification(room=chat_room, notification_for=user_check[0], notification_by_email=request.user.email)
				notification.save()
				print("notification created for this user+chat_room")
				logging.info("Notification for new msg created for this user+chatroom")
			else:
				print("notification already exists for this user/chat_room")
				logging.info("notification already exists for this user/chat_room")

			logging.info("saved the msg in the database");
			return HttpResponse(status=204);


		else:
			logging.info(" Client is sending the msg to an unknown user.")
			print("No username was found")
			return HttpResponse("No such account exists")

@login_required
def delete_msg_notification(request):
	if request.method == 'POST':
		print("Client sent a delete_msg_notification post request (HTTP POST request) and inside the router")

		profile = Profile.objects.get(email=request.user.email)

		notification_by = request.POST.get('notification_by', None)

		obj = Message_Notification.objects.filter(notification_for=profile, notification_by_email=notification_by)

		if (obj):

			obj.delete()
			print "deleted the notification"

			return HttpResponse(status=204)
		else:
			print "No Such notification exists!!!"
			return HttpResponse(status=401)

@login_required
def my_groups(request):
	groups = GroupTable.objects.filter(member = Profile.objects.get(email = request.user.email))
	groups = reversed(groups);

	profile = Profile.objects.get(email=request.user.email)

	friendList = Friendship.objects.filter(creator=profile)
	return render(request, 'basic_app/my_groups.html', {'groups':groups, 'friendList':friendList,'profile':profile})


@login_required
def group_new(request):
	profile = Profile.objects.get(email=request.user.email)

	friendList = Friendship.objects.filter(creator=profile)
	return render(request, 'basic_app/group_new.html', {'friendList':friendList,'profile':profile})

@login_required
def group_create(request):
	

	name = request.POST.get('name')
	description = request.POST.get('description')
	creator=Profile.objects.get(email=request.user.email)

	form = GroupImageUploadForm(request.POST, request.FILES)
	if form.is_valid():
		group = Group(name=name, description=description, creator=creator, creation_date=datetime.now(),image=form.cleaned_data['image'])
		print "image received"
	else:
		group = Group(name=name, description=description, creator=creator, creation_date=datetime.now())
		print "image not received"
	group.save()

	group_table = GroupTable(group = group, member = creator)
	group_table.save()
	groups = GroupTable.objects.filter(member = Profile.objects.get(email = request.user.email))
	groups = reversed(groups)

	profile = Profile.objects.get(email=request.user.email)

	friendList = Friendship.objects.filter(creator=profile)

	return render(request, 'basic_app/my_groups.html', {'groups':groups, 'friendList':friendList,'profile':profile})


def isMember(user,group):
	for item in GroupTable.objects.filter(member=user):
		if item.group==group and item.member==user:
			return True
	return False



@login_required
def group(request,id):
	group = Group.objects.get(id = id)
	profile = Profile.objects.get(email=request.user.email)
	friendList = Friendship.objects.filter(creator=profile)
	if request.method == 'GET':
		profile=Profile.objects.get(email = request.user.email)
		posts = get_all_posts_related_to_group(int(id))
		req = TempFriendRequest.objects.filter(requestTo=profile)
		if posts:
			last_postID= posts.last().id
		else:
			last_postID = -1
		posts_liked_by_user = list(posts.filter(liked_by=profile))
		posts=reversed(posts)
		comments = get_group_comments_of_all_posts(posts)
		notification = Message_Notification.objects.filter(notification_for=profile)
		members = GroupTable.objects.filter(group=group)
		if group.creator == profile:
			member_type="creator"
		elif isMember(profile,group):
			member_type="member"
		else:
			member_type="none"
		print "member type"
		print member_type

		if(notification):
			print("notifications exist for this user")
			print notification[0].room

	return render(request, 'basic_app/group.html', {'group':group, 'profile':profile,'comments':comments, 'last_postID': last_postID, 'posts_liked_by_user':posts_liked_by_user,'notification':notification,'member_type':member_type,'friendList':friendList,'members':members},)

@login_required
def group_members(request,id):
	group=Group.objects.get(id=id)
	members = GroupTable.objects.filter(group=group)
	profile = Profile.objects.get(email=request.user.email)
	friendList = Friendship.objects.filter(creator=profile)
	if group.creator == profile:
		member_type="creator"
	elif isMember(profile,group):
		member_type="member"
	else:
		member_type="none"
	return render(request,'basic_app/group_members.html',{'members':members,'group':group,'profile':profile,'friendList':friendList,'member_type':member_type})




@login_required
def group_files(request,id):
	group = Group.objects.get(id=id)
	members=GroupTable.objects.filter(group=group)
	profile=Profile.objects.get(email=request.user.email)

	if group.creator == profile:
		member_type="creator"
	elif isMember(profile,group):
		member_type="member"
	else:
		member_type="none"
	if request.method=="POST":
		print "post happens"
		form = FileUploadForm(request.POST, request.FILES)
		if form.is_valid():
			print "form valid happens"
			file = GroupFile(file=form.cleaned_data['file'],uploaded_by=profile,group=group)
			file.save()


	files=GroupFile.objects.filter(group=group)
	friendList = Friendship.objects.filter(creator=profile)

	return render(request, 'basic_app/group_files.html', {'files': files, 'group': group,'members':members,'profile':profile,'friendList':friendList,'member_type':member_type})





def get_all_posts_related_to_group(id):

	posts = GroupPost.objects.all().filter(group = Group.objects.get(id = id))
	ordered_posts = posts.order_by('pub_date')
	return ordered_posts


@login_required
def group_like_post(request):
	if request.method == 'POST':


		profile = Profile.objects.get(email=request.user.email)

		logging.info(" Client " + request.user.username + " wants to like a Post")


		receivedID = request.POST.get('postID', None)

		
		post = GroupPost.objects.filter(id=int(receivedID))

		#If post is found then increment the like counter for that post and also add the user to the like_by field
		if post:
			print ("Post found")

			if post[0].liked_by.all().filter(email=request.user.email) :
				print ("Post already liked by user, hence unliking it now")
				logging.info("Post Found. And user has already liked it, so now unliking it")
				post[0].likes -= 1
				post[0].liked_by.remove(profile)
				post[0].save()
				logging.info("Decrementing likes count for this post and removing user from liked_by field")
				data = {"data": 0}
				return JsonResponse(data, status=201)
			else:
				logging.info("Post Found and not previously liked by user. Incrementing Like counter and adding user to liked_by field ")
				post[0].likes += 1
				post[0].liked_by.add(profile)
				post[0].save()
				data = {"data": 1}
				return JsonResponse(data, status=201)
		else:
			print("Post not found")
			return HttpResponse("POST not found, or the POST ID was manipulated!!!",status=400)
		#print friendList[0].friend


@login_required
def group_likedBy(request):
	if request.method == 'POST':

		print("Client sent an Ajax likedBy request (HTTP POST request) and inside the router")

		profile = Profile.objects.get(email=request.user.email)

		logging.info(" Client " + request.user.username + " wants to see who has liked the post")


		receivedID = request.POST.get('postID', None)

		print ("PostID received is " + receivedID)
		post = GroupPost.objects.filter(id=int(receivedID))

		#If post is found then increment the like counter for that post and also add the user to the like_by field
		if post:
			print ("Post found")
			logging.info("Post Found. Incrementing Like counter and adding user to liked_by field ")

			people = post[0].liked_by.all()

			data = {
				"people": [],
			};


			for i in people:
				data.setdefault("people", []).append(i.email)


			# need to embed post text, post owner, postID

			#people_json = json.dumps(list(people), cls=DjangoJSONEncoder)

			# response_data = {"data": data}
			data = {"data": data}
			return JsonResponse(data, status=201)

			print "Sending people list to client and send 200 back to Client"
			return HttpResponse(status=204)
		else:
			print("Post not found")
			return HttpResponse("POST not found, or the POST ID was manipulated!!!",status=404)
		#print friendList[0].friend

@login_required
def group_comment_submit(request):
	# Remember to also set login url in settings.py!
	# LOGIN_URL = '/basic_app/user_login/'

	if request.method == 'POST':

		

		
			#received = request.POST['text']
		received = request.POST.get('text', None)
		postID = request.POST.get('postID', None)
		# = json.loads(request.body)
		
		post=GroupPost.objects.filter(id=int(postID))

		#to make it harder for client to hack set id of the post to something like hash(post_content + timenow())
		if post:  #if the post exists then add the comment to the db.

			profile = Profile.objects.get(email=request.user.email)

			comment=GroupComment(text= received, owner= profile, pub_date= datetime.now(), which_post=post[0])

			comment.save()

			logging.info(" Send a status=204 response back to Client. This should reload the page on client side(as instructed by ajax success function on the frontend)")
			return HttpResponse(status=204)
		else:
			logging.info("No such postID exists..Client may have changed the postID manually!!!")
			return HttpResponse("incorrect post")

	else:
		return HttpResponse("incorrect post")



@login_required
def group_post_submit(request):

	if request.method == 'POST':

		received = request.POST.get('text', None)
		group_id= request.POST.get('group_id', None)
		
		profile = Profile.objects.get(email=request.user.email)

		post = GroupPost(group = Group.objects.get(id = group_id), text= received, owner = profile, pub_date= datetime.now())

		post.save()

		return HttpResponse(status=204)
	else:
		return HttpResponse("incorrect post")


def get_group_comments_of_all_posts(posts):

	#Below we have to use an Ordered Dict because we want to iterate over dict in the way they are entered in the dictionary.
	#if you dont use orderedDict then when iterating over keys you dont get the order of insertion
	dictionary = OrderedDict()  #dictionary will hold key value pairs. Where key is the post and value is the QuerySet which contains all comments for that post

	for post in posts:
		dictionary[post]=GroupComment.objects.filter(which_post=post)
		#print post.pub_date

	
	#	print key.pub_date

	return dictionary


@login_required
def group_check_new_post(request):
	# Remember to also set login url in settings.py!
	# LOGIN_URL = '/basic_app/user_login/'

	if request.method == 'GET':

		
			#received = request.POST['text']
		#The client sends us the last postID it has receieved
		receivedID = request.GET.get('last_postID', None)
		

		group_id = request.GET.get('group_id', None)

		#Our job now is to get all posts related to client after the last_postID

		profile = Profile.objects.get(email=request.user.email)

		posts= get_all_posts_related_to_group(group_id)

		#get all posts greater than lastID
		new_posts= posts.filter(id__gt = int(receivedID))

		#new_posts = reversed(new_posts)


		if new_posts:
			logging.info("Sending new posts to the client ")
			data= "Got a new POST for you . the post contains :" + new_posts[0].text

			data = {
				"post_text": [],
				"post_owner": [],
				"post_ID": []
			};

			#get the latest posts to be on the top of the feed
			new_posts = reversed(new_posts)
			#need to embed post text, post owner, postID

			for i in new_posts:
				data.setdefault("post_text", []).append(i.text)
				data.setdefault("post_owner", []).append(i.owner.first_name)
				data.setdefault("post_ID", []).append(i.id)

			#response_data = {"data": data}
			data = {"data": data}
			return JsonResponse(data, status=201)


		#logging.info(" Send a status=204 response back to Client. This should reload the page on client side(as instructed by ajax success function on the frontend)")
		logging.info("There are no new posts for the client ")
		response_data= {"data": "I got nothing for you", "status": 0}
		return JsonResponse(response_data, status=201)

def isAlreadyGroupMember(group,profile):
	for item in GroupTable.objects.filter(member=profile,group=group):
		if item.group==group and item.member==profile:
			return True
	return False
@login_required
def join_group(request,id):
	_group=Group.objects.get(id=id)
	profile=Profile.objects.get(email=request.user.email)
	if isAlreadyGroupMember(_group,profile)==False:
		GroupTable(group=_group,member=profile).save()
	return group(request,id)

@login_required
def leave_group(request,id):
	GroupTable.objects.get(group=Group.objects.get(id=id),member=Profile.objects.get(email=request.user.email)).delete()
	return group(request, id)
@login_required
def delete_group(request,id):
	#GroupTable.objects.get(group=Group.objects.get(id=id),member=Profile.objects.get(email=request.user.email)).delete()
	Group.objects.get(id=id).delete()
	return my_groups(request)

def send_message_file(request):
	if request.method == 'POST' and request.FILES['file']:
		print "GOT FILE UPLOAD POST REQUEST"
		msg_for = request.POST.get('msg_To', None)
		print ("The file is sent for the user: " + msg_for)
		myfile = request.FILES['file']
		print ("filename is :" + myfile.name)
		user_check = Profile.objects.filter(email=msg_for)
		profile = Profile.objects.get(email=request.user.email)

		if (user_check):
			save_path = os.path.join(settings.MEDIA_ROOT, 'uploads',   str(uuid.uuid4().hex), str(uuid.uuid4().int), myfile.name)
			path = default_storage.save(save_path, request.FILES['file'])
			print ("save_path is " + save_path)
			print ("url_path is " + path)
			# logic to compute the chat_room. Chat room are there for efficient retrieval of msgs from the database
			if (request.user.email > msg_for):
				chat_room = request.user.email + "-" + msg_for
			else:
				chat_room = msg_for + "-" + request.user.email

			req = Message(room=chat_room, messageFrom=profile, messageTo=user_check[0], text="",
						  pub_date=datetime.now(), file_name= myfile.name, file_url = save_path)
			req.save()
			check_notification = Message_Notification.objects.filter(room=chat_room, notification_for=user_check[0])
			if (not check_notification):
				print "notification doesnt exist for this chat_room and this user"
				notification = Message_Notification(room=chat_room, notification_for=user_check[0],
													notification_by_email=request.user.email)
				notification.save()
				print("notification created for this user+chat_room")
				logging.info("Notification for new msg created for this user+chatroom")
			else:
				print("notification already exists for this user/chat_room")
				logging.info("notification already exists for this user/chat_room")

			logging.info("saved the msg in the database");

			data = {"file_url": save_path}
			return JsonResponse(data, status=201)
		else:
			logging.info(" Client is sending the msg to an unknown user.")
			print("No username was found")
			return HttpResponse("No such account exists")



@login_required
def file_download(request, uuid1, uuid2,filename):
	print ("filename is : ") + filename
	print "User has requested for a protected path "
	logging.info("The requested path is protected and recvd by django ")
	# return HttpResponse("test 1231 23")

	file_url = "/media/uploads/" + uuid1 + "/" + uuid2 + "/" + filename
	profile = Profile.objects.get(email=request.user.email)
	print("file is requested by ") + request.user.email
	print("file requested is ") + filename
	obj = Message.objects.filter(file_url=file_url, permissions=profile)
	if (obj):
		print("file exists and user is allowed to access the file")
		response = HttpResponse()

		response["Content-Disposition"] = "attachment; filename=" + filename
		# url = '/media/uploads/1f0be521c3c440fb8f12384e8791255d/164922054665066116217429700692136172375/WebSockets.docx' # this will obviously $
		url = file_url
		# let nginx determine the correct content type
		print "Requested file url is "+url
		response['Content-Type'] = ""
		response['X-Accel-Redirect'] = url
		return response

	else:
		print("file does not exist or user not allowed to view it")

		return HttpResponse("404. File not found or you are not allowed to access the file")


#Profile pages

def get_all_posts_related_to_one_user(user):

    posts = Post.objects.all().filter(owner=user)
    ordered_posts = posts.order_by('pub_date')

    return ordered_posts

@login_required
def profile_self(request):
    profile = Profile.objects.get(email=request.user.email)
    posts = get_all_posts_related_to_one_user(profile)
    if posts:
        last_postID = posts.last().id
    else:
        last_postID = -1

    # find all posts that this user has liked. This is then converted to list which is then used in the template
    # to display Liked or Like on the button. "Liked" will show on buttons for which user has liked the post
    posts_liked_by_user = list(posts.filter(liked_by=profile))

    posts = reversed(posts)

    comments = get_comments_of_all_posts(posts)

    # print("Now printing after getting dictionary")
    # for key, value in comments.iteritems():
    #	print key.pub_date
    friendList = Friendship.objects.filter(creator=profile)

    notification = Message_Notification.objects.filter(notification_for=profile)#to change

    if (notification):
        print("notifications exist for this user")
        print notification[0].room
    # post_clone = reversed(post_clone)
    # comments = sorted(comments.items)
    return render(request, 'basic_app/profile_self.html',
                  {'profile': profile,'comments': comments, 'last_postID': last_postID,
                   'posts_liked_by_user': posts_liked_by_user, 'friendList': friendList,
                   'notification': notification}, )

@login_required
def profile_other(request,id):
    profile=Profile.objects.get(email=request.user.email)
    profile_other=Profile.objects.get(id=id)
    posts = get_all_posts_related_to_one_user(profile_other)
    if posts:
        last_postID = posts.last().id
    else:
        last_postID = -1

    # find all posts that this user has liked. This is then converted to list which is then used in the template
    # to display Liked or Like on the button. "Liked" will show on buttons for which user has liked the post
    posts_liked_by_user = list(posts.filter(liked_by=profile))

    posts = reversed(posts)

    comments = get_comments_of_all_posts(posts)

    # print("Now printing after getting dictionary")
    # for key, value in comments.iteritems():
    #	print key.pub_date
    friendList = Friendship.objects.filter(creator=profile)

    notification = Message_Notification.objects.filter(notification_for=profile)  # to change

    if (notification):
        print("notifications exist for this user")
        print notification[0].room
    # post_clone = reversed(post_clone)
    # comments = sorted(comments.items)
    return render(request, 'basic_app/profile_other.html',
                  {'profile': profile, 'comments': comments, 'last_postID': last_postID,
                   'posts_liked_by_user': posts_liked_by_user, 'friendList': friendList,
                   'notification': notification,'profile_other':profile_other}, )


@login_required
def profile_edit(request):
    _profile = Profile.objects.get(email=request.user.email)
    if request.method=='POST':
        first_name=request.POST.get("first_name")
        if len(first_name)>0:
            _profile.first_name = first_name
        last_name = request.POST.get("last_name")
        if len(last_name) > 0:
            _profile.last_name = last_name

       
        _profile.discipline = request.POST.get("discipline")
        _profile.start_date = request.POST.get("start_date")
        _profile.grad_date = request.POST.get("grad_date")
        _profile.city = request.POST.get("city")
        _profile.province = request.POST.get("province")
        _profile.country = request.POST.get("country")
        _profile.interests = request.POST.get("interests")
        _profile.courses = request.POST.get("courses")
        _profile.title=request.POST.get("title")
        _profile.phone=request.POST.get("phone")
        _profile.dob=request.POST.get("dob")

        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
        	_profile.profile_pic = form.cleaned_data['image']
        
        _profile.save()
        request.method = "GET"
        return profile(request)
    else:
    	friendList = Friendship.objects.filter(creator=_profile)
    	return render(request,'basic_app/profile_edit.html',{'profile':_profile,'friendList':friendList})
        

@login_required
def photos(request):
    profile = Profile.objects.get(email=request.user.email)
    if request.method=='GET':
        photos=ImageTable.objects.filter(uploaded_by=profile)
        return render(request,'basic_app/photos.html',{'photos':photos,'profile':profile})
    elif request.method=="POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image=ImageTable(image = form.cleaned_data['image'],caption=request.POST.get("caption"),uploaded_by=Profile.objects.get(email=request.user.email))
            image.save()
            photos = ImageTable.objects.filter(uploaded_by=profile)
            friendList = Friendship.objects.filter(creator=profile)
            return render(request, 'basic_app/photos.html', {'photos': photos, 'profile': profile,'friendList':friendList})

@login_required
def detailed_photo(request,id):
    profile=Profile.objects.get(email=request.user.email)
    photo=ImageTable.objects.get(id=id)
    friendList = Friendship.objects.filter(creator=profile)
    return render(request, 'basic_app/detailed_photo.html', {'photo': photo, 'profile': profile,'friendList':friendList})

@login_required
def delete_photo(request,id):
    profile = Profile.objects.get(email=request.user.email)
    ImageTable.objects.get(id=id).delete()
    photos = ImageTable.objects.filter(uploaded_by=profile)
    friendList = Friendship.objects.filter(creator=profile)
    return render(request, 'basic_app/photos.html', {'photos': photos, 'profile': profile,'friendList':friendList})

@login_required
def my_courses(request):
	courses = CourseTable.objects.filter(member = Profile.objects.get(email = request.user.email))
	courses = reversed(courses);

	profile = Profile.objects.get(email=request.user.email)

	friendList = Friendship.objects.filter(creator=profile)
	return render(request, 'basic_app/my_courses.html', {'courses':courses, 'friendList':friendList,'profile':profile})


@login_required
def course_new(request):
	profile = Profile.objects.get(email=request.user.email)

	friendList = Friendship.objects.filter(creator=profile)
	return render(request, 'basic_app/course_new.html', {'friendList':friendList,'profile':profile})

@login_required
def course_create(request):
	
	code = request.POST.get('course_code')
	name = request.POST.get('course_name')
	term = request.POST.get('term')
	year = request.POST.get('year')
	office_hours = request.POST.get('office_hours')
	section = request.POST.get('lecture_section')
	office_location = request.POST.get('office_location')
	description = request.POST.get('description')
	creator=Profile.objects.get(email=request.user.email)

	course = Course(name=name, code=code, term=term, year = year, office_hours = office_hours,office_location = office_location, section = section, description=description, creator=creator, creation_date=datetime.now())
	course.save()

	course_table = CourseTable(course = course, member = creator)
	course_table.save()
	courses = CourseTable.objects.filter(member = Profile.objects.get(email = request.user.email))
	courses = reversed(courses)

	profile = Profile.objects.get(email=request.user.email)

	friendList = Friendship.objects.filter(creator=profile)

	return render(request, 'basic_app/my_courses.html', {'courses':courses, 'friendList':friendList,'profile':profile})






@login_required
def course(request,id):
	course = Course.objects.get(id = id)
	profile = Profile.objects.get(email=request.user.email)
	friendList = Friendship.objects.filter(creator=profile)
	if request.method == 'GET':
		profile=Profile.objects.get(email = request.user.email)
		posts = get_all_posts_related_to_course(int(id))
		req = TempFriendRequest.objects.filter(requestTo=profile)
		if posts:
			last_postID= posts.last().id
		else:
			last_postID = -1
		posts_liked_by_user = list(posts.filter(liked_by=profile))
		posts=reversed(posts)
		comments = get_course_comments_of_all_posts(posts)
		notification = Message_Notification.objects.filter(notification_for=profile)
		members = CourseTable.objects.filter(course=course)
		if course.creator == profile:
			member_type="creator"
		elif isAlreadyCourseMember(course,profile):
			member_type="member"
		else:
			member_type="none"
		print "member type"
		print member_type

		if(notification):
			print("notifications exist for this user")
			print notification[0].room

	return render(request, 'basic_app/course.html', {'course':course,'profile':profile,'comments':comments, 'last_postID': last_postID, 'posts_liked_by_user':posts_liked_by_user,'notification':notification,'member_type':member_type,'friendList':friendList,'members':members},)

@login_required
def course_members(request,id):
	course=Course.objects.get(id=id)
	members = CourseTable.objects.filter(course=course)
	profile = Profile.objects.get(email=request.user.email)
	friendList = Friendship.objects.filter(creator=profile)
	if course.creator == profile:
		member_type="creator"
	elif isAlreadyCourseMember(course,profile):
		member_type="member"
	else:
		member_type="none"
	return render(request,'basic_app/course_members.html',{'members':members,'course':course,'profile':profile,'friendList':friendList,'member_type':member_type})




@login_required
def course_files(request,id):
	course = Course.objects.get(id=id)
	members=CourseTable.objects.filter(course=course)
	profile = Profile.objects.get(email=request.user.email)
	friendList = Friendship.objects.filter(creator=profile)
	if course.creator == profile:
		member_type="creator"
	elif isAlreadyCourseMember(course,profile):
		member_type="member"
	else:
		member_type="none"
	if request.method=="POST":
		print "post happens"
		form = FileUploadForm(request.POST, request.FILES)
		if form.is_valid():
			print "form valid happens"
			file = CourseFile(file=form.cleaned_data['file'],uploaded_by=profile,course=course)
			file.save()


	files=CourseFile.objects.filter(course=course)
	print "file......"
	print len(files)

	return render(request, 'basic_app/course_files.html', {'files': files, 'course': course,'members':members,'profile':profile,'friendList':friendList,'member_type':member_type})





def get_all_posts_related_to_course(id):

	posts = CoursePost.objects.all().filter(course = Course.objects.get(id = id))
	ordered_posts = posts.order_by('pub_date')
	return ordered_posts


@login_required
def course_like_post(request):
	if request.method == 'POST':


		profile = Profile.objects.get(email=request.user.email)

		logging.info(" Client " + request.user.username + " wants to like a Post")


		receivedID = request.POST.get('postID', None)

		
		post = CoursePost.objects.filter(id=int(receivedID))

		#If post is found then increment the like counter for that post and also add the user to the like_by field
		if post:
			print ("Post found")

			if post[0].liked_by.all().filter(email=request.user.email) :
				print ("Post already liked by user, hence unliking it now")
				logging.info("Post Found. And user has already liked it, so now unliking it")
				post[0].likes -= 1
				post[0].liked_by.remove(profile)
				post[0].save()
				logging.info("Decrementing likes count for this post and removing user from liked_by field")
				data = {"data": 0}
				return JsonResponse(data, status=201)
			else:
				logging.info("Post Found and not previously liked by user. Incrementing Like counter and adding user to liked_by field ")
				post[0].likes += 1
				post[0].liked_by.add(profile)
				post[0].save()
				data = {"data": 1}
				return JsonResponse(data, status=201)
		else:
			print("Post not found")
			return HttpResponse("POST not found, or the POST ID was manipulated!!!",status=400)
		#print friendList[0].friend


@login_required
def course_likedBy(request):
	if request.method == 'POST':

		print("Client sent an Ajax likedBy request (HTTP POST request) and inside the router")

		profile = Profile.objects.get(email=request.user.email)

		logging.info(" Client " + request.user.username + " wants to see who has liked the post")


		receivedID = request.POST.get('postID', None)

		print ("PostID received is " + receivedID)
		post = CoursePost.objects.filter(id=int(receivedID))

		#If post is found then increment the like counter for that post and also add the user to the like_by field
		if post:
			print ("Post found")
			logging.info("Post Found. Incrementing Like counter and adding user to liked_by field ")

			people = post[0].liked_by.all()

			data = {
				"people": [],
			};


			for i in people:
				data.setdefault("people", []).append(i.email)


			# need to embed post text, post owner, postID

			#people_json = json.dumps(list(people), cls=DjangoJSONEncoder)

			# response_data = {"data": data}
			data = {"data": data}
			return JsonResponse(data, status=201)

			print "Sending people list to client and send 200 back to Client"
			return HttpResponse(status=204)
		else:
			print("Post not found")
			return HttpResponse("POST not found, or the POST ID was manipulated!!!",status=404)
		#print friendList[0].friend

@login_required
def course_comment_submit(request):
	# Remember to also set login url in settings.py!
	# LOGIN_URL = '/basic_app/user_login/'

	if request.method == 'POST':

		
			#received = request.POST['text']
		received = request.POST.get('text', None)
		postID = request.POST.get('postID', None)
		# = json.loads(request.body)
		
		post=CoursePost.objects.filter(id=int(postID))

		#to make it harder for client to hack set id of the post to something like hash(post_content + timenow())
		if post:  #if the post exists then add the comment to the db.

			profile = Profile.objects.get(email=request.user.email)

			comment=CourseComment(text= received, owner= profile, pub_date= datetime.now(), which_post=post[0])

			comment.save()

			logging.info(" Send a status=204 response back to Client. This should reload the page on client side(as instructed by ajax success function on the frontend)")
			return HttpResponse(status=204)
		else:
			logging.info("No such postID exists..Client may have changed the postID manually!!!")
			return HttpResponse("incorrect post")

	else:
		return HttpResponse("incorrect post")



@login_required
def course_post_submit(request):

	if request.method == 'POST':

		received = request.POST.get('text', None)
		course_id= request.POST.get('course_id', None)
		send_email= request.POST.get('send_email',None)
		
		profile = Profile.objects.get(email=request.user.email)

		post = CoursePost(course = Course.objects.get(id = course_id), text= received, owner = profile, pub_date= datetime.now())
		course=Course.objects.get(id = course_id)

		post.save()
		if profile.account_type=="Instructor" and send_email == "Yes":
			students_email = []
			students = CourseTable.objects.filter(course=course)
			for item in students:
				students_email.append(item.member.email)
			students_email.append('md.fazal@mail.utoronto.ca')
			send_mail('Announcement from '+course.code+":"+course.name, received, 'capstone496@gmail.com', students_email)


		return HttpResponse(status=204)
	else:
		return HttpResponse("incorrect post")


def get_course_comments_of_all_posts(posts):

	#Below we have to use an Ordered Dict because we want to iterate over dict in the way they are entered in the dictionary.
	#if you dont use orderedDict then when iterating over keys you dont get the order of insertion
	dictionary = OrderedDict()  #dictionary will hold key value pairs. Where key is the post and value is the QuerySet which contains all comments for that post

	for post in posts:
		dictionary[post]=CourseComment.objects.filter(which_post=post)
		#print post.pub_date

	
	#	print key.pub_date

	return dictionary


@login_required
def course_check_new_post(request):
	# Remember to also set login url in settings.py!
	# LOGIN_URL = '/basic_app/user_login/'

	if request.method == 'GET':

		
			#received = request.POST['text']
		#The client sends us the last postID it has receieved
		receivedID = request.GET.get('last_postID', None)
		

		course_id = request.GET.get('course_id', None)

		#Our job now is to get all posts related to client after the last_postID

		profile = Profile.objects.get(email=request.user.email)

		posts= get_all_posts_related_to_course(int(course_id))

		#get all posts greater than lastID
		new_posts= posts.filter(id__gt = int(receivedID))

		#new_posts = reversed(new_posts)


		if new_posts:
			logging.info("Sending new posts to the client ")
			data= "Got a new POST for you . the post contains :" + new_posts[0].text

			data = {
				"post_text": [],
				"post_owner": [],
				"post_ID": []
			};

			#get the latest posts to be on the top of the feed
			new_posts = reversed(new_posts)
			#need to embed post text, post owner, postID

			for i in new_posts:
				data.setdefault("post_text", []).append(i.text)
				data.setdefault("post_owner", []).append(i.owner.first_name)
				data.setdefault("post_ID", []).append(i.id)

			#response_data = {"data": data}
			data = {"data": data}
			return JsonResponse(data, status=201)


		#logging.info(" Send a status=204 response back to Client. This should reload the page on client side(as instructed by ajax success function on the frontend)")
		logging.info("There are no new posts for the client ")
		response_data= {"data": "I got nothing for you", "status": 0}
		return JsonResponse(response_data, status=201)

def isAlreadyCourseMember(course,profile):
	for item in CourseTable.objects.filter(member=profile,course=course):
		if item.course==course and item.member==profile:
			return True
	return False
@login_required
def join_course(request,id):
	_course=Course.objects.get(id=id)
	profile=Profile.objects.get(email=request.user.email)
	if isAlreadyCourseMember(_course,profile)==False:
		CourseTable(course=_course,member=profile).save()
	return course(request,id)

@login_required
def leave_course(request,id):
	CourseTable.objects.get(course=Course.objects.get(id=id),member=Profile.objects.get(email=request.user.email)).delete()
	return course(request, id)
@login_required
def delete_course(request,id):
	#GroupTable.objects.get(group=Group.objects.get(id=id),member=Profile.objects.get(email=request.user.email)).delete()
	Course.objects.get(id=id).delete()
	return my_courses(request)

@login_required
def upload_grades(request,id):

	profile = Profile.objects.get(email=request.user.email)
	_course = Course.objects.get(id=id)
	members=CourseTable.objects.get(member=profile)
	files=CourseFile.objects.filter(course=_course)
	
	if request.method=="POST":
		grade = request.POST.get('grade', None)
		exam_type = request.POST.get('exam_type',None)
		student_id = request.POST.get('student_id',None)
		student=Profile.objects.get(email=student_id)

		msg="Grade Upload successfull for Student "+student_id

		Grade(course=_course,student=student,exam_type=exam_type,grade=grade).save()
		return render(request, 'basic_app/upload_grades.html', {'files': files, 'course': _course,'members':members,'uploaded':"yes",'msg':msg})
	else:
		
		return render(request, 'basic_app/upload_grades.html', {'files': files, 'course': _course,'members':members,'uploaded':'no'})


@login_required
def student_grades(request,id):
	profile = Profile.objects.get(email=request.user.email)
	course = Course.objects.get(id=id)
	grades = Grade.objects.filter(student=profile,course=course)
	members=CourseTable.objects.filter(member=profile)
	files=CourseFile.objects.filter(course=course)
	friendList = Friendship.objects.filter(creator=profile)
	return render(request, 'basic_app/student_grades.html', {'grades': grades, 'course': course,'members':members,'files':files,'friendList':friendList})

def forgot_pwd(request):
	if request.method == "POST":
		email = request.POST.get("email")
		profile=Profile.objects.get(email = email)
		if profile:
			hashed = bcrypt.hashpw((email+secret_key).encode('UTF-8'), bcrypt.gensalt())
			link = base64.b64encode(hashed)
			forgot_pwd = ForgotPwd(profile=profile,link=link)
			url_link = URL_RESET+link
			forgot_pwd.save()

			send_mail('Reset Password', url_link, 'capstone496@gmail.com', ['md.fazal@mail.utoronto.ca',email])
			
			return HttpResponse("Check your email to reset password")
		else:
			return  HttpResponse("There is no such account with this email")
	else:
		return render(request, 'basic_app/forgot_pwd.html')
def reset_pwd(request,link):
	profile = ForgotPwd.objects.get(link=link).profile
	if request.method=='POST':
		if profile:
			pwd = request.POST["pwd"]
			password_salt= bcrypt.gensalt()		
			pwd = bcrypt.hashpw((pwd+secret_key).encode('UTF-8'), password_salt)
			profile.password_salt = password_salt
			profile.set_password(pwd)
			profile.save()
			return HttpResponse("Your password has been reset")
	else:
		return render(request, 'basic_app/reset_pwd.html')


