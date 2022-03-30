from django.contrib.auth import mixins as auth_mixins
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from final_project.accounts.models import Profile
from final_project.main.models import Equipment, Post


# Create New Post
class CreatePostView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = Post
    fields = ('title', 'picture', 'description',)
    template_name = 'posts/create_post.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


# Edit Post View
class EditPostView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = Post
    fields = ('title', 'picture', 'description',)
    template_name = 'posts/edit_post.html'
    success_url = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user == self.object.creator:
            return HttpResponse('You must be the trainer to edit the equipment!')

        return super(EditPostView, self).dispatch(request, *args, **kwargs)


# Delete Post View
class DeletePostView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = Post
    fields = ()
    template_name = 'posts/delete_post.html'
    success_url = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user == self.object.creator:
            return HttpResponse('You must be the trainer to edit the equipment!')

        return super(DeletePostView, self).dispatch(request, *args, **kwargs)


# Show All Posts
class ShowPostsView(views.ListView):
    model = Post
    template_name = 'posts/all_posts.html'
    context_object_name = 'posts'


# Like Post
def like_post(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user
    if user in post.people_who_disliked:
        post.people_who_disliked.remove(user)
        post.people_who_liked.append(user)
        if post.dislikes >= 0:
            post.dislikes -= 1
        post.likes += 1
    elif user not in post.people_who_liked:
        post.people_who_liked.append(user)
        post.likes += 1

    elif user in post.people_who_liked:
        post.people_who_liked.remove(user)
        post.likes -= 1

    post.save()

    return redirect('show all posts')


# Dislike Post
def dislike_post(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user

    if user in post.people_who_liked:
        post.people_who_liked.remove(user)
        post.people_who_disliked.append(user)
        if post.likes >= 0:
            post.likes -= 1
        post.dislikes += 1

    elif user not in post.people_who_disliked:
        post.people_who_disliked.append(user)
        post.dislikes += 1

    elif user in post.people_who_disliked:
        post.people_who_disliked.remove(user)
        post.dislikes -= 1

    post.save()

    return redirect('show all posts')

