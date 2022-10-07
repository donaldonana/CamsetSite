from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    # path('vote', views.vote, name='vote'),
    path('upload', views.upload, name='upload'),
    path('save', views.save, name='save'), 
    path('delete', views.delete, name='delete'), 

    path('DeleteAll', views.DeleteAll, name='DeleteAll'), 
    path('admin', views.admin, name='admin'),
    path('help', views.help, name='help'),
    path("list_result", views.ListResult, name='list_result'),
       
]
