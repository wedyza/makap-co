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
from .models import Message, userProfile, Portfolio
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.files.storage import FileSystemStorage

nameEncounter = 0
def home(request):
    if request.method == 'GET':
        fullname = request.GET.get('fullname')
        userprofile = userProfile.objects.filter(fullName=fullname)
        if (len(userprofile) > 0):
            user = userprofile[0].user
            return redirect('profile/' + user.username)
    profiles = userProfile.objects.all()
    context = {
        'profiles': profiles
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
        login(request, user)
        messages.success(request, 'Вы успешно завершили регистрацию, теперь, пожалуйста, заполните свой профиль')
        return redirect('edit-profile')
    else:
        return HttpResponse('Неправильная ссылка')


def registerPage(request):
    global nameEncounter
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            user_profile = userProfile.objects.create(user=user, fullName="ИмяПользователя" + str(nameEncounter))
            nameEncounter += 1
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
    user_profile = userProfile.objects.get(user=request.user)
    if request.method == 'POST' and 'text-data' in request.POST:
        cho = request.POST.get('edu-base')
        school = request.POST.get('school-inputs')
        contacts = request.POST.get('contacts-input')
        role = request.POST.get('role-input')
        skills = request.POST.get('skills-input')
        exp = request.POST.get('exp-input')
        user_profile.fullName = request.POST.get('user-name')
        user_profile.education = cho
        user_profile.edu_base = school
        user_profile.contacts = contacts
        user_profile.level = role
        user_profile.chars = skills
        user_profile.exp = exp
        user_profile.save()
        return redirect('edit-profile')
    elif request.method == 'POST' and 'image-data' in request.POST:
        image = request.FILES.get('avatar-input', False)
        file = request.FILES.get('resume-input', False)
        if image:
            user_profile.avatar = image
        if file:
            user_profile.resume = file
        user_profile.save()
        return redirect('edit-profile')
    else:
        return render(request, 'edit-profile.html', {'user_profile': user_profile})

def watch_portfolio(request, username):
    user = User.objects.get(username=username)
    portfolios = Portfolio.objects.filter(user=user)
    context = {
        'portfolios': portfolios
    }
    return render(request, 'portfolio.html', context)

def edit_portfolio(request):
    user = request.user
    if request.method == 'POST' and "id" in request.POST:
        image = request.FILES.get('image', False)
        description = request.POST.get('description')
        name = request.POST.get('name')
        link = request.POST.get('link')
        id = request.POST.get('id')

        print(request.FILES)
        new_portfolio = Portfolio.objects.get(user=user, id=id)
        if image:
            new_portfolio.image = image
        new_portfolio.description = description
        new_portfolio.name = name
        new_portfolio.link = link
        new_portfolio.save()
        return redirect('edit-portfolio')

    elif request.method == 'POST':
        image = request.FILES.get('image')
        description = request.POST.get('description')
        name = request.POST.get('name')
        link = request.POST.get('link')
        if image:
            new_portfolio = Portfolio.objects.create(user=user, link=link, name=name, image=image, description=description)
        else:
            new_portfolio = Portfolio.objects.create(user=user, link=link, name=name, description=description)
        print(request.POST)
        return redirect('edit-portfolio')



    portfolios = Portfolio.objects.filter(user=user)

    context = {
        'portfolios': portfolios,
        'length': len(portfolios)
    }
    return render(request, 'my-portfolio.html', context)

def about(request):
    return render(request, 'about.html')

def portfolios_list(request):
    userProfiles = userProfile.objects.all()
    portfolios = Portfolio.objects.all()

    context = {
        'projects' : portfolios,
        'profiles' : userProfiles
    }

    return render(request, 'portfolio-list.html', context)