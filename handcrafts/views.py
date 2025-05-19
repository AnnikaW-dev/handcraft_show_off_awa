from django.views.generic import (
    CreateView, ListView,
    DetailView, DeleteView,
    UpdateView
    )
from .models import Post
from .forms import Handcraftform

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    )

# Create your views here.


class Handcrafts(ListView):
    """
    View all recipes
    """
    template_name = 'handcrafts/handcrafts.html'
    model = Post
    context_object_name = 'handcrafts'

    def get_queryset(self):
        return Post.objects.filter(status=1).order_by('-created_on')


class HandcraftDetail(DetailView):

    """
    View a singel Post
    """
    template_name = 'handcrafts/handcraft_detail.html'
    model = Post
    context_object_name = 'handcraft'


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
    success_url = '/handcrafts'

    def test_func(self):
        return self.request.user == self.get_object().author
