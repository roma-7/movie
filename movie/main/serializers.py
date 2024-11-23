from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.db.models import Avg


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    age = serializers.IntegerField(min_value=18)
    phone_number = serializers.CharField(max_length=15)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = Profile.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            age=validated_data["age"],
            phone_number=validated_data["phone_number"],
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email"),
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Неверные учетные данные.")
        return user


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "status"]


class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "age",
            "phone_number",
            "email",
            "status",
        ]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["country_name"]


class DirectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ["director_name"]


class DirectorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ["director_name", "bio", "photo", "age"]


class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["actor_name"]


class ActorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["actor_name", "age", "bio", "photo"]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"


class MomentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moments
        fields = ["moments"]


class ReviewSerializer(serializers.ModelSerializer):
    user = ProfileListSerializer()
    created_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta:
        model = Review
        fields = ["user", "text", "created_date", "parent_review"]


class MovieLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ["language", "video", "movie"]


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeMovie
        fields = ["label"]


class JanreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Janre
        fields = ["janre_name"]


class MovieListSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(required=False)

    class Meta:
        model = Movie
        fields = [
            "movie_name",
            "average_rating",
            "description",
            "year",
            "status_movie",
            "movie_image",
        ]


class MovieDetailSerializer(serializers.ModelSerializer):
    janre = JanreSerializer(many=True)
    actor = ActorListSerializer(many=True)
    country = CountrySerializer(many=True)
    director = DirectorListSerializer()
    types = TypeSerializer(many=True)
    languages = MovieLanguagesSerializer(many=True)
    average_rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    moments = MomentsSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            "movie_name",
            "description",
            "director",
            "actor",
            "country",
            "movie_time",
            "types",
            "moments",
            "movie_trailer",
            "year",
            "average_rating",
            "reviews",
            "status_movie",
            "movie_image",
            "languages",
            "janre",
        ]

    def get_average_rating(self, obj):
        ratings = (
            Rating.objects.filter(movie=obj)
            .exclude(stars__isnull=True)
            .values_list("stars", flat=True)
        )
        if ratings:
            return round(sum(ratings) / len(ratings), 2)
        return None


class FavoriteMovieSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)

    def get_movie(self, obj):
        # Получаем фильм с подсчетом среднего рейтинга
        movie = Movie.objects.annotate(average_rating=Avg("rating_movie__stars")).get(
            id=obj.movie.id
        )
        return MovieListSerializer(movie).data

    class Meta:
        model = FavoriteMovie
        fields = ["movie"]


class FavoriteSerializer(serializers.ModelSerializer):
    carts = FavoriteMovieSerializer(many=True, read_only=True)
    user = ProfileListSerializer(read_only=True)
    created = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta:
        model = Favorite
        fields = ["user", "created", "carts"]


class HistorySerializer(serializers.ModelSerializer):
    viewed_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    user = ProfileListSerializer(read_only=True)
    movie = MovieListSerializer(read_only=True)
    class Meta:
        model = History
        fields = ["movie", "user", "viewed_at"]
