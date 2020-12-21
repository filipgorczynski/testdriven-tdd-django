from movies.serializers import MovieSerializer


def test_valid_movie_serializer():
    valid_serializer_data = {
        "title": "Rising Arizona",
        "genre": "comedy",
        "year": "1987",
    }
    serializer = MovieSerializer(data=valid_serializer_data)

    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert serializer.errors == {}


def test_invalid_movie_serializer():
    invalid_serializer_data = {
        "title": "Rising Arizona",
        "genre": "comedy",
    }
    serializer = MovieSerializer(data=invalid_serializer_data)

    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert "year" in serializer.errors
    assert str(serializer.errors["year"][0]) == "This field is required."
