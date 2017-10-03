from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^tasks_list/$', views.tasks_list, name='tasks_list'),
    url(r'^home/$', views.home, name='home'),
    url(r'^add_students/$', views.add_students, name='add_students'),
    url(r'^task_details/(?P<task_id>\d+)/$', views.task_details, name='task_details'),
    url(r'^group_details/(?P<group_id>\d+)/$', views.group_details, name='group_details'),
    url(r'^add_evals/(?P<group_id>\d+)/(?P<task_id>\d+)/$', views.add_evals, name='add_evals'),
    url(r'^get_subms/(?P<group_id>\d+)/(?P<tasks_set_id>\d+)/$', views.get_subms, name='get_subms'),
    url('^$',  views.home)
]

