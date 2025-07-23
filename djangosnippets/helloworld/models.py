from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# バッジの種類
class Badge(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    threshold = models.PositiveIntegerField(help_text="このポイント数で獲得")
    date_awarded = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

# ユーザープロフィール（ポイント・現在のバッジなど＋追加フィールド）
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    badge = models.ForeignKey(Badge, null=True, blank=True, on_delete=models.SET_NULL)
    # プロフィール編集用フィールド
    nickname = models.CharField(max_length=30, blank=True)
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    show_badges = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

# ユーザーがどのバッジを取得したかの履歴
class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"

# 学習記録
class StudyLog(models.Model):
    SUBJECT_CHOICES = (
        ('math', '数学'),
        ('physics', '物理'),
        ('prog', 'プログラミング'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    subject = models.CharField(max_length=30, choices=SUBJECT_CHOICES)
    hours = models.DecimalField(max_digits=4, decimal_places=2)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.subject}"

# Snippetモデル（おそらく使っている場合）
class Snippet(models.Model):
    date = models.DateField()
    subject = models.CharField(max_length=100)
    hours = models.FloatField()
    comment = models.TextField()

    def __str__(self):
        return self.subject

# Q&A 投稿・回答
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}さんの回答"

# User作成時に自動でUserProfileも作る
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
