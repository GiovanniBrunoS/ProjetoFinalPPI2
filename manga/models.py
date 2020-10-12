import os, logging, re
from django.conf import settings
from django.db import models
from django.utils import timezone
from zipfile import ZipFile
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.dispatch import receiver

from .validators import validate_file_extension, validate_image_extension

logger = logging.getLogger('__name__')


def get_manga_path(instance, filename):
    return "manga/%s/%s/%s/%s" % (str(instance.manga.pk),instance.language, instance.chapter_number, filename)

class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Manga(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class MangaChapter(models.Model):
    ENGLISH = 'EN'
    PORTUGUESE = 'PT'
    PORTUGUESE_PT = 'PT-pt'
    SPANISH = 'ES'
    LANGUAGES = [
        ('EN', 'en-us'),
        ('PT', 'pt-br'),
        ('PT-pt', 'pt-pt'),
        ('ES', 'es-es')
    ]
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    chapter_number = models.DecimalField(max_digits=6 ,decimal_places=1)
    title = models.CharField(max_length=200)
    language = models.CharField(max_length=5, choices=LANGUAGES)
    created_date = models.DateTimeField(auto_now=True)
    chapter = models.FileField(blank=True, validators=[validate_file_extension], upload_to=get_manga_path)

    def __str__(self):
        return '{} - {} {}'.format(self.manga.title, self.chapter_number, self.title)

    def save(self, *args, **kwargs):
        super(MangaChapter, self).save(*args, **kwargs)
        if self.chapter:
            zip_file = ZipFile(self.chapter)
            for name in zip_file.namelist():
                data = zip_file.read(name)
                try:
                    from PIL import Image
                    image = Image.open(BytesIO(data))
                    image.load()
                    image = Image.open(BytesIO(data))
                    image.verify()
                except ImportError:
                    logger.error("Erro na extração de imagem")
                    pass
                except:
                    continue
                number = os.path.split(name)[1]
                number = number.split(".")[0]
                number = re.sub("[^0-9]", "", number)
                name = os.path.split(name)[1]
                path = "manga/%s/%s/%s/%s" % (str(self.manga.pk), self.language, self.chapter_number, name)
                saved_path = default_storage.save(path, ContentFile(data))
                mp = MangaPage(manga_chapter=self, page_number=number, page=saved_path)
                mp.save()
            zip_file.close()
            self.chapter.delete()


class MangaPage(models.Model):
    manga_chapter = models.ForeignKey(MangaChapter, on_delete=models.CASCADE)
    page_number = models.IntegerField()
    page = models.ImageField(validators=[validate_image_extension])

    def __str__(self):
        return '{} - page {}'.format(self.manga_chapter.title, self.page_number)

    def delete(self):
        if self.page:
            self.page.delete()
        super(MangaPage, self).delete()


def _delete_file(path):
   if os.path.isfile(path):
       os.remove(path)

@receiver(models.signals.post_delete, sender=MangaPage)
def delete_page_file(sender, instance, *args, **kwargs):
    if instance.page:
        _delete_file(instance.page.path)
