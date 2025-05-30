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

from .models import Post, Comment
from .forms import Handcraftform, CommentForm


class Handcrafts(ListView):
    """
    View all handcrafts
    """
    template_name = 'handcrafts/handcrafts.html'
    model = Post
    context_object_name = 'handcrafts'

    def get_queryset(self):
        return Post.objects.filter(status=1).order_by('-created_on')


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
        comments = Comment.objects.filter(
            post=handcraft, approved=True).order_by('created_on')
        context['comments'] = comments
        context['comment_form'] = CommentForm()
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
