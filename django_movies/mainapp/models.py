from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

import datetime


class Person(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        abstract = True


class Actor(Person):
    photo = models.ImageField(upload_to='actor_photos')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('about_actor', kwargs={'actor_slug': self.slug})

    def get_absolute_url_for_update(self):
        return reverse('update_actor', kwargs={'actor_slug': self.slug})

    def get_absolute_url_for_delete(self):
        return reverse('delete_actor', kwargs={'actor_slug': self.slug})

    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'


class Director(Person):
    photo = models.ImageField(upload_to='director_photos')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('about_director', kwargs={'director_slug': self.slug})

    def get_absolute_url_for_update(self):
        return reverse('update_director', kwargs={'director_slug': self.slug})

    def get_absolute_url_for_delete(self):
        return reverse('delete_director', kwargs={'director_slug': self.slug})

    class Meta:
        verbose_name = 'Director'
        verbose_name_plural = 'Directors'


class Genre(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Saga(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Saga'
        verbose_name_plural = 'Sagas'


class Movie(models.Model):
    title = models.CharField(max_length=150)
    tagline = models.CharField(blank=True, max_length=150)
    about = models.TextField(blank=True)
    year = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=150)
    world_premiere = models.DateField(default=datetime.date.today)
    poster = models.ImageField(upload_to='movie_posters')
    video = models.URLField(max_length=1000, default='https://hnembed.cc/embed/movie/imdb_movie_id')
    actors = models.ManyToManyField(Actor, related_name='movies')
    directors = models.ManyToManyField(Director, related_name='movies')
    genres = models.ManyToManyField(Genre, related_name='movies')
    saga = models.ForeignKey(Saga, on_delete=models.SET_NULL, null=True, blank=True, related_name='movies')
    budget = models.PositiveIntegerField(default=0, help_text='Budget in US dollars')
    fees = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('about_movie', kwargs={'movie_slug': self.slug})

    def get_absolute_url_for_update(self):
        return reverse('update_movie', kwargs={'movie_slug': self.slug})

    def get_absolute_url_for_delete(self):
        return reverse('delete_movie', kwargs={'movie_slug': self.slug})

    def add_comment_absolute_url(self):
        return reverse('add_comment', kwargs={'comment_id': self.pk, 'movie_slug': self.movie.slug})

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(validators=[
        MaxValueValidator(10),
        MinValueValidator(1),
    ])

    def __str__(self) -> str:
        return f'By {self.user} on {self.movie}: {self.score}'
    
    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments')

    def __str__(self):
        return f'Comment by {self.author} on {self.movie}: {self.text}'

    def get_absolute_url_for_update(self):
        return reverse('update_comment', kwargs={'comment_id': self.pk, 'movie_slug': self.movie.slug})

    def get_absolute_url_for_delete(self):
        return reverse('delete_comment', kwargs={'comment_id': self.pk, 'movie_slug': self.movie.slug})


TROUBLESHOOT_CHOICES = (
    ('no_error_category', 'Not selected'),
    ('page_load_error', 'The page does not load'),
    ('quality_error', 'Movie quality is bad'),
    ('account_error', 'Can\'t change account information'),
)


class Troubleshoot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='troubleshoots')
    category = models.CharField(choices=TROUBLESHOOT_CHOICES, default='no_error_category', max_length=150)
    description = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
