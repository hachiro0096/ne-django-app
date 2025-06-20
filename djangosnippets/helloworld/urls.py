"""from django.urls import path

from helloworld import views

urlpatterns = [
    path("new", views.snippet_new, name="snippet_new"),
    path("<int:snippet_id>", views.snippet_detail, name="snippet_detail"),
    path("<int:snippet_id>/edit", views.snippet_edit, name="snippet_edit"),
]"""

from django.urls import path
from helloworld import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

urlpatterns = [
    path('new/', views.snippet_new, name='snippet_new'),
    path('<int:snippet_id>/', views.snippet_detail, name='snippet_detail'),
    path('<int:snippet_id>/edit/', views.snippet_edit, name='snippet_edit'),
    path(
        'login/',
        LoginView.as_view(
            redirect_authenticated_user=True,
            template_name='snippets/login.html'
        ),
        name='login'
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        'signup/',
        CreateView.as_view(
            template_name='snippets/signup.html',
            form_class=UserCreationForm,
            success_url='/'
        ),
        name='signup'
    ),
]


'''urlpatterns = [
    # 一覧
    path('',                   views.top,           name='top'),

    # 新規作成：/helloworld/new/
    path('new/',               views.snippet_new,   name='snippet_new'),

    # 詳細：/helloworld/123/
    path('<int:snippet_id>/',  views.snippet_detail, name='snippet_detail'),

    # 編集：/helloworld/123/edit/
    path('<int:snippet_id>/edit/', views.snippet_edit, name='snippet_edit'),


]'''
