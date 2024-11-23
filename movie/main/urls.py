from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import *


urlpatterns = [
    path("", MovieListView.as_view({"get": "list"}), name="movie_list"),
    path('<int:pk>/', MovieDetailView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}), name="movie_detail"),
    
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    path("users/", ProfileListView.as_view({"get": "list"}), name="profile"),
    path("users/<int:pk>/", ProfileDetailView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}), name="profile_detail"),
    
    path("favorite/", FavoriteView.as_view({"get": "list"}), name="favorite"),
    path("favorite/<int:pk>/", FavoriteMovieView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}), name="favorite_detail"),
    
    
    path("actors/", ActorListView.as_view({"get": "list"}), name="actor"),
    path("actors/<int:pk>/", ActorDetailView.as_view({"get": "list", "put": "update", "delete": "destroy"}), name="actors"),
    
    
    path("janres/", JanreView.as_view({"get": "list"}), name="janre"),
    
    
    path("director/", DirectorListView.as_view({"get": "list"}), name="director"),
    path("director/<int:pk>/", DirectorDetailView.as_view({"get": "list", "put": "update", "delete": "destroy"}), name="director"),

    path("history/", HistoryView.as_view({"get": "list"}), name="history"),

]
