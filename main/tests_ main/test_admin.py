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


class PubAdminTest(TestCase):

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
        self.client.login(email=self.user.email, password=self.password)

    def test_exist_buttons(self):
        response = self.client.get('/admin/main/pub/add/')
        self.assertContains(response, 'class="submit-row"')
        self.assertContains(response, '<input type="submit" value="Publish" name="_publish">')
        self.assertContains(response, '<input type="submit" value="Publish off" name="_offpublish">')

    def test_press_publish_button(self):
        pub = main_models.Pub.objects.create(author=self.user,
                                             text='some text',
                                             title='some title',
                                             is_pub=False)
        url = '/admin/main/pub/{}/change/'.format(pub.id)
        response = self.client.post(url, data={
            'text': pub.text,
            'author': pub.author.id,
            'title': pub.title,
            'is_pub': pub.is_pub,
            '_publish': 'Publish',
        })
        pub = main_models.Pub.objects.filter(id=pub.id)
        self.assertEqual(len(pub), 1)
        self.assertTrue(pub[0].is_pub)

    def test_press_publishoff_button(self):
        pub = main_models.Pub.objects.create(author=self.user,
                                             text='some text',
                                             title='some title',
                                             is_pub=True)
        url = '/admin/main/pub/{}/change/'.format(pub.id)
        response = self.client.post(url, data={
            'text': pub.text,
            'author': pub.author.id,
            'title': pub.title,
            'is_pub': pub.is_pub,
            '_offpublish': "Publish+off"
        })
        pub = main_models.Pub.objects.filter(id=pub.id)
        self.assertEqual(len(pub), 1)
        self.assertFalse(pub[0].is_pub)
