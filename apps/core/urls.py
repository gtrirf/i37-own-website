from django.urls import path
from .views import MainInfoView, CareerListView, SocialLinkListView

urlpatterns = [
    path('main-info/', MainInfoView.as_view(), name='main-info'),
    path('career/', CareerListView.as_view(), name='career-list'),
    path('social-links/', SocialLinkListView.as_view(), name='social-links-list'),
]
