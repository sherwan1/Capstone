"""learning_users URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from basic_app import views

from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    url(r'^$', views.user_login, name='user_login'),  # views.index,name='index'),
    #url(r'^special/',views.special,name='special'),
    #url(r'^admin/', admin.site.urls),
    url(r'^basic_app/',include('basic_app.urls')),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^messages$', views.user_messages, name='user_messages'),
    url(r'^post_submit$',views.post_submit,name='post_submit'),
    url(r'^comment_submit$', views.comment_submit, name='comment_submit'),
    url(r'^search$', views.search, name='search'),
    url(r'^welcome$', views.welcome, name='welcome'),
    url(r'^sendFriendRequest$', views.sendFriendRequest, name='sendFriendRequest'),
    url(r'^friendRequests$', views.friendRequests, name='friendRequests'),
    url(r'^friendList$', views.friendList, name='friendList'),
    url(r'^check_new_post$', views.check_new_post, name='check_new_post'),
    url(r'^like_post$', views.like_post, name='like_post'),
    url(r'^likedBy$', views.likedBy, name='likedBy'),
    url(r'^chat_auth_token$', views.chat_auth_token, name='chat_auth_token'),
    url(r'^send_message$', views.send_message, name='send_message'),
    url(r'^delete_msg_notification$', views.delete_msg_notification, name='delete_msg_notification'),
    url(r'^send_message_file$', views.send_message_file, name='send_message_file'),
    url(r'^my_groups$', views.my_groups, name='my_groups'),
    url(r'^group_new$', views.group_new, name='group_new'), 
    url(r'^group_create$', views.group_create, name='group_create'),    
    url(r'^group/(?P<id>[0-9]*)/$',views.group,name="group"),
    url(r'^group_post_submit$',views.group_post_submit,name='group_post_submit'), 
    url(r'^group_check_new_post$', views.group_check_new_post, name='group_check_new_post'), 
    url(r'^group_like_post$', views.group_like_post, name='group_like_post'),
    url(r'^group_likedBy$', views.group_likedBy, name='group_likedBy'),
    url(r'^group_comment_submit$', views.group_comment_submit, name='group_comment_submit'),
    url(r'^join_group/(?P<id>[0-9]*)/$', views.join_group, name='join_group'),
    url(r'^leave_group/(?P<id>[0-9]*)/$', views.leave_group, name='leave_group'),
    url(r'^profile_edit$', views.profile_edit, name='profile_edit'),
    url(r'^photos$', views.photos, name='photos'),
    url(r'^photo/(?P<id>[0-9]+)/$', views.detailed_photo, name="detailed_photo"),
    url(r'^photo/delete/(?P<id>[0-9]+)/$', views.delete_photo, name="delete_photo"),
    url(r'^profile_self/$', views.profile_self, name='profile_self'),
    url(r'^profile/(?P<id>[0-9]+)/$', views.profile_other, name="profile_other"),
    url(r'^group_members/(?P<id>[0-9]+)/$', views.group_members, name="group_members"),
    url(r'^group_files/(?P<id>[0-9]+)/$', views.group_files, name="group_files"),
    url(r'^delete_group/(?P<id>[0-9]+)/$', views.delete_group, name="delete_group"),
    url(r'^my_courses$', views.my_courses, name='my_courses'),
    url(r'^course_new$', views.course_new, name='course_new'), 
    url(r'^course_create$', views.course_create, name='course_create'),    
    url(r'^course/(?P<id>[0-9]*)/$',views.course,name="course"),
    url(r'^course_post_submit$',views.course_post_submit,name='course_post_submit'), 
    url(r'^course_check_new_post$', views.course_check_new_post, name='course_check_new_post'), 
    url(r'^course_like_post$', views.course_like_post, name='course_like_post'),
    url(r'^course_likedBy$', views.course_likedBy, name='course_likedBy'),
    url(r'^course_comment_submit$', views.course_comment_submit, name='course_comment_submit'),
    url(r'^join_course/(?P<id>[0-9]*)/$', views.join_course, name='join_course'),
    url(r'^leave_course/(?P<id>[0-9]*)/$', views.leave_course, name='leave_course'),
    url(r'^course_members/(?P<id>[0-9]+)/$', views.course_members, name="course_members"),
    url(r'^course_files/(?P<id>[0-9]+)/$', views.course_files, name="course_files"),
    url(r'^delete_course/(?P<id>[0-9]+)/$', views.delete_course, name="course_group"),
    url(r'^upload_grades/(?P<id>[0-9]+)/$', views.upload_grades, name="upload_grade"),
    url(r'^student_grades/(?P<id>[0-9]+)/$', views.student_grades, name="my_grades"),
    url(r'^download/(?P<uuid1>\w+)/(?P<uuid2>\w+)/(?P<filename>[a-zA-Z0-9_.-/:?=# ]+)', views.file_download, name='file_download'),
    url(r'^forgot_pwd$', views.forgot_pwd, name='forgot_pwd'),
    url(r'^reset_pwd/(?P<link>[A-Za-z0-9]*)/$',views.reset_pwd,name="reset_pwd"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
