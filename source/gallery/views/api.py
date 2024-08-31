from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from gallery.models.photo import Photo
from gallery.models.album import Album
import json

def add_to_favorites(request):
    try:
        data = json.loads(request.body)
        item_type = data.get('item_type')
        item_id = data.get('item_id')
        print("Received data for adding to favorites:", item_type, item_id)

        if item_type == 'photo':
            photo = get_object_or_404(Photo, id=item_id)
            if photo not in request.user.profile.favorite_photos.all():
                request.user.profile.favorite_photos.add(photo)
                return JsonResponse({'status': 'added'})
            else:
                return JsonResponse({'error': 'Photo already in favorites'}, status=400)
        elif item_type == 'album':
            album = get_object_or_404(Album, id=item_id)
            if album not in request.user.profile.favorite_albums.all():
                request.user.profile.favorite_albums.add(album)
                return JsonResponse({'status': 'added'})
            else:
                return JsonResponse({'error': 'Album already in favorites'}, status=400)
        return JsonResponse({'error': 'Invalid item type'}, status=400)
    except Exception as e:
        print("Error processing request:", e)
        return JsonResponse({'error': 'Bad request'}, status=400)

def remove_from_favorites(request):
    try:
        data = json.loads(request.body)
        item_type = data.get('item_type')
        item_id = data.get('item_id')
        print("Received data for removing from favorites:", item_type, item_id)

        if item_type == 'photo':
            photo = get_object_or_404(Photo, id=item_id)
            if photo in request.user.profile.favorite_photos.all():
                request.user.profile.favorite_photos.remove(photo)
                return JsonResponse({'status': 'removed'})
            else:
                return JsonResponse({'error': 'Photo not in favorites'}, status=400)
        elif item_type == 'album':
            album = get_object_or_404(Album, id=item_id)
            if album in request.user.profile.favorite_albums.all():
                request.user.profile.favorite_albums.remove(album)
                return JsonResponse({'status': 'removed'})
            else:
                return JsonResponse({'error': 'Album not in favorites'}, status=400)
        return JsonResponse({'error': 'Invalid item type'}, status=400)
    except Exception as e:
        print("Error processing request:", e)
        return JsonResponse({'error': 'Bad request'}, status=400)
