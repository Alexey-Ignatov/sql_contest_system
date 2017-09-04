from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^tasks_list/$', views.tasks_list, name='tasks_list'),
    url(r'^home/$', views.home, name='home'),
    url(r'^task_details/(?P<task_id>\d+)/$', views.task_details, name='task_details'),

]

