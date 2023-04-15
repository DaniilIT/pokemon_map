import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
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
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=local_time,
        disappeared_at__gt=local_time
    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        pokemon = pokemon_entity.pokemon
        image_url = request.build_absolute_uri(pokemon.image.url) if pokemon.image \
            else DEFAULT_IMAGE_URL
        add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon, image_url)

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
    current_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    requested_pokemon = {
        'title_ru': current_pokemon.title,
        'title_en': current_pokemon.title_en,
        'title_jp': current_pokemon.title_jp,
        'description': current_pokemon.description,
        'img_url': current_pokemon.image.url if current_pokemon.image else None,
    }
    if previous_evolution := current_pokemon.previous_evolution:
        requested_pokemon['previous_evolution'] = {
            'pokemon_id': previous_evolution.id,
            'img_url': previous_evolution.image.url if previous_evolution.image else None,
            'title_ru': previous_evolution.title,
        }
    if next_evolution := current_pokemon.next_evolutions.first():
        requested_pokemon['next_evolution'] = {
            'pokemon_id': next_evolution.id,
            'img_url': next_evolution.image.url if next_evolution.image else None,
            'title_ru': next_evolution.title,
        }

    local_time = localtime()
    pokemon_entities = current_pokemon.pokemon_entities.filter(
        appeared_at__lte=local_time,
        disappeared_at__gt=local_time
    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        pokemon = pokemon_entity.pokemon
        image_url = request.build_absolute_uri(pokemon.image.url) if pokemon.image \
            else DEFAULT_IMAGE_URL
        add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon, image_url)

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': requested_pokemon
    })
