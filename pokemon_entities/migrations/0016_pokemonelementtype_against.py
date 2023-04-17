# Generated by Django 3.1.14 on 2023-04-17 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0015_pokemonelementtype_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonelementtype',
            name='against',
            field=models.ManyToManyField(related_name='beats', to='pokemon_entities.PokemonElementType', verbose_name='Силен против'),
        ),
    ]
