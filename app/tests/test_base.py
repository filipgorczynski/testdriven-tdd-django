import json

from django.test import Client
from django.urls import reverse


def test_hello_world():
    assert "hello world" == "hello world"
    assert "foo" != "bar"


def test_ping():
    client = Client()
    url = reverse("ping")
    response = client.get(url)
    content = json.loads(response.content)
    assert response.status_code == 200
    assert content["ping"] == "pong!"
