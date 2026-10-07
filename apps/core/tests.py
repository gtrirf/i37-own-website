import shutil
import tempfile
from io import BytesIO

from django.apps import apps
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from apps.blog.models import Blog
from apps.core.models import Career
from apps.images import WebPFileSystemStorage, convert_existing_images

TEMP_MEDIA = tempfile.mkdtemp()


def make_image(fmt='PNG', size=(3000, 1500), mode='RGBA'):
    buffer = BytesIO()
    Image.new(mode, size, (200, 30, 30, 128) if mode == 'RGBA' else (200, 30, 30)).save(buffer, format=fmt)
    return buffer.getvalue()


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class WebPConversionTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)

    def test_upload_is_saved_as_webp_and_resized(self):
        career = Career.objects.create(name='X', logo=SimpleUploadedFile('logo.png', make_image()))
        self.assertTrue(career.logo.name.startswith('career/logos/logo'))
        self.assertTrue(career.logo.name.endswith('.webp'))
        with Image.open(career.logo.path) as img:
            self.assertEqual(img.format, 'WEBP')
            self.assertEqual(max(img.size), 2000)
            self.assertEqual(img.mode, 'RGBA')

    def test_unchanged_webp_field_is_not_reconverted(self):
        career = Career.objects.create(name='X', logo=SimpleUploadedFile('a.jpg', make_image('JPEG', mode='RGB')))
        name = career.logo.name
        career.name = 'Y'
        career.save()
        self.assertEqual(career.logo.name, name)

    def test_existing_images_and_blog_content_are_converted(self):
        old_logo = default_storage.save('career/logos/old.jpg', ContentFile(make_image('JPEG', mode='RGB')))
        career = Career.objects.create(name='X', logo=SimpleUploadedFile('tmp.webp', b''))
        Career.objects.filter(pk=career.pk).update(logo=old_logo)  # signal chetlab o'tiladi

        old_inline = default_storage.save('blog/content_uploads/inline.png', ContentFile(make_image()))
        blog = Blog.objects.create(
            title='T',
            content=f'<p>a</p><img src="https://api.i37.uz/media/{old_inline}" alt="x"><img src="https://other.com/a.png">',
        )

        with self.captureOnCommitCallbacks(execute=True):
            convert_existing_images(apps, delete_originals=True, log=lambda *a: None)

        career.refresh_from_db()
        blog.refresh_from_db()
        self.assertTrue(career.logo.name.endswith('.webp'))
        self.assertTrue(default_storage.exists(career.logo.name))
        self.assertIn('src="https://api.i37.uz/media/blog/content_uploads/inline.webp"', blog.content)
        self.assertIn('src="https://other.com/a.png"', blog.content)
        self.assertFalse(default_storage.exists(old_logo))
        self.assertFalse(default_storage.exists(old_inline))

        # ikkinchi marta ishlatish hech narsani o'zgartirmaydi
        converted, originals = convert_existing_images(apps, log=lambda *a: None)
        self.assertEqual((converted, originals), (0, []))

    def test_ckeditor_storage_saves_webp_in_upload_path(self):
        name = WebPFileSystemStorage().save('photo.jpeg', ContentFile(make_image('JPEG', mode='RGB'), name='photo.jpeg'))
        self.assertEqual(name, 'blog/content_uploads/photo.webp')
