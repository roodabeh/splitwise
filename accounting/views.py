import random

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect

from accounting.models import User, Friendship


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است!')
    return render(request, 'login.html')


def check_code_validity(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.POST['phone'])
        # if str(user.verification_code) == request.POST['code']:
        #     login(request, user)
        #     if user.verified:
        #         return render(request, 'update_password.html')
        #     else:
        #         user.verified = True
        #         user.save()
        #         return redirect('/')
        # else:
        #     messages.error(request, 'کد اشتباه است!')
        #     return render(request, 'check_code_validity.html', context={
        #         'phone': request.POST['phone'],
        #     })
        login(request, user)
        if user.verified:
            return render(request, 'update_password.html')
        else:
            user.verified = True
            user.save()
            return redirect('/')
    return redirect('/')


def verify_phone(request, user):
    user.verification_code = random.randint(1001, 10000)
    # user.save()
    # r = requests.get(
    #     'x=کد تایید شما: ' +
    #     str(user.verification_code) + '&to=' +
    #     user.phone + '&lineNo=0'
    # )
    # print(r.text)
    return render(request, 'check_code_validity.html', context={
        'phone': request.POST['phone'],
    })


def sign_up_view(request):
    if request.method == 'POST':
        user = User.objects.filter(username=request.POST['phone']).first()
        if user:
            if user.verified:
                messages.error(request, 'کاربری با این شماره موجود است!')
                return render(request, 'sign_up.html')
            else:
                return verify_phone(request, user)
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['phone']
            password = request.POST['password']
            address = request.POST['address']
            email = request.POST['email']
            user = User.objects.create_user(
                username=username,
                phone=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                address=address
            )
            return verify_phone(request, user)
    return render(request, 'sign_up.html')


def forgot_password(request):
    if request.method == 'POST':
        user = User.objects.filter(username=request.POST['phone']).first()
        if user:
            if user.verified:
                return verify_phone(request, user)
            else:
                messages.error(request, 'فرایند ثبت‌نام تکمیل نشده است!')
                return render(request, 'sign_up.html')
        else:
            messages.error(request, 'کاربری با این شماره موجود نیست!')
            return render(request, 'forgot_password.html')
    return render(request, 'forgot_password.html')


def update_password(request):
    if request.method == 'POST' and request.user.is_authenticated:
        request.user.set_password(request.POST['password'])
        request.user.save()
        return redirect('/')
    return redirect('/forgot_password/')


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'user_profile.html')
    return redirect('/login/')


def edit_information(request):
    if request.user.is_authenticated:
        return render(request, 'edit_information.html')
    return redirect('/login/')


def update_information(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.email = request.POST.get('email')
            request.user.email_verified = False
            request.user.save()
        return redirect('/profile/')
    return redirect('/login/')


def logout_view(request):
    logout(request)
    return redirect('/')


def find_user_by_phone_num(phone_num):
    try:
        return User.objects.get(username=phone_num)
    except:
        return None


def visit_other_user_profile(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.method == 'POST':
        other_user = find_user_by_phone_num(request.POST.get('other_phone'))
        if other_user:
            content = {
                'other_first_name': other_user.first_name,
                'other_last_name': other_user.last_name,
                'other_phone': other_user.phone,
                'is_friend': is_friend(request.user, other_user)
            }
            return render(request, 'other_user_profile.html', context=content)
        else:
            messages.error(request, 'شماره‌ی مورد نظر موجود نیست!')
            return redirect('/profile/')


def is_friend(user1, user2):
    if Friendship.objects.filter(user=user1, friend=user2).count() == 0:
        return False
    return True


def refresh_other_user_profile(request, friend, friendship_state):
    content = {
        'other_first_name': friend.first_name,
        'other_last_name': friend.last_name,
        'other_phone': friend.phone,
        'is_friend': friendship_state
    }
    return render(request, 'other_user_profile.html', context=content)


def add_friend(request, phone):
    user1 = request.user
    user2 = find_user_by_phone_num(phone)
    Friendship.objects.create(user=user1, friend=user2)
    print("add friend")
    print(Friendship.objects.all())
    return refresh_other_user_profile(request, user2, True)


def delete_friend(request, phone):
    user1 = request.user
    user2 = find_user_by_phone_num(phone)
    Friendship.objects.filter(user=user1, friend=user2).delete()
    print("delete friend")
    print(Friendship.objects.all())
    return refresh_other_user_profile(request, user2, False)


def list_of_friends(request):
    if request.user.is_authenticated:
        friends = []
        for friendship in Friendship.objects.filter(user=request.user):
            friends.append(
                (friendship.friend.first_name,
                 friendship.friend.last_name,
                 friendship.friend.phone)
            )
        print(friends)
        content = {
            'friends': friends
        }
        return render(request, 'friends_list.html', context=content)
    return redirect('/login/')


def visit_friend_profile(request, phone):
    if request.user.is_authenticated:
        if request.method == 'POST':
            other_user = find_user_by_phone_num(phone)
            if other_user:
                print("hi")
                content = {
                    'other_first_name': other_user.first_name,
                    'other_last_name': other_user.last_name,
                    'other_phone': other_user.phone,
                    'is_friend': is_friend(request.user, other_user)
                }
                return render(request, 'other_user_profile.html', context=content)
            else:
                messages.error(request, 'شماره‌ی مورد نظر موجود نیست!')
                # TODO: ask TA
                return redirect('/profile/')
    return redirect('/login/')
