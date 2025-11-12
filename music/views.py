from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render


from .models import Genre, Song


@login_required(login_url='/registration/login/')
def music(request):
    title = "Музыка"
    genres = Genre.objects.all()
    genre_id = request.GET.get('genre')
    query = request.GET.get('q')
    songs = Song.objects.all()
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
        'selected_genre': genre_id,
        'title': title
    })
