import random

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect

from accounting.forms import *


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
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.filter(username=request.POST['phone']).first()
            if user:
                if user.verified:
                    messages.error(request, 'کاربری با این شماره موجود است!')
                else:
                    return verify_phone(request, user)
            else:
                user = User.objects.create_user(
                    username=request.POST['phone'],
                    phone=request.POST['phone'],
                    email=request.POST['email'],
                    password=request.POST['password'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    address=request.POST['address']
                )

                # user = form.save()
                #
                # user.first_name = request.POST['first_name']
                # user.last_name = request.POST['last_name']
                # user.phone = request.POST['phone']
                # user.password = request.POST['password']
                # user.address = request.POST['address']
                # user.email = request.POST['email']
                #
                # user.save()
                # form.save_m2m()

                return verify_phone(request, user)
    else:
        form = UserForm()
    return render(request, 'sign_up.html', context={'form': form})


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
        return render(request, 'profile.html')
    return redirect('/login/')


def edit_information(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UserForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)

                request.user.avatar = user.avatar
                request.user.first_name = request.POST['first_name']
                request.user.last_name = request.POST['last_name']
                request.user.email = request.POST['email']
                request.user.email_verified = False

                request.user.save()
                form.save_m2m()

                return redirect('/profile/')
        else:
            form = UserForm()
        return render(request, 'edit_information.html', context={'form': form})
    else:
        return redirect('/login/')


def user_info(request):
    if request.user.is_authenticated:
        return render(request, 'user_info.html')
    return redirect('/login/')


def find_friend_view(request):
    if request.user.is_authenticated:
        return render(request, 'find_friend.html')
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


# ************************* Group *************************

def create_group(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ExpenseGroupForm(request.POST, request.FILES)
            if form.is_valid():
                person = request.user
                group = form.save(commit=False)

                group.name = request.POST['name']
                group.owner = request.user

                group.save()
                form.save_m2m()

                Membership.objects.create(person=person, group=group)
                print("create_group")
                print(Membership.objects.all())
                return redirect('/visit_group/{}'.format(group.id))
        else:
            form = ExpenseGroupForm()
        return render(request, 'group/create_group.html', context={'form': form})
    else:
        return redirect('/login/')


def visit_group(request, group_id):
    if request.user.is_authenticated:
        group = ExpenseGroup.objects.get(pk=group_id)
        for member in group.members.all():
            member.debt = 0
            member.save()
        expenses = Expense.objects.filter(group=group_id)
        print(expenses)
        member_debts = {}
        my_debt = 0
        for expense in expenses:
            if expense.spender.username == request.user.username:
                debts = Debt.objects.filter(expense=expense)
                for debt in debts:
                    print(debt.share, debt.person.first_name)
                    if debt.share > 0:
                        print(member_debts.keys(),debt.person.username)
                        member_debts[debt.person.username] = member_debts.get(debt.person.username,0) + expense.cost*debt.share
            else:
                debts = Debt.objects.filter(expense=expense, person=request.user)
                for debt in debts:
                    my_debt += expense.cost*debt.share

        member = group.members.all().filter(username=request.user.username)[0]
        member.debt = my_debt
        member.save()
        for member_debt in member_debts.keys():
            print(member_debt,member_debts[member_debt])
            member = group.members.all().filter(username=member_debt)[0]
            member.debt = member_debts[member_debt]
            member.save()

        context = {
            'group_id': group_id,
            'owner_id': group.owner.id,
            'is_owner': group.owner.id == request.user.id,
            'members': group.members.all(),
            'expenses': expenses,
        }

        return render(request, 'group/visit_group.html', context=context)
    else:
        return redirect('/login/')


def add_member(request, group_id):
    if request.user.is_authenticated:
        group = ExpenseGroup.objects.get(pk=group_id)
        if request.method == 'POST':
            if request.user.id == group.owner.id:
                other_user = find_user_by_phone_num(request.POST['phone'])
                if other_user:
                    Membership.objects.create(person=other_user, group=group)
                else:
                    messages.error(request, 'کاربر مورد نظر موجود نیست!')
        return redirect('/visit_group/{}'.format(group.id))
    else:
        return redirect('/login/')


def del_member(request, group_id):
    if request.user.is_authenticated:
        group = ExpenseGroup.objects.get(pk=group_id)
        if request.method == 'POST':
            if request.user.id == group.owner.id:
                other_user = find_user_by_phone_num(request.POST['submit'])
                if other_user:
                    Membership.objects.filter(person=other_user, group=group).delete()
        return redirect('/visit_group/{}'.format(group.id))
    else:
        return redirect('/login/')


def delete_group(request, group_id):
    if request.user.is_authenticated:
        group = ExpenseGroup.objects.get(pk=group_id)
        if request.method == 'POST':
            if request.user.id == group.owner.id:
                group.members.clear()
                group.delete()
                return redirect('/list_of_groups/')
        return redirect('/visit_group/{}'.format(group.id))
    else:
        return redirect('/login/')


def list_of_groups(request):
    if request.user.is_authenticated:
        groups = []
        for membership in Membership.objects.filter(person=request.user):
            # group = membership.group
            # group.members.clear()
            # group.delete()
            groups.append(membership.group)
        content = {
            'groups': groups
        }
        return render(request, 'group/groups_list.html', context=content)
    return redirect('/login/')


# ************************* Expense *************************

def add_expense(request, group_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(group_id)
            group = ExpenseGroup.objects.get(pk=group_id)
            print(group.members.all())
            context = {
                'group_id': group_id,
                'members': group.members.all(),
            }
            return render(request, 'group/add_expense.html', context=context)
        return redirect('/visit_group/{}'.format(group_id))
    else:
        return redirect('/login/')


def confirm_expense(request, group_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            group = ExpenseGroup.objects.get(pk=group_id)
            expense = Expense.objects.create(group=group, cost=request.POST["cost"], spender=request.user)
            shares = []
            for member in group.members.all():
                shares.append(int(request.POST["share_" + member.username]))
            print(shares, sum(shares))
            i = 0
            for member in group.members.all():
                if member.username != request.user.username:
                    Debt.objects.create(expense=expense, share=shares[i] / sum(shares), person=member)
                else:
                    Debt.objects.create(expense=expense, share=(shares[i] - sum(shares)) / sum(shares), person=member)
                i += 1
        return redirect('/visit_group/{}'.format(group_id))
    else:
        return redirect('/login/')

def checkout_expense(request, group_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(group_id)
            group = ExpenseGroup.objects.get(pk=group_id)
            for member in group.members.all():
                member.debt = 0
                member.save()
            print(group.members.all())
            expenses = Expense.objects.filter(group=group_id)
            member_debts = {}
            for expense in expenses:
                if expense.spender.username != request.user.username:
                    debts = Debt.objects.filter(expense=expense, person=request.user)
                    print("debtsdebts",debts)
                    for debt in debts:
                        member_debts[expense.spender.username] = member_debts.get(expense.spender.username,0) + expense.cost*debt.share

            for member_debt in member_debts.keys():
                print(member_debt,member_debts[member_debt])
                member = group.members.all().filter(username=member_debt)[0]
                member.debt = member_debts[member_debt]
                member.save()

            context = {
                'group_id': group_id,
                'members': group.members.all(),
            }
            return render(request, 'group/checkout_expense.html', context=context)
        return redirect('/visit_group/{}'.format(group_id))
    else:
        return redirect('/login/')

def confirm_checkout_expense(request, group_id, user_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            group = ExpenseGroup.objects.get(pk=group_id)
            for member in group.members.all():
                member.debt = 0
                member.save()

            expenses = Expense.objects.filter(group=group_id)
            for expense in expenses:
                print(expense.spender.id,user_id)
                if expense.spender.id == int(user_id):
                    print("hereee")
                    debts = Debt.objects.filter(expense=expense, person=request.user)
                    for debt in debts:
                        PastCheckouts.objects.create(cost=expense.cost*debt.share, payer=request.user, reciever= expense.spender)
                        debt.delete()
                print("PastCheckouts",PastCheckouts.objects.get(pk=group_id))

            context = {
                'group_id': group_id,
                'members': group.members.all(),
            }

            return render(request, 'group/checkout_expense.html', context=context)
        else:
            return redirect('/visit_group/{}'.format(group_id))
    else:
        return redirect('/login/')

