# Generated by Django 4.0.2 on 2022-09-27 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_userviewtimestamp_user_product_unique_constraint'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('position',), 'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='position',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
