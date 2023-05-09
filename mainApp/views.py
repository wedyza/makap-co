from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.utils.encoding import force_bytes, force_str
from .token import account_activation_token
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .models import Message, userProfile
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

def home(request):
    filters = request.GET.get('text') if request.GET.get('text') != None else ''
    users = User.objects.filter(username__icontains=filters)
    context = {
        'users': users
    }
    return render(request, 'home.html', context)

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Такого пользователя не существует')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during authorisation.')
    return render(request, 'login.html')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Вы успешно завершили регистрацию, теперь, пожалуйста, заполните свой профиль')
        return redirect('edit-profile')
    else:
        return HttpResponse('Неправильная ссылка')

def reset_password(request, uidb64, token):

    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            return HttpResponse('Все норм бро')

    context = {
        'form': SetPasswordForm()
    }
    return render(request, 'password_reset.html', context)

def registerPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            user_profile = userProfile.objects.create(user=user)

            current_site = get_current_site(request)
            mail_subject = 'Ссылка для активации аккаунта отправлена на вашу почту'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Подтвердите свой адрес для завершения регистрации')
        else:
            messages.error(request, 'Что-то пошло не так..')
    else:
        form = SignupForm()
    return render(request, 'register.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def recoveryPage(request):
    if request.method == 'POST':
        pass_reset_form = PasswordResetForm(request.POST)
        if pass_reset_form.is_valid():
            print('Я вроде работаю')
            mail = pass_reset_form.cleaned_data['email']
            try:
                user = User.objects.get(email=mail)
            except:
                user = False
                messages.error(request, 'Something went wrong..')
            if user:
                subject = 'Запрошен сброс пароля'
                email_template_name = 'password_reset_email.html'
                current_site = get_current_site(request)
                msg_html = render_to_string(email_template_name, {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user)),
                    'token': account_activation_token.make_token(user),
                })
                email = EmailMessage(
                    subject, msg_html, mail
                )
                email.send()
            else:
                messages.error(request, 'Такого пользователя не существует')
    return render(request, 'recovery.html')

@login_required(login_url='login')
def chat(request, username):
    opponent = User.objects.get(username=username)
    dialogue_messages = Message.objects.filter(
        Q(sender=request.user, getter=opponent) |
        Q(sender=opponent, getter=request.user)
    )
    users = User.objects.all()
    count = len(users) - 1


    context = {
        'opponent': opponent,
        'dialogue_messages': dialogue_messages,
        'users': users,
        'inside': True,
        'counter': count
    }
    return render(request, 'chat.html', context)

@login_required(login_url='login')
def chat_template(request):
    context = {
        'users': User.objects.all(),
        'inside': False
    }
    return render(request, 'chat.html', context)


def send(request):
    body = request.POST.get('body')
    sender = request.POST.get('sender')
    getter = request.POST.get('getter')


    new_message = Message.objects.create(body=body, sender=sender, getter=getter)
    new_message.save()
    return HttpResponse('All good')

def get_messages(request, username):
    opponent = User.objects.get(username=username)
    dialogue_messages = Message.objects.filter(
        Q(sender=request.user.username, getter=opponent.username) |
        Q(sender=opponent.username, getter=request.user.username)
    )
    return JsonResponse({"messages": list(dialogue_messages.values())})

def profile(request, username):
    user = User.objects.get(username=username)
    user_profile = userProfile.objects.get(user=user)
    if request.method == 'POST':
        user_profile.avatar = request.POST.get('img')
        user_profile.save()
    context = {
        'user_profile': user_profile
    }
    return render(request, 'profile.html', context)

def edit_profile(request):
    return render(request, 'edit-profile.html')