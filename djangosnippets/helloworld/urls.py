from django.urls import path
from . import views

urlpatterns = [
    path('', views.top, name='top'),
    path('signup/', views.signup, name='signup'),
    path('log_list/', views.log_list, name='log_list'),
    path('log_new/', views.log_new, name='log_new'),
    path('log/<int:pk>/', views.log_detail, name='log_detail'),
    path('log/<int:pk>/edit/', views.log_edit, name='log_edit'),
    path('log/<int:pk>/delete/', views.log_delete, name='log_delete'),
    path('dashboard/', views.dashboard, name='dashboard'),




    # 他のURLも追加していく
]
