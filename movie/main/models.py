from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Profile(AbstractUser):
    age = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(18), MaxValueValidator(100)],
    )
    phone_number = models.CharField(max_length=15, blank=True)
    STATUS_USER = (
        ("pro", "PRO"),
        ("simple", "SIMPLE"),
    )
    status = models.CharField(choices=STATUS_USER, default="simple", max_length=15)

    def __str__(self):
        return self.username


class Country(models.Model):
    country_name = models.CharField(max_length=100)

    def __str__(self):
        return self.country_name


class Director(models.Model):
    director_name = models.CharField(max_length=100)
    bio = models.TextField()
    age = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to="director_photo/", blank=True, null=True)

    def __str__(self):
        return self.director_name


class Actor(models.Model):
    actor_name = models.CharField(max_length=100)
    bio = models.TextField()
    age = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to="actor_photo/", blank=True, null=True)

    def __str__(self):
        return self.actor_name


class Janre(models.Model):
    janre_name = models.CharField(max_length=100)

    def __str__(self):
        return self.janre_name


class TypeMovie(models.Model):
    key = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label


class Movie(models.Model):
    movie_name = models.CharField(max_length=100)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name="directors")  
    actor = models.ManyToManyField(Actor, related_name="actors")  
    year = models.PositiveIntegerField(default=0)
    country = models.ManyToManyField(Country, related_name="countries")  
    janre = models.ManyToManyField(Janre, related_name="janres")  
    description = models.TextField()
    types = models.ManyToManyField(TypeMovie, related_name="types")  
    movie_time = models.PositiveIntegerField(default=0)
    movie_trailer = models.FileField(upload_to="movie_trailer/", blank=True, null=True)
    movie_image = models.ImageField(upload_to="movie_image/", blank=True, null=True)
    STATUS_MOVIE = (
        ("pro", "PRO"),
        ("simple", "SIMPLE"),
    )
    status_movie = models.CharField(
        choices=STATUS_MOVIE, default="simple", max_length=15
    )

    def __str__(self):
        return self.movie_name


class MovieLanguages(models.Model):
    language = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="languages")  
    video = models.FileField(upload_to="movie_video/", blank=True, null=True)

    def __str__(self):
        return self.language


class Moments(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="moments") 
    moments = models.ImageField(upload_to="moments/")


class Rating(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="user_ratings")  
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="rating_movie")
    stars = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        verbose_name="Рейтинг",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.movie} - {self.user} - {self.stars} stars"



class Review(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField()
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    parent_review = models.ForeignKey('self', related_name='replies', null=True, blank=True,
                                      on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.movie}'

class Favorite(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="favorites")  
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"


class FavoriteMovie(models.Model):
    cart = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name="carts")   
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="favorited_by") 

    def __str__(self):
        return f"{self.cart} - {self.movie}"


class History(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="history") 
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="viewed_by")
    viewed_at = models.DateField(auto_now_add=True)
