from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from helloworld.views import top, snippet_new, snippet_edit, snippet_detail

from django.contrib import admin
from django.urls import path

# URL設定（通常はプロジェクト側のurls.pyに置きますが、テスト用にここに記述しています）
urlpatterns = [
    path('', top, name='top'),
    path('admin/', admin.site.urls),
]

# --- Topページのテスト ---
class TopPageViewTest(TestCase):
    def test_top_returns_200(self):
        request = HttpRequest()
        response = top(request)
        self.assertEqual(response.status_code, 200)

    def test_top_returns_expected_content(self):
        request = HttpRequest()
        response = top(request)
        self.assertEqual(response.content, b'Hello World by Takumi')


# --- スニペット新規作成URLのテスト ---
class CreateSnippetTest(TestCase):
    def test_should_resolve_snippet_new(self):
        found = resolve('helloworld/new')
        self.assertEqual(snippet_new, found.func)


# --- スニペット詳細URLのテスト ---
class SnippetDetailTest(TestCase):
    def test_should_resolve_snippet_detail(self):
        found = resolve('helloworld/1')
        self.assertEqual(snippet_detail, found.func)


# --- スニペット編集URLのテスト ---
class EditSnippetTest(TestCase):
    def test_should_resolve_snippet_edit(self):
        found = resolve('helloworld/1/edit')
        self.assertEqual(snippet_edit, found.func)
