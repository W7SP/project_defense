from django.contrib.auth import mixins as auth_mixins
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic as views
from final_project.accounts.models import Profile
from final_project.main.models import Courses
from final_project.main.views.generic_views import RedirectToIndexView


# Create New Course (requires Trainer's permissions)
class CreateCourseView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = Courses
    fields = ('name', 'price', 'description', 'duration', 'picture', 'link_to_platform',)
    template_name = 'courses/create_course.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm('main.add_courses'):
            return HttpResponse('You must be a trainer to create new courses!')

        return super(CreateCourseView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.coach = self.request.user
        return super().form_valid(form)


# Edit Course View (requires Author's permissions)
class EditCourseView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = Courses
    fields = ('name', 'price', 'description', 'picture', 'duration',)
    template_name = 'courses/edit_course.html'
    success_url = reverse_lazy("user's listings")

    def dispatch(self, request, *args, **kwargs):
        current_course = self.get_object()
        if not self.request.user.has_perm('main.change_courses') or not current_course.coach.id == self.request.user.id:
            return HttpResponse('You must be the trainer to edit the course!')

        return super(EditCourseView, self).dispatch(request, *args, **kwargs)


# Delete Course View (requires Trainer's permissions)
class DeleteCourseView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = Courses
    fields = ()
    template_name = 'courses/delete_course.html'
    success_url = reverse_lazy("user's listings")

    def dispatch(self, request, *args, **kwargs):
        current_course = self.get_object()
        if not self.request.user.has_perm('main.delete_courses') or not current_course.coach.id == self.request.user.id:
            return HttpResponse('You must be the trainer to delete the course!')

        return super(DeleteCourseView, self).dispatch(request, *args, **kwargs)


# Show Course Shop items
class CoursesShopView(views.ListView):
    model = Courses
    template_name = 'marketplace/courses_shop.html'
    context_object_name = 'courses'


# Buy Course
class BuyCourseView(views.UpdateView):
    model = Courses
    fields = ()
    template_name = 'marketplace/buy_course.html'
    success_url = reverse_lazy('index')

    def get(self, *args, **kwargs):
        result = super().get(*args, **kwargs)
        course = self.object
        user = self.request.user.id
        profile = Profile.objects.get(user_id=user)
        if profile.account_balance >= course.price:
            profile.account_balance -= course.price
            profile.save()
            course.participants.add(profile)
        else:
            return HttpResponse('u poor')

        return result
