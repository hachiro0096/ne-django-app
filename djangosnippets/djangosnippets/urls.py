from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('helloworld.urls')),  # アプリ名を適宜変更
    path('accounts/', include('django.contrib.auth.urls')),  # ★追加（ログイン/ログアウトなど）
]

# メディアファイル配信設定（開発環境のみ）
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
