from django.urls import path, include, re_path

from . import views
# from AppAuth.views import auth_validate

urlpatterns = [

    #path('', include(router.urls)),
    path("login",views.login_user, name = 'login'),
    path("register", views.register, name = 'register'),
    path("logout_user", views.logout_user, name='logout_user'),

    # re_path(r'^auth_validate/$', auth_validate , name='auth_validate'),


    ]