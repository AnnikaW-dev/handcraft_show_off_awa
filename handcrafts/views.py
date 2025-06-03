from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    CreateView, ListView,
    DetailView, DeleteView,
    UpdateView
    )
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    )
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count

from .models import Post, Comment, Favorite, HANDCRAFT_TYPES
from .forms import Handcraftform, CommentForm


class Handcrafts(ListView):
    """
    View all handcrafts
    """
    template_name = 'handcrafts/handcrafts.html'
    model = Post
    context_object_name = 'handcrafts'


    def get_queryset(self):
        queryset = Post.objects.filter(status=1)

        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(handcraft_type=category)

        # Sorting
        sort = self.request.GET.get('sort', 'created_on')
        direction = self.request.GET.get('direction', 'desc')

        # Whiteliist fields allowed for sorting
        valid_sort_fields = ['title', 'created_on']
        if sort not in valid_sort_fields:
            sort = 'created_on'

        if direction == 'desc':
            sort =f'-{sort}'

        return queryset.order_by(sort)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Favorites
        if self.request.user.is_authenticated:
            favorit_ids = Favorite.objects.filter(
                user=self.request.user).values_list(
                    'post_id', flat=True)
            context['user_favorites'] = list(favorit_ids)
        else:
            context['user_favorites'] = []

        # Pass current filters

        context['current_category'] = self.request.GET.get('category', '')
        context['current_sort'] = self.request.GET.get('sort', 'created_on')
        context['current_direction'] = self.request.GET.get('direction', 'desc')

        # Category counted for sidebar /filter
        context['handcraft_types'] = HANDCRAFT_TYPES

        return context

class HandcraftDetail(DetailView):

    """
    View a single Post
    """
    template_name = 'handcrafts/handcraft_detail.html'
    model = Post
    context_object_name = 'handcraft'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        handcraft = self.get_object()
        user = self.request.user
        comments = Comment.objects.filter(
            post=handcraft, approved=True).order_by('created_on')
        context['comments'] = comments
        context['comment_form'] = CommentForm()


        # Favoritstatus
        if user.is_authenticated:
            context['is_favorite'] = Favorite.objects.filter(user=user, post=handcraft).exists()
        else:
            context['is_favorite'] = False

        return context



    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been submitted and awaiting approval') # noqa
            return redirect('handcraft_detail', slug=self.object.slug)

        # If form is not valid, re-render the page with form errors
        context = self.get_context_data(**kwargs)
        context['comment_form'] = comment_form
        return self.render_to_response(context)



class AddHandcraft(LoginRequiredMixin, CreateView):
    """
    Add handcraft view
    """
    template_name = 'handcrafts/add_handcraft.html'
    model = Post
    form_class = Handcraftform
    success_url = '/handcrafts/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AddHandcraft, self).form_valid(form)


class EditHandcraft(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Edit a Handcraft post
    """
    model = Post
    template_name = 'handcrafts/edit_handcraft.html'
    form_class = Handcraftform
    success_url = '/handcrafts/'

    def test_func(self):
        return self.request.user == self.get_object().author


class DeleteHandcraft(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a Handcraft post
    """
    model = Post
    success_url = '/handcrafts/'

    def test_func(self):
        return self.request.user == self.get_object().author

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author == request.user:
        comment.delete()
        messages.success(request,"Comment deleted.")
    else: messages.error(request, 'You dont have premisson to delete this comment.')
    return redirect('handcraft_detail', slug=comment.post.slug)

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        messages.success(request, "You dont have premission to edit this comment.")
        return redirect('handcraft_detail', slug=comment.post.slug)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated")
            return redirect('handcraft_detail', slug=comment.post.slug)

    else:
        form = CommentForm(instance=comment)

    return render(request, 'handcrafts/edit_comment.html', {'form':form})

@login_required
def toggle_favorite(request, slug):
    post = get_object_or_404(Post, slug=slug)
    favorite, created = Favorite.objects.get_or_create(user=request.user, post=post)

    if not created:
        favorite.delete()
        messages.info(request, "Removed from favorites")
    else:
        messages.success(request, "Added to favorites")

    return redirect(request.META.get('HTTP_REFERER', 'handcrafts'))

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('post')
    return render(request, 'handcrafts/favorite_list.html', {
        'favorites': favorites,
        'user_favorites': [fav.post.id for fav in favorites],
        })
