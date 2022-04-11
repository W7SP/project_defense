from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import redirect

from final_project.accounts.forms import UserRegistrationForm
from django.contrib.auth import views as auth_views
from django.views import generic as views
from django.contrib.auth import login
from django.urls import reverse_lazy
from final_project.accounts.models import AppUser, Profile
from final_project.main.models import Courses, Equipment, StudyBook


# Register and login automatically with email
class UserRegistrationView(views.CreateView):
    form_class = UserRegistrationForm
    template_name = 'auth_accounts/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        # user => self.object
        # request => self.request
        login(self.request, self.object)
        return result


# Login
class UserLoginView(auth_views.LoginView):
    template_name = 'auth_accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('index')


# Logout
class UserLogoutView(auth_views.LogoutView):
    def get_next_page(self):
        return reverse_lazy('index')


# Delete User
class DeleteUserView(LoginRequiredMixin, views.DeleteView):
    model = AppUser
    template_name = 'auth_accounts/delete_user.html'
    success_url = reverse_lazy('index')


# Edit User Profile Info
class EditUserView(LoginRequiredMixin, views.UpdateView):
    model = Profile
    fields = ('first_name', 'last_name', 'picture', 'date_of_birth', 'gender',)
    template_name = 'auth_accounts/edit_user.html'
    success_url = reverse_lazy('index')


# View Profile Info and Details
class ProfileDetailsView(LoginRequiredMixin, views.DetailView):
    model = Profile
    template_name = 'accounts_info/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        job = 'user'
        if self.request.user.is_superuser:
            job = 'Site Admin'
        elif self.request.user.has_perm('main.add_studybook'):
            job = 'Author'
        elif self.request.user.has_perm('main.add_course'):
            job = 'Coach'
        elif self.request.user.has_perm('main.add_equipment'):
            job = 'Trainer'

        context.update({
            'job': job,
        })

        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.id == kwargs['pk']:
            return redirect('index')

        return super(ProfileDetailsView, self).dispatch(request, *args, **kwargs)


# Show all courses that the User has bought
class UsersCoursesView(LoginRequiredMixin, views.ListView):
    model = Courses
    template_name = 'accounts_info/user_courses.html'
    context_object_name = 'courses'

    def get_queryset(self):
        user_id = self.request.user.id
        courses = list(Courses.objects.filter(participants=user_id))
        return courses


# Show all products that the User has bought
class UsersProductsView(LoginRequiredMixin, views.ListView):
    model = Equipment
    template_name = 'accounts_info/user_products.html'
    context_object_name = 'equipments'

    def get_queryset(self):
        user_id = self.request.user.id

        equipments = list(Equipment.objects.filter(owners=user_id))
        return equipments

    def get_context_data(self, **kwargs):
        user_id = self.request.user.id
        context = super(UsersProductsView, self).get_context_data(**kwargs)
        context.update({
            'books': list(StudyBook.objects.filter(owners=user_id))
        })
        return context


# Show user's bought products of the market
class UsersListingsView(LoginRequiredMixin, views.ListView):
    model = Equipment
    template_name = 'accounts_info/user_listings.html'
    context_object_name = 'equipments'

    def get_context_data(self, **kwargs):
        user_id = self.request.user.id
        context = super(UsersListingsView, self).get_context_data(**kwargs)
        context.update({
            'books': list(StudyBook.objects.filter(author=user_id)),
            'courses': list(Courses.objects.filter(coach=user_id)),
            'equipments': list(Equipment.objects.filter(seller=user_id)),
        })
        return context

    def get_queryset(self):
        user_id = self.request.user.id

        equipments = list(Equipment.objects.filter(owners=user_id))
        return equipments


# Change User Password
class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("index")
    template_name = "auth_accounts/password_change.html"


