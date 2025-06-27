from django.shortcuts import render, redirect
from .models import StudyLog
from .forms import StudyLogForm
from django.contrib.auth.decorators import login_required

@login_required
def log_list(request):
    logs = StudyLog.objects.filter(user=request.user).order_by('-date')
    total_points = logs.aggregate(total=models.Sum('points'))['total'] or 0
    return render(request, 'snippets/log_list.html', {
        'logs': logs,
        'total_points': total_points,
    })

@login_required
def log_list(request):
    logs = StudyLog.objects.filter(user=request.user).order_by('-date')
    total_points = logs.aggregate(total=models.Sum('points'))['total'] or 0

    # バッジの計算
    def get_badge(points):
        if points >= 100:
            return "ゴールドバッジ 🥇"
        elif points >= 50:
            return "シルバーバッジ 🥈"
        elif points >= 10:
            return "ブロンズバッジ 🥉"
        else:
            return "ビギナー"

    badge = get_badge(total_points)
    return render(request, 'snippets/log_list.html', {
        'logs': logs,
        'total_points': total_points,
        'badge': badge,
    })

@login_required
def log_list(request):
    logs = StudyLog.objects.filter(user=request.user).order_by('-date')
    return render(request, 'snippets/log_list.html', {'logs': logs})

@login_required
def log_new(request):
    if request.method == "POST":
        form = StudyLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.points = min(10, len(log.content) // 10)  # 例：文字数でポイント計算
            log.save()
            return redirect('log_list')
    else:
        form = StudyLogForm()
    return render(request, 'snippets/log_new.html', {'form': form})
