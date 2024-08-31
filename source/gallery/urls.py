from django.urls import path
from .views.photo_view import PhotoListView, PhotoDetailView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView, PhotoAccessView
from .views.album_view import AlbumDetailView, AlbumCreateView, AlbumUpdateView, AlbumDeleteView

urlpatterns = [
    path('photos/', PhotoListView.as_view(), name='photo_list'),
    path('photos/<int:pk>/', PhotoDetailView.as_view(), name='photo_detail'),
    path('photos/create/', PhotoCreateView.as_view(), name='photo_create'),
    path('photos/<int:pk>/edit/', PhotoUpdateView.as_view(), name='photo_edit'),
    path('photos/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),
    path('photos/access/<str:token>/', PhotoAccessView.as_view(), name='photo_access'),

    path('albums/<int:pk>/', AlbumDetailView.as_view(), name='album_detail'),
    path('albums/create/', AlbumCreateView.as_view(), name='album_create'),
    path('albums/<int:pk>/edit/', AlbumUpdateView.as_view(), name='album_edit'),
    path('albums/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album_delete'),
]
