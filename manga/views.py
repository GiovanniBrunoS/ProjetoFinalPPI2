from django.shortcuts import render, get_object_or_404, redirect
from zipfile import ZipFile
from PIL import Image
import base64, os, logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from .models import Manga, MangaChapter, MangaPage, Author, Artist
from .forms import MangaForm, ChapterForm, AuthorForm, ArtistForm

logger = logging.getLogger('__name__')

def author_list(request):
    author_list = Author.objects.order_by('name')
    return render(request, 'manga/author_list.html', {'author_list': author_list})

@login_required
def author_new(request):
    if request.method == "POST":
         form = AuthorForm(request.POST)
         if form.is_valid():
             author = form.save(commit=False)
             author.save()
             logger.info("Autor criado com sucesso")
             messages.success(request,"Autor criado com sucesso")
             return redirect('author_list')
    else:
        form = AuthorForm()
    return render(request, 'manga/author_edit.html', {'form': form})

@login_required
def author_edit(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
         form = AuthorForm(request.POST, instance=author)
         if form.is_valid():
             author = form.save(commit=False)
             author.save()
             logger.info("Autor editado com sucesso")
             messages.success(request,"Autor editado com sucesso")
             return redirect('author_list')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'manga/author_edit.html', {'form': form})

@login_required
def author_remove(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if(request.user.is_staff):
        author.delete()
        messages.warning(request,"Autor removido com sucesso")
    else:
        logger.error("Usuario não autorizado tentando fazer remoção de autor")
    return redirect('author_list')

def artist_list(request):
    artist_list = Artist.objects.order_by('name')
    return render(request, 'manga/artist_list.html', {'artist_list': artist_list})

@login_required
def artist_new(request):
    if request.method == "POST":
         form = ArtistForm(request.POST)
         if form.is_valid():
             artist = form.save(commit=False)
             artist.save()
             logger.info("Artista criado com sucesso")
             messages.success(request,"Artista criado com sucesso")
             return redirect('artist_list')
    else:
        form = ArtistForm()
    return render(request, 'manga/artist_edit.html', {'form': form})

@login_required
def artist_edit(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    if request.method == "POST":
         form = ArtistForm(request.POS, instance=artist)
         if form.is_valid():
             artist = form.save(commit=False)
             artist.save()
             logger.info("Artista editado com sucesso")
             messages.success(request,"Artista editado com sucesso")
             return redirect('artist_list')
    else:
        form = ArtistForm(instance=artist)
    return render(request, 'manga/artist_edit.html', {'form': form})

@login_required
def artist_remove(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    if(request.user.is_staff):
        artist.delete()
        messages.warning(request,"Artista removido com sucesso")
    else:
        logger.error("Usuario não autorizado tentando fazer remoção de artista")
    return redirect('artist_list')

def manga_list(request):
    manga_list = Manga.objects.order_by('title')
    return render(request, 'manga/manga_list.html', {'manga_list': manga_list})

def manga_detail(request, pk):
    manga = get_object_or_404(Manga, pk=pk)
    chapters = MangaChapter.objects.filter(manga=manga)
        
    return render(request, 'manga/manga_detail.html', {'manga': manga, 'chapters':chapters})

@login_required
def manga_new(request):
     if request.method == "POST":
         form = MangaForm(request.POST)
         if form.is_valid():
             manga = form.save(commit=False)
             manga.save()
             logger.info("Manga criado com sucesso")
             messages.success(request,"Manga criado com sucesso")
             return redirect('manga_detail', pk=manga.pk)
     else:
         form = MangaForm()
     return render(request, 'manga/manga_edit.html', {'form': form})

@login_required
def manga_edit(request, pk):
     manga = get_object_or_404(Manga, pk=pk)
     if request.method == "POST":
         form = MangaForm(request.POST, instance=manga)
         if form.is_valid():
             manga = form.save(commit=False)
             manga.save()
             logger.info("Manga editado com sucesso")
             messages.success(request, "Manga editado com sucesso")
             return redirect('manga_detail', pk=manga.pk)
     else:
         form = MangaForm(instance=manga)
     return render(request, 'manga/manga_edit.html', {'form': form})

@login_required
def manga_remove(request, pk):
    manga = get_object_or_404(Manga, pk=pk)
    if(request.user.is_staff):
        manga.delete()
        messages.warning(request,"Manga removido com sucesso")
    else:
        logger.error("Usuario não autorizado tentando fazer remoção de manga")
    return redirect('manga_list')

@login_required
def chapter_new(request, pk):
    manga = get_object_or_404(Manga, pk=pk)
    if request.method == "POST":
        form = ChapterForm(request.POST, request.FILES)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.manga = manga
            chapter.save()
            logger.info("Capitulo criado com sucesso")
            messages.success(request, "Manga criado com sucesso")
            return redirect('manga_detail', pk=manga.pk)
    else:
        form = ChapterForm()
    return render(request, 'manga/chapter_new.html', {'form': form})

def reader(request, mangapk, chapterpk):
    chapter = get_object_or_404(MangaChapter, pk=chapterpk)
    pages = MangaPage.objects.filter(manga_chapter=chapter).order_by('page_number')

    return render(request, 'manga/reader.html', {'pages': pages, 'chapter': chapter})
