"""
Rasmlarni WebP formatiga o'tkazish uchun umumiy yordamchilar.

- Admin orqali yuklangan har qanday rasm (ImageField) saqlanishidan oldin WebP ga o'tkaziladi.
- CKEditor orqali blog matniga yuklangan rasmlar ham WebPFileSystemStorage orqali WebP bo'ladi.
- Mavjud rasmlar `convert_images_to_webp` management command / data migration orqali o'tkaziladi.
"""
import logging
import os
import re
from io import BytesIO
from urllib.parse import unquote, urlparse

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.db.models.signals import pre_save
from PIL import Image, ImageOps

logger = logging.getLogger('apps.images')

WEBP_QUALITY = 82
MAX_DIMENSION = 2000  # px — kattaroq rasmlar shu o'lchamga kichraytiriladi

RASTER_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.webp', '.avif', '.heic', '.ico'}


def webp_name(name):
    """'blog/images/photo.PNG' -> 'blog/images/photo.webp'"""
    return f'{os.path.splitext(name)[0]}.webp'


def is_webp(name):
    return os.path.splitext(name or '')[1].lower() == '.webp'


def is_raster_image(name):
    return os.path.splitext(name or '')[1].lower() in RASTER_EXTENSIONS


def image_to_webp_bytes(fp):
    """Fayl obyektidagi rasmni WebP bytes ga o'tkazadi (EXIF orientatsiya, resize, animatsiya hisobga olinadi)."""
    with Image.open(fp) as img:
        if getattr(img, 'is_animated', False):
            buffer = BytesIO()
            img.save(buffer, format='WEBP', save_all=True, quality=WEBP_QUALITY, method=6)
            return buffer.getvalue()

        img = ImageOps.exif_transpose(img)
        if img.mode not in ('RGB', 'RGBA'):
            has_alpha = img.mode in ('LA', 'PA') or (img.mode == 'P' and 'transparency' in img.info)
            img = img.convert('RGBA' if has_alpha else 'RGB')

        img.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.Resampling.LANCZOS)

        buffer = BytesIO()
        img.save(buffer, format='WEBP', quality=WEBP_QUALITY, method=6)
        return buffer.getvalue()


def _convert_on_save(sender, instance, field_names, **kwargs):
    for field_name in field_names:
        file = getattr(instance, field_name)
        # _committed=False — fayl yangi yuklangan, hali storage ga yozilmagan
        if not file or getattr(file, '_committed', True) or is_webp(file.name):
            continue
        try:
            file.seek(0)
            data = image_to_webp_bytes(file)
        except Exception:
            logger.exception('WebP ga o\'tkazib bo\'lmadi: %s', file.name)
            continue
        name = webp_name(os.path.basename(file.name))
        # save=False — model saqlanishi davom etadi, FileField.pre_save faylni storage ga yozadi
        file.save(name, ContentFile(data), save=False)


def register_webp_fields(model, *field_names):
    """Model ImageField larini saqlashda avtomatik WebP ga o'tkazishni yoqadi."""
    def handler(sender, instance, **kwargs):
        _convert_on_save(sender, instance, field_names, **kwargs)

    pre_save.connect(handler, sender=model, weak=False, dispatch_uid=f'webp_{model._meta.label}')


class WebPFileSystemStorage(FileSystemStorage):
    """CKEditor yuklagan rasmlarni WebP qilib, CKEDITOR_5_UPLOAD_PATH papkasiga saqlaydigan storage."""

    def save(self, name, content, max_length=None):
        name = name or content.name
        upload_path = getattr(settings, 'CKEDITOR_5_UPLOAD_PATH', '')
        if upload_path and not os.path.dirname(name):
            name = os.path.join(upload_path, name)
        if is_raster_image(name) and not is_webp(name):
            try:
                content.seek(0)
                content = ContentFile(image_to_webp_bytes(content))
                name = webp_name(name)
            except Exception:
                logger.exception('CKEditor rasmini WebP ga o\'tkazib bo\'lmadi: %s', name)
                content.seek(0)
        return super().save(name, content, max_length=max_length)


