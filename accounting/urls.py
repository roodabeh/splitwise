from django.urls import path

from accounting.views import *

urlpatterns = [
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('update_password/', update_password, name='update_password'),
    path('login/', login_view, name='login'),
    path('sign_up/', sign_up_view, name='sign_up'),
    path('signup/', sign_up_view, name='signup'),
    path('check_code_validity/', check_code_validity, name='check_code_validity'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('edit_information/', edit_information, name='edit_information'),
    path('user_info/', user_info, name='user_info'),
    path('list_of_friends/', list_of_friends, name='list_of_friends'),
    path('visit_other_user_profile/', visit_other_user_profile, name='visit_other_user_profile'),
    path('add_friend/<str:phone>/', add_friend, name='add_friend'),
    path('delete_friend/<str:phone>/', delete_friend, name='delete_friend'),
    path('visit_friend_profile/<str:phone>/', visit_friend_profile, name='check_friend'),
    path('find_friend/', find_friend_view, name='find_friend'),

    # ************************* Group *************************
    path('create_group/', create_group, name='create_group'),
    path('visit_group/<str:group_id>/', visit_group, name='visit_group'),
    path('add_member/<str:group_id>/', add_member, name='add_member'),
    path('del_member/<str:group_id>/', del_member, name='del_member'),
    path('delete_group/<str:group_id>/', delete_group, name='delete_group'),
    path('list_of_groups/', list_of_groups, name='list_of_groups'),

    # ************************* Expense *************************
    path('add_expense/<str:group_id>/', add_expense, name='add_expense'),
    path('confirm_expense/<str:group_id>/', confirm_expense, name='confirm_expense'),
    path('checkout_expense/<str:group_id>/', checkout_expense, name='checkout_expense'),
    path('confirm_checkout_expense/<str:group_id>/<str:user_id>/', confirm_checkout_expense, name='confirm_checkout_expense'),

    path('', profile, name='profile'),
]
