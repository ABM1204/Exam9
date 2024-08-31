from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
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
    context_object_name = 'photo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo = self.get_object()
        if self.request.user == photo.author:
            if photo.token:
                context['access_link'] = self.request.build_absolute_uri(f'/photos/access/{photo.token}/')
            else:
                context['can_generate_link'] = True
        return context

    def post(self, request, *args, **kwargs):
        photo = self.get_object()
        if request.user == photo.author and not photo.token:
            photo.generate_token()
        return self.get(request, *args, **kwargs)


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


class PhotoAccessView(DetailView):
    model = Photo
    template_name = 'photo/photo_detail.html'
    context_object_name = 'photo'

    def get_object(self, queryset=None):
        token = self.kwargs.get('token')
        return get_object_or_404(Photo, token=token)
