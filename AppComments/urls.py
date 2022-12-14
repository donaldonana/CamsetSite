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
    path('filtering', views.filtering, name='filtering'),
    # path('finduser', views.finduser, name='finduser'),
    

    path("stats", views.stats, name='stats'),
    path("StatsPagination", views.StatsPagination, name='StatsPagination'),
    
       
]