# ── Mavjud rasmlarni o'tkazish ────────────────────────────────────────────────

# (app_label, model_name, field_name)
IMAGE_FIELDS = [
    ('core', 'MainInfo', 'photo'),
    ('core', 'Career', 'logo'),
    ('blog', 'BlogImage', 'photo'),
    ('portfolio', 'ProjectImage', 'photo'),
]

IMG_SRC_RE = re.compile(r'(<img\b[^>]*?\bsrc=["\'])([^"\']+)(["\'])', re.IGNORECASE)


def _convert_stored_file(name, storage=default_storage):
    """Storage dagi faylni WebP ga o'tkazib, yangi nomini qaytaradi (o'tkazilmasa None)."""
    if not name or is_webp(name) or not is_raster_image(name) or not storage.exists(name):
        return None
    with storage.open(name, 'rb') as f:
        data = image_to_webp_bytes(f)
    return storage.save(webp_name(name), ContentFile(data))


def _media_name_from_url(url):
    """'/media/x.png' yoki 'https://api.i37.uz/media/x.png' -> 'x.png'"""
    path = unquote(urlparse(url).path)
    if not path.startswith(settings.MEDIA_URL):
        return None
    return path[len(settings.MEDIA_URL):]


def convert_existing_images(apps_registry, delete_originals=False, log=print):
    """
    Bazadagi barcha ImageField rasmlarini va Blog.content ichidagi CKEditor rasmlarini WebP ga o'tkazadi.
    Idempotent: allaqachon .webp bo'lganlar o'tkazib yuboriladi.
    `apps_registry` — django.apps.apps yoki migratsiyadagi `apps`.
    """
    originals = []
    converted = 0

    for app_label, model_name, field_name in IMAGE_FIELDS:
        model = apps_registry.get_model(app_label, model_name)
        for obj in model.objects.exclude(**{field_name: ''}).iterator():
            old_name = getattr(obj, field_name).name
            try:
                new_name = _convert_stored_file(old_name)
            except Exception as exc:
                log(f'  ! {model_name}#{obj.pk} {old_name}: {exc}')
                continue
            if new_name:
                model.objects.filter(pk=obj.pk).update(**{field_name: new_name})
                originals.append(old_name)
                converted += 1
                log(f'  {old_name} -> {new_name}')

    # CKEditor orqali blog matniga qo'yilgan rasmlar
    Blog = apps_registry.get_model('blog', 'Blog')
    url_cache = {}
    for blog in Blog.objects.filter(content__icontains='<img').iterator():
        def replace(match):
            url = match.group(2)
            if url not in url_cache:
                url_cache[url] = None
                old_name = _media_name_from_url(url)
                try:
                    new_name = _convert_stored_file(old_name)
                except Exception as exc:
                    log(f'  ! Blog#{blog.pk} {old_name}: {exc}')
                    new_name = None
                if new_name:
                    originals.append(old_name)
                    log(f'  {old_name} -> {new_name}')
                    # host (agar bo'lsa) saqlanadi, faqat path almashadi
                    url_cache[url] = urlparse(url)._replace(path=default_storage.url(new_name)).geturl()
            new_url = url_cache[url]
            return f'{match.group(1)}{new_url}{match.group(3)}' if new_url else match.group(0)

        new_content = IMG_SRC_RE.sub(replace, blog.content)
        if new_content != blog.content:
            Blog.objects.filter(pk=blog.pk).update(content=new_content)
            converted += 1

    if delete_originals and originals:
        # Faqat DB tranzaksiyasi muvaffaqiyatli commit bo'lgandan keyin o'chiriladi
        transaction.on_commit(lambda: [default_storage.delete(name) for name in originals])

    return converted, originals
