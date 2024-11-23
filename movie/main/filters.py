from  django_filters import FilterSet
from .models import *



class Movie_filter(FilterSet):
    class Meta:
        model = Movie
        fields = {
            "country": ['exact'],
            'actor': ['exact'],
            'janre': ['exact'],
            'year': ['gt', 'lt'],
            'status_movie': ['exact']
        }
