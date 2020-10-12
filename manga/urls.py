from django.urls import path
from . import views

urlpatterns = [
    path('', views.manga_list, name='manga_list'),
    path('<int:pk>/', views.manga_detail, name='manga_detail'),
    path('new-manga/', views.manga_new, name='manga_new'),
    path('<int:pk>/edit/', views.manga_edit, name='manga_edit'),
    path('<int:pk>/remove/', views.manga_remove, name='manga_remove'),
    path('<int:pk>/new_chapter/', views.chapter_new, name='chapter_new'),
    path('<int:mangapk>/<int:chapterpk>', views.reader, name='reader'),
    path('new-author/', views.author_new , name='author_new'),
    path('author/<int:pk>/', views.author_edit , name='author_edit'),
    path('author/remove/<int:pk>/', views.author_remove , name='author_remove'),
    path('author/list/', views.author_list , name='author_list'),
    path('new-artist/', views.artist_new, name='artist_new'),
    path('artist/<int:pk>/', views.artist_edit, name='artist_edit'),
    path('artist/remove/<int:pk>/', views.artist_remove , name='artist_remove'),
    path('artist/list/', views.artist_list , name='artist_list'),
]