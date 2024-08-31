from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from gallery.forms import PhotoForm
from gallery.models.photo import Photo


class PhotoListView(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'
    context_object_name = 'photos'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Photo.objects.filter(is_private=False).union(
                Photo.objects.filter(author=self.request.user)
            ).order_by('-created_at')
        else:
            return Photo.objects.filter(is_private=False).order_by('-created_at')


class PhotoDetailView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'photo/photo_detail.html'
    context_object_name = 'photo_detail'


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photo/photo_form.html'
    success_url = reverse_lazy('photo_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.album and form.instance.album.author != self.request.user:
            return HttpResponseForbidden("ERROR")
        if form.instance.album and form.instance.album.is_private:
            form.instance.is_private = True
        return super().form_valid(form)


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photo/photo_form.html'
    success_url = reverse_lazy('photo_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if form.instance.author != self.request.user:
            return HttpResponseForbidden("ERROR")
        if form.instance.album and form.instance.album.is_private:
            form.instance.is_private = True
        return super().form_valid(form)

    def test_func(self):
        photo = self.get_object()
        return self.request.user == photo.author or self.request.user.has_perm('gallery.change_photo')


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo
    template_name = 'photo/photo_delete.html'
    success_url = reverse_lazy('photo_list')

    def test_func(self):
        photo = self.get_object()
        return self.request.user == photo.author or self.request.user.has_perm('gallery.delete_photo')
