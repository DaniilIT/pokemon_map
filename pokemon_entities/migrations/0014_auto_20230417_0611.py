# Generated by Django 3.1.14 on 2023-04-17 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0013_auto_20230415_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='PokemonElementType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Стихия',
                'verbose_name_plural': 'Стихии',
            },
        ),
        migrations.AddField(
            model_name='pokemon',
            name='element_type',
            field=models.ManyToManyField(related_name='pokemos', to='pokemon_entities.PokemonElementType', verbose_name='Стихии'),
        ),
    ]
