from django.conf.urls import url
from basic_app import views

# SET THE NAMESPACE!
app_name = 'basic_app'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^confirm/(?P<hash>[A-Za-z0-9]*)/$',views.confirm_sign_up,name="confirm"),#sign up
    url(r'^post_submit$', views.post_submit, name='post_submit'),
    url(r'^comment_submit$', views.comment_submit, name='comment_submit'),
    url(r'^search$', views.search, name='search'),
    url(r'^sendFriendRequest$', views.sendFriendRequest, name='sendFriendRequest'),
    url(r'^friendRequests$', views.friendRequests, name='friendRequests'),
    url(r'^friendList$', views.friendList, name='friendList'),
    url(r'^chat_auth_token$', views.chat_auth_token, name='chat_auth_token'),
    url(r'^my_groups$', views.my_groups, name='my_groups'),


]

