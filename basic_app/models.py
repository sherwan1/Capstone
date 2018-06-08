from django.db import models
from django.contrib.auth.models import User
import uuid
#from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config
#from neo4django.db import models



class Profile(User):

    # Create relationship (don't inherit from User!)
    #user = models.OneToOneField(User)
    
    # Add any additional attributes you want
    #portfolio_site = models.URLField(blank=True)
    # pip install pillow to use this!
    #profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    password_salt = models.CharField(max_length=150,null=True)
    #uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    #online_status = models.BooleanField(default=False) #how do we check if user is online or not. What if the window is closed but user is online?

    # file will be uploaded to MEDIA_ROOT/pic_folder
    profile_pic = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/no-img.jpg')


    #Additional field
    phone = models.CharField(max_length=15, null=True)
    contact_email = models.CharField(max_length=150, null=True)
    start_date = models.CharField(max_length=150, null=True)
    grad_date = models.CharField(max_length=150, null=True)
    city = models.CharField(max_length=150, null=True)
    province = models.CharField(max_length=150, null=True)
    country = models.CharField(max_length=150, null=True)
    interests = models.CharField(max_length=150, null=True)
    courses = models.CharField(max_length=1500, null=True)
    title = models.CharField(max_length=150, null=True)
    discipline = models.CharField(max_length=150, null=True)
    dob = models.CharField(max_length=150, null=True)
    account_type= models.CharField(max_length=150, null=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username

    def getInterests(self):
        if self.interests is None:
            return []
        return self.interests.split(",")
    def getCourses(self):
        if self.courses is None:
            return []
        return self.courses.split(",")
    def phoneExists(self):
        if self.phone is not None:
            if len(self.phone)>0:
                return True
            else:
                return False
        else:
            return False
    def profilePicExist(self):
        if self.profile_pic_exist=="yes":
            return True
        else:
            return False

class ImageTable(models.Model):
    image = models.ImageField(upload_to="media", blank=True)
    uploaded_by = models.ForeignKey(Profile, related_name="uploaded_by", on_delete=models.CASCADE)
    uploaded_time = models.DateTimeField(auto_now_add=True, null=True)
    caption = models.CharField(max_length=150, null=True)




#class Friend(models.Model):
#	email = models.CharField(max_length=30)
#	date_of_friendship = models.DateTimeField(null=True)
#	friends = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

class Friendship(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    creator = models.ForeignKey(Profile, related_name="friendship_creator_set")
    friend = models.ForeignKey(Profile, related_name="friend_set")




class TempUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password= models.CharField(max_length=130)
    link =  models.CharField(max_length=150,null=True)
    password_salt= models.CharField(max_length=150,null=True)
    account_type=models.CharField(max_length=150,null=True)



    

#all models have primary key by default

class Post(models.Model):
    text = models.CharField(max_length=1000)		      #each post will have a max length of 1000chars(for now, can change later)
    pub_date = models.DateTimeField()			      #each post will have a publication date/time field
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="owner")  #we associate each post with its owner using the Foreignkey
    likes = models.IntegerField(default=0)              #By default when a post is created No one has liked it yet so default number of like is 0
    liked_by = models.ManyToManyField(Profile, related_name="liked_by")
    post_photo_directory = models.CharField(max_length=1000, null=True)
    video_url= models.CharField(max_length=1000, null=True)

class Photo_links(models.Model):
    url_link = models.CharField(max_length=1000, null=True)
    which_post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
	text = models.CharField(max_length=1000)		     	 #each commment will have a max length of 1000chars(for now, can change later)
	pub_date = models.DateTimeField()				 #each comment will have a publication date/time field
	owner = models.ForeignKey(Profile, on_delete=models.CASCADE) 	 #we associate each comment with its owner using the Foreignkey
	which_post = models.ForeignKey(Post, on_delete=models.CASCADE)  #we associate each comment with a post using the Foreignkey (comments can only be posted under the posts)

	

class TempFriendRequest(models.Model):
    requestFrom = models.ForeignKey(Profile, related_name="friend_making_request")
    requestTo = models.ForeignKey(Profile, related_name="sending_request_to")

class Message(models.Model):
    room = models.CharField(max_length=1000)  #room would communication between 2 parties. This would be a unqiue value calculated by combining the id's of 2 ppl
    messageFrom = models.ForeignKey(Profile, related_name="msg_from")
    messageTo = models.ForeignKey(Profile, related_name="msg_to")
    text = models.CharField(max_length=10000)
    pub_date = models.DateTimeField()
    file_name = models.CharField(max_length=512, null=True)
    file_url = models.CharField(max_length=1500, null=True)
    #file = models.ForeignKey(Document, related_name="document")
    #file_check = models.BooleanField(default=False)

    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Message_Notification(models.Model):
    #only one notification per room. If the notification already exists for that room then dont generate again
    #Once the user sees the chat room that mean he has seen all the messages in the chat room and
    #hence we can delete the notification for that chat room then.
    room = models.CharField(max_length=1000) #generate notification for a room only. Dont generate notifications for every msg, this isnt a good soln
    notification_for = models.ForeignKey(Profile, related_name="notification_for")
    notification_by_email = models.CharField(max_length=1000)


class Group(models.Model):
    name = models.CharField(max_length=1000)  #room would communication between 2 parties. This would be a unqiue value calculated by combining the id's of 2 ppl
    creator = models.ForeignKey(Profile, related_name="creator")
    description = models.CharField(max_length=10000)
    creation_date = models.DateTimeField()
    image = models.ImageField(upload_to='media', default='pic_folder/no_pic_grp.png')

class GroupTable(models.Model):
    group = models.ForeignKey(Group, related_name="groups")
    member = models.ForeignKey(Profile, related_name="member")
    
class GroupPost(models.Model):
    group = models.ForeignKey(Group, related_name="group")
    text = models.CharField(max_length=1000)              #each post will have a max length of 1000chars(for now, can change later)
    pub_date = models.DateTimeField()                 #each post will have a publication date/time field
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="group_owner")  #we associate each post with its owner using the Foreignkey
    likes = models.IntegerField(default=0)              #By default when a post is created No one has liked it yet so default number of like is 0
    liked_by = models.ManyToManyField(Profile, related_name="group_liked_by")
        
