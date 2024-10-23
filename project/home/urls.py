from django.urls import path
from .import views
urlpatterns = [
    path('cadmin',views.cadmin,name='cadmin'),
    path('detials/<int:id>',views.user_detials,name='user_detials'),
    path('delete/<int:id>',views.delete_user,name='delete'),
    path('register',views.user_creation,name='register'),
    path('login',views.login_page,name='login'),
    path('',views.main_page,name='main'),
    path('logout',views.user_logout,name='logout'),
    path('edit/<int:id>',views.edit_user,name='edit_user'),
    path('signup',views.user_signup,name='signup'),
]
