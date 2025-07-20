from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('helloworld.urls')),  # アプリ名を適宜
    path('accounts/', include('django.contrib.auth.urls')),  # ★これを追加
]
