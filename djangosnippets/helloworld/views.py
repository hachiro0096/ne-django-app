
# ne-django-app/djangosnippets/helloworld/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import StudyLog
from .forms import StudyLogForm


@login_required
def log_list(request):
    logs = StudyLog.objects.filter(user=request.user).order_by('-date')
    total_points = logs.aggregate(total=Sum('points'))['total'] or 0

    # バッジ計算例
    if total_points >= 100:
        badge = "ゴールドバッジ 🥇"
    elif total_points >= 50:
        badge = "シルバーバッジ 🥈"
    elif total_points >= 10:
        badge = "ブロンズバッジ 🥉"
    else:
        badge = "ビギナー"

    return render(request, 'snippets/log_list.html', {
        'logs': logs,
        'total_points': total_points,
        'badge': badge,
    })

@login_required
def log_new(request):
    if request.method == 'POST':
        form = StudyLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.points = min(10, len(log.content) // 10)
            log.save()
            return redirect('log_list')
    else:
        form = StudyLogForm()
    return render(request, 'snippets/log_new.html', {'form': form})
# helloworld/views.py

from django.shortcuts          import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth       import login as auth_login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)          # 登録後に自動ログイン
            return redirect('top')             # トップページへリダイレクト
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })
