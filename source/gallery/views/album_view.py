from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from gallery.forms import AlbumForm
from gallery.models.album import Album
from gallery.models.photo import Photo

class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'album/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user == self.object.author:
            album_photos = Photo.objects.filter(album=self.object).order_by('-created_at')
        else:
            album_photos = Photo.objects.filter(album=self.object, is_private=False).order_by('-created_at')
        context['album_photos'] = album_photos
        return context

class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'album/album_form.html'
    success_url = reverse_lazy('photo_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AlbumUpdateView(LoginRequiredMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'album/album_form.html'
    success_url = reverse_lazy('album_list')

    def form_valid(self, form):
        if form.instance.author != self.request.user:
            return HttpResponseForbidden("ERROR")
        if form.instance.is_private:
            form.instance.photos.update(is_private=False)
        return super().form_valid(form)


class AlbumDeleteView(LoginRequiredMixin, DeleteView):
    model = Album
    template_name = 'album/album_delete.html'
    success_url = reverse_lazy('album_list')

    def get_album(self, queryset=None):
        album = super().get_object(queryset)
        if album.author != self.request.user:
            return HttpResponseForbidden("ERROR")
        return album




        

