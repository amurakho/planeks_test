from django.test import TestCase
from django.core.management import call_command


class CustomUserTest(TestCase):
    # i should change EMAIL_BACKEND to test email but i cannt do it because i will stop send messages to real emal
    # so its one thing that i should test in this view(like i understand)

    # similar situation with confirm email
    # at first i should change my EMAIL_BACKEND - to save messages in folder in next - check it

    # i think i dont need to ckeck some thing like context, used template, etc because its django code.
    pass

