# ne-django-app/djangosnippets/helloworld/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # トップページ
    path('', views.log_list,   name='top'),
    # サインアップ用
    path('signup/', views.signup, name='signup'),
    # 学習ログ一覧
    path('logs/',    views.log_list, name='log_list'),
    path('logs/new/', views.log_new, name='log_new'),
]
