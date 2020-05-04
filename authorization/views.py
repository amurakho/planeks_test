from django.views import generic
from django.http import HttpResponse

from authorization import forms, tasks, models


class RegistrationView(generic.CreateView):
    form_class = forms.RegisterForm
    success_url = "/accounts/login"
    template_name = "registration/register.html"

    def form_valid(self, form):
        """
            delay the task with data(email, key, user_id)
        """
        response = super(RegistrationView, self).form_valid(form)
        to_email = self.object.email
        confirmation_key = self.object.confirmation_key
        user_id = self.object.id
        # to send without html pass message parameter
        tasks.send_email.delay(to_email, user_key=confirmation_key, user_id=user_id)
        return response


def confirm_email(request, id, key):
    """
        Get user by id
        confirm user by key
        make user is active
    """
    try:
        user = models.CustomUser.objects.get(pk=int(id))
    except:
        return HttpResponse('Activation link is invalid!')
    user.confirm_email(key)
    if not user.is_confirmed:
        return HttpResponse('Activation link is invalid!')
    else:
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation.')

