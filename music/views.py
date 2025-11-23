from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.http import JsonResponse

from .models import Genre, Song, Album, Artist, Vote

@login_required(login_url='/registration/login/')
def music(request):
    title = "Музыка"
    genres = Genre.objects.all()
    genre_id = request.GET.get('genre')
    query = request.GET.get('q')
    songs = Song.objects.all()
    albums = Album.objects.all()
    artists = Artist.objects.all()
    if genre_id:
        songs = songs.filter(genre_id=genre_id)
    if query:
        # songs = songs.filter(
        #     Q(title__icontains=query) |
        #     Q(artist__name__icontains=query)
        # )

        songs = Song.objects.filter(
            Q(title__icontains=query) |  # — поиск по названию песни.
            Q(artist__name__icontains=query) |  # — поиск по имени исполнителя.
            Q(album__title__icontains=query) |  # — поиск по названию альбома.
            Q(genre__name__icontains=query)  # — поиск по жанру.
        ).distinct()  # distinct(), чтобы избежать дублирования результатов

    return render(request, 'music.html', {
        'songs': songs,
        'genres': genres,
        'albums': albums,
        'artists': artists,
        'selected_genre': genre_id,
        'title': title
    })

@login_required(login_url='/registration/login/')
def artist_songs_view(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    songs = Song.objects.filter(artist=artist)
    number_of_songs = songs.count()  # Уже имеем queryset песен, считаем их сразу

    context = {
        'artist': artist,
        'songs': songs,
        'number_of_songs': number_of_songs,
    }
    
    return render(request, 'artist_songs.html', context)





@login_required(login_url='/registration/login/')
def toggle_vote(request, model_type, object_id, vote_type):
    """
    Обрабатывает AJAX-запрос для голосования.
    Определяет, является ли это лайком или дизлайком и создает или обновляет соответствующую запись.
    """
    if request.method == 'POST':
        # Получаем объект (песню или альбом)
        obj = None
        if model_type == 'song':
            obj = get_object_or_404(Song, pk=object_id)
        elif model_type == 'album':
            obj = get_object_or_404(Album, pk=object_id)

        # Проверяем, существует ли уже голосование
        try:
            existing_vote = Vote.objects.get(
                user=request.user,
                song=obj if isinstance(obj, Song) else None,
                album=obj if isinstance(obj, Album) else None
            )

            # Если уже есть голосование, проверяем, отличается ли тип
            if existing_vote.vote_type != vote_type:
                existing_vote.vote_type = vote_type
                existing_vote.save()
            else:
                # Удаляем голос, если пользователь повторяет тот же выбор
                existing_vote.delete()

        except Vote.DoesNotExist:
            # Создаем новое голосование
            new_vote = Vote(
                song=obj if isinstance(obj, Song) else None,
                album=obj if isinstance(obj, Album) else None,
                user=request.user,
                vote_type=vote_type
            )
            new_vote.save()

        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)