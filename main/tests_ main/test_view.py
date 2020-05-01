from django.test import TestCase, Client
from django.core.management import call_command

from authorization import models
from main import models as main_models


def create_user():
    """
        Create user
    """
    password = 'test124512'
    user_data = {
        'email': 'test@i.ua',
        'password': password
    }

    user = models.CustomUser.objects.create_superuser(**user_data)
    user.save()
    return user, password


class PubCreationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
            Login
        """
        call_command('creategroups')

        cls.user, cls.password = create_user()
        cls.client = Client()
        cls.index_url = '/'

    def setUp(self) -> None:
        r = self.client.login(email=self.user.email, password=self.password)

    def test_admin_creation(self):
        response = self.client.post('/create/', data={
            'text': 'some text',
            'title': 'some title',
        })
        pub = main_models.Pub.objects.filter(slug='some-title')
        self.assertEqual(len(pub), 1)
        self.assertTrue(pub[0].is_pub)

    def test_user_creation(self):
        password = 'test124512'
        user_data = {
            'email': 'test1@i.ua',
            'password': password
        }
        user = models.CustomUser.objects.create_user(**user_data)
        self.client.logout()

        r = self.client.post('/accounts/login/', data={
            'username': user.email,
            'password': password
        })
        response = self.client.post('/create/', data={
            'text': 'some text',
            'title': 'some title1',
        })
        pub = main_models.Pub.objects.all()
        self.assertEqual(len(pub), 1)
        self.assertFalse(pub[0].is_pub)

