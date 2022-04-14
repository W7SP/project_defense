from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.decorators.cache import cache_page

from final_project.accounts.models import Profile
from final_project.main.models import StudyBook


# Create New Book (requires Author's permissions)
class CreateBookView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = StudyBook
    fields = ('name', 'price', 'cover', 'description',)
    template_name = 'books/create_book.html'
    success_url = reverse_lazy('book shop')
    PERMISSION_REQUIRED = 'main.add_studybook'
    ERROR_MESSAGE = 'You must be an author to create a book!'

    def post(self, request, *args, **kwargs):
        return super().post(self, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.PERMISSION_REQUIRED):
            return HttpResponse(self.ERROR_MESSAGE)

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

    PERMISSION_REQUIRED = 'main.change_studybook'
    ERROR_MESSAGE = 'You must be an author to create a book!'

    def dispatch(self, request, *args, **kwargs):
        current_book = self.get_object()
        if not self.request.user.has_perm(self.PERMISSION_REQUIRED) or not current_book.author.id == self.request.user.id:
            return HttpResponse(self.ERROR_MESSAGE)

        return super(EditBookView, self).dispatch(request, *args, **kwargs)


# Delete Book View (requires Author's permissions)
class DeleteBookView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = StudyBook
    fields = ()
    template_name = 'books/delete_book.html'
    success_url = reverse_lazy("user's listings")

    PERMISSION_REQUIRED = 'main.delete_studybook'
    ERROR_MESSAGE = 'You must be an author to create a book!'

    def dispatch(self, request, *args, **kwargs):
        current_book = self.get_object()
        if not self.request.user.has_perm(self.PERMISSION_REQUIRED) or not current_book.author.id == self.request.user.id:
            return HttpResponse(self.ERROR_MESSAGE)

        return super(DeleteBookView, self).dispatch(request, *args, **kwargs)


# Show Book Shop items
# # Cache for 5 minutes
# @cache_page(5 * 60)
class BookShopView(views.ListView):
    model = StudyBook
    template_name = 'marketplace/books_shop.html'
    context_object_name = 'books'
    ordering = ['name']


# Buy Book
class BuyBookView(views.UpdateView):
    model = StudyBook
    fields = ()
    template_name = 'marketplace/buy_book.html'
    success_url = reverse_lazy('book shop')

    def post(self, request, *args, **kwargs):
        result = super().post(self, *args, **kwargs)
        book = self.object
        user = self.request.user.id
        profile = Profile.objects.get(user_id=user)
        if profile.account_balance >= book.price:
            profile.account_balance -= book.price
            profile.save()
            book.owners.add(profile)

            seller_id = book.author.id
            seller = Profile.objects.get(pk=seller_id)
            seller.account_balance += book.price
            seller.save()
        else:
            return HttpResponse('You can\'t afford to buy this book')

        return result

"""    # def get(self, *args, **kwargs):
    #     result = super().get(*args, **kwargs)
    #     book = self.object
    #     user = self.request.user.id
    #     profile = Profile.objects.get(user_id=user)
    #     if profile.account_balance >= book.price:
    #         profile.account_balance -= book.price
    #         profile.save()
    #         book.owners.add(profile)
    #     else:
    #         return HttpResponse('You can\'t afford to buy this book')
    #
    #     return result"""
