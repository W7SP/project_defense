from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy
from django.views import generic as views

from final_project.accounts.models import Profile
from final_project.main.forms import ContactForm


class RedirectToIndexView(views.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        success_url = reverse_lazy('index')
        return success_url


# Show Home Page View
class HomeView(views.TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        try:
            profile = Profile.objects.get(pk=current_user.id)
            context['profile'] = profile.first_name
        except:
            pass
        context['show_only_register_and_login'] = True
        return context


# Show About Us Page
class AboutUsView(views.TemplateView):
    template_name = 'main/about_us.html'


# CONTACT VIEW
def contact_us_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email_receiver = 'petko.adm@gmail.com'
            cd = form.cleaned_data
            subject = cd['subject']
            message = cd['message']

            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email_receiver])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("index")

    form = ContactForm()
    return render(request, "main/contact_us.html", {'form': form})
