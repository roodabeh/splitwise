from django.urls import path

from accounting.views import forgot_password, profile, logout_view, login_view, sign_up_view, check_code_validity, \
    edit_information, update_information, update_password, visit_other_user_profile, add_friend, delete_friend, list_of_friends,\
    visit_friend_profile

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
    path('update_information/', update_information, name='update_information'),
    path('list_of_friends/', list_of_friends, name='list_of_friends'),
    path('visit_other_user_profile/', visit_other_user_profile, name='visit_other_user_profile'),
    path('add_friend/<str:phone>/', add_friend, name='add_friend'),
    path('delete_friend/<str:phone>/', delete_friend, name='delete_friend'),
    path('visit_friend_profile/<str:phone>/', visit_friend_profile, name='check_friend'),
    path('', profile, name='profile'),
]
