from _collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse
import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from users.models import NewDataUser


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('http', 'api.vk.com', '/method/users.get', None, urlencode(
        OrderedDict(fields=','.join(('bdate', 'sex', 'about')), access_token=response['access_token'], v='5.92')),
                          None))
    resp = requests.get(api_url)
    if resp.status_code != 200:
        return
    data = resp.json()['response'][0]
    if data['sex']:
        user.newdatauser.gender = NewDataUser.MALE if data['sex'] == 2 else NewDataUser.FEMALE

    if data['about']:
        user.newdatauser.about_me = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    user.save()