from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from gallery.forms import PhotoForm
from gallery.models.photo import Photo


class PhotoListView(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'
    context_object_name = 'photo_list'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Photo.objects.filter(is_private=False) | Photo.objects.filter(author=self.request.user)
        else:
            return Photo.objects.filter(is_private=False)


class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photo/photo_detail.html'
    context_object_name = 'photo_detail'


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photo/photo_form.html'
    success_url = reverse_lazy('photo_list')

    def get_form_kwargs(self):
        kwrgs = super().get_form_kwargs()
        kwrgs['user'] = self.request.user
        return kwrgs

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.album and form.instance.album.author != self.request.user:
            return HttpResponseForbidden("ERROR")
        if form.instance.album and form.instance.album.is_private:
            form.instance.is_private = True
        return super().form_valid(form)


class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photo/photo_form.html'
    success_url = reverse_lazy('photo_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if form.instanse.author != self.request.user:
            return HttpResponseForbidden("ERROR")
        if form.instance.author and form.instance.album.is_private:
            form.instance.is_private = True
        return super().form_valid(form)


class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = 'photo/photo_delete.html'
    success_url = reverse_lazy('photo_list')
    def get_photo(self, queryset=None):
        photo = super().get_object(queryset=queryset)
        if photo.author != self.request.user:
            return HttpResponseForbidden("ERROR")
        return photo





        