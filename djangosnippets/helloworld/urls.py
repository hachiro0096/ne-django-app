from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', views.top, name='top'),
    path('signup/', views.signup, name='signup'),
    path('log_list/', views.log_list, name='log_list'),
    path('log_new/', views.log_new, name='log_new'),
    path('log/<int:pk>/', views.log_detail, name='log_detail'),
    path('log/<int:pk>/edit/', views.log_edit, name='log_edit'),
    path('log/<int:pk>/delete/', views.log_delete, name='log_delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('questions/', views.question_list, name='question_list'),
    path('questions/new/', views.question_new, name='question_new'),
    path('questions/<int:pk>/', views.question_detail, name='question_detail'),
    path('questions/<int:pk>/answer/', views.answer_new, name='answer_new'),


    path('profile/edit/', views.profile_edit, name='profile_edit'),

    path('accounts/logout/', LogoutView.as_view(), name='logout'),






    # 他のURLも追加していく
]
