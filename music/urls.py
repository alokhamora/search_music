from django.urls import path

from . import views

app_name = 'music'


urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search')
]