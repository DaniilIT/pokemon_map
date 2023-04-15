from django.db import models  # noqa F401
from django.utils import timezone


class Pokemon(models.Model):
	title = models.CharField('Название', max_length=200)
	title_en = models.CharField('Название на английском', max_length=200, blank=True)
	title_jp = models.CharField('Название на японском', max_length=200, blank=True)
	description = models.TextField('Описание', blank=True)
	image = models.ImageField('Картинка', upload_to='pokemons', null=True, blank=True)
	previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL,
		related_name='next_evolutions', verbose_name='Произошли от', null=True, blank=True)

	class Meta:
		verbose_name = 'Вид покемона'
		verbose_name_plural = 'Виды покемонов'

	def __str__(self):
		return self.title


class PokemonEntity(models.Model):
	pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Вид покемона')
	lat = models.FloatField('Широта')
	lon = models.FloatField('Долгота')
	appeared_at = models.DateTimeField('Появится в', default=timezone.now)
	disappeared_at = models.DateTimeField('Исчезнет в', default=timezone.now)
	level = models.IntegerField('Уровень', default=1)
	health = models.IntegerField('Здоровье', null=True, blank=True)
	strength = models.IntegerField('Атака', null=True, blank=True)
	defence = models.IntegerField('Защита', null=True, blank=True)
	stamina = models.IntegerField('Выносливость', null=True, blank=True)

	class Meta:
		verbose_name = 'Покемон'
		verbose_name_plural = 'Покемоны'

	def __str__(self):
		return f'{self.pokemon.title}, level: {self.level}'
