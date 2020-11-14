from django.urls import path
from .views import (index,
                    other_page,
                    BBLoginView,
                    BBLogoutView,
                    profile,
                    ChangeUserinfoView,
                    BBPasswordChageView,
                    RegisterDoneView,
                    RegisterUserVuew,
                    user_activate,
                    DeleteUserView,
                    BBPasswordResetView,
                    BBPasswordResetDoneView,
                    BBPasswordResetConfirmView,
                    BBPasswordResetCompleteView,
                    by_rubric,
                    detail,
                    profile_bb_detail,
                    profile_bb_add,
                    profile_bb_change,
                    profile_bb_delete,
                    comment_change,
                    comment_delete,
)




app_name = 'main'
urlpatterns = [
    path('accounts/password_reset/', BBPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', BBPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>', BBPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', BBPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserVuew.as_view(), name='register'),
    path('accounts/comments/comment_change/<int:pk>/', comment_change, name='comment_change'),
    path('accounts/comments/comment_delete/<int:pk>/', comment_delete, name='comment_delete'),
    path('accounts/profile/change/', ChangeUserinfoView.as_view(), name='profile_change'),
    path('accounts/profile/change/<int:pk>/', profile_bb_change, name='profile_bb_change'),
    path('accounts/profile/delete/<int:pk>/', profile_bb_delete, name='profile_bb_delete'),
    path('accounts/profile/add/', profile_bb_add, name='profile_bb_add'),
    path('accounts/profile/<int:pk>/', profile_bb_detail, name='profile_bb_detail'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', BBPasswordChageView.as_view(), name='password_change'),
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),

]

