from rest_framework import serializers

from movies.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("id", "title", "genre", "year", "created_date", "updated_date")
        read_only_fields = ("id", "created_date", "updated_date")
