from django.urls import path, include
from . import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path('register/', views.signup, name='signup'),
    path('transactions/', views.TransactionApiView.as_view()),
    path('transactions/detail/<int:tid>/', views.TransactionDetailApiView.as_view()),
    path('konto/erstellen', views.konto_create, name='konto_create'),
    path('profile/', views.profile_data, name="user_profile"),
    path('konto/uberweisen', views.konto_uberweisen, name='konto_uberweisen'),
    path('verwalten/', views.manage, name='verwalten'),
    path('konto/kuendigen', views.konto_kuendigen, name="konto_kuendigen")
]