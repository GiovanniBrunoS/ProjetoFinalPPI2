from django.contrib import admin
from .models import Author, Artist, Manga, MangaChapter, MangaPage

admin.site.register(Author)
admin.site.register(Artist)
admin.site.register(Manga)
admin.site.register(MangaChapter)
admin.site.register(MangaPage)