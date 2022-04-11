from django.urls import path

from final_project.accounts.views import UserRegistrationView, UserLoginView, UserLogoutView, DeleteUserView, \
    EditUserView, ChangePasswordView, ProfileDetailsView, UsersCoursesView, UsersProductsView, UsersListingsView
from final_project.main.views.post_views import ShowUserPostsView

urlpatterns = (
    path('register/', UserRegistrationView.as_view(), name='register user'),
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),

    path('user/edit/<int:pk>', EditUserView.as_view(), name='edit user'),
    path('user/delete/<int:pk>/', DeleteUserView.as_view(), name='delete user'),
    path('user/password/change/<int:pk>/', ChangePasswordView.as_view(), name='change password'),

    path('profile/details/<int:pk>', ProfileDetailsView.as_view(), name='profile details'),
    path('user/courses/', UsersCoursesView.as_view(), name='user\'s courses'),
    path('user/products/', UsersProductsView.as_view(), name='user\'s products'),
    path('user/listings/', UsersListingsView.as_view(), name='user\'s listings'),
    path('user/posts/', ShowUserPostsView.as_view(), name='user\'s posts'),

)
