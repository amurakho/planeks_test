from django.test import TestCase
from django.core.management import call_command

from authorization import models


class CustomUserTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('creategroups')

        cls.EMAIL = 'test@i.ua'
        cls.USER_DATA = {
            'email': cls.EMAIL,
            'password': 'test124512'
        }

        cls.NAME = 'Test'
        cls.SURNAME = 'Test'
        cls.DATE = '2020-02-02'
        cls.ADD_DATA = {
            'name': cls.NAME,
            'surname': cls.SURNAME,
            'birth_date': cls.DATE,
        }

    def test_user_creation_superuser(self):
        models.CustomUser.objects.create_superuser(**self.USER_DATA)

        user = models.CustomUser.objects.filter(email=self.EMAIL)

        self.assertEqual(len(user), 1)
        self.assertTrue(user[0].has_perm('pub.can_publish'))

    def test_user_creation_default(self):
        models.CustomUser.objects.create(**self.USER_DATA)

        user = models.CustomUser.objects.filter(email=self.EMAIL)

        self.assertEqual(len(user), 1)
        self.assertFalse(user[0].has_perm('pub.can_publish'))

    def test_user_creation_addition_info(self):
        data = self.USER_DATA.copy()
        data.update(self.ADD_DATA)

        models.CustomUser.objects.create(**data)

        user = models.CustomUser.objects.filter(email=self.EMAIL)

        self.assertEqual(len(user), 1)
        self.assertFalse(user[0].has_perm('pub.can_publish'))
        self.assertEqual(user[0].name, self.NAME)
        self.assertEqual(user[0].surname, self.SURNAME)
        self.assertEqual(str(user[0].birth_date), self.DATE)

