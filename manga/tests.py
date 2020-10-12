from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import CustomUser
from .models import Author, Artist, Manga, MangaChapter, MangaPage

def create_user(name):
    UserModel = get_user_model()
    if not UserModel.objects.filter(username=name).exists():
        user = UserModel.objects.create_user(name, password='!@SDRDsada55')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

def create_autor(name):
    if not Author.objects.filter(name=name).exists():
        author = Author.objects.create(name=name)
        author.save()
        return author

def create_artist(name):
    if not Artist.objects.filter(name=name).exists():
        artist = Artist.objects.create(name=name)
        artist.save()
        return artist

def create_manga(author, artist, title):
    if not Manga.objects.filter(title=title).exists():
        manga = Manga.objects.create(author=author, artist=artist, title=title, description='Lorem Ipsum')
        manga.save()
        return manga

def create_manga_chapter(manga):
    if not MangaChapter.objects.filter(manga=manga).exists():
        manga_chapter = MangaChapter.objects.create(manga=manga, chapter_number=1, title='Test Chapter', created_date='2020-10-12',language='PT')
        manga_chapter.save()
        return manga_chapter

class AuthorTestCase(TestCase):

    def setUp(self):
        author = create_autor('Kubo Tite')
    
    def test_author(self):
        author = Author.objects.get(name='Kubo Tite')
        self.assertNotEqual(str(author),'Shiraishi Akira')


class ArtistTestCase(TestCase):

    def setUp(self):
        artist = create_artist('Kubo Tite')
    
    def test_artist(self):
        artist = Artist.objects.get(name='Kubo Tite')
        self.assertEqual(str(artist),'Kubo Tite')


class MangaTestCase(TestCase):

    def setUp(self):
        author = create_autor('Kubo Tite')
        artist = create_artist('Kubo Tite')
        manga = create_manga(author, artist, 'Test Manga')

    def test_manga(self):
        manga = Manga.objects.get(title='Test Manga')
        self.assertEqual(str(manga), 'Test Manga')
        self.assertEqual(str(manga.author), 'Kubo Tite')
        self.assertEqual(str(manga.artist), 'Kubo Tite')


class MangaChapterTestCase(TestCase):

    def setUp(self):
        author = create_autor('Kubo Tite')
        artist = create_artist('Kubo Tite')
        manga = create_manga(author, artist, 'Test Manga')
        manga_chapter = create_manga_chapter(manga)

    def test_manga(self):
        manga = Manga.objects.get(title='Test Manga')
        manga_chapter = MangaChapter.objects.get(manga=manga)
        self.assertEqual(str(manga_chapter.manga), 'Test Manga')
        self.assertEqual(manga_chapter.chapter_number, 1)
        self.assertEqual(str(manga_chapter.title), 'Test Chapter')
        self.assertEqual(str(manga_chapter.language), 'PT')


