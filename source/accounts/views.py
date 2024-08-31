from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, View, DetailView
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import RegistrationForm
from gallery.models.album import Album
from gallery.models.photo import Photo
from accounts.models import Profile

User = get_user_model()

class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "accounts/registration.html"
    model = User
    success_url = reverse_lazy('photo_list')

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url:
            return next_url
        return reverse('photo_list')



class UserLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('photo_list')
        return render(request, 'accounts/login.html', {'form': form})



class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/user_profile.html'
    context_object_name = 'user_profile'

    def get(self, request, pk):
        user_profile = get_object_or_404(User, pk=pk)
        public_albums = Album.objects.filter(author=user_profile, is_private=False)
        public_photos = Photo.objects.filter(author=user_profile, is_private=False, album__isnull=True)

        context = {
            'user_profile': user_profile,
            'public_albums': public_albums,
            'public_photos': public_photos,
        }

        if request.user == user_profile:
            private_albums = Album.objects.filter(author=user_profile, is_private=True)
            private_photos = Photo.objects.filter(author=user_profile, is_private=True, album__isnull=True)
            favorite_albums = request.user.profile.favorite_albums.filter(is_private=False)
            favorite_photos = request.user.profile.favorite_photos.filter(is_private=False)

            context.update({
                'private_albums': private_albums,
                'private_photos': private_photos,
                'favorite_albums': favorite_albums,
                'favorite_photos': favorite_photos,
            })

        return render(request, 'accounts/user_profile.html', context)


class UserFavoritesView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        favorite_albums = profile.favorite_albums.filter(is_private=False)
        favorite_photos = profile.favorite_photos.filter(is_private=False)
        context = {
            'favorite_albums': favorite_albums,
            'favorite_photos': favorite_photos,
        }
        return render(request, 'accounts/user_favorites.html', context)
