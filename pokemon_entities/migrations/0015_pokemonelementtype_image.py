# Generated by Django 3.1.14 on 2023-04-17 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0014_auto_20230417_0611'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonelementtype',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='elements', verbose_name='Картинка'),
        ),
    ]