class GroupComment(models.Model):
    text = models.CharField(max_length=1000)                 #each commment will have a max length of 1000chars(for now, can change later)
    pub_date = models.DateTimeField()                #each comment will have a publication date/time field
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)     #we associate each comment with its owner using the Foreignkey
    which_post = models.ForeignKey(GroupPost, on_delete=models.CASCADE)  #we associate each comment with a post using the Foreignkey (comments can only be posted under the posts)


class GroupFile(models.Model):
    file = models.FileField(upload_to="media", blank=True)
    uploaded_by = models.ForeignKey(Profile, related_name="uploaded_by_file", on_delete=models.CASCADE)
    group=models.ForeignKey(Group, related_name="group_file",on_delete=models.CASCADE)

class Course(models.Model):
    name = models.CharField(max_length=1000)  #room would communication between 2 parties. This would be a unqiue value calculated by combining the id's of 2 ppl
    code = models.CharField(max_length=1000)
    section = models.CharField(max_length=1000)
    term = models.CharField(max_length=1000)
    year = models.CharField(max_length=1000)
    office_hours = models.CharField(max_length=1000, null=True)
    office_location = models.CharField(max_length=1000, null=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.CharField(max_length=10000)
    creation_date = models.DateTimeField()
   

class CourseTable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    member = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
class CoursePost(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)              #each post will have a max length of 1000chars(for now, can change later)
    pub_date = models.DateTimeField()                 #each post will have a publication date/time field
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)  #we associate each post with its owner using the Foreignkey
    likes = models.IntegerField(default=0)              #By default when a post is created No one has liked it yet so default number of like is 0
    liked_by = models.ManyToManyField(Profile, related_name="course_liked_by")
        
class CourseComment(models.Model):
    text = models.CharField(max_length=1000)                 #each commment will have a max length of 1000chars(for now, can change later)
    pub_date = models.DateTimeField()                #each comment will have a publication date/time field
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)     #we associate each comment with its owner using the Foreignkey
    which_post = models.ForeignKey(CoursePost, on_delete=models.CASCADE)  #we associate each comment with a post using the Foreignkey (comments can only be posted under the posts)

class CourseFile(models.Model):
    file = models.FileField(upload_to="media", blank=True)
    uploaded_by = models.ForeignKey(Profile, related_name="course_uploaded_by_file", on_delete=models.CASCADE)
    course=models.ForeignKey(Course, related_name="course_file",on_delete=models.CASCADE)

class Grade(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    student=models.ForeignKey(Profile,on_delete=models.CASCADE)
    grade=models.CharField(max_length=1000)
    exam_type=models.CharField(max_length=1000)

class ForgotPwd(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    link = models.CharField(max_length=150,null = True)




#class Document(models.Model):
 #   file_name = models.CharField(max_length=255, default=None)
  #  document_url = models.CharField(max_length=1500, default=None)
   # uploaded_at = models.DateTimeField(auto_now_add=True)

