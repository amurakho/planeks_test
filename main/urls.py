from django.urls import path

from main import views

urlpatterns = [
    path('', views.PubList.as_view(), name='pub_list'),
    path('pub/<slug:slug>', views.PubDetail.as_view(), name='pub_detail'),
    path('create/', views.PubCreation.as_view(), name='create_pub'),
]
