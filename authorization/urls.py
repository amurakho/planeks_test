from django.urls import path, include

from authorization import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('confirm/<id>/<key>', views.confirm_email, name='confirm')
]
