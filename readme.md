# planeks_test
Django-simple-blog

First what you need to launch:
1. use requirements.txt
2. ./manage.py migrate
3. launch custom command for group creation - ./manage.py creategroups (you can check this file in /main/management/command/creategroups.py)
4. launch redis - redis-server(at default port 6379 (if you want to change port you should also change CELERY_BROKER_URL and CELERY_RESULT_BACKEND in settings))
5. launch celery - celery -A planeks_test worker -l info
6. ./manage runserver

## main part:
  1. Two models - one for publications(Pub), another for comments(Comment).
  2. There views - 
    PubList(list of publication)(also get only is_pub=True publications). 
    PubDetai(publication detail)(working with slug field)(in post-method you can check task-delay(this task work when someone make a comment for pub).
    PubCreation(create publication)(works only when user is loggin)
  3. Two forms - CommentForm and PubCreationForm(the names speak for themselves)
  4. One celery task - send_email_about_comment(get pub author email and pub url, send email to author with url)
  5. Also here is creategroups command(/main/management/command/creategroups.py)
  6. Some unit-tests:
    test_admin.PubAdminTest - test publication admin
    test_view.PubCreationTest - test creation from request(view)
##  authorization
  1. One model - CustomUser(inherits SimpleEmailConfirmationUserMixin and AbstractUser)(make email field requirement and username - not)(use new manager(UserManager). UserManager - is simple manager(i make create_user and create_superuser methods but forget simple create)
  2. Two views - RegistrationView(in form_valid method you can check task delay. This task send an email to new user. Mech of unconfirmed user is not defined.). confirm_emailfunc  which get chek user confirmation link.
  3. One signal - add_user_to_group(Add user to group(at defauld to 'user') when its created.
  4. There forms - RegisterForm, UserChangeForm, UserCreationForm(clean_password2 - check passwords, overwritten save - save this password)
  5. One task - send_email(send email with url to user for confirmation account)(main parameter is to_email.user_key, user_id, message is optional. When you pass message parameter - the email will be in plain text(without html). So when 'message' is None, task will send email with html(you can find template in /templates/registration/confirm_email.html
  6. Admin - UserAdmin
  
  
  SendGrid key is already in settngs(SENDGRID_API_KEY)
