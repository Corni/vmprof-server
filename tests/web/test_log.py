import pytest

from django.contrib import auth
from vmprofile.models import Log as Profile


@pytest.mark.django_db
def test_log_get_user(client):

    username = 'username'
    password = 'thepassword'

    user = auth.models.User.objects.create_user(
        username,
        'username@vmprof.com',
        password
    )

    Profile.objects.create(user=user, checksum="1", data="{}")
    Profile.objects.create(user=None, checksum="2", data="{}")

    response = client.get('/api/log/')

    assert len(response.data['results']) == 2

    client.login(username=username, password=password)

    response = client.get('/api/log/')
    assert len(response.data['results']) == 1

    response = client.get('/api/log/?all=True')
    assert len(response.data['results']) == 2
