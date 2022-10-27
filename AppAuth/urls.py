from django.urls import path, include, re_path

from . import views
# from AppAuth.views import auth_validate

urlpatterns = [

    #path('', include(router.urls)),
    path("login",views.login_user, name = 'login'),
    path("register", views.register, name = 'register'),
    path("logout_user", views.logout_user, name='logout_user'),
    path("AddToCheked", views.AddToCheked, name='AddToCheked'),
    path("MoveToCheked", views.MoveToCheked, name='MoveToCheked'), 
    path("DeleteChecked", views.DeleteChecked, name='DeleteChecked'), 
    

    



    # re_path(r'^auth_validate/$', auth_validate , name='auth_validate'),


    ]