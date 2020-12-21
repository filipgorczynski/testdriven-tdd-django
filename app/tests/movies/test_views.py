from django.test import Client

import pytest

from movies.models import Movie


@pytest.fixture
def client():
    return Client()


@pytest.fixture(scope="function")
def add_movie():
    def _add_movie(title, genre, year):
        movie = Movie.objects.create(title=title, genre=genre, year=year)
        return movie

    return _add_movie


@pytest.mark.django_db
def test_add_movie(client):
    movies_counter = int(Movie.objects.count())
    response = client.post(
        "/api/movies/",
        {
            "title": "The Big Lebowski",
            "genre": "comedy",
            "year": "1998",
        },
    )

    assert response.status_code == 201
    assert response.data["title"] == "The Big Lebowski"

    assert int(Movie.objects.count()) != movies_counter


@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    movies_counter = int(Movie.objects.count())
    response = client.post("/api/movies/", {}, content_type="application/json")

    assert response.status_code == 400
    assert int(Movie.objects.count()) == movies_counter


@pytest.mark.django_db
def test_add_movie_invalid_json_keys(client):
    movies_counter = int(Movie.objects.count())
    response = client.post(
        "/api/movies/",
        {
            "title": "The Big Lebowski",
            "genre": "comedy",
        },
        content_type="application/json",
    )

    assert response.status_code == 400
    assert int(Movie.objects.count()) == movies_counter


@pytest.mark.django_db
def test_add_movie_invalid_json_additional_keys(client):
    movies_counter = int(Movie.objects.count())
    response = client.post(
        "/api/movies/",
        {
            "title": "The Big Lebowski",
            "genre": "comedy",
            "year": "1998",
            "cast": "Jeff Bridges",
        },
        content_type="application/json",
    )

    assert response.status_code == 201
    assert int(Movie.objects.count()) != movies_counter


@pytest.mark.django_db
def test_get_single_movie(client, add_movie):
    movie = add_movie(title="The Big Lebowski", genre="comedy", year="1998")
    response = client.get(f"/api/movies/{movie.id}/")

    assert response.status_code == 200
    assert response.data["title"] == "The Big Lebowski"


@pytest.mark.django_db
def test_get_single_movie_incorrect_id(client):
    response = client.get("/api/movies/9999999999/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_get_all_movies(client, add_movie):
    movie_one = add_movie(title="The Big Lebowski", genre="comedy", year="1998")
    movie_two = add_movie("No Country for Old Men", "thriller", "2007")

    response = client.get("/api/movies/")

    assert response.status_code == 200
    assert response.data[0]["title"] == movie_one.title
    assert response.data[1]["title"] == movie_two.title
