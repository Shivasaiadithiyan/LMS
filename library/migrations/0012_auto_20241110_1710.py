# Generated by Django 3.0.5 on 2024-11-10 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_pendingfine'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issuedbook',
            name='enrollment',
        ),
        migrations.RemoveField(
            model_name='issuedbook',
            name='isbn',
        ),
        migrations.AddField(
            model_name='issuedbook',
            name='book',
            field=models.ForeignKey(default=223131, on_delete=django.db.models.deletion.CASCADE, to='library.Book'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='issuedbook',
            name='student',
            field=models.ForeignKey(default=21414142, on_delete=django.db.models.deletion.CASCADE, to='library.StudentExtra'),
            preserve_default=False,
        ),
    ]
