from django.db import migrations


def forwards(apps, schema_editor):
    from apps.images import convert_existing_images
    # Eski png/jpg fayllar faqat migratsiya muvaffaqiyatli commit bo'lgandan keyin o'chiriladi
    convert_existing_images(apps, delete_originals=True)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('blog', '0002_alter_blog_content'),
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
