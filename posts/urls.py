from django.contrib import admin
from django.urls import path, re_path

from posts.views import *


app_name = 'postsurl'

urlpatterns = [
    path('', posts_home ,name="home"),
    path('create/', post_create, name = "create"),
    path('mooryn/<str:slug>/', post_detail, name = "detail"),
    path('list/', post_list, name = "list"),
    path('<str:slug>/edit/', post_update, name = "update"),
    path('<str:slug>/delete/', post_delete, name = "delete"),

]


# urlpatterns = [
# 	url(r'^$', "posts.views.post_list"),
#     url(r'^create/$', "posts.views.post_create"),
#     url(r'^detail/$', "posts.views.post_detail"),
#     url(r'^update/$', "posts.views.post_update"),
#     url(r'^delete/$', "posts.views.post_delete"),
#     #url(r'^posts/$', "<appname>.views.<function_name>"),
# ]