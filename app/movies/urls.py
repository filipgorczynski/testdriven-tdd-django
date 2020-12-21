from django.urls import path

from movies.views import MovieDetail, MovieList

urlpatterns = [
    path("movies/", MovieList.as_view()),
    path("movies/<int:pk>/", MovieDetail.as_view()),
]
