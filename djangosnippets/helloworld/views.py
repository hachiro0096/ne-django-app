from django.shortcuts import render, get_object_or_404
from .models import StudyLog
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Badge, UserProfile, UserBadge, StudyLog
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import StudyLogForm
from datetime import date, timedelta
from django.shortcuts import render, redirect
from .forms import SnippetForm
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from .forms import ProfileForm

@login_required
def profile_edit(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_edit')  # 保存後自分にリダイレクト（または他ページへ）
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'snippets/profile_edit.html', {'form': form, 'profile': profile})


def question_list(request):
    questions = Question.objects.all().order_by('-created')
    return render(request, 'snippets/question_list.html', {'questions': questions})

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()
    return render(request, 'snippets/question_detail.html', {'question': question, 'answers': answers})

@login_required
def question_new(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'snippets/question_new.html', {'form': form})

@login_required
def answer_new(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', pk=pk)
    else:
        form = AnswerForm()
    return render(request, 'snippets/answer_new.html', {'form': form, 'question': question})

def snippet_new(request):
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_list')  # ログ一覧に遷移（urls.pyのnameと合わせる）
    else:
        form = SnippetForm()
    return render(request, 'snippets/snippet_new.html', {'form': form})


@login_required
def dashboard(request):
    # 直近7日間の学習ログを取得
    today = date.today()
    week_ago = today - timedelta(days=6)
    logs = StudyLog.objects.filter(user=request.user, date__range=[week_ago, today]).order_by('date')

    # 日ごとの合計時間
    daily_data = {}
    for i in range(7):
        d = week_ago + timedelta(days=i)
        daily_data[d] = 0

    for log in logs:
        daily_data[log.date] += float(log.hours)

    total_hours = sum(daily_data.values())
    labels = [d.strftime("%m/%d") for d in daily_data.keys()]
    data = [daily_data[d] for d in daily_data.keys()]

    context = {
        'total_hours': total_hours,
        'labels': labels,
        'data': data,
    }
    return render(request, 'snippets/dashboard.html', context)


@login_required
def log_delete(request, pk):
    log = get_object_or_404(StudyLog, pk=pk, user=request.user)
    if request.method == "POST":
        log.delete()
        return redirect('log_list')  # ログ一覧ページ名に変更
    return render(request, 'snippets/log_delete.html', {'log': log})


def log_edit(request, pk):
    log = get_object_or_404(StudyLog, pk=pk, user=request.user)
    if request.method == "POST":
        form = StudyLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            return redirect('log_detail', pk=log.pk)
    else:
        form = StudyLogForm(instance=log)
    return render(request, 'snippets/log_edit.html', {'form': form})


def log_detail(request, pk):
    log = get_object_or_404(StudyLog, pk=pk, user=request.user)
    return render(request, 'snippets/log_detail.html', {'log': log})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 適宜ログイン画面のnameに合わせて変更
    else:
        form = UserCreationForm()
    return render(request, 'snippets/signup.html', {'form': form})


def top(request):
    return render(request, 'snippets/top.html')


# ポイント追加とバッジチェックの関数
def add_points_and_check_badge(user, points_to_add):
    # プロフィール取得（なければ作る）
    profile, _ = UserProfile.objects.get_or_create(user=user)
    # ポイント加算
    profile.points += points_to_add
    profile.save()

    # バッジの判定
    badges = Badge.objects.filter(threshold__lte=profile.points).order_by('-threshold')
    if badges.exists():
        badge = badges.first()
        # すでに取得済みか確認
        if not UserBadge.objects.filter(user=user, badge=badge).exists():
            # バッジ取得記録を作成
            UserBadge.objects.create(user=user, badge=badge)
            # 最新バッジをプロフィールにも保存
            profile.badge = badge
            profile.save()

@login_required
def log_new(request):
    if request.method == "POST":
        # StudyLogFormはforms.pyに定義が必要
        from .forms import StudyLogForm
        form = StudyLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            add_points_and_check_badge(request.user, points_to_add=10)
            return redirect('log_list')
    else:
        from .forms import StudyLogForm
        form = StudyLogForm()
    return render(request, 'snippets/log_new.html', {'form': form})

@login_required
def log_list(request):
    logs = StudyLog.objects.filter(user=request.user).order_by('-date')
    return render(request, 'snippets/log_list.html', {'logs': logs})

# そのほかのviewも同様にUserProfile/BadgeのimportだけでOKです
