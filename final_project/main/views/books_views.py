from django.contrib.auth import mixins as auth_mixins
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic as views
from final_project.accounts.models import Profile
from final_project.main.models import StudyBook


# Create New Book (requires Author's permissions)
class CreateBookView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = StudyBook
    fields = ('name', 'price', 'description',)
    template_name = 'books/create_book.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm('main.add_studybook'):
            return HttpResponse('You must be an author to create a book!')

        return super(CreateBookView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Edit Book View (requires Author's permissions)
class EditBookView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = StudyBook
    fields = ('name', 'price', 'description',)
    template_name = 'books/edit_book.html'
    success_url = reverse_lazy("user's listings")

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm('main.change_studybook'):
            return HttpResponse('You must be the author to edit the book!')

        return super(EditBookView, self).dispatch(request, *args, **kwargs)


# Delete Book View (requires Author's permissions)
class DeleteBookView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = StudyBook
    fields = ()
    template_name = 'books/delete_book.html'
    success_url = reverse_lazy("user's listings")

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm('main.delete_studybook'):
            return HttpResponse('You must be the author to delete the book!')

        return super(DeleteBookView, self).dispatch(request, *args, **kwargs)


# Show Book Shop items
class BookShopView(views.ListView):
    model = StudyBook
    template_name = 'marketplace/books_shop.html'
    context_object_name = 'books'


# Buy Book
class BuyBookView(views.UpdateView):
    model = StudyBook
    fields = ()
    template_name = 'marketplace/buy_book.html'
    success_url = reverse_lazy('index')

    def get(self, *args, **kwargs):
        result = super().get(*args, **kwargs)
        book = self.object
        user = self.request.user.id
        profile = Profile.objects.get(user_id=user)
        if profile.account_balance >= book.price:
            profile.account_balance -= book.price
            profile.save()
            book.owners.add(profile)
        else:
            return HttpResponse('u poor')

        return result
