from django.urls import path
from .views import posts, post_detail, add_post, edit_post, delete_post, send_email

app_name = 'blog'

urlpatterns = [
    path('', posts, name='posts'),
    path('post/<int:id>/', post_detail, name='post_detail'),

    path('add_post/', add_post, name='add_post'),
    path('edit/<int:id>/', edit_post, name='edit_post'),
    path('delete/<int:id>/', delete_post, name='delete_post'),
    path('send_email/', send_email, name='send_email'),
]

