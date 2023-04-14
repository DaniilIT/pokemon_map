import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime


from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    local_time = localtime()
    pokemons_entity = PokemonEntity.objects.filter(appeared_at__lte=local_time, disappeared_at__gt=local_time)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entity:
        pokemon = pokemon_entity.pokemon
        if pokemon.image:
            add_pokemon(
                folium_map,
                pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon.image.url)
            )
        else:
            add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon)

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url) if pokemon.image else None,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        current_pokemon = Pokemon.objects.get(id=pokemon_id)
        requested_pokemon = {
            'title': 'title',
            'title_ru': current_pokemon.title,
            'title_en': current_pokemon.title_en,
            'title_jp': current_pokemon.title_jp,
            'description': current_pokemon.description,
            'img_url': current_pokemon.image.url if current_pokemon.image else None,
            'next_evolution': {
                'pokemon_id': 'pokemon_id',
                'img_url': 'img_url',
                'title_ru': 'title_ru',
            },
            # 'element_type': 'element_type',
        }
        if previous_evolution := current_pokemon.previous_evolution:
            requested_pokemon['previous_evolution'] = {
                'pokemon_id': previous_evolution.id,
                'img_url': previous_evolution.image.url if previous_evolution.image else None,
                'title_ru': previous_evolution.title,
            }
    except PokemonEntity.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    local_time = localtime()
    pokemons_entity = PokemonEntity.objects.filter(
        pokemon__id=pokemon_id,
        appeared_at__lte=local_time,
        disappeared_at__gt=local_time
    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entity:
        pokemon = pokemon_entity.pokemon
        if pokemon.image:
            add_pokemon(
                folium_map,
                pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon.image.url)
            )
        else:
            add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon)

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': requested_pokemon
    })
