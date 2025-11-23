from django.urls import path
from .views import music, artist_songs_view, toggle_vote

app_name = 'music'

urlpatterns = [
    path('', music, name='music'),
    path('artist/<int:artist_id>/songs/', artist_songs_view, name='artist_songs_view'),

    # path('toggle_vote/', toggle_vote, name='toggle_vote'),  # Назначение маршрута
    path('toggle_vote/<str:model_type>/<int:object_id>/<str:vote_type>/', toggle_vote, name='toggle_vote'),

]